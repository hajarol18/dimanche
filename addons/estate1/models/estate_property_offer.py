from odoo import models,fields, api
from datetime import timedelta, date
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection = [('accepted','Accepted'),('refused','Refused')], copy = False)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute="_compute_date_deadline", string = "Deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ('check_price','CHECK (price > 0)','the offer price must be positive'),
    ]
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()  
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - create_date.date()).days if record.date_deadline else 0

    partner_id = fields.Many2one ("res.partner", string = 'Partner', required = True )
    property_id = fields.Many2one ("estate.property", required = True )

    def action_accept(self):
        for offer in self:
            accepted_offers = self.search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted'),
                ('id', '!=', offer.id)
            ])
            if accepted_offers:
                raise UserError("Une autre offre a déjà été acceptée pour cette propriété.")

            offer.status = 'accepted'

            offer.property_id.selling_price = offer.price
            offer.property_id.buyer = offer.partner_id
            offer.property_id.state = 'offer accepted'

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'

    can_accept = fields.Boolean(compute='_compute_can_accept_refuse')
    can_refuse = fields.Boolean(compute='_compute_can_accept_refuse')

    @api.depends('status')
    def _compute_can_accept_refuse(self):
        for offer in self:
            offer.can_accept = offer.status in (False, None)
            offer.can_refuse = offer.status in (False, None)

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        new_price = vals.get('price')
        property_obj = self.env['estate.property'].browse(property_id)
        max_offer = max(property_obj.offer_ids.mapped('price') or [0])
        if new_price < max_offer:
            raise UserError("Vous ne pouvez pas placer une offre inférieure à celle déjà existante.")
        offer = super().create(vals)
        if property_obj.state == 'new':
            property_obj.state = 'offer received'
        return offer
    
    property_type_id = fields.Many2one(related="property_id.property_type")