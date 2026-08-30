from odoo import models

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def unlink(self):
        """
        Journal lines belonging to Draft Journal Entries can be
        internally removed and recreated by Odoo while editing the
        Draft Journal Entry.

        Delete Control must not block those internal operations.
        """

        draft_lines = self.filtered(
            lambda line: line.move_id
            and line.move_id.state == "draft"
        )

        other_lines = self - draft_lines

        result = True

        if draft_lines:
            result = super(
                AccountMoveLine,
                draft_lines,
            ).unlink()

        if other_lines:
            result = super(
                AccountMoveLine,
                other_lines,
            ).unlink() and result

        return result

