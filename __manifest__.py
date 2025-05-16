# -*- encoding: utf-8 -*-
{
    'name': 'Perroinversiones',
    'version': '1.0',
    'category': 'Custom',
    'description': """ Perroinversiones """,
    'author': 'aquíH',
    'website': 'http://aquih.com/',
    'depends': ['sale_renting'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'wizard/replica_wizard_view.xml',
    ],
}