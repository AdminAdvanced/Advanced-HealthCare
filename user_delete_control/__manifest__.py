{
    "name": "User Delete Control",
    "version": "18.0.1.0.0",
    "category": "Administration",
    "summary": "Control delete permissions per user and record type",
    "description": """
        User Delete Control
        ===================
        
        Allows administrators to control delete permissions for individual users
        and specific record types.
        
        Features
        --------
        * Globally restrict delete permissions for selected users.
        * Restrict deletion for specific record types.
        * Backend protection against unauthorized unlink() operations.
        * UI protection for list and form views.
        * Easy configuration from the user form.
        
        This module helps administrators prevent accidental or unauthorized
        record deletion while keeping normal Odoo workflows unchanged.
        """,
    "author": "Bushra AlAmarnah",
    "website": "https://github.com/bushraamarnah/odoo-delete-permissions-control",
    "license": "LGPL-3",
    "depends": [
        "base",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "user_delete_control/static/src/js/delete_control.js",
        ],
    },
    "installable": True,
    "application": False,
}