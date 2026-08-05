# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"


    exchange_rate = fields.Float(
        string="Exchange Rate",
        digits=(12, 6),
    )


    expected_exchange_rate = fields.Float(
        string="System Exchange Rate",
        compute="_compute_expected_exchange_rate",
        digits=(12, 6),
    )


    @api.depends(
        "currency_id",
        "company_currency_id",
        "payment_date",
    )
    def _compute_expected_exchange_rate(self):

        for wizard in self:

            if (
                not wizard.currency_id
                or wizard.currency_id == wizard.company_currency_id
            ):
                wizard.expected_exchange_rate = 1.0
                continue


            wizard.expected_exchange_rate = (
                wizard.company_currency_id._get_conversion_rate(
                    wizard.company_currency_id,
                    wizard.currency_id,
                    wizard.company_id,
                    wizard.payment_date,
                )
            )


    @api.onchange(
        "currency_id",
        "payment_date",
    )
    def _onchange_currency_rate(self):

        for wizard in self:

            if wizard.currency_id != wizard.company_currency_id:
                wizard.exchange_rate = (
                    wizard.expected_exchange_rate
                )


    def action_refresh_exchange_rate(self):

        for wizard in self:
            wizard.exchange_rate = wizard.expected_exchange_rate


    def _create_payment_vals_from_wizard(self, batch_result):

        vals = super()._create_payment_vals_from_wizard(
            batch_result
        )

        vals.update({
            "exchange_rate": self.exchange_rate,
        })

        return vals