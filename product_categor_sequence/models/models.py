from odoo import models, fields, api

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
        # لا نلمس أي create أثناء install / tests
        if self.env.context.get('install_mode') or self.env.context.get('test_enable'):
            return super().create(vals_list)

        for vals in vals_list:
            if vals.get('default_code'):
                continue

            categ_id = vals.get('categ_id')
            if not categ_id:
                continue

            category = self.env['product.category'].browse(categ_id)
            if not category or not category.x_product_sequence_id:
                continue

            vals['default_code'] = category.x_product_sequence_id.next_by_id()

        return super().create(vals_list)
