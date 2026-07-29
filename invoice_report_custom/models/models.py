from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoiced_lot_values(self):
        """Add Arabic fields to Odoo lot values."""
        res = super()._get_invoiced_lot_values()

        for line in res:
            lot = self.env["stock.lot"].browse(line.get("lot_id"))

            if lot.exists():
                product = lot.product_id

                line.update({
                    "product_name_ar": product.product_tmpl_id.x_studio_product_name_ar or "",
                    "uom_name_ar": lot.product_uom_id.x_studio_unit_of_measure_ar or "",
                })

        return res

    def get_invoice_line_lots(self, invoice_line):
        """
        Return only the lots that belong to THIS invoice line.
        Works for:
        - Sales Orders
        - Deliveries
        - Partial Deliveries
        - Multiple Lots
        - Same product repeated several times
        """

        self.ensure_one()

        result = []

        # Get stock moves linked to this invoice line only
        stock_moves = invoice_line.sale_line_ids.mapped("move_ids").filtered(
            lambda m: m.state == "done"
        )

        for move in stock_moves:

            move_lines = move.move_line_ids.filtered(lambda ml: ml.lot_id)

            for ml in move_lines:

                result.append({
                    "lot_name": ml.lot_id.name,
                    "quantity": ml.quantity,
                    "uom_name": ml.product_uom_id.name,
                })

        # Remove duplicates if any
        unique = []
        seen = set()

        for item in result:
            key = (
                item["lot_name"],
                item["quantity"],
                item["uom_name"],
            )

            if key not in seen:
                seen.add(key)
                unique.append(item)

        return unique