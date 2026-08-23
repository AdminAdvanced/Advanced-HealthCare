from collections import defaultdict
from odoo import models
from odoo.fields import Datetime


class AccountMove(models.Model):
    _inherit = "account.move"

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

                # --- حل مشكلة التاريخ والـ Timezone ---
                exp_date = lot.expiration_date

                if exp_date:
                    # تحويل الوقت من UTC إلى الـ Timezone الخاص بالجهة/المستخدم في أودو
                    local_exp_date = Datetime.context_timestamp(self, exp_date)
                    result[key]["expiration_date"] = local_exp_date.strftime("%d/%m/%Y")
                else:
                    result[key]["expiration_date"] = ""

        return list(result.values())