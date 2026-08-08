# -*- coding: utf-8 -*-
# from odoo import http


# class PrintPreviewAll(http.Controller):
#     @http.route('/print_preview_all_disabled/print_preview_all_disabled', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/print_preview_all_disabled/print_preview_all_disabled/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('print_preview_all_disabled.listing', {
#             'root': '/print_preview_all_disabled/print_preview_all_disabled',
#             'objects': http.request.env['print_preview_all_disabled.print_preview_all_disabled'].search([]),
#         })

#     @http.route('/print_preview_all_disabled/print_preview_all_disabled/objects/<model("print_preview_all_disabled.print_preview_all_disabled"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('print_preview_all_disabled.object', {
#             'object': obj
#         })

