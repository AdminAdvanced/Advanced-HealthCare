# -*- coding: utf-8 -*-

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

    @api.model
    def _get_trigger_fields_to_synchronize(self):
        return super()._get_trigger_fields_to_synchronize() + (
            'exchange_rate',
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

    def _prepare_move_line_default_vals(
        self,
        write_off_line_vals=None,
        force_balance=None
    ):
        line_vals_list = super()._prepare_move_line_default_vals(
            write_off_line_vals=write_off_line_vals,
            force_balance=force_balance,
        )

        self.ensure_one()

        if (
            self.currency_id != self.company_id.currency_id
            and self.exchange_rate
        ):

            # amount in foreign currency
            liquidity_amount_currency = line_vals_list[0]['amount_currency']

            # 1 company currency = X foreign currency
            liquidity_balance = (
                liquidity_amount_currency / self.exchange_rate
            )

            line_vals_list[0].update({
                'debit': liquidity_balance if liquidity_balance > 0 else 0.0,
                'credit': -liquidity_balance if liquidity_balance < 0 else 0.0,
            })

            counterpart_balance = -liquidity_balance

            line_vals_list[1].update({
                'debit': counterpart_balance if counterpart_balance > 0 else 0.0,
                'credit': -counterpart_balance if counterpart_balance < 0 else 0.0,
            })

        return line_vals_list