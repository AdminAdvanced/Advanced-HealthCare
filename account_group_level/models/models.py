from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountGroup(models.Model):
    _inherit = 'account.account'

    x_parent_id = fields.Many2one(
        'account.account',
        string='Parent Group',
        ondelete='restrict'
    )

    level = fields.Integer(
        string='Level',
        compute='_compute_level',
        store=True
    )

    @api.depends('x_parent_id')
    def _compute_level(self):
        for rec in self:
            level = 1
            parent = rec.x_parent_id
            while parent:
                level += 1
                parent = parent.x_parent_id
            rec.level = level

    @api.constrains('x_parent_id')
    def _check_no_recursive_parent(self):
        for rec in self:
            parent = rec.x_parent_id
            while parent:
                if parent == rec:
                    raise ValidationError(
                        'Recursive parent groups are not allowed.'
                    )
                parent = parent.x_parent_id
