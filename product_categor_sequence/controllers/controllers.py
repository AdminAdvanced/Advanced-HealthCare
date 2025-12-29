# -*- coding: utf-8 -*-
# from odoo import http


# class ProductCategorSequence(http.Controller):
#     @http.route('/product_categor_sequence/product_categor_sequence', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_categor_sequence/product_categor_sequence/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_categor_sequence.listing', {
#             'root': '/product_categor_sequence/product_categor_sequence',
#             'objects': http.request.env['product_categor_sequence.product_categor_sequence'].search([]),
#         })

#     @http.route('/product_categor_sequence/product_categor_sequence/objects/<model("product_categor_sequence.product_categor_sequence"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_categor_sequence.object', {
#             'object': obj
#         })

