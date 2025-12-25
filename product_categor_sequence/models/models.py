from odoo import models, fields, api, exceptions

class ProductCategory(models.Model):
    _inherit = 'product.category'

    x_product_sequence_id = fields.Many2one(
        'ir.sequence',
        string='Product Sequence'
    )

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # لا نولّد كود إذا كان موجود
            if vals.get('default_code'):
                continue

            categ_id = vals.get('categ_id')
            if not categ_id:
                continue

            category = self.env['product.category'].browse(categ_id).exists()
            if not category:
                continue

            sequence = category.x_product_sequence_id
            if not sequence:
                continue

            vals['default_code'] = sequence.next_by_id()

        return super().create(vals_list)

