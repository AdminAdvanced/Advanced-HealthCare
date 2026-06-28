# -*- coding: utf-8 -*-
# from odoo import http


# class DefaultPackaging(http.Controller):
#     @http.route('/default_packaging/default_packaging', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/default_packaging/default_packaging/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('default_packaging.listing', {
#             'root': '/default_packaging/default_packaging',
#             'objects': http.request.env['default_packaging.default_packaging'].search([]),
#         })

#     @http.route('/default_packaging/default_packaging/objects/<model("default_packaging.default_packaging"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('default_packaging.object', {
#             'object': obj
#         })

