from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    x_product_sequence_id = fields.Many2one(
        'ir.sequence',
        string='Product Sequence'
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

