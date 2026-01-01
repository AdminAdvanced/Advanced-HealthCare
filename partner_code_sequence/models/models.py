from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_code = fields.Char(
        string='Contact Code',
        copy=False,
        index=True
    )
    city_id = fields.Many2one(
        'res.city',
        string='City.',
        domain = "[('country_id', '=', country_id)]"
    )
    show_in_customer = fields.Boolean(compute='_compute_show_flags',store=True)
    show_in_vendor = fields.Boolean(compute='_compute_show_flags',store=True)

    _sql_constraints = [
        ('contact_code_unique', 'unique(contact_code)', 'Contact Code must be unique!')
    ]

    @api.depends('category_id')
    def _compute_show_flags(self):
        for partner in self:
            partner.show_in_customer = False
            partner.show_in_vendor = False

            for cat in partner.category_id:
                if cat.show_in_customer:
                    partner.show_in_customer = True
                if cat.show_in_vendor:
                    partner.show_in_vendor = True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('contact_code'):
                continue

            category_ids = []

            for command in vals.get('category_id', []):
                if command[0] == 6:        # (6, 0, [ids])
                    category_ids += command[2]
                elif command[0] == 4:      # (4, id)
                    category_ids.append(command[1])

            if category_ids:
                categories = self.env['res.partner.category'].browse(category_ids)
                for cat in categories:
                    if cat.sequence_id:
                        vals['contact_code'] = cat.sequence_id.next_by_id()
                        break

        return super().create(vals_list)

class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    sequence_id = fields.Many2one(
        'ir.sequence',
        string='Contact Sequence'
    )
    show_in_customer = fields.Boolean("Show in Customer")
    show_in_vendor = fields.Boolean("Show in Vendor")


