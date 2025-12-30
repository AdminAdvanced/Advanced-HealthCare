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
        safe_vals_list = []
        for vals in vals_list:
            try:
                if vals.get('default_code'):
                    safe_vals_list.append(vals)
                    continue

                categ_id = vals.get('categ_id')
                if not categ_id:
                    safe_vals_list.append(vals)
                    continue

                category = self.env['product.category'].browse(categ_id)
                if not category or not category.exists():
                    safe_vals_list.append(vals)
                    continue

                sequence = category.x_product_sequence_id
                if sequence:
                    vals['default_code'] = sequence.next_by_id()
            except Exception as e:
                # أي خطأ أثناء test أو automated creation، نتجاهله
                pass

            safe_vals_list.append(vals)

        return super().create(safe_vals_list)

