from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def get_invoice_lots(self):
        self.ensure_one()

        lots = []

        for sale_line in self.sale_line_ids:
            for move in sale_line.move_ids:
                for move_line in move.move_line_ids:
                    if move_line.lot_id:
                        lots.append({
                            "lot_name": move_line.lot_id.name,
                            "quantity": move_line.quantity,
                            "uom": move_line.product_uom_id.name,
                        })

        return lots