from odoo import fields, models


class SaleApprovalConfig(models.Model):
    _name = 'sale.approval.config'
    _description = 'Sales Approval Configuration'

    name = fields.Char(
        string='Configuration Name',
        required=True,
        default='Sales Approval Configuration',
    )

    enable_discount_approval = fields.Boolean(
        string='Require Approval: Discount Exceeds Pricelist',
        default=True,
        help=(
            'Require approval when the salesperson gives a discount '
            'greater than the discount allowed by the applicable pricelist rule.'
        ),
    )

    enable_credit_limit_approval = fields.Boolean(
        string='Require Approval: Credit Limit',
        default=True,
        help=(
            'Require approval when the sales order exceeds the customer '
            'available credit.'
        ),
    )

    enable_overdue_approval = fields.Boolean(
        string='Require Approval: Overdue Payments',
        default=True,
        help=(
            'Require approval when the customer has overdue unpaid invoices.'
        ),
    )

    enable_uninvoiced_sales_approval = fields.Boolean(
        string='Require Approval: Uninvoiced Sales',
        default=True,
        help=(
            'Require approval when the customer already has confirmed '
            'sales orders that have not yet been fully invoiced.'
        ),
    )