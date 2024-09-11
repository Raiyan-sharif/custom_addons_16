
{
    'name': 'Assignment',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'sequence': 20,
    'summary': 'Oder Management',
    'description': """
         Assignment of OBS Solution
         """,
    'author': 'Raiyan Sharif',
    'website': 'https://github.com/Raiyan-sharif',
    'depends': ['web','base', 'sale', 'account'],
    'images': ['static/description/icon.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_assets.xml',
        'views/dashboard_view.xml',
        'views/order_view.xml',
        'views/portal_view.xml',
        'reports/profit_report.xml',
        'i18n/en.po',
    ],
    'qweb': [
        'static/src/js/dashboard.js',
        'static/src/css/dashboard.css',
    ],
    "installable": True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
