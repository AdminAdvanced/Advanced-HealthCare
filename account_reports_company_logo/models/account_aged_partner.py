# -*- coding: utf-8 -*-

from odoo import models


class AgedReceivableReportHandler(models.AbstractModel):
    _inherit = "account.aged.receivable.report.handler"

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

    def _custom_line_postprocessor(self, report, options, lines):
        lines = super()._custom_line_postprocessor(
            report,
            options,
            lines,
        )

        for line in lines:
            model, model_id = report._get_model_info_from_id(line["id"])

            if model == "res.partner" and model_id:
                partner = self.env["res.partner"].browse(model_id)

                partner_name = self._get_partner_display_name(partner)

                if partner.contact_code:
                    line["name"] = (
                        f"{partner.contact_code} - {partner_name}"
                    )
                else:
                    line["name"] = partner_name

        return lines


class AgedPayableReportHandler(models.AbstractModel):
    _inherit = "account.aged.payable.report.handler"

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

    def _custom_line_postprocessor(self, report, options, lines):
        lines = super()._custom_line_postprocessor(
            report,
            options,
            lines,
        )

        for line in lines:
            model, model_id = report._get_model_info_from_id(line["id"])

            if model == "res.partner" and model_id:
                partner = self.env["res.partner"].browse(model_id)

                partner_name = self._get_partner_display_name(partner)

                if partner.contact_code:
                    line["name"] = (
                        f"{partner.contact_code} - {partner_name}"
                    )
                else:
                    line["name"] = partner_name

        return lines