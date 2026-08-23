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
        """
        Return only the lots that actually belong to this invoice line.

        Customer Invoice:
            Only OUTGOING stock moves are considered.

        Customer Credit Note:
            Only RETURN / INCOMING stock moves are considered.

        Lots are aggregated by lot so the same lot is not displayed
        multiple times when it exists in multiple stock moves.
        """

        self.ensure_one()

        result = defaultdict(lambda: {
            "lot_name": "",
            "quantity": 0.0,
            "uom_name": "",
            "expiration_date": "",
        })

        # ---------------------------------------------------------
        # Get stock moves related to this invoice line
        # ---------------------------------------------------------
        stock_moves = invoice_line.sale_line_ids.mapped("move_ids").filtered(
            lambda move: move.state == "done"
        )

        # ---------------------------------------------------------
        # Determine whether this is an Invoice or Credit Note
        # ---------------------------------------------------------
        is_credit_note = self.move_type == "out_refund"

        for move in stock_moves:

            # -----------------------------------------------------
            # CUSTOMER INVOICE
            # We only want goods delivered TO the customer.
            # -----------------------------------------------------
            if not is_credit_note:

                if move.location_dest_id.usage != "customer":
                    continue

            # -----------------------------------------------------
            # CUSTOMER CREDIT NOTE
            # We only want goods returned FROM the customer.
            # -----------------------------------------------------
            else:

                if move.location_id.usage != "customer":
                    continue

            # -----------------------------------------------------
            # Get move lines containing lots
            # -----------------------------------------------------
            move_lines = move.move_line_ids.filtered(
                lambda ml: ml.lot_id
            )

            for ml in move_lines:

                lot = ml.lot_id

                if not lot:
                    continue

                key = lot.id

                result[key]["lot_name"] = lot.name
                result[key]["quantity"] += ml.quantity
                result[key]["uom_name"] = ml.product_uom_id.name

                # -------------------------------------------------
                # LOT EXPIRATION DATE
                # -------------------------------------------------
                result[key]["expiration_date"] = (
                    lot.expiration_date.strftime("%d/%m/%Y")
                    if lot.expiration_date
                    else ""
                )

        return list(result.values())