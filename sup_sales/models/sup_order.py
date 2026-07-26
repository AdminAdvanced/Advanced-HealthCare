from odoo import models, fields, api


class SupSalesOrder(models.Model):

    _name = "sup.sales.order"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "SUP Sales Order"


    name = fields.Char(
        default="New",
        readonly=True,
        tracking = True
    )


    quotation_id = fields.Many2one(
        "sup.sales.quotation",
        string="Quotation"
    )

    customer_id = fields.Many2one(
        "sup.sales.customer",
        string="Customer",
        required=True,
        tracking = True
    )

    date = fields.Date(
        default=fields.Date.today,
        tracking = True
    )


    state = fields.Selection(
        [
            ("draft","Draft"),
            ("confirmed","Confirmed"),
            ("cancel","Cancelled"),
        ],
        default="draft",
        tracking = True
    )


    line_ids = fields.One2many(
        "sup.sales.order.line",
        "order_id"
    )


    total_amount = fields.Float(
        compute="_compute_total",
        store=True
    )



    @api.depends(
        "line_ids.subtotal"
    )
    def _compute_total(self):

        for rec in self:

            rec.total_amount = sum(
                rec.line_ids.mapped("subtotal")
            )

    @api.model_create_multi
    def create(self, vals):

        if vals.get("name") == "New":

            vals["name"] = self.env["ir.sequence"].next_by_code(
                "sup.sales.order"
            )

        return super().create(vals)

    def action_confirm(self):
        self.write({
            "state": "confirmed"
        })

    def action_cancel(self):
        self.write({
            "state": "cancel"
        })

class SupSalesOrderLine(models.Model):

    _name = "sup.sales.order.line"
    _description = "SUP Sales Order Line"



    order_id = fields.Many2one(
        "sup.sales.order",
        ondelete="cascade"
    )


    product_id = fields.Many2one(
        "product.product"
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



    @api.depends(
        "qty",
        "price"
    )
    def _compute_subtotal(self):

        for rec in self:

            rec.subtotal = (
                rec.qty *
                rec.price
            )

    def action_confirm(self):

        for rec in self:
            rec.state = "confirmed"

    def action_cancel(self):

        for rec in self:
            rec.state = "cancel"