# -*- coding: utf-8 -*-
# Part of DigitsCode. See LICENSE file for full copyright and licensing details.
# © 2026 DigitsCode (Digital Integrated Transformation Solutions)
# Developer: DigitsCode <info@digitscode.com>
# Website: https://www.digitscode.com
{
    'name': 'Digits ZATCA | Tax Total (Fix Issue)',
    'summary': 'Temporary fix for ZATCA warning BR-KSA-EN16931-09 until Odoo core restores the second TaxTotal node.',
    'description': """
Digits ZATCA | Tax Total (Fix Issue)
====================================

Temporary workaround — uninstall this module once Odoo 18 core
restores the second document-level TaxTotal on SAR invoices.

Fixes the recurring ZATCA warning on Saudi sales invoices:

    Invoice was Accepted by ZATCA (with Warnings)
    [202] BR-KSA-EN16931-09
    Only one tax total (BG-22) without tax subtotals (BG-23) must be
    provided when tax currency code is provided.

Screenshot of the warning (from Odoo chatter after a successful send):

    static/description/screenshot_zatca_warning.png

Cause
-----
Odoo 18 always sends TaxCurrencyCode (company currency, usually SAR).
ZATCA then requires TWO document-level cac:TaxTotal nodes:

1. Tax total WITH TaxSubtotal  (VAT breakdown in the invoice currency)
2. Tax total WITHOUT TaxSubtotal (BT-111, VAT amount in the tax/accounting currency)

A core 18.0 change dropped node (2) when the invoice currency equals the
company currency (SAR). The invoice is still accepted, but every SAR
invoice gets this warning.

What this module does
---------------------
Overrides account.edi.xml.ubl_21.zatca to restore node (2) for SAR invoices.
Foreign-currency invoices already have that node in standard Odoo; it is
not duplicated.

Safe for multi-company (uses the invoice company currency, not env.company),
multi-currency, and Arabic/English UI (no extra user-facing strings).

Already-sent invoices stay accepted; only new XML submissions are fixed.

Developed by Digital Integrated Transformation Solutions (DigitsCode).
    """,
    'author': 'Digital Integrated Transformation Solutions (DigitsCode)',
    'maintainer': 'Digital Integrated Transformation Solutions (DigitsCode)',
    'website': 'https://www.digitscode.com',
    'email': 'info@digitscode.com',
    'company': 'Digital Integrated Transformation Solutions (DigitsCode)',
    'category': 'Accounting/Localizations',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'depends': [
        'l10n_sa_edi',
    ],
    'data': [],
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/screenshot_zatca_warning.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
