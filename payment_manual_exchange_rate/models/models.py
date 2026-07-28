# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class payment_manual_exchange_rate(models.Model):
#     _name = 'payment_manual_exchange_rate.payment_manual_exchange_rate'
#     _description = 'payment_manual_exchange_rate.payment_manual_exchange_rate'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

