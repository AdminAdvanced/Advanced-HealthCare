# -*- coding: utf-8 -*-
# from odoo import http


# class SalesOrderEdit(http.Controller):
#     @http.route('/sales_order_edit/sales_order_edit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_order_edit/sales_order_edit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_order_edit.listing', {
#             'root': '/sales_order_edit/sales_order_edit',
#             'objects': http.request.env['sales_order_edit.sales_order_edit'].search([]),
#         })

#     @http.route('/sales_order_edit/sales_order_edit/objects/<model("sales_order_edit.sales_order_edit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_order_edit.object', {
#             'object': obj
#         })

