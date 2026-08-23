from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    confirmed_uninvoiced_sales = fields.Monetary(
        string='Confirmed Uninvoiced Sales',
        compute='_compute_confirmed_uninvoiced_sales',
        currency_field='company_currency_id',
        help=(
            'Total amount, including taxes, remaining to be invoiced '
            'from confirmed sales orders for this customer.'
        ),
    )

    available_credit = fields.Monetary(
        string='Available Credit',
        compute='_compute_available_credit',
        currency_field='company_currency_id',
        help=(
            'Credit limit minus total receivable and confirmed '
            'uninvoiced sales.'
        ),
    )

    company_currency_id = fields.Many2one(
        'res.currency',
        string='Company Currency',
        compute='_compute_company_currency',
    )

    @api.depends('company_id')
    def _compute_company_currency(self):
        for partner in self:
            partner.company_currency_id = (
                partner.company_id.currency_id
                or self.env.company.currency_id
            )

    def _compute_confirmed_uninvoiced_sales(self):
        SaleOrder = self.env['sale.order']

        for partner in self:
            commercial_partner = partner.commercial_partner_id

            orders = SaleOrder.search([
                ('partner_id', 'child_of', commercial_partner.id),
                ('state', 'in', ['sale', 'done']),
            ])

            total = 0.0

            for order in orders:
                for line in order.order_line:
                    if line.display_type:
                        continue

                    if line.amount_to_invoice > 0:
                        total += line.amount_to_invoice

            partner.confirmed_uninvoiced_sales = total
    @api.depends(
        'credit_limit',
        'credit',
        'confirmed_uninvoiced_sales',
    )
    def _compute_available_credit(self):
        for partner in self:
            partner.available_credit = (
                partner.credit_limit
                - partner.credit
                - partner.confirmed_uninvoiced_sales
            )

