# -*- coding: utf-8 -*-
# from odoo import http


# class ProductCategorySequence(http.Controller):
#     @http.route('/product_category_sequence/product_category_sequence', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_category_sequence/product_category_sequence/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_category_sequence.listing', {
#             'root': '/product_category_sequence/product_category_sequence',
#             'objects': http.request.env['product_category_sequence.product_category_sequence'].search([]),
#         })

#     @http.route('/product_category_sequence/product_category_sequence/objects/<model("product_category_sequence.product_category_sequence"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_category_sequence.object', {
#             'object': obj
#         })

