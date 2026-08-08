{
    "name": "Print Preview All Reports",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "summary": "Preview PDF reports before printing",
    "depends": ["web"],
    "assets": {
        "web.assets_backend": [
            "print_preview_all_disabled/static/src/js/print_preview.js",
            "print_preview_all_disabled/static/src/xml/print_preview.xml",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}