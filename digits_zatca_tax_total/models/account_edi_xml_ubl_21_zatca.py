# -*- coding: utf-8 -*-
# Part of DigitsCode. See LICENSE file for full copyright and licensing details.
# © 2026 DigitsCode (Digital Integrated Transformation Solutions)
# Developer: DigitsCode <info@digitscode.com>
# Website: https://www.digitscode.com
from odoo import models


class AccountEdiXmlUBL21Zatca(models.AbstractModel):
    """Restore the document-level TaxTotal required by BR-KSA-EN16931-09."""

    _inherit = 'account.edi.xml.ubl_21.zatca'

    def _l10n_sa_get_additional_tax_total_vals(self, invoice, vals):
        """Keep one TaxTotal without subtotals whenever TaxCurrencyCode is sent.

        Odoo 18 always sets ``tax_currency_code`` to the company currency (SAR).
        ZATCA rule BR-KSA-EN16931-09 then requires exactly one document-level
        ``cac:TaxTotal`` without ``cac:TaxSubtotal`` (BT-111).

        A core 18.0 change skipped that second node for SAR invoices, which
        produces a recurring ZATCA warning on every SAR invoice. Odoo 19 still
        emits the second node; this override restores the same structure on 18.0
        without duplicating it on foreign-currency invoices.
        """
        tax_total_vals = super()._l10n_sa_get_additional_tax_total_vals(invoice, vals)
        if any('tax_subtotal_vals' not in tax_total for tax_total in tax_total_vals):
            return tax_total_vals

        if invoice.currency_id != invoice.company_currency_id:
            tax_amount = abs(vals['taxes_vals']['tax_amount'])
        else:
            tax_amount = abs(vals['taxes_vals']['tax_amount_currency'])

        return tax_total_vals + [{
            'currency': invoice.company_currency_id,
            'currency_dp': invoice.company_currency_id.decimal_places,
            'tax_amount': tax_amount,
        }]
