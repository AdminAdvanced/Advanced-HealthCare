from odoo import models, fields, api, exceptions

class ProductCategory(models.Model):
    _inherit = 'product.category'

    x_product_sequence_id = fields.Many2one(
        'ir.sequence',
        string='Product Sequence'
    )

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    _sql_constraints = [
        ('default_code_uniq', 'unique(default_code)', 'Product code must be unique!')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('default_code') and vals.get('categ_id'):
                category = self.env['product.category'].browse(vals['categ_id'])
                if category.x_product_sequence_id:
                    vals['default_code'] = category.x_product_sequence_id.next_by_id()
        return super().create(vals_list)
