from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    is_default = fields.Boolean(string="Default Packaging")
    product_id = fields.Many2one('product.product', string="Product")

    @api.onchange('is_default')
    def _onchange_is_default(self):
        if self.is_default and self.product_id:
            # نزيل الـ default الآخر داخل الـ one2many في form view قبل الحفظ
            for pack in self.product_id.packaging_ids:
                if pack != self:
                    pack.is_default = False


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_uom_qty')
    def _onchange_product_id_default_packaging(self):
        if not self.product_id:
            return

        default_packaging = self.env['product.packaging'].search([
            ('product_id', '=', self.product_id.id),
            ('is_default', '=', True),
        ], limit=1)

        if default_packaging:
            self.product_packaging_id = default_packaging


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id', 'product_qty')  # product_qty بدل product_uom_qty في الـ purchase
    def _onchange_product_id_default_packaging(self):
        if not self.product_id:
            return

        default_packaging = self.env['product.packaging'].search([
            ('product_id', '=', self.product_id.id),
            ('is_default', '=', True),
        ], limit=1)

        if default_packaging:
            self.product_packaging_id = default_packaging