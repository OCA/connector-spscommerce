# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'EDI Integration with SPS Commerce',
    'summary': 'Integrate with retail stores using SPS Commerce',
    'version': '9.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'depends': [
        'procurement',
        'account',
        'delivery',
        'sale_stock',
        'sale_automatic_workflow',
    ],
    'data':[
        'views/sale_view.xml',
        'views/stock_view.xml',
        'views/company_config_settings_view.xml',
        'views/account_invoice_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'development_status': 'beta',
    'maintainers': ['smangukiya'],
}
