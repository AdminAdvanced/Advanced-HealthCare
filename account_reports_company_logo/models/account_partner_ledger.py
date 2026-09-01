# -*- coding: utf-8 -*-

from odoo import models


class PartnerLedgerCustomHandler(models.AbstractModel):
    _inherit = "account.partner.ledger.report.handler"

    def _get_partner_display_name(self, partner):
        """Return partner name according to the current user's language."""
        if not partner:
            return ""

        partner_name = partner.name or ""

        if (
            self.env.user.lang
            and self.env.user.lang.startswith("ar")
            and partner.x_studio_name_ar
        ):
            partner_name = partner.x_studio_name_ar

        return partner_name

    def _get_report_line_partners(
        self,
        options,
        partner,
        partner_values,
        level_shift=0,
    ):
        line = super()._get_report_line_partners(
            options,
            partner,
            partner_values,
            level_shift,
        )

        if partner:
            partner_name = self._get_partner_display_name(partner)

            if partner.contact_code:
                line["name"] = f"{partner.contact_code} - {partner_name}"
            else:
                line["name"] = partner_name

        return line