#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour la mise à jour du module SmartAgriDecision
avec les nouvelles données marocaines simplifiées
"""

import os
import sys
import subprocess
import time

def main():
    print("🚀 TEST DE MISE À JOUR DU MODULE SMARTAGRI - MAROC")
    print("=" * 60)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists('docker-compose.yml'):
        print("❌ ERREUR: docker-compose.yml non trouvé")
        print("   Exécutez ce script depuis le répertoire racine du projet")
        return False
    
    print("✅ Répertoire correct détecté")
    
    # Vérifier l'état des conteneurs
    print("\n📊 Vérification de l'état des conteneurs...")
    try:
        result = subprocess.run(['docker-compose', 'ps'], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la vérification des conteneurs: {e}")
        return False
    
    # Vérifier que le module est bien installé
    print("\n🔍 Vérification du module dans Odoo...")
    print("   Allez sur http://localhost:10019")
    print("   Vérifiez que SmartAgriDecision apparaît dans Applications")
    
    # Instructions pour l'utilisateur
    print("\n📋 INSTRUCTIONS POUR LA MISE À JOUR:")
    print("1. Ouvrez http://localhost:10019 dans votre navigateur")
    print("2. Allez dans Applications > SmartAgriDecision")
    print("3. Cliquez sur 'Mettre à jour' (bouton de mise à jour)")
    print("4. Attendez que la mise à jour se termine")
    print("5. Vérifiez qu'il n'y a plus d'erreurs")
    
    print("\n🎯 RÉSULTAT ATTENDU:")
    print("   ✅ Module mis à jour avec succès")
    print("   ✅ Données marocaines chargées")
    print("   ✅ Aucune erreur de formatage")
    print("   ✅ Types de sol marocains visibles")
    print("   ✅ Exploitations marocaines visibles")
    print("   ✅ Stations météo marocaines visibles")
    
    print("\n⚠️  EN CAS D'ERREUR:")
    print("   - Vérifiez les logs: docker-compose logs odoo")
    print("   - Redémarrez: docker-compose restart odoo")
    print("   - Contactez l'assistant pour analyse")
    
    print("\n🚀 PRÊT POUR LA MISE À JOUR !")
    print("   Suivez les instructions ci-dessus...")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Script terminé avec succès")
    else:
        print("\n❌ Script terminé avec des erreurs")
        sys.exit(1)
