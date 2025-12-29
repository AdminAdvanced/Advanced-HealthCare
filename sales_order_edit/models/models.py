from odoo import models, fields, api


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    create_credit_note = fields.Boolean(string="Create Credit Note Automatically")

    def _create_credit_note_from_invoice(self, picking, return_picking):
        sale_order = picking.sale_id
        if not sale_order:
            return False

        invoice = sale_order.invoice_ids.filtered(
            lambda inv: inv.move_type == 'out_invoice' and inv.state == 'posted'
        )
        if not invoice:
            return False

        # Collect returned qty
        return_lines = {}
        for move in return_picking.move_ids:
            qty_returned = sum(move.move_line_ids.mapped('quantity'))
            if qty_returned > 0:
                return_lines[move.product_id.id] = qty_returned

        if not return_lines:
            return False

        # Create normal full credit note
        credit_notes = invoice._reverse_moves(cancel=False)
        credit_note = credit_notes and credit_notes[0] or False

        if not credit_note:
            return False

        # Modify lines inside created credit note
        for line in credit_note.invoice_line_ids:
            if line.product_id.id in return_lines:
                line.quantity = return_lines[line.product_id.id]
            else:
                line.quantity = 0

        # Remove zero quantity lines
        zero_lines = credit_note.invoice_line_ids.filtered(lambda l: l.quantity == 0)
        if zero_lines:
            zero_lines.unlink()

        return credit_note

    def action_create_returns(self):
        print("DEBUG: action_create_returns executed")

        res = super().action_create_returns()

        return_picking_ids = res.get('res_id') or []
        return_picking = self.env['stock.picking'].browse(return_picking_ids)
        original_picking = self.picking_id

        if self.create_credit_note:
            print("DEBUG: create_credit_note = True")
            self._create_credit_note_from_invoice(original_picking, return_picking)

        return res

