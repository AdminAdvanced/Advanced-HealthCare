from collections import defaultdict

from odoo import _, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"


    def _get_sale_line_invoiced_qty(self, sale_line, exclude_move=None):

        qty = 0.0

        invoice_lines = sale_line.invoice_lines.filtered(
            lambda l:
            l.move_id
            and l.move_id.state == "posted"
            and l.move_id.move_type in (
                "out_invoice",
                "out_refund",
            )
            and l.move_id != exclude_move
        )

        for line in invoice_lines:

            if line.move_id.move_type == "out_refund":
                qty -= line.product_uom_id._compute_quantity(
                    line.quantity,
                    sale_line.product_uom
                )

            else:
                qty += line.product_uom_id._compute_quantity(
                    line.quantity,
                    sale_line.product_uom
                )

        return qty



    def action_post(self):

        for move in self:

            if move.move_type not in (
                "out_invoice",
                "out_refund",
            ):
                continue


            current_qty = defaultdict(float)


            for line in move.invoice_line_ids:

                if not line.sale_line_ids:
                    continue


                for sale_line in line.sale_line_ids:

                    qty = line.product_uom_id._compute_quantity(
                        line.quantity,
                        sale_line.product_uom
                    )


                    if move.move_type == "out_refund":
                        qty = -qty


                    current_qty[sale_line] += qty



            errors = []


            for sale_line, qty in current_qty.items():

                ordered_qty = sale_line.product_uom_qty

                invoiced_before = self._get_sale_line_invoiced_qty(
                    sale_line,
                    move
                )

                total = invoiced_before + qty


                if total > ordered_qty:

                    errors.append({
                        "product": sale_line.product_id.display_name,
                        "ordered": ordered_qty,
                        "previous": invoiced_before,
                        "allowed": ordered_qty - invoiced_before,
                        "current": qty,
                        "total": total,
                    })


            if errors:

                message = _(
                    "Cannot post this invoice.\n\n"
                    "The following products exceed the Sales Order quantity:\n\n"
                )


                for error in errors:

                    message += _(
                        "Product: %(product)s\n"
                        "Ordered Quantity: %(ordered)s\n"
                        "Already Invoiced: %(previous)s\n"
                        "Current Delivery: %(current)s\n"
                        "Allowed Delivery: %(allowed)s\n",
                        **error
                    )


                raise ValidationError(message)


        return super().action_post()