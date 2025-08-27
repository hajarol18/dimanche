#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de fonctionnalité du module SmartAgriDecision
Ce fichier permet de tester que le module se charge correctement
"""

import logging

_logger = logging.getLogger(__name__)

def test_module_loading(env):
    """Test que le module se charge correctement"""
    try:
        # Test de chargement des modèles
        soil_type = env['smart_agri_soil_type']
        exploitation = env['smart_agri_exploitation']
        parcelle = env['smart_agri_parcelle']
        culture = env['smart_agri_culture']
        rotation = env['smart_agri_rotation_culturelle']
        objectif = env['smart_agri_objectif_rotation']
        
        _logger.info("✅ Tous les modèles se chargent correctement")
        return True
        
    except Exception as e:
        _logger.error(f"❌ Erreur lors du chargement des modèles: {e}")
        return False

def test_menu_creation(env):
    """Test que les menus sont créés correctement"""
    try:
        # Vérifier que le menu principal existe
        menu_root = env.ref('smart_agri_decision.menu_smart_agri_root')
        menu_analyse = env.ref('smart_agri_decision.menu_analyse')
        menu_rotation = env.ref('smart_agri_decision.menu_smart_agri_rotation_culturelle')
        
        _logger.info("✅ Tous les menus sont créés correctement")
        return True
        
    except Exception as e:
        _logger.error(f"❌ Erreur lors de la vérification des menus: {e}")
        return False

def run_tests(env):
    """Exécute tous les tests"""
    _logger.info("🧪 Démarrage des tests du module SmartAgriDecision...")
    
    tests_passed = 0
    total_tests = 2
    
    if test_module_loading(env):
        tests_passed += 1
        
    if test_menu_creation(env):
        tests_passed += 1
    
    _logger.info(f"📊 Résultats des tests: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        _logger.info("🎉 Tous les tests sont passés avec succès !")
        return True
    else:
        _logger.error("💥 Certains tests ont échoué")
        return False
