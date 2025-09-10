from odoo import models,fields

class PropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = 'name'

    name = fields.Char(required = True)
    color = fields.Integer(string = "Color")

    _sql_constraints = [
        ('check_tag_name','unique(name)','the tag name must be unique'),
    ]