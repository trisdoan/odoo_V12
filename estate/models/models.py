# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,
                                    default=lambda self: (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d'))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,
                                 copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(string='State',
                             selection=[('new', 'New'), ('offer received', 'Offer Received'),
                                        ('offer accepted', 'Offer Accepted'),
                                        ('sold', 'Sold'),
                                        ('canceled', 'Canceled')],
                             default='New')
    # relational field
    property_type_id = fields.Many2one("estate_property_type.estate_property_type",
                                       string="Property Type")
    buyer = fields.Many2one("res.partner",
                            string="Buyer",
                            copy=False,
                            )
    seller = fields.Many2one("res.users",
                             string="Seller",
                             default=lambda self: self.env.user,
                             )
    tag_ids = fields.Many2many("estate.estate_property_tag", string="Tag")
    offer_ids = fields.One2many("estate.estate_property_offer", "property_id", string="Offer")


class EstatePropertyTag(models.Model):
    _name = "estate.estate_property_tag"
    name = fields.Char(required=True)


class EstatePropertyOffer(models.Model):
    _name = "estate.estate_property_offer"
    price = fields.Float()
    status = fields.Selection(string='Status',
                              selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
                              copy=False)
    partner_id = fields.Many2one("res.partner",
                                 required=True,
                                 )
    property_id = fields.Many2one("estate.property",
                                  required=True,
                                  )
