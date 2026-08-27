from odoo import _, exceptions, models


class Base(models.AbstractModel):
    _inherit = "base"

    def unlink(self):
        # ---------------------------------------------------------
        # Odoo may call unlink() on an empty recordset internally.
        # This is not a real delete operation.
        # ---------------------------------------------------------
        if not self:
            return super().unlink()

        # ---------------------------------------------------------
        # Some Odoo internal operations need to delete/update
        # analytic lines while posting/resetting documents.
        # This is an internal operation, not a user delete action.
        # ---------------------------------------------------------
        if self.env.context.get("skip_analytic_sync"):
            return super().unlink()

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