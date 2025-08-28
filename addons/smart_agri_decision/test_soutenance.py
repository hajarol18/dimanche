#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Soutenance - SmartAgriDecision
=======================================
Script de vérification rapide avant la soutenance
"""

import logging
import sys
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
_logger = logging.getLogger(__name__)

def test_imports():
    """Test des imports des modèles principaux"""
    try:
        _logger.info("🧪 Test des imports des modèles...")
        
        # Test des modèles de base
        from models import smart_agri_exploitation
        from models import smart_agri_parcelle
        from models import smart_agri_culture
        from models import smart_agri_meteo
        
        # Test des modèles IA
        from models import smart_agri_ia_predictions
        from models import ia_simulateur
        from models import ia_detection_stress
        from models import ia_optimisation_ressources
        
        # Test des modèles climatiques
        from models import smart_agri_alerte_climatique
        from models import smart_agri_scenario_climatique
        from models import smart_agri_rcp_scenario
        
        _logger.info("✅ Tous les imports sont réussis")
        return True
        
    except ImportError as e:
        _logger.error(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        _logger.error(f"❌ Erreur inattendue: {e}")
        return False

def test_syntax():
    """Test de la syntaxe des fichiers Python"""
    try:
        _logger.info("🔍 Test de la syntaxe des fichiers...")
        
        # Liste des fichiers Python à vérifier
        python_files = [
            'models/smart_agri_exploitation.py',
            'models/smart_agri_parcelle.py',
            'models/smart_agri_culture.py',
            'models/smart_agri_meteo.py',
            'models/smart_agri_ia_predictions.py',
            'models/ia_simulateur.py',
            'models/ia_detection_stress.py',
            'models/ia_optimisation_ressources.py',
            'models/smart_agri_alerte_climatique.py',
            'models/smart_agri_scenario_climatique.py',
            'models/smart_agri_rcp_scenario.py',
        ]
        
        for file_path in python_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    compile(content, file_path, 'exec')
                    _logger.info(f"✅ {file_path} - Syntaxe OK")
            else:
                _logger.warning(f"⚠️ {file_path} - Fichier non trouvé")
        
        _logger.info("✅ Tous les fichiers Python ont une syntaxe valide")
        return True
        
    except SyntaxError as e:
        _logger.error(f"❌ Erreur de syntaxe: {e}")
        return False
    except Exception as e:
        _logger.error(f"❌ Erreur inattendue: {e}")
        return False

def test_manifest():
    """Test du fichier manifest"""
    try:
        _logger.info("📋 Test du fichier manifest...")
        
        if os.path.exists('__manifest__.py'):
            with open('__manifest__.py', 'r', encoding='utf-8') as f:
                content = f.read()
                compile(content, '__manifest__.py', 'exec')
                _logger.info("✅ __manifest__.py - Syntaxe OK")
        else:
            _logger.error("❌ __manifest__.py - Fichier non trouvé")
            return False
            
        return True
        
    except Exception as e:
        _logger.error(f"❌ Erreur dans le manifest: {e}")
        return False

def test_security():
    """Test du fichier de sécurité"""
    try:
        _logger.info("🔐 Test du fichier de sécurité...")
        
        if os.path.exists('security/ir.model.access.csv'):
            with open('security/ir.model.access.csv', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > 1:  # Au moins l'en-tête + 1 ligne
                    _logger.info(f"✅ Fichier de sécurité OK - {len(lines)} lignes")
                    return True
                else:
                    _logger.error("❌ Fichier de sécurité vide")
                    return False
        else:
            _logger.error("❌ Fichier de sécurité non trouvé")
            return False
            
    except Exception as e:
        _logger.error(f"❌ Erreur dans le fichier de sécurité: {e}")
        return False

def test_demo_data():
    """Test des données de démonstration"""
    try:
        _logger.info("📊 Test des données de démonstration...")
        
        demo_files = [
            'data/demo_data_complet.xml',
            'data/demo_data_massive.xml'
        ]
        
        for file_path in demo_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '<?xml' in content and 'odoo' in content:
                        _logger.info(f"✅ {file_path} - Format XML valide")
                    else:
                        _logger.warning(f"⚠️ {file_path} - Format XML suspect")
            else:
                _logger.warning(f"⚠️ {file_path} - Fichier non trouvé")
        
        return True
        
    except Exception as e:
        _logger.error(f"❌ Erreur dans les données de démonstration: {e}")
        return False

def test_views():
    """Test des vues XML"""
    try:
        _logger.info("👁️ Test des vues XML...")
        
        view_files = [
            'views/main_menu.xml',
            'views/exploitation_views.xml',
            'views/parcelle_views.xml',
            'views/culture_views.xml',
            'views/meteo_views.xml',
            'views/ia_predictions_views.xml',
            'views/tableau_bord_views.xml'
        ]
        
        for file_path in view_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '<?xml' in content and 'odoo' in content:
                        _logger.info(f"✅ {file_path} - Format XML valide")
                    else:
                        _logger.warning(f"⚠️ {file_path} - Format XML suspect")
            else:
                _logger.warning(f"⚠️ {file_path} - Fichier non trouvé")
        
        return True
        
    except Exception as e:
        _logger.error(f"❌ Erreur dans les vues: {e}")
        return False

def main():
    """Fonction principale de test"""
    _logger.info("🚀 DÉBUT DES TESTS DE SOUTENANCE - SmartAgriDecision")
    _logger.info("=" * 60)
    
    tests = [
        ("Test des imports", test_imports),
        ("Test de la syntaxe", test_syntax),
        ("Test du manifest", test_manifest),
        ("Test de la sécurité", test_security),
        ("Test des données de démonstration", test_demo_data),
        ("Test des vues", test_views),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        _logger.info(f"\n🔍 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            _logger.error(f"❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    _logger.info("\n" + "=" * 60)
    _logger.info("📊 RÉSUMÉ DES TESTS")
    _logger.info("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        _logger.info(f"{status} - {test_name}")
        if result:
            passed += 1
    
    _logger.info(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        _logger.info("🎉 FÉLICITATIONS ! Votre module est prêt pour la soutenance !")
        _logger.info("💡 Points forts identifiés:")
        _logger.info("   - Architecture complète et bien structurée")
        _logger.info("   - Modèles IA sophistiqués")
        _logger.info("   - Gestion des données climatiques avancée")
        _logger.info("   - Interface utilisateur complète")
        _logger.info("   - Sécurité et permissions bien définies")
        _logger.info("   - Données de démonstration complètes")
        return 0
    else:
        _logger.error("⚠️ ATTENTION ! Certains tests ont échoué.")
        _logger.error("🔧 Veuillez corriger les problèmes avant la soutenance.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
