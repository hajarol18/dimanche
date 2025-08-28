# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json

class SmartAgriParcelleMap(models.Model):
    _inherit = 'smart_agri_parcelle'
    
    @api.model
    def get_map_data(self):
        """
        Récupère les données des parcelles pour l'affichage sur la carte Leaflet
        """
        parcelles = self.search([])
        result = []
        
        for parcelle in parcelles:
            # Préparation des données pour la carte
            parcelle_data = {
                'id': parcelle.id,
                'name': parcelle.name,
                'code': parcelle.code,
                'surface': parcelle.surface,
                'geo_area': parcelle.geo_area,
                'latitude': parcelle.latitude,
                'longitude': parcelle.longitude,
                'exploitation_name': parcelle.exploitation_id.name if parcelle.exploitation_id else False,
                'type_sol_name': parcelle.type_sol_id.name if parcelle.type_sol_id else False,
            }
            
            # Ajout des données géospatiales si disponibles
            if parcelle.geo_polygon:
                try:
                    # Conversion du WKT en GeoJSON si nécessaire
                    if parcelle.geo_polygon.startswith('POLYGON') or parcelle.geo_polygon.startswith('MULTIPOLYGON'):
                        # Utilisation de la bibliothèque shapely pour convertir WKT en GeoJSON
                        from shapely import wkt
                        from shapely.geometry import mapping
                        
                        geom = wkt.loads(parcelle.geo_polygon)
                        geojson = mapping(geom)
                        parcelle_data['geo_polygon'] = json.dumps(geojson)
                    else:
                        # Si c'est déjà du GeoJSON, on le passe tel quel
                        parcelle_data['geo_polygon'] = parcelle.geo_polygon
                except Exception as e:
                    parcelle_data['geo_polygon'] = False
                    parcelle_data['geo_error'] = str(e)
            
            result.append(parcelle_data)
        
        return result