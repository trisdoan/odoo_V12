# -*- coding: utf-8 -*-
from odoo import http

# class EstatePropertyType(http.Controller):
#     @http.route('/estate_property_type/estate_property_type/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estate_property_type/estate_property_type/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('estate_property_type.listing', {
#             'root': '/estate_property_type/estate_property_type',
#             'objects': http.request.env['estate_property_type.estate_property_type'].search([]),
#         })

#     @http.route('/estate_property_type/estate_property_type/objects/<model("estate_property_type.estate_property_type"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estate_property_type.object', {
#             'object': obj
#         })