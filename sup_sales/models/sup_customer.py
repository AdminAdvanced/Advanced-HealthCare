from odoo import models, fields, api


class SupCustomer(models.Model):
    _name = "sup.sales.customer"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "SUP Sales Customer"
    _order = "id desc"

    company_type = fields.Selection(
        [
            ("person", "Individual"),
            ("company", "Company"),
        ],
        string="Contact Type",
        default="company",
        tracking=True,
    )

    name = fields.Char(
        string="Customer Name",
        required=True,
        tracking=True,
    )

    name_ar = fields.Char(
        string="Name (Arabic)",
        tracking=True,
    )

    code = fields.Char(
        string="Customer Code",
        required=True,
        copy=False,
        readonly=True,
    )

    street = fields.Char(
        string="Street",
        tracking=True,
    )

    district = fields.Char(
        string="District",
        tracking=True,
    )

    city = fields.Char(
        string="City",
        tracking=True,
    )

    state_id = fields.Many2one(
        "res.country.state",
        string="State",
        tracking=True,
    )

    zip = fields.Char(
        string="ZIP",
        tracking=True,
    )

    country_id = fields.Many2one(
        "res.country",
        string="Country",
        tracking=True,
    )

    building_number = fields.Char(
        string="Building Number",
        tracking=True,
    )

    plot_identification = fields.Char(
        string="Plot Identification",
        tracking=True,
    )

    vat = fields.Char(
        string="VAT Number",
        tracking=True,
    )

    uf_number = fields.Char(
        string="UF Number",
        tracking=True,
    )

    phone = fields.Char(
        string="Phone",
        tracking=True,
    )

    mobile = fields.Char(
        string="Mobile",
        tracking=True,
    )

    email = fields.Char(
        string="Email",
        tracking=True,
    )

    website = fields.Char(
        string="Website",
        tracking=True,
    )

    lang = fields.Selection(
        selection=lambda self: self.env["res.lang"].get_installed(),
        string="Language",
        tracking=True,
    )

    active = fields.Boolean(
        default=True,
        tracking=True,
    )

    quotation_count = fields.Integer(
        compute="_compute_counts",
        string="Quotations",
    )

    order_count = fields.Integer(
        compute="_compute_counts",
        string="Sales Orders",
    )

    def action_view_quotations(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Quotations",
            "res_model": "sup.sales.quotation",
            "view_mode": "list,form",
            "domain": [("customer_id", "=", self.id)],
        }

    def action_view_orders(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Sales Orders",
            "res_model": "sup.sales.order",
            "view_mode": "list,form",
            "domain": [("customer_id", "=", self.id)],
        }

    def _compute_counts(self):
        quotation_obj = self.env["sup.sales.quotation"]
        order_obj = self.env["sup.sales.order"]

        for rec in self:
            rec.quotation_count = quotation_obj.search_count([
                ("customer_id", "=", rec.id)
            ])
            rec.order_count = order_obj.search_count([
                ("customer_id", "=", rec.id)
            ])

    @api.model
    def create(self, vals):

        if vals.get("code", "New") == "New":
            seq = self.env["ir.sequence"].next_by_code(
                "sup.customer"
            )
            vals["code"] = seq or "New"

        return super().create(vals)