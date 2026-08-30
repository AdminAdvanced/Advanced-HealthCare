import logging

from odoo import _, exceptions, models


_logger = logging.getLogger(__name__)


class Base(models.AbstractModel):
    _inherit = "base"

    _DELETE_CONTROL_DRAFT_MODELS = {
        "sale.order",
        "purchase.order",
        "account.move",
        "account.payment",
        "stock.picking",
    }

    _DELETE_CONTROL_STATE_FIELDS = {
        "sale.order": "state",
        "purchase.order": "state",
        "account.move": "state",
        "account.payment": "state",
        "stock.picking": "state",
    }

    _DELETE_CONTROL_DRAFT_STATES = {
        "sale.order": {"draft", "sent"},
        "purchase.order": {"draft", "sent"},
        "account.move": {"draft"},
        "account.payment": {"draft"},
        "stock.picking": {"draft"},
    }

    def _delete_control_is_draft(self):
        model_name = self._name

        if model_name not in self._DELETE_CONTROL_DRAFT_MODELS:
            return False

        state_field = self._DELETE_CONTROL_STATE_FIELDS.get(model_name)

        if not state_field or state_field not in self._fields:
            return False

        draft_states = self._DELETE_CONTROL_DRAFT_STATES.get(
            model_name,
            {"draft"},
        )

        return all(
            record[state_field] in draft_states
            for record in self
        )

    def unlink(self):

        if not self:
            return super().unlink()

        user = self.env.user

        if user._is_superuser():
            return super().unlink()

        # Odoo internal dynamic unlink operation.
        # This happens while creating/reversing documents
        # such as Credit Notes.
        if self.env.context.get("dynamic_unlink"):
            return super().unlink()

        if user._is_delete_restricted(self):
            raise exceptions.UserError(
                _(
                    "Deleting records in '%s' is restricted for your account."
                )
                % self._description
            )

        return super().unlink()