# -*- coding: utf-8 -*-
# from odoo import http


# class SaleCreditControl(http.Controller):
#     @http.route('/sale_credit_control/sale_credit_control', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_credit_control/sale_credit_control/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_credit_control.listing', {
#             'root': '/sale_credit_control/sale_credit_control',
#             'objects': http.request.env['sale_credit_control.sale_credit_control'].search([]),
#         })

#     @http.route('/sale_credit_control/sale_credit_control/objects/<model("sale_credit_control.sale_credit_control"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_credit_control.object', {
#             'object': obj
#         })

