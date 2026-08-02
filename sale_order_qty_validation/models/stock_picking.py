from collections import defaultdict

from odoo import _, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_sale_line_delivered_qty(self, sale_line, exclude_picking=None):
        """
        Return delivered quantity from completed deliveries
        for a specific sale order line.
        """

        qty = 0.0

        moves = sale_line.move_ids.filtered(
            lambda m:
            m.state == "done"
            and m.picking_id
            and m.picking_id != exclude_picking
        )

        for move in moves:
            qty += move.product_uom._compute_quantity(
                move.quantity,
                sale_line.product_uom
            )

        return qty


    def button_validate(self):

        for picking in self:

            errors = []

            current_qty = defaultdict(float)

            for move in picking.move_ids_without_package:

                if (
                    move.state == "cancel"
                    or not move.sale_line_id
                ):
                    continue

                sale_line = move.sale_line_id

                qty = move.product_uom._compute_quantity(
                    move.quantity,
                    sale_line.product_uom
                )

                current_qty[sale_line] += qty


            for sale_line, qty in current_qty.items():

                ordered_qty = sale_line.product_uom_qty

                delivered_before = self._get_sale_line_delivered_qty(
                    sale_line,
                    picking
                )

                total = delivered_before + qty


                if total > ordered_qty:

                    errors.append({
                        "product": sale_line.product_id.display_name,
                        "ordered": ordered_qty,
                        "previous": delivered_before,
                        "current": qty,
                        "total": total,
                    })


            if errors:

                message = _(
                    "Cannot validate this delivery.\n\n"
                    "The following products exceed the Sales Order quantity:\n\n"
                )

                for error in errors:
                    message += _(
                        "Product: %(product)s\n"
                        "Ordered Quantity: %(ordered)s\n"
                        "Already Delivered: %(previous)s\n"
                        "Current Delivery: %(current)s\n"
                        "Total: %(total)s\n\n",
                        **error
                    )

                raise ValidationError(message)


        return super().button_validate()