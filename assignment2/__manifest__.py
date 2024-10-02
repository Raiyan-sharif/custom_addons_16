{
    'name': 'Assignment 2',
    'version': '16.0.1.0.0',
    'category': 'Report',
    'sequence': 20,
    'summary': 'Report',
    'description': """
         Assignment 2 of OBS Solution
         """,
    'author': 'Raiyan Sharif',
    'website': 'https://github.com/Raiyan-sharif',
    'depends': ['base', 'account', 'web','hr'],
    'images': ['static/description/icon.png'],
    'data': [
        'views/assignment2_invoice_views.xml',
        'views/assignment2_invoice_menu.xml',
        'security/ir.model.access.csv',
        'report/assignment2_invoice_report_template.xml',
        'report/assignment2_invoice_report_action.xml',
    ],
    'qweb': [
    ],
    "installable": True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
