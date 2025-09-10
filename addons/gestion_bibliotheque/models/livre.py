from odoo import models, fields

class Livre(models.Model):
    _name = 'gestion.bibliotheque.livre'
    _description = 'Livre'

    name = fields.Char(string='Titre', required=True)
    auteur = fields.Char(string='Auteur')
    date_publication = fields.Date(string='Date de publication')
    genre = fields.Selection([
        ('roman', 'Roman'),
        ('science', 'Science'),
        ('histoire', 'Histoire'),
        ('autre', 'Autre')
    ], string='Genre', default='roman')
    disponible = fields.Boolean(string='Disponible', default=True)
