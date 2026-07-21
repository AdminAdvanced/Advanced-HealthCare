from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    x_studio_salesman = fields.Many2one(
        "hr.employee",
        string="Salesman",
        readonly=True,
    )

    x_studio_sales_manager = fields.Many2one(
        "hr.employee",
        string="Sales Manager",
        readonly=True,
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res.update({
            "x_studio_salesman": "s.x_studio_salesman",
            "x_studio_sales_manager": "s.x_studio_sales_manager",
        })
        return res

    def _group_by_sale(self):
        return super()._group_by_sale() + """
            ,s.x_studio_salesman
            ,s.x_studio_sales_manager
        """