#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test des scénarios RCP (Representative Concentration Pathways)
Ce fichier teste la fonctionnalité des scénarios climatiques
"""

import logging

_logger = logging.getLogger(__name__)

def test_rcp_scenario_creation(env):
    """Test la création d'un scénario RCP"""
    try:
        # Créer un scénario RCP de test
        rcp_data = {
            'name': 'Test RCP 4.5',
            'description': 'Scénario de test RCP 4.5',
            'rcp_type': 'rcp_4_5',
            'annee_debut': 2025,
            'annee_fin': 2100,
            'temperature_rise': 1.8,
            'co2_concentration': 650,
            'notes': 'Scénario de test pour validation'
        }
        
        rcp_scenario = env['smart_agri_rcp_scenario'].create(rcp_data)
        
        if rcp_scenario:
            _logger.info("✅ Scénario RCP créé avec succès")
            # Nettoyer le test
            rcp_scenario.unlink()
            return True
        else:
            _logger.error("❌ Échec de la création du scénario RCP")
            return False
            
    except Exception as e:
        _logger.error(f"❌ Erreur lors de la création du scénario RCP: {e}")
        return False

def test_rotation_culturelle_creation(env):
    """Test la création d'une rotation culturelle"""
    try:
        # Créer une rotation culturelle de test
        rotation_data = {
            'name': 'Test Rotation Blé-Maïs',
            'description': 'Rotation de test blé-maïs',
            'objectif_principal': 'test',
            'notes': 'Rotation de test pour validation'
        }
        
        rotation = env['smart_agri_rotation_culturelle'].create(rotation_data)
        
        if rotation:
            _logger.info("✅ Rotation culturelle créée avec succès")
            # Nettoyer le test
            rotation.unlink()
            return True
        else:
            _logger.error("❌ Échec de la création de la rotation culturelle")
            return False
            
    except Exception as e:
        _logger.error(f"❌ Erreur lors de la création de la rotation culturelle: {e}")
        return False

def test_objectif_rotation_creation(env):
    """Test la création d'un objectif de rotation"""
    try:
        # Créer un objectif de rotation de test
        objectif_data = {
            'name': 'Test Objectif Rotation',
            'description': 'Objectif de test pour rotation',
            'notes': 'Objectif de test pour validation'
        }
        
        objectif = env['smart_agri_objectif_rotation'].create(objectif_data)
        
        if objectif:
            _logger.info("✅ Objectif de rotation créé avec succès")
            # Nettoyer le test
            objectif.unlink()
            return True
        else:
            _logger.error("❌ Échec de la création de l'objectif de rotation")
            return False
            
    except Exception as e:
        _logger.error(f"❌ Erreur lors de la création de l'objectif de rotation: {e}")
        return False

def run_rcp_tests(env):
    """Exécute tous les tests RCP"""
    _logger.info("🧪 Démarrage des tests RCP et rotations culturelles...")
    
    tests_passed = 0
    total_tests = 3
    
    if test_rcp_scenario_creation(env):
        tests_passed += 1
        
    if test_rotation_culturelle_creation(env):
        tests_passed += 1
        
    if test_objectif_rotation_creation(env):
        tests_passed += 1
    
    _logger.info(f"📊 Résultats des tests RCP: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        _logger.info("🎉 Tous les tests RCP sont passés avec succès !")
        return True
    else:
        _logger.error("💥 Certains tests RCP ont échoué")
        return False
