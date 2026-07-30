# -*- coding: utf-8 -*-

from odoo import models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _prepare_move_lines_per_type(self, write_off_line_vals=None, force_balance=None):
        """
        Override Odoo payment journal item preparation
        to use manual exchange rate when provided.

        Manual rate format:
        1 Company Currency = X Payment Currency

        Example:
        1 SAR = 0.30 USD

        Balance calculation:
        USD amount / 0.30 = SAR balance
        """

        self.ensure_one()

        line_vals_per_type = super()._prepare_move_lines_per_type(
            write_off_line_vals=write_off_line_vals,
            force_balance=force_balance,
        )

        if (
                self.currency_id != self.company_currency_id
                and self.exchange_rate
        ):

            liquidity_lines = line_vals_per_type.get(
                'liquidity_lines',
                []
            )

            counterpart_lines = line_vals_per_type.get(
                'counterpart_lines',
                []
            )

            # Update liquidity line balance
            for line in liquidity_lines:
                amount_currency = line.get('amount_currency', 0.0)

                if amount_currency:
                    line['balance'] = (
                            amount_currency / self.exchange_rate
                    )

            # Keep journal entry balanced
            liquidity_balance = sum(
                line.get('balance', 0.0)
                for line in liquidity_lines
            )

            counterpart_balance = -liquidity_balance

            for line in counterpart_lines:
                line['balance'] = counterpart_balance

        return line_vals_per_type