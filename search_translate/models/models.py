from odoo import models, fields, api
from odoo.osv import expression


class ResCity(models.Model):
    _inherit = 'res.city'

    def name_get(self):
        result = []
        for rec in self:
            name = rec.name or ''
            if rec.x_studio_city_name_ar:
                name = f"{rec.name} - {rec.x_studio_city_name_ar}"
            result.append((rec.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []

        if name:
            domain = [
                '|',
                ('name', operator, name),
                ('x_studio_city_name_ar', operator, name),
            ]

        return self.search(domain + args, limit=limit).name_get()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []

        if name:
            domain = [
                '|', '|',
                ('name', operator, name),
                ('x_studio_name_ar', operator, name),
                ('vat', operator, name),  # الرقم الضريبي
            ]
        else:
            domain = []

        records = self.search(domain + args, limit=limit)
        return [(rec.id, rec.display_name) for rec in records]


class ResCountryState(models.Model):
    _inherit = ['res.country.state']

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []

        if name:
            domain = [
                '|',
                ('name', operator, name),
                ('x_studio_state_name_ar', operator, name),
            ]
        else:
            domain = []

        records = self.search(domain + args, limit=limit)
        return [(rec.id, rec.display_name) for rec in records]


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []

        if name:
            domain = [
                '|', '|','|','|','|',
                ('product_tmpl_id.name', operator, name),
                ('product_tmpl_id.x_studio_product_name_ar', operator, name),
                ('name', operator, name),
                ('x_studio_product_name_ar', operator, name),
                ('default_code', operator, name),  # كود المنتج
                ('x_studio_sku', operator, name),
                ('product_tmpl_id.x_studio_sku', operator, name),
            ]
        else:
            domain = []

        records = self.search(domain + args, limit=limit)
        return [(rec.id, rec.display_name) for rec in records]
