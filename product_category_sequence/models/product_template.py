from odoo import models, api


class ProductTemplate(models.Model):

    _inherit = "product.template"


    @api.model_create_multi
    def create(self, vals_list):

        # إنشاء المنتجات أولاً
        products = super().create(vals_list)


        for product in products:


            # جلب الكاتجوري المختارة للمنتج
            category = product.categ_id


            # إذا كانت الكاتجوري مفعلة للـ Sequence
            if category.is_sequence_category:


                # قراءة الرقم الحالي
                number = category.sequence_next_number


                # تكوين الـ Reference
                reference = (
                    f"{category.sequence_prefix or ''}"
                    f"{str(number).zfill(category.sequence_padding)}"
                )


                # وضع الرقم في Internal Reference
                # هذا هو حقل default_code
                product.default_code = reference


                # تحديث الرقم القادم
                category.sequence_next_number += category.sequence_step


        return products