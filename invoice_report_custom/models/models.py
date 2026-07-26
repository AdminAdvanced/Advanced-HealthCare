# -*- coding: utf-8 -*-
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoiced_lot_values(self):
        values = super()._get_invoiced_lot_values()

        for val in values:
            lot = self.env['stock.lot'].browse(val['lot_id'])
            val['product_id'] = lot.product_id.id

        return values