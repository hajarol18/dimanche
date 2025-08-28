# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import json
import logging

_logger = logging.getLogger(__name__)

class SmartAgriGeojsonWizard(models.TransientModel):
    """Assistant pour importer des données GeoJSON"""
    
    _name = 'smart_agri_geojson_wizard'
    _description = 'Assistant Import GeoJSON'
    _rec_name = 'parcelle_id'
    
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle', required=True)
    geojson_file = fields.Binary('Fichier GeoJSON', required=True)
    file_name = fields.Char('Nom du fichier')
    overwrite_existing = fields.Boolean('Écraser géométrie existante', default=True)
    
    def action_import(self):
        """Importe les données GeoJSON dans la parcelle"""
        self.ensure_one()
        
        if not self.geojson_file:
            raise ValidationError("Veuillez sélectionner un fichier GeoJSON à importer.")
            
        try:
            # Décodage du fichier binaire
            geojson_str = self.geojson_file.decode('utf-8')
            geojson_data = json.loads(geojson_str)
            
            # Validation du format GeoJSON
            if 'type' not in geojson_data:
                raise ValidationError("Format GeoJSON invalide: 'type' manquant.")
                
            # Traitement selon le type de GeoJSON
            if geojson_data['type'] == 'FeatureCollection':
                if 'features' not in geojson_data or not geojson_data['features']:
                    raise ValidationError("FeatureCollection sans features.")
                # Utiliser la première feature
                feature = geojson_data['features'][0]
                self._process_feature(feature)
            elif geojson_data['type'] == 'Feature':
                self._process_feature(geojson_data)
            else:
                # Géométrie directe
                self._process_geometry(geojson_data)
                
            return {'type': 'ir.actions.act_window_close'}
            
        except Exception as e:
            _logger.error("Erreur lors de l'import GeoJSON: %s", str(e))
            raise ValidationError(f"Erreur lors de l'import GeoJSON: {str(e)}")
    
    def _process_feature(self, feature):
        """Traite une feature GeoJSON"""
        if 'geometry' not in feature:
            raise ValidationError("Feature sans géométrie.")
            
        geometry = feature['geometry']
        self._process_geometry(geometry)
        
        # Traitement des propriétés si présentes
        if 'properties' in feature and feature['properties']:
            props = feature['properties']
            # Mise à jour des propriétés de la parcelle si elles existent dans les propriétés GeoJSON
            update_vals = {}
            for field in ['name', 'code', 'surface']:
                if field in props and props[field]:
                    update_vals[field] = props[field]
            
            if update_vals:
                self.parcelle_id.write(update_vals)
    
    def _process_geometry(self, geometry):
        """Traite une géométrie GeoJSON"""
        if 'type' not in geometry:
            raise ValidationError("Géométrie sans type.")
            
        geo_type = geometry['type']
        
        # Mise à jour de la géométrie selon son type
        if geo_type == 'Point':
            # Point: mise à jour du geo_point
            if self.overwrite_existing or not self.parcelle_id.geo_point:
                coords = geometry['coordinates']
                self.parcelle_id.write({
                    'geo_point': f'POINT({coords[0]} {coords[1]})',
                    'longitude': coords[0],
                    'latitude': coords[1]
                })
        elif geo_type in ['Polygon', 'MultiPolygon']:
            # Polygon ou MultiPolygon: mise à jour du geo_polygon
            if self.overwrite_existing or not self.parcelle_id.geo_polygon:
                # Conversion du GeoJSON en WKT
                wkt = self._geojson_to_wkt(geometry)
                self.parcelle_id.write({'geo_polygon': wkt})
        else:
            raise ValidationError(f"Type de géométrie non supporté: {geo_type}")
    
    def _geojson_to_wkt(self, geometry):
        """Convertit une géométrie GeoJSON en format WKT"""
        geo_type = geometry['type']
        coords = geometry['coordinates']
        
        if geo_type == 'Point':
            return f"POINT({coords[0]} {coords[1]})"
        elif geo_type == 'Polygon':
            # Format: POLYGON((x1 y1, x2 y2, ...))
            rings = []
            for ring in coords:
                points = [f"{p[0]} {p[1]}" for p in ring]
                rings.append(f"({', '.join(points)})")
            return f"POLYGON({', '.join(rings)})"
        elif geo_type == 'MultiPolygon':
            # Format: MULTIPOLYGON(((x1 y1, x2 y2, ...)), ((...)))
            polygons = []
            for poly in coords:
                rings = []
                for ring in poly:
                    points = [f"{p[0]} {p[1]}" for p in ring]
                    rings.append(f"({', '.join(points)})")
                polygons.append(f"({', '.join(rings)})")
            return f"MULTIPOLYGON({', '.join(polygons)})"
        else:
            raise ValidationError(f"Conversion en WKT non supportée pour le type: {geo_type}")