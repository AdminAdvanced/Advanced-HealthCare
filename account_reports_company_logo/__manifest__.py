# -*- coding: utf-8 -*-
{
    "name": "Accounting Reports Company Logo",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "summary": "Adds company logo to Accounting PDF reports",
    "author": "Your Company",
    "license": "LGPL-3",

    "depends": [
        "account_reports",
        "account",
    ],

    "data": [
        "views/account_reports_company_information.xml",
        "views/invoice_report.xml",
    ],

    "installable": True,
    "application": False,
}