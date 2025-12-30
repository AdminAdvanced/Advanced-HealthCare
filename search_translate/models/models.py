from odoo import models, fields, api

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
                '|',
                ('name', operator, name),
                ('x_studio_name_ar', operator, name),
            ]
        else:
            domain = []

        records = self.search(domain + args, limit=limit)
        return [(rec.id, rec.display_name) for rec in records]
