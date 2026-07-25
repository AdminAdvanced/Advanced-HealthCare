from odoo import models, fields, api

class SupQuotation(models.Model):
    _name = "sup.sales.quotation"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "SUP Sales Quotation"
    _order = "id desc"

    name = fields.Char(
        string="Quotation Number",
        required=True,
        copy=False,
        readonly=True,
        default="New",
    )

    customer_id = fields.Many2one(
        "sup.sales.customer",
        string="Customer",
        required=True,
        tracking=True,
    )

    invoice_address_id = fields.Many2one(
        "sup.sales.customer",
        string="Invoice Address",
    )

    delivery_address_id = fields.Many2one(
        "sup.sales.customer",
        string="Delivery Address",
    )

    quotation_date = fields.Date(
        string="Quotation Date",
        default=fields.Date.today,
        tracking=True,
    )

    expiration_date = fields.Date(
        string="Expiration",
    )

    pricelist = fields.Many2one(
        "product.pricelist",
        string="Pricelist",
    )

    payment_terms = fields.Many2one(
        "account.payment.term",
        string="Payment Terms",
    )

    salesman_id = fields.Many2one(
        "hr.employee",
        string="Salesman",
    )

    sales_manager_id = fields.Many2one(
        "hr.employee",
        string="Sales Manager",
    )

    state = fields.Selection(
        [
            ("draft", "Quotation"),
            ("sent", "Quotation Sent"),
            ("sale", "Sales Order"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        tracking=True,
    )

    line_ids = fields.One2many(
        "sup.sales.quotation.line",
        "quotation_id",
        string="Products",
    )

    total_amount = fields.Float(
        compute="_compute_total",
        store=True,
        tracking=True,
    )

    date = fields.Date(
        string="Date",
        default=fields.Date.today
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        readonly=True,
    )

    partner_ref = fields.Char(
        string="Customer Reference",
    )

    note = fields.Text(
        string="Terms and Conditions",
    )

    amount_untaxed = fields.Monetary(
        string="Untaxed Amount",
        compute="_compute_amounts",
        store=True,
        currency_field="currency_id",
    )

    amount_tax = fields.Monetary(
        string="Taxes",
        compute="_compute_amounts",
        store=True,
        currency_field="currency_id",
    )

    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_amounts",
        store=True,
        currency_field="currency_id",
    )

    @api.depends(
        "line_ids.price_subtotal",
        "line_ids.price_tax",
    )
    def _compute_amounts(self):

        for order in self:
            untaxed = sum(
                order.line_ids.mapped("price_subtotal")
            )

            tax = sum(
                order.line_ids.mapped("price_tax")
            )

            order.amount_untaxed = untaxed
            order.amount_tax = tax
            order.amount_total = untaxed + tax

    @api.depends("line_ids.subtotal")
    def _compute_total(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped("subtotal"))

    @api.model
    def create(self, vals):

        if vals.get("name", "New") == "New":
            seq = self.env["ir.sequence"].next_by_code(
                "sup.sales.quotation"
            )
            vals["name"] = seq or "New"

        return super().create(vals)

    def action_send(self):
        self.write({"state": "sent"})

    def action_confirm(self):
        self.write({"state": "sale"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_print(self):
        return self.env.ref(
            "sup_sales.action_report_sup_quotation"
        ).report_action(self)

    def action_print(self):

        return self.env.ref(
            "sup_sales.action_report_sup_quotation"
        ).report_action(self)

class SupQuotationLine(models.Model):

    _name = "sup.sales.quotation.line"
    _description = "SUP Quotation Line"


    quotation_id = fields.Many2one(
        "sup.sales.quotation",
        ondelete="cascade"
    )


    product_id = fields.Many2one(
        "product.product",
        string="Product"
    )


    description = fields.Char()


    qty = fields.Float(
        default=1
    )


    price = fields.Float()


    subtotal = fields.Float(
        compute="_compute_subtotal",
        store=True
    )

    product_uom_qty = fields.Float(
        string="Quantity",
        default=1,
    )

    price_unit = fields.Float(
        string="Unit Price",
    )

    discount = fields.Float(
        string="Discount (%)",
        default=0,
    )

    tax_ids = fields.Many2many(
        "account.tax",
        string="Taxes",
    )

    currency_id = fields.Many2one(
        related="quotation_id.currency_id",
        store=True,
    )

    price_subtotal = fields.Monetary(
        string="Amount",
        compute="_compute_amount",
        store=True,
        currency_field="currency_id",
    )

    price_tax = fields.Monetary(
        string="Tax",
        compute="_compute_amount",
        store=True,
        currency_field="currency_id",
    )

    @api.depends(
        "qty",
        "price"
    )
    @api.depends(
        "product_uom_qty",
        "price_unit",
        "discount",
        "tax_ids",
    )
    def _compute_amount(self):

        for line in self:
            price = line.price_unit * (
                    1 - (line.discount / 100.0)
            )

            taxes = line.tax_ids.compute_all(
                price,
                currency=line.currency_id,
                quantity=line.product_uom_qty,
                product=line.product_id,
            )

            line.price_subtotal = taxes["total_excluded"]
            line.price_tax = taxes["total_included"] - taxes["total_excluded"]

    @api.onchange("product_id")
    def _onchange_product(self):

        if self.product_id:
            self.description = self.product_id.display_name

            self.price_unit = self.product_id.lst_price

            self.tax_ids = self.product_id.taxes_id


    def _compute_subtotal(self):

        for rec in self:

            rec.subtotal = (
                rec.qty *
                rec.price
            )

