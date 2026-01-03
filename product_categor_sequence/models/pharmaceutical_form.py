from odoo import models, fields, api

class PharmaceuticalForm(models.Model):
    _name = 'pharmaceutical.form'
    _description = 'Pharmaceutical Form'
    _parent_name = 'parent_id'
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'parent_path, name'

    name = fields.Char(required=True, translate=True)

    parent_id = fields.Many2one(
        'pharmaceutical.form',
        string='Parent Form',
        index=True,
        ondelete='cascade'
    )

    child_ids = fields.One2many(
        'pharmaceutical.form',
        'parent_id',
        string='Child Forms'
    )

    parent_path = fields.Char(index=True)

    complete_name = fields.Char(
        compute='_compute_complete_name',
        store=True
    )

    _sql_constraints = [
        ('name_parent_uniq',
         'unique(name, parent_id)',
         'The name must be unique per parent.')
    ]

    @api.depends('name', 'parent_id', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for rec in self:
            if rec.parent_id and rec.parent_id.complete_name:
                rec.complete_name = f"{rec.parent_id.complete_name} / {rec.name}"
            else:
                rec.complete_name = rec.name

    def name_get(self):
        return [(rec.id, rec.complete_name or rec.name or '') for rec in self]
