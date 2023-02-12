# -*- coding: utf-8 -*-
{
    'name': "Fleet Repair Management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Hendra Himawan",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Fleet Repair',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet', 'stock', 'account', 'purchase', 'sale_management'],

    # always loaded
    'data': [
        'data/ir_sequence_data.xml',
        'security/fleet_repair.xml',
        'security/ir.model.access.csv',
        'views/fleet_repair_views.xml',
        'views/fleet_diagnosis_views.xml',
        'views/fleet_work_order_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'report/ir_actions_report.xml',
        'report/ir_actions_report_templates.xml',
        'wizards/diagnosis_assign_technician_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
