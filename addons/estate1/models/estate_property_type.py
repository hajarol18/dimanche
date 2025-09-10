from odoo import models,fields, api

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = 'sequence,name'

    name = fields.Char(required = True)
    sequence = fields.Integer('Sequence', default=1)

    _sql_constraints = [
        ('check_type_name','unique(name)','the type name must be unique'),
    ]

    property_ids = fields.One2many('estate.property','property_type',string = "Properties")

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string='Offers'
    )

    offer_count = fields.Integer(
        string='Number of Offers',
        compute='_compute_offer_count',
        store=True
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)