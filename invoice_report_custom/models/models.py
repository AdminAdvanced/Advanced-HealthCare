from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoiced_lot_values(self):
        res = super()._get_invoiced_lot_values()

        for lot_line in res:

            lot = self.env["stock.lot"].browse(lot_line.get("lot_id"))

            if lot.exists():

                product = lot.product_id

                lot_line.update({
                    "product_name_en": product.name,

                    "product_name_ar": (
                        product.product_tmpl_id.x_studio_product_name_ar
                        or product.name
                    ),

                    "uom_name_en": lot.product_uom_id.name,

                    "uom_name_ar": (
                        lot.product_uom_id.x_studio_unit_of_measure_ar
                        or lot.product_uom_id.name
                    ),
                })

        return res

    def get_invoice_line_lots(self, invoice_line):
        self.ensure_one()

        result = []

        lot_values = self._get_invoiced_lot_values()

        for lot in lot_values:
            if lot.get("product_name_en") == invoice_line.product_id.name:
                result.append(lot)

        return result