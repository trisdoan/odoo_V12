# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


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
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    living_area = fields.Integer()
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
                             default='new')
    # relational field
    property_type_id = fields.Many2one("estate.estate_property_type",
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

    # computed field
    total_area = fields.Float(compute="_compute_total")

    best_price = fields.Float(compute="_compute_best_price", default=0)

    # onchange field
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if not record.offer_ids.mapped("price"):
                record.best_price = 0
            else:
                record.best_price = max(record.offer_ids.mapped("price"))

    # business logic: set status
    def set_cancel(self):
        self.ensure_one()
        if not self.state == 'sold':
            self.state = 'canceled'
        else:
            raise UserError("Sold property cannot be canceled")
        return True

    def set_sold(self):
        self.ensure_one()
        if not self.state == 'canceled':
            self.state = 'sold'
        else:
            raise UserError("Cancel property cannot be sold")
        return True

    # SQL constraints
    _sql_constraints = [
        ('check_expected_price', 'check(expected_price > 0)', 'The expected price must be strictly positive'),
        ('check_selling_price', 'check(selling_price > 0)', 'The selling price must be strictly positive')
    ]

    # Python constraints
    @api.constrains("selling_price")
    def check_selling_price(self):
        for price in self:
            if float_compare(self.selling_price, self.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError("Selling price must bigger")


class PropertyType(models.Model):
    _name = 'estate.estate_property_type'
    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_type_name', 'unique(name)', 'The type name must be unique')
    ]


class EstatePropertyTag(models.Model):
    _name = "estate.estate_property_tag"
    name = fields.Char(required=True)
    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'The tag name must be unique')
    ]


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
                                  # required=True,
                                  )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline",
                                inverse="_inverse_date_deadline"
                                )
    _sql_constraints = [
        ('check_offer_price', 'check(price > 0)', 'The offer price must be positive')
    ]

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (record.create_date + timedelta(days=record.validity)).strftime('%Y-%m-%d')
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    @api.depends("create_date", "date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (fields.Datetime.to_datetime(record.date_deadline) - record.create_date).days

    @api.depends("property_id.buyer", "property_id.selling_price")
    def set_accept(self):
        self.ensure_one()
        for record in self:
            record.status = "accepted"
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price

    def set_refuse(self):
        self.ensure_one()
        for record in self:
            record.status = "refused"
