# -*- coding: utf-8 -*-
# from odoo import http


# class CustomAgedPartnerBalancePeriods(http.Controller):
#     @http.route('/custom_aged_partner_balance_periods/custom_aged_partner_balance_periods', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_aged_partner_balance_periods/custom_aged_partner_balance_periods/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_aged_partner_balance_periods.listing', {
#             'root': '/custom_aged_partner_balance_periods/custom_aged_partner_balance_periods',
#             'objects': http.request.env['custom_aged_partner_balance_periods.custom_aged_partner_balance_periods'].search([]),
#         })

#     @http.route('/custom_aged_partner_balance_periods/custom_aged_partner_balance_periods/objects/<model("custom_aged_partner_balance_periods.custom_aged_partner_balance_periods"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_aged_partner_balance_periods.object', {
#             'object': obj
#         })

