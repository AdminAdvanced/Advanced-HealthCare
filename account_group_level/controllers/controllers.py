# -*- coding: utf-8 -*-
# from odoo import http


# class AccountGroupLevel(http.Controller):
#     @http.route('/account_group_level/account_group_level', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_group_level/account_group_level/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_group_level.listing', {
#             'root': '/account_group_level/account_group_level',
#             'objects': http.request.env['account_group_level.account_group_level'].search([]),
#         })

#     @http.route('/account_group_level/account_group_level/objects/<model("account_group_level.account_group_level"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_group_level.object', {
#             'object': obj
#         })

