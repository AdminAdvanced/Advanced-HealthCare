from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoiced_lot_values(self):
        """
        Extend standard lot values:
        - Add Arabic product name
        - Add Arabic UoM
        - Add invoice line reference
        """

        res = super()._get_invoiced_lot_values()

        for line in res:

            lot = self.env["stock.lot"].browse(line.get("lot_id"))

            if lot.exists():
                product = lot.product_id

                line.update({
                    "product_name_ar": product.product_tmpl_id.x_studio_product_name_ar or "",
                    "uom_name_ar": lot.product_uom_id.x_studio_unit_of_measure_ar or "",
                })

                # Find related invoice line
                move_lines = self.env["stock.move.line"].search([
                    ("lot_id", "=", lot.id),
                    ("move_id.state", "=", "done"),
                    ("move_id.sale_line_id", "!=", False),
                ])

                invoice_lines = self.env["account.move.line"].search([
                    ("move_id", "in", self.ids),
                    ("product_id", "=", product.id),
                ])

                if invoice_lines:
                    line["invoice_line_ids"] = invoice_lines.ids

        return res


    def get_invoice_line_lots(self, invoice_line):
        """
        Return lots related to this exact invoice line.
        Supports:
        - Sales Order invoices
        - Direct invoices
        """

        self.ensure_one()

        result = []

        lot_values = self._get_invoiced_lot_values()

        for lot in lot_values:

            invoice_line_ids = lot.get("invoice_line_ids", [])

            if invoice_line.id in invoice_line_ids:

                result.append({
                    "lot_name": lot.get("lot_name"),
                    "quantity": lot.get("quantity"),
                    "uom_name": lot.get("uom_name"),
                    "uom_name_ar": lot.get("uom_name_ar", ""),
                    "product_name_ar": lot.get("product_name_ar", ""),
                })

        return result