from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoiced_lot_values(self):
        res = super()._get_invoiced_lot_values()

        for line in res:
            lot = self.env["stock.lot"].browse(line.get("lot_id"))

            if lot.exists():
                product = lot.product_id

                line.update({
                    "product_name_ar": (
                        product.product_tmpl_id.x_studio_product_name_ar
                        or ""
                    ),

                    "uom_name_ar": (
                        lot.product_uom_id.x_studio_unit_of_measure_ar
                        or ""
                    ),
                })

        return res