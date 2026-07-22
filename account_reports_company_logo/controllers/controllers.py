# -*- coding: utf-8 -*-
# from odoo import http


# class AccountReportsCompanyLogo(http.Controller):
#     @http.route('/account_reports_company_logo/account_reports_company_logo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_reports_company_logo/account_reports_company_logo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_reports_company_logo.listing', {
#             'root': '/account_reports_company_logo/account_reports_company_logo',
#             'objects': http.request.env['account_reports_company_logo.account_reports_company_logo'].search([]),
#         })

#     @http.route('/account_reports_company_logo/account_reports_company_logo/objects/<model("account_reports_company_logo.account_reports_company_logo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_reports_company_logo.object', {
#             'object': obj
#         })

