from odoo import models, fields
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):

    _inherit = "product.category"


    # Checkbox لتحديد أن هذه الكاتجوري هي آخر Level
    # والمنتجات التي تحتها تستخدم Sequence
    is_sequence_category = fields.Boolean(
        string="Is Last Level Sequence Category?"
    )


    # Prefix بداية الرقم
    # مثال:
    # CF-001
    sequence_prefix = fields.Char(
        string="Prefix"
    )


    # عدد الخانات بعد الـ Prefix
    # مثال:
    # 5 يعطي 00001
    sequence_padding = fields.Integer(
        string="Sequence Size",
        default=5
    )


    # مقدار الزيادة بعد كل Product
    # مثال:
    # 1 => 1,2,3
    # 10 => 10,20,30
    sequence_step = fields.Integer(
        string="Step",
        default=1
    )


    # الرقم القادم الذي سيتم استخدامه
    sequence_next_number = fields.Integer(
        string="Next Number",
        default=1
    )


    def write(self, vals):

        result = super().write(vals)


        for category in self:

            # التأكد أن الكاتجوري المختارة كـ Last Level
            # لا تحتوي على Sub Categories
            if (
                category.is_sequence_category
                and category.child_id
            ):

                raise ValidationError(
                    "Sequence category must be the last level category."
                )


        return result