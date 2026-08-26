from odoo import _, exceptions, models


class Base(models.AbstractModel):
    _inherit = "base"

    def unlink(self):
        user = self.env.user

        if not user._is_superuser():
            if user._is_delete_restricted(self):
                raise exceptions.UserError(
                    _(
                        "Deleting records in '%s' is restricted for your account."
                    )
                    % self._description
                )

        return super().unlink()