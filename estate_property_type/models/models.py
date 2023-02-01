# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PropertyType(models.Model):
    _name = 'estate_property_type.estate_property_type'
    name = fields.Char(required=True)


