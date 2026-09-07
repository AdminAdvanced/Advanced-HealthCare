from datetime import datetime, timedelta

from odoo import models


class AgedPartnerBalanceCustomHandler(models.AbstractModel):
    _inherit = "account.aged.partner.balance.report.handler"

    def _custom_options_initializer(self, report, options, previous_options):
        super()._custom_options_initializer(
            report,
            options,
            previous_options,
        )

        interval = options.get("aging_interval", 30)

        for column in options.get("columns", []):
            label = column.get("expression_label")

            if label == "period5":
                column["name"] = f"{interval * 4 + 1}-{interval * 5}"

            elif label == "period6":
                column["name"] = f"{interval * 5 + 1}-{interval * 6}"

            elif label == "period7":
                column["name"] = "Older"

    def _build_domain_from_period(self, options, period):
        """
        Aging periods:

        period0 = At Date
        period1 = 1-30
        period2 = 31-60
        period3 = 61-90
        period4 = 91-120
        period5 = 121-150
        period6 = 151-180
        period7 = Older (181+)
        """

        if period == "total" or not period or not period[-1].isdigit():
            return []

        period_number = int(period[-1])
        date_to = options["date"]["date_to"]

        # At Date
        if period_number == 0:
            return [
                "|",
                ("date_maturity", ">=", date_to),
                "&",
                ("date_maturity", "=", False),
                ("date", ">=", date_to),
            ]

        options_date_to = datetime.strptime(
            date_to,
            "%Y-%m-%d",
        )

        # Older = 181+
        if period_number == 7:
            period_end = options_date_to - timedelta(days=180)

            return [
                "|",
                ("date_maturity", "<=", period_end),
                "&",
                ("date_maturity", "=", False),
                ("date", "<=", period_end),
            ]

        # 1-30, 31-60, ..., 151-180
        period_end = options_date_to - timedelta(
            days=30 * (period_number - 1) + 1
        )

        period_start = options_date_to - timedelta(
            days=30 * period_number
        )

        return [
            "|",
            "&",
            ("date_maturity", ">=", period_start),
            ("date_maturity", "<=", period_end),
            "&",
            "&",
            ("date_maturity", "=", False),
            ("date", ">=", period_start),
            ("date", "<=", period_end),
        ]


class AgedReceivableCustomHandler(models.AbstractModel):
    _inherit = "account.aged.receivable.report.handler"

    def _custom_unfold_all_batch_data_generator(
        self,
        report,
        options,
        lines_to_expand_by_function,
    ):
        """
        Odoo 18's standard aged partner optimization is hardcoded
        to 6 periods.

        We now have 8 periods, so disable that optimization and
        allow the normal report computation to handle the lines.
        """
        return {}


class AgedPayableCustomHandler(models.AbstractModel):
    _inherit = "account.aged.payable.report.handler"

    def _custom_unfold_all_batch_data_generator(
        self,
        report,
        options,
        lines_to_expand_by_function,
    ):
        """
        Odoo 18's standard aged partner optimization is hardcoded
        to 6 periods.

        We now have 8 periods, so disable that optimization and
        allow the normal report computation to handle the lines.
        """
        return {}