from collections import defaultdict

from odoo import _, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_sale_line_delivered_qty(self, sale_line, exclude_picking=None):
        """
        Return net delivered quantity from completed stock moves
        for a specific sale order line.

        Normal delivery  -> +
        Customer return  -> -
        """

        qty = 0.0

        moves = sale_line.move_ids.filtered(
            lambda m:
            m.state == "done"
            and m.picking_id
            and m.picking_id != exclude_picking
        )

        for move in moves:

            converted_qty = move.product_uom._compute_quantity(
                move.quantity,
                sale_line.product_uom
            )

            # Normal Delivery
            if move.location_dest_id.usage == "customer":
                qty += converted_qty

            # Return from Customer
            elif move.location_id.usage == "customer":
                qty -= converted_qty

        return qty

    def _get_current_picking_sale_quantities(self, picking):
        """
        Return quantities of the current picking grouped by sale order line.
        """

        current_qty = defaultdict(float)

        for move in picking.move_ids_without_package:

            if move.state == "cancel":
                continue

            sale_line = move.sale_line_id

            # In some return cases sale_line_id may not be directly set.
            if not sale_line and move.origin_returned_move_id:
                sale_line = move.origin_returned_move_id.sale_line_id

            if not sale_line:
                continue

            qty = move.product_uom._compute_quantity(
                move.quantity,
                sale_line.product_uom
            )

            current_qty[sale_line] += qty

        return current_qty

    def _is_return_picking(self):
        self.ensure_one()

        return any(
            move.origin_returned_move_id
            for move in self.move_ids_without_package
        )

    def button_validate(self):

        for picking in self:

            current_qty = self._get_current_picking_sale_quantities(
                picking
            )

            errors = []

            # =========================================================
            # RETURN
            # =========================================================
            if picking._is_return_picking():

                for sale_line, return_qty in current_qty.items():

                    # Quantity delivered before this return.
                    #
                    # Important:
                    # exclude current picking so its return quantity
                    # is NOT already included in the calculation.
                    delivered_before = self._get_sale_line_delivered_qty(
                        sale_line,
                        picking
                    )

                    if return_qty > delivered_before:

                        errors.append({
                            "product": sale_line.product_id.display_name,
                            "delivered": delivered_before,
                            "current": return_qty,
                            "allowed": max(delivered_before, 0.0),
                        })

                if errors:

                    message = _(
                        "Cannot validate this return.\n\n"
                        "The following products exceed the quantity "
                        "that was delivered to the customer:\n\n"
                    )

                    for error in errors:

                        message += _(
                            "Product: %(product)s\n"
                            "Delivered Quantity: %(delivered)s\n"
                            "Current Return: %(current)s\n"
                            "Allowed Return: %(allowed)s\n\n",
                            **error
                        )

                    raise ValidationError(message)

            # =========================================================
            # NORMAL DELIVERY
            # =========================================================
            else:

                for sale_line, qty in current_qty.items():

                    ordered_qty = sale_line.product_uom_qty

                    delivered_before = (
                        self._get_sale_line_delivered_qty(
                            sale_line,
                            picking
                        )
                    )

                    total = delivered_before + qty

                    if total > ordered_qty:

                        errors.append({
                            "product": sale_line.product_id.display_name,
                            "ordered": ordered_qty,
                            "previous": delivered_before,
                            "allowed": ordered_qty - delivered_before,
                            "current": qty,
                            "total": total,
                        })

                if errors:

                    message = _(
                        "Cannot validate this delivery.\n\n"
                        "The following products exceed the Sales Order "
                        "quantity:\n\n"
                    )

                    for error in errors:

                        message += _(
                            "Product: %(product)s\n"
                            "Ordered Quantity: %(ordered)s\n"
                            "Already Delivered: %(previous)s\n"
                            "Current Delivery: %(current)s\n"
                            "Allowed Delivery: %(allowed)s\n\n",
                            **error
                        )

                    raise ValidationError(message)

        return super().button_validate()