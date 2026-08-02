# -*- coding: utf-8 -*-
# from odoo import http


# class SaleOrderQtyValidation(http.Controller):
#     @http.route('/sale_order_qty_validation/sale_order_qty_validation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_qty_validation/sale_order_qty_validation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_qty_validation.listing', {
#             'root': '/sale_order_qty_validation/sale_order_qty_validation',
#             'objects': http.request.env['sale_order_qty_validation.sale_order_qty_validation'].search([]),
#         })

#     @http.route('/sale_order_qty_validation/sale_order_qty_validation/objects/<model("sale_order_qty_validation.sale_order_qty_validation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_qty_validation.object', {
#             'object': obj
#         })

