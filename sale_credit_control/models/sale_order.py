from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pricelist_item_id = fields.Many2one(store=True)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_state = fields.Selection(
        [
            ('not_required', 'Not Required'),
            ('pending', 'Pending Approval'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        string='Approval Status',
        default='not_required',
        copy=False,
    )

    discount_approval_required = fields.Boolean(
        string='Discount Approval Required',
        compute='_compute_approval_requirements',
        store=True,
    )

    credit_limit_approval_required = fields.Boolean(
        string='Credit Limit Approval Required',
        compute='_compute_approval_requirements',
        store=True,
    )

    overdue_approval_required = fields.Boolean(
        string='Overdue Approval Required',
        compute='_compute_approval_requirements',
        store=True,
    )

    uninvoiced_sales_approval_required = fields.Boolean(
        string='Uninvoiced Sales Approval Required',
        compute='_compute_approval_requirements',
        store=True,
    )

    approval_required = fields.Boolean(
        string='Approval Required',
        compute='_compute_approval_requirements',
        store=True,
    )

    approval_reason = fields.Text(
        string='Approval Reason',
        compute='_compute_approval_requirements',
        store=True,
    )

    @api.depends(
        'partner_id',
        'amount_total',
        'order_line.discount',
        'order_line.pricelist_item_id',
        'order_line.pricelist_item_id.percent_price',
    )
    def _compute_approval_requirements(self):

        Config = self.env['sale.approval.config']

        # Get the first active configuration.
        config = Config.search([], limit=1)

        for order in self:

            discount_required = False
            credit_required = False
            overdue_required = False
            uninvoiced_required = False

            reasons = []

            # ---------------------------------------------------------
            # 1. DISCOUNT APPROVAL
            # ---------------------------------------------------------

            if config and config.enable_discount_approval:

                for line in order.order_line:

                    if line.display_type:
                        continue

                    if not line.product_id:
                        continue

                    employee_discount = line.discount or 0.0

                    rule = line.pricelist_item_id

                    if rule:
                        allowed_discount = rule.percent_price or 0.0
                    else:
                        allowed_discount = 0.0

                    if employee_discount > allowed_discount:

                        discount_required = True

                        reasons.append(
                            "Discount exceeds pricelist limit for %s "
                            "(Applied: %.2f%%, Allowed: %.2f%%)"
                            % (
                                line.product_id.display_name,
                                employee_discount,
                                allowed_discount,
                            )
                        )

            # ---------------------------------------------------------
            # 2. CREDIT LIMIT APPROVAL
            # ---------------------------------------------------------

            if config and config.enable_credit_limit_approval:

                partner = order.partner_id.commercial_partner_id

                if partner:

                    available_credit = partner.available_credit

                    if order.amount_total > available_credit:

                        credit_required = True

                        reasons.append(
                            "Sales Order exceeds customer's available credit "
                            "(Order: %.2f, Available Credit: %.2f)"
                            % (
                                order.amount_total,
                                available_credit,
                            )
                        )

            # ---------------------------------------------------------
            # 3. OVERDUE PAYMENT APPROVAL
            # ---------------------------------------------------------

            if config and config.enable_overdue_approval:

                partner = order.partner_id.commercial_partner_id

                if partner:

                    overdue_amount = getattr(partner, 'total_all_overdue', 0.0)
                    if overdue_amount > 0:
                        overdue_required = True

                        reasons.append(
                            "Customer has overdue unpaid invoices "
                            "(Overdue Amount: %.2f)"
                            % overdue_amount
                        )

            # ---------------------------------------------------------
            # 4. UNINVOICED SALES APPROVAL
            # ---------------------------------------------------------

            if config and config.enable_uninvoiced_sales_approval:

                partner = order.partner_id.commercial_partner_id

                if partner:

                    uninvoiced_amount = partner.confirmed_uninvoiced_sales

                    if uninvoiced_amount > 0:

                        uninvoiced_required = True

                        reasons.append(
                            "Customer has confirmed uninvoiced sales "
                            "(Uninvoiced Amount: %.2f)"
                            % uninvoiced_amount
                        )

            # ---------------------------------------------------------
            # FINAL RESULT
            # ---------------------------------------------------------

            order.discount_approval_required = discount_required
            order.credit_limit_approval_required = credit_required
            order.overdue_approval_required = overdue_required
            order.uninvoiced_sales_approval_required = uninvoiced_required

            order.approval_required = (
                discount_required
                or credit_required
                or overdue_required
                or uninvoiced_required
            )

            order.approval_reason = '\n'.join(reasons)

    def action_confirm(self):
        orders_to_confirm = self.env['sale.order']

        for order in self:

            if order.approval_required and order.approval_state != 'approved':
                order.approval_state = 'pending'
            else:
                orders_to_confirm |= order

        if orders_to_confirm:
            return super(SaleOrder, orders_to_confirm).action_confirm()

        return True