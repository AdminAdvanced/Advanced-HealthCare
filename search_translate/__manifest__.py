# -*- coding: utf-8 -*-
{
    'name': "search_translate",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """
Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', "contacts" ,"base_address_extended", 'sale',
    'hr',],
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/sale_report_views.xml',
        'views/account_reports_logo.xml',
    ],
    "installable": True,
    "license": "LGPL-3",
}

