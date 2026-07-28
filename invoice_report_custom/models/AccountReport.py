from odoo import models


class AccountReport(models.Model):
    _inherit = "account.report"

    def get_default_report_filename(self, options, extension):
        filename = super().get_default_report_filename(options, extension)

        # Partner Ledger فقط
        if self.id != self.env.ref("account_reports.partner_ledger_report").id:
            return filename

        partner_ids = options.get("partner_ids") or []

        if len(partner_ids) == 1:
            partner = self.env["res.partner"].browse(partner_ids[0])
            return f"{partner.name}.{extension}"

        return filename