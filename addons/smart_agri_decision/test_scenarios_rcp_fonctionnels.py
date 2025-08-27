#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests fonctionnels complets pour SmartAgriDecision
Ce fichier exécute tous les tests pour valider le module
"""

import logging
from . import test_module_functionality
from . import test_rcp_scenarios
from . import test_leaflet_integration

_logger = logging.getLogger(__name__)

def run_all_tests(env):
    """Exécute tous les tests du module"""
    _logger.info("🚀 Démarrage des tests complets SmartAgriDecision...")
    
    total_tests = 0
    passed_tests = 0
    
    # Test 1: Fonctionnalité de base du module
    _logger.info("=" * 50)
    _logger.info("🧪 TEST 1: Fonctionnalité de base du module")
    _logger.info("=" * 50)
    
    if test_module_functionality.run_tests(env):
        passed_tests += 1
    total_tests += 1
    
    # Test 2: Scénarios RCP et rotations culturelles
    _logger.info("=" * 50)
    _logger.info("🧪 TEST 2: Scénarios RCP et rotations culturelles")
    _logger.info("=" * 50)
    
    if test_rcp_scenarios.run_rcp_tests(env):
        passed_tests += 1
    total_tests += 1
    
    # Test 3: Intégration Leaflet
    _logger.info("=" * 50)
    _logger.info("🧪 TEST 3: Intégration Leaflet et cartographie")
    _logger.info("=" * 50)
    
    if test_leaflet_integration.run_leaflet_tests(env):
        passed_tests += 1
    total_tests += 1
    
    # Résultats finaux
    _logger.info("=" * 50)
    _logger.info("📊 RÉSULTATS FINAUX DES TESTS")
    _logger.info("=" * 50)
    _logger.info(f"Tests réussis: {passed_tests}/{total_tests}")
    _logger.info(f"Taux de réussite: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        _logger.info("🎉 FÉLICITATIONS ! Tous les tests sont passés avec succès !")
        _logger.info("✅ Votre module SmartAgriDecision est prêt pour la soutenance !")
        return True
    else:
        _logger.error("💥 ATTENTION ! Certains tests ont échoué.")
        _logger.error("🔧 Veuillez corriger les problèmes avant la soutenance.")
        return False

def test_soutenance_scenarios(env):
    """Tests spécifiques pour la soutenance"""
    _logger.info("🎓 TESTS SPÉCIAUX POUR LA SOUTENANCE")
    _logger.info("=" * 50)
    
    try:
        # Test de création d'une exploitation complète
        exploitation_data = {
            'name': 'Ferme de Démonstration',
            'adresse': '123 Route des Champs, 75000 Paris',
            'latitude': 48.8566,
            'longitude': 2.3522,
            'notes': 'Exploitation de démonstration pour la soutenance'
        }
        
        exploitation = env['smart_agri_exploitation'].create(exploitation_data)
        _logger.info("✅ Exploitation de démonstration créée")
        
        # Test de création d'une parcelle
        parcelle_data = {
            'name': 'Champ Principal',
            'exploitation_id': exploitation.id,
            'surface': 25.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'notes': 'Parcelle principale de démonstration'
        }
        
        parcelle = env['smart_agri_parcelle'].create(parcelle_data)
        _logger.info("✅ Parcelle de démonstration créée")
        
        # Test de création d'un scénario RCP
        rcp_data = {
            'name': 'Scénario Soutenance RCP 8.5',
            'description': 'Scénario pessimiste pour la démonstration',
            'rcp_type': 'rcp_8_5',
            'annee_debut': 2025,
            'annee_fin': 2100,
            'temperature_rise': 4.5,
            'co2_concentration': 1200,
            'notes': 'Scénario de démonstration pour la soutenance'
        }
        
        rcp = env['smart_agri_rcp_scenario'].create(rcp_data)
        _logger.info("✅ Scénario RCP de démonstration créé")
        
        # Nettoyer les données de test
        parcelle.unlink()
        rcp.unlink()
        exploitation.unlink()
        
        _logger.info("🎯 Tous les scénarios de soutenance sont fonctionnels !")
        return True
        
    except Exception as e:
        _logger.error(f"❌ Erreur lors des tests de soutenance: {e}")
        return False

def main():
    """Fonction principale pour exécuter les tests"""
    _logger.info("🚀 SmartAgriDecision - Tests de Validation")
    _logger.info("=" * 50)
    _logger.info("Ce module teste toutes les fonctionnalités de SmartAgriDecision")
    _logger.info("Préparez-vous pour votre soutenance ! 🎓")
    
    # Note: Cette fonction sera appelée depuis Odoo
    pass
