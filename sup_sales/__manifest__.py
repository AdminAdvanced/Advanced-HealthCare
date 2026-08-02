{
    "name": "SUP Sales",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": "Simple Sales Management without Delivery and Invoice",
    "author": "Advanced Event Solution / Bushra Alamarnah",

    "depends": [
        "base",
        "product",
        'mail',
        'hr',
        "account",
    ],

    "data": [
        "security/ir.model.access.csv",

        "data/sequence.xml",

        "views/customer_views.xml",
        "views/quotation_views.xml",
        "views/order_views.xml",
        "views/menu.xml",
        "views/search_quotation_views.xml",
        'report/quotation_report.xml',
        'report/quotation_template.xml',
    ],

    "installable": True,
    "application": True,
    "license": "LGPL-3",
}