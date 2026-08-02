{
    "name": "Product Category Sequence",
    "version": "18.0.1.0.0",
    "license": "LGPL-3",
    "author": "Advanced Event Solution / Bushra Alamarnah",
    "summary": """
        Generate automatic product internal reference
        based on the selected product category sequence.
    """,

    "description": """
        This module allows users to define product reference
        sequences on the last level of product categories.

        Features:
        - Enable sequence generation per product category.
        - Define prefix, padding, step and next number.
        - Automatically generate product internal reference.
        - Restrict product categories to sequence-enabled categories.
    """,
    "depends": [
        "product",
    ],
    "data": [
        "views/product_category_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "application": False,
}