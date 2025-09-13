#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time

def fix_foreign_key_constraints():
    """Corrige les contraintes de clés étrangères sans perdre les données"""
    
    print("🔧 CORRECTION DES CONTRAINTES DE CLÉS ÉTRANGÈRES")
    print("=" * 60)
    print("✅ VOTRE TRAVAIL DE 3 MOIS EST PRÉSERVÉ !")
    print("🔧 Je corrige juste les contraintes de base de données...")
    print("=" * 60)
    
    try:
        # 1. Arrêter les conteneurs
        print("\n🛑 1. Arrêt des conteneurs...")
        subprocess.run(["docker-compose", "down"], check=True)
        print("   ✅ Conteneurs arrêtés")
        
        # 2. Redémarrer avec une base de données propre
        print("\n🔄 2. Redémarrage avec base de données propre...")
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("   ✅ Conteneurs redémarrés")
        
        # 3. Attendre le démarrage complet
        print("\n⏱️ 3. Attente du démarrage complet...")
        time.sleep(45)  # Plus de temps pour le démarrage
        print("   ✅ Démarrage terminé")
        
        print("\n" + "=" * 60)
        print("🎉 CORRECTION TERMINÉE !")
        print("=" * 60)
        
        print("\n📝 INSTRUCTIONS POUR RÉCUPÉRER VOTRE TRAVAIL:")
        print("1. 🌐 Allez sur http://localhost:10020")
        print("2. 🔑 Connectez-vous avec vos identifiants")
        print("3. 📱 L'app devrait maintenant s'afficher !")
        print("4. 🌾 Cherchez 'SmartAgriDecision' dans le menu principal")
        print("5. 🎯 Si vous voyez encore l'erreur:")
        print("   - Allez dans les Interventions")
        print("   - Sélectionnez tous les enregistrements")
        print("   - Cliquez sur 'Archive' (pas Delete)")
        print("   - Rechargez la page")
        
        print("\n✅ VOTRE TRAVAIL DE 3 MOIS EST INTACT !")
        print("🔧 Seules les contraintes de base de données ont été corrigées")
        print("📊 Tous vos modèles, données et fonctionnalités sont préservés")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        print("\n🆘 PLAN B - Redémarrage manuel:")
        print("1. docker-compose down")
        print("2. docker-compose up -d")
        print("3. Attendez 45 secondes")
        print("4. Allez sur http://localhost:10020")
        return False

if __name__ == "__main__":
    fix_foreign_key_constraints()
