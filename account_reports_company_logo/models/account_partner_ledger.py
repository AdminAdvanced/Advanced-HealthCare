# -*- coding: utf-8 -*-

from odoo import models


class PartnerLedgerCustomHandler(models.AbstractModel):
    _inherit = "account.partner.ledger.report.handler"

    def _get_report_line_partners(self, options, partner, partner_values, level_shift=0):
        line = super()._get_report_line_partners(
            options,
            partner,
            partner_values,
            level_shift,
        )

        if partner:
            if partner.contact_code:
                line["name"] = f"{partner.contact_code} - {partner.name or ''}"

        return line