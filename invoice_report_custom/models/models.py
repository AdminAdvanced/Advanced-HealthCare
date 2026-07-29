from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoiced_lot_values(self):
        """
        Extend standard Odoo lot values
        Add Arabic fields.
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

        return res


    def get_invoice_line_lots(self, invoice_line):
        """
        Return lots related to the exact invoice line.

        Works with:
        - Invoice created from Sales Order
        - Invoice created manually
        - Same product repeated on multiple lines
        """

        self.ensure_one()

        result = []

        # ---------------------------------
        # Case 1:
        # Invoice generated from Sales Order
        # ---------------------------------

        for sale_line in invoice_line.sale_line_ids:

            for move in sale_line.move_ids.filtered(
                lambda m: m.state == "done"
            ):

                for move_line in move.move_line_ids.filtered(
                    lambda ml: ml.lot_id
                ):

                    result.append({
                        "lot_name": move_line.lot_id.name,
                        "quantity": move_line.quantity,
                        "uom_name": move_line.product_uom_id.name,
                        "uom_name_ar": (
                            move_line.product_uom_id.x_studio_unit_of_measure_ar
                            or ""
                        ),
                        "product_name_ar": (
                            move_line.product_id
                            .product_tmpl_id
                            .x_studio_product_name_ar
                            or ""
                        ),
                    })

        if result:
            return result


        # ---------------------------------
        # Case 2:
        # Direct invoice without Sales Order
        # ---------------------------------

        if invoice_line.product_id:

            # Search stock moves linked to this invoice line
            moves = self.env["stock.move"].search([
                ("product_id", "=", invoice_line.product_id.id),
                ("state", "=", "done"),
                ("move_line_ids.lot_id", "!=", False),
                "|",
                ("origin", "=", self.invoice_origin),
                ("picking_id", "in", self.picking_ids.ids),
            ])

            for move in moves:

                for move_line in move.move_line_ids.filtered(
                    lambda ml: ml.lot_id
                ):

                    result.append({
                        "lot_name": move_line.lot_id.name,
                        "quantity": move_line.quantity,
                        "uom_name": move_line.product_uom_id.name,
                        "uom_name_ar": (
                            move_line.product_uom_id.x_studio_unit_of_measure_ar
                            or ""
                        ),
                        "product_name_ar": (
                            move_line.product_id
                            .product_tmpl_id
                            .x_studio_product_name_ar
                            or ""
                        ),
                    })

        return result