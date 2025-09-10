from odoo import models,fields, api
from odoo.tools import date_utils
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default = lambda self: date_utils.add(fields.Date.today(),months = 3))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection = [('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')])

    active = fields.Boolean(default = True)
    state = fields.Selection(required = True, copy = False, default = 'new', selection = [('new','New'),('offer received','Offer Received'), ('offer accepted','Offer Accepted'), ('sold','Sold'), ('cancelled','Cancelled')])

    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)

    property_type = fields.Many2one('estate.property.type', string='Property Type')
    property_tags = fields.Many2many('estate.property.tag', string='Property Tag')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer", string = "Best Offer")

    _sql_constraints = [
        ('check_expected_price','CHECK (expected_price > 0)','the expected price must be positive'),
        ('check_selling_price','CHECK (selling_price >= 0)', 'the selling price must be positive'),     
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.garden_area or 0) + (record.living_area or 0)
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.onchange('garden_area','garden_orientation')
    def _onchange_garden(self):
        if self.garden :
            self.garden_area = 10
            self.garden_orientation = 'north'
        else : 
            self.garden_area = 0
            self.garden_orientation = None

    def cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("You cannot cancel a sold property.")
            record.state = 'cancelled'

    def sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A cancelled property cannot be set as sold.")
            record.state = 'sold'

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero (record.selling_price,precision_digits=2):
                continue
            if float_compare(record.selling_price,0.9*record.expected_price, precision_digits=2) < 0:
                raise ValidationError("The selling offer cannot be lower than 90% of the expected price")
            
    can_cancel = fields.Boolean(compute='_compute_button_visibility')
    can_mark_sold = fields.Boolean(compute='_compute_button_visibility')

    @api.depends('state')
    def _compute_button_visibility(self):
        for rec in self:
            rec.can_cancel = rec.state not in ('cancelled', 'sold')
            rec.can_mark_sold = rec.state not in ('cancelled', 'sold')

    cannot_add = fields.Boolean(compute='_compute_cannot_add')
    @api.depends('state')
    def _compute_cannot_add(self):
        for offer in self:
            offer.cannot_add = offer.state in ['offer accepted', 'sold', 'cancelled']

    has_offer_received = fields.Boolean(compute='_compute_has_offer_received', store=True)
    has_offer_accepted = fields.Boolean(compute='_compute_has_offer_accepted')

    @api.depends('offer_ids')
    def _compute_has_offer_received(self):
        for record in self:
            record.has_offer_received = bool(record.offer_ids)

    @api.depends('offer_ids.status')
    def _compute_has_offer_accepted(self):
        for record in self:
            record.has_offer_accepted = any(offer.status == 'accepted' for offer in record.offer_ids)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_property(self):
        for record in self:
            if (record.state not in ['new', 'cancelled']):
                raise UserError("Vous ne pouvez pas supprimer une propriété que si elle est 'New' ou 'cancelled'.")
        
        