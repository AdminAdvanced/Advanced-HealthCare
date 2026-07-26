# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceReportCustom(http.Controller):
#     @http.route('/invoice_report_custom/invoice_report_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_report_custom/invoice_report_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_report_custom.listing', {
#             'root': '/invoice_report_custom/invoice_report_custom',
#             'objects': http.request.env['invoice_report_custom.invoice_report_custom'].search([]),
#         })

#     @http.route('/invoice_report_custom/invoice_report_custom/objects/<model("invoice_report_custom.invoice_report_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_report_custom.object', {
#             'object': obj
#         })

