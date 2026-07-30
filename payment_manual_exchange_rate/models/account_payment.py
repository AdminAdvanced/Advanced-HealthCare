# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    exchange_rate = fields.Float(
        string="Exchange Rate",
        digits=(12, 6),
        help="Manual exchange rate: 1 company currency = X payment currency",
    )

    expected_exchange_rate = fields.Float(
        string="System Exchange Rate",
        compute="_compute_expected_exchange_rate",
        digits=(12, 6),
    )

    exchange_rate_label = fields.Char(
        compute="_compute_exchange_rate_label"
    )

    @api.depends(
        "currency_id",
        "company_currency_id",
        "date",
    )
    def _compute_expected_exchange_rate(self):
        for payment in self:

            if (
                not payment.currency_id
                or payment.currency_id == payment.company_currency_id
            ):
                payment.expected_exchange_rate = 1.0
                continue

            payment.expected_exchange_rate = (
                payment.company_currency_id._get_conversion_rate(
                    payment.company_currency_id,
                    payment.currency_id,
                    payment.company_id,
                    payment.date,
                )
            )


    @api.onchange(
        "currency_id",
        "date",
    )
    def _onchange_currency_rate(self):
        for payment in self:
            if payment.currency_id != payment.company_currency_id:
                payment.exchange_rate = payment.expected_exchange_rate


    def action_refresh_exchange_rate(self):

        for payment in self:
            payment.exchange_rate = payment.expected_exchange_rate

        return True

    @api.depends(
        'currency_id',
        'company_currency_id',
        'exchange_rate'
    )
    def _compute_exchange_rate_label(self):
        for payment in self:
            if payment.currency_id != payment.company_currency_id:
                payment.exchange_rate_label = (
                    f"1 {payment.company_currency_id.name} = "
                    f"{payment.exchange_rate:.6f} "
                    f"{payment.currency_id.name}"
                )
            else:
                payment.exchange_rate_label = False


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