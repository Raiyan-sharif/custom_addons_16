
{
    'name': 'Assignment',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 20,
    'summary': 'Oder Management',
    'description': """
         Assignment of OBS Solution
         """,
    'author': 'Raiyan Sharif',
    'website': 'https://github.com/Raiyan-sharif',
    'depends': ['base', 'hr', 'stock'],
    'images': ['static/description/icon.png'],
    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        # 'views/admin_support_view.xml',
        # 'wizard/admin_support_summary_report_view.xml',
        # 'views/admin_support_tag_view.xml',
        # 'views/admin_support_type_view.xml',
        # 'views/admin_support_seq.xml',
        # 'views/menu_items.xml',
    ],
    "installable": True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
