{
    'name': 'Invoice Report Custom',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'depends': ['account',
                'l10n_gcc_invoice',
                'l10n_sa',],
    'data': [
        'views/invoice_report.xml',
    ],
    'installable': True,
}