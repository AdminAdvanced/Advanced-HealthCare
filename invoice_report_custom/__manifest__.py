{
    'name': 'Invoice Report Custom',
    'version': '18.0.1.0',
    "author": "Advanced Event Solution / Bushra Alamarnah",
    'license': 'LGPL-3',
    'depends': ['account',
                'l10n_gcc_invoice',
                'l10n_sa',
                'stock_account',
                'sale_stock',
                'l10n_gcc_invoice_stock_account',
                ],
    'assets': {
        'web.report_assets_common': [
            'invoice_report_custom/static/src/css/report.css',
        ],
    },
    'data': [
        'data/paperformat.xml',
        'views/invoice_report.xml',
    ],
    'installable': True,
}