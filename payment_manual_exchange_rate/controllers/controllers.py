# -*- coding: utf-8 -*-
# from odoo import http


# class PaymentManualExchangeRate(http.Controller):
#     @http.route('/payment_manual_exchange_rate/payment_manual_exchange_rate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payment_manual_exchange_rate/payment_manual_exchange_rate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment_manual_exchange_rate.listing', {
#             'root': '/payment_manual_exchange_rate/payment_manual_exchange_rate',
#             'objects': http.request.env['payment_manual_exchange_rate.payment_manual_exchange_rate'].search([]),
#         })

#     @http.route('/payment_manual_exchange_rate/payment_manual_exchange_rate/objects/<model("payment_manual_exchange_rate.payment_manual_exchange_rate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment_manual_exchange_rate.object', {
#             'object': obj
#         })

