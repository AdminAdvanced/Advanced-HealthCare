# -*- coding: utf-8 -*-
# from odoo import http


# class SupSales(http.Controller):
#     @http.route('/sup_sales/sup_sales', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sup_sales/sup_sales/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sup_sales.listing', {
#             'root': '/sup_sales/sup_sales',
#             'objects': http.request.env['sup_sales.sup_sales'].search([]),
#         })

#     @http.route('/sup_sales/sup_sales/objects/<model("sup_sales.sup_sales"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sup_sales.object', {
#             'object': obj
#         })

