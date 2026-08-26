{
    "name": "User Delete Control",
    "version": "18.0.1.0.0",
    "category": "Administration",
    "summary": "Control delete permissions per user and record type",
    "description": """
        Allows administrators to control delete permissions per user.

        Features:
        - Hide delete option globally
        - Hide delete option for specific record types
        - Backend protection against unlink()
        - UI protection for list and form views
    """,
    "author": "Advanced Event Solution",
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