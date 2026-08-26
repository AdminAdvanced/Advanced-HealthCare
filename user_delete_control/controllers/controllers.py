# -*- coding: utf-8 -*-
# from odoo import http


# class UserDeleteControl(http.Controller):
#     @http.route('/user_delete_control/user_delete_control', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/user_delete_control/user_delete_control/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('user_delete_control.listing', {
#             'root': '/user_delete_control/user_delete_control',
#             'objects': http.request.env['user_delete_control.user_delete_control'].search([]),
#         })

#     @http.route('/user_delete_control/user_delete_control/objects/<model("user_delete_control.user_delete_control"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('user_delete_control.object', {
#             'object': obj
#         })

