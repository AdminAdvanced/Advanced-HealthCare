# -*- coding: utf-8 -*-
# from odoo import http


# class PartnerCodeSequence(http.Controller):
#     @http.route('/partner_code_sequence/partner_code_sequence', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partner_code_sequence/partner_code_sequence/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('partner_code_sequence.listing', {
#             'root': '/partner_code_sequence/partner_code_sequence',
#             'objects': http.request.env['partner_code_sequence.partner_code_sequence'].search([]),
#         })

#     @http.route('/partner_code_sequence/partner_code_sequence/objects/<model("partner_code_sequence.partner_code_sequence"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partner_code_sequence.object', {
#             'object': obj
#         })

