# -*- coding: utf-8 -*-

from odoo import models


class AgedReceivableReportHandler(models.AbstractModel):
    _inherit = "account.aged.receivable.report.handler"

    def _custom_line_postprocessor(self, report, options, lines):
        lines = super()._custom_line_postprocessor(report, options, lines)

        for line in lines:
            model, model_id = report._get_model_info_from_id(line['id'])

            if model == 'res.partner' and model_id:
                partner = self.env['res.partner'].browse(model_id)

                if partner.contact_code:
                    line['name'] = f"{partner.contact_code} - {partner.name or ''}"

        return lines


class AgedPayableReportHandler(models.AbstractModel):
    _inherit = "account.aged.payable.report.handler"

    def _custom_line_postprocessor(self, report, options, lines):
        lines = super()._custom_line_postprocessor(report, options, lines)

        for line in lines:
            model, model_id = report._get_model_info_from_id(line['id'])

            if model == 'res.partner' and model_id:
                partner = self.env['res.partner'].browse(model_id)

                if partner.contact_code:
                    line['name'] = f"{partner.contact_code} - {partner.name or ''}"

        return lines