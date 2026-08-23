from collections import defaultdict
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
        self.ensure_one()

        result = defaultdict(lambda: {
            "lot_name": "",
            "quantity": 0.0,
            "uom_name": "",
            "expiration_date": "",
        })

        stock_moves = invoice_line.sale_line_ids.mapped("move_ids").filtered(
            lambda move: move.state == "done"
        )

        is_credit_note = self.move_type == "out_refund"

        for move in stock_moves:
            if not is_credit_note:
                if move.location_dest_id.usage != "customer":
                    continue
            else:
                if move.location_id.usage != "customer":
                    continue

            move_lines = move.move_line_ids.filtered(lambda ml: ml.lot_id)

            for ml in move_lines:
                lot = ml.lot_id
                if not lot:
                    continue

                key = lot.id

                result[key]["lot_name"] = lot.name
                result[key]["quantity"] += ml.quantity
                result[key]["uom_name"] = ml.product_uom_id.name or ""

                # LOT EXPIRATION DATE
                exp_date = getattr(lot, 'expiration_date', False) or getattr(lot, 'use_date', False)
                result[key]["expiration_date"] = exp_date.strftime("%d/%m/%Y") if exp_date else ""

        return list(result.values())