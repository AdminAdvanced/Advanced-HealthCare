{
    'name': 'Sale Credit Control',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Credit control and sales approval checks',
    'depends': [
        'sale',
        'account',
        'sales_team'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/sale_approval_config_views.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}