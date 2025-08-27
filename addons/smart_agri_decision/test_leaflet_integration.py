#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de l'intégration Leaflet pour la cartographie
Ce fichier teste la fonctionnalité de cartographie interactive
"""

import logging

_logger = logging.getLogger(__name__)

def test_leaflet_assets_loading(env):
    """Test que les assets Leaflet se chargent correctement"""
    try:
        # Vérifier que les assets Leaflet sont disponibles
        assets = env['ir.asset'].search([
            ('name', 'ilike', 'leaflet'),
            ('bundle', '=', 'web.assets_backend')
        ])
        
        if assets:
            _logger.info(f"✅ Assets Leaflet trouvés: {len(assets)}")
            return True
        else:
            _logger.warning("⚠️ Aucun asset Leaflet trouvé - vérifiez l'intégration")
            return False
            
    except Exception as e:
        _logger.error(f"❌ Erreur lors de la vérification des assets Leaflet: {e}")
        return False

def test_parcelle_geolocation(env):
    """Test la géolocalisation des parcelles"""
    try:
        # Créer une parcelle de test avec géolocalisation
        parcelle_data = {
            'name': 'Test Parcelle Géolocalisée',
            'surface': 10.5,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'notes': 'Parcelle de test pour validation géolocalisation'
        }
        
        parcelle = env['smart_agri_parcelle'].create(parcelle_data)
        
        if parcelle and parcelle.latitude and parcelle.longitude:
            _logger.info("✅ Parcelle avec géolocalisation créée avec succès")
            # Nettoyer le test
            parcelle.unlink()
            return True
        else:
            _logger.error("❌ Échec de la création de la parcelle géolocalisée")
            return False
            
    except Exception as e:
        _logger.error(f"❌ Erreur lors de la création de la parcelle géolocalisée: {e}")
        return False

def test_exploitation_geolocation(env):
    """Test la géolocalisation des exploitations"""
    try:
        # Créer une exploitation de test avec géolocalisation
        exploitation_data = {
            'name': 'Test Exploitation Géolocalisée',
            'adresse': '123 Rue de Test, 75001 Paris',
            'latitude': 48.8566,
            'longitude': 2.3522,
            'notes': 'Exploitation de test pour validation géolocalisation'
        }
        
        exploitation = env['smart_agri_exploitation'].create(exploitation_data)
        
        if exploitation and exploitation.latitude and exploitation.longitude:
            _logger.info("✅ Exploitation avec géolocalisation créée avec succès")
            # Nettoyer le test
            exploitation.unlink()
            return True
        else:
            _logger.error("❌ Échec de la création de l'exploitation géolocalisée")
            return False
            
    except Exception as e:
        _logger.error(f"❌ Erreur lors de la création de l'exploitation géolocalisée: {e}")
        return False

def run_leaflet_tests(env):
    """Exécute tous les tests Leaflet"""
    _logger.info("🧪 Démarrage des tests d'intégration Leaflet...")
    
    tests_passed = 0
    total_tests = 3
    
    if test_leaflet_assets_loading(env):
        tests_passed += 1
        
    if test_parcelle_geolocation(env):
        tests_passed += 1
        
    if test_exploitation_geolocation(env):
        tests_passed += 1
    
    _logger.info(f"📊 Résultats des tests Leaflet: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        _logger.info("🎉 Tous les tests Leaflet sont passés avec succès !")
        return True
    else:
        _logger.error("💥 Certains tests Leaflet ont échoué")
        return False
