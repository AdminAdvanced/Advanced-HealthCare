# -*- coding: utf-8 -*-
# from odoo import http


# class PrintPreviewAll(http.Controller):
#     @http.route('/print_preview_all/print_preview_all', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/print_preview_all/print_preview_all/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('print_preview_all.listing', {
#             'root': '/print_preview_all/print_preview_all',
#             'objects': http.request.env['print_preview_all.print_preview_all'].search([]),
#         })

#     @http.route('/print_preview_all/print_preview_all/objects/<model("print_preview_all.print_preview_all"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('print_preview_all.object', {
#             'object': obj
#         })

