from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    hide_delete_all = fields.Boolean(
        string="Hide Delete Option in All Records",
        help="Prevent this user from deleting any record in the system.",
    )

    delete_restriction_ids = fields.Many2many(
        comodel_name="ir.model",
        relation="res_users_delete_restriction_rel",
        column1="user_id",
        column2="model_id",
        string="Hide Delete Option for Specific Records",
        help="Select the record types for which delete should be disabled.",
    )

    def _is_delete_restricted(self, records):
        self.ensure_one()

        if not records:
            return False

        if self.hide_delete_all:
            return True

        restricted_models = self.delete_restriction_ids.mapped("model")

        return any(
            record._name in restricted_models
            for record in records
        )

    @api.model
    def check_user_delete_restriction(self, model_name):
        user = self.env.user

        if user.hide_delete_all:
            return True

        return model_name in user.delete_restriction_ids.mapped("model")