from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def get_invoice_line_lots(self, invoice_line):
        """Return lots for a specific invoice line."""

        self.ensure_one()

        result = []

        lot_values = self._get_invoiced_lot_values()

        if not invoice_line.product_id:
            return result

        product_name = invoice_line.product_id.display_name

        for lot in lot_values:
            if lot.get("product_name") == product_name:
                result.append({
                    "lot_name": lot.get("lot_name"),
                    "quantity": lot.get("quantity"),
                    "uom_name": lot.get("uom_name"),
                })

        return result