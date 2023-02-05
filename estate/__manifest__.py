# -*- coding: utf-8 -*-
{
    'name': "Estate Property",
    'description': """
        learn from odoo.com
    """,

    'author': "Tris",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "views/estate_menus.xml",
        "views/estate_property_views.xml",
        "views/res_users_form.xml",

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
