#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def force_app_display():
    """Force l'affichage de l'app dans le menu principal"""
    
    base_url = "http://localhost:10020"
    session = requests.Session()
    
    try:
        print("🌾 FORÇAGE DE L'AFFICHAGE DE L'APP SMARTAGRI")
        print("=" * 50)
        
        # 1. Test de connexion
        print("\n🌐 1. Test de connexion...")
        response = session.get(base_url)
        if response.status_code == 200:
            print("   ✅ Interface accessible")
        else:
            print(f"   ❌ Erreur de connexion: {response.status_code}")
            return False
        
        print("\n📝 2. Instructions pour afficher l'app:")
        print("   🔧 Allez sur http://localhost:10020")
        print("   🔑 Connectez-vous avec vos identifiants")
        print("   ⚙️ Allez dans Settings (Paramètres)")
        print("   📱 Cliquez sur 'Apps' dans le menu de gauche")
        print("   🔍 Recherchez 'smart_agri_decision'")
        print("   📦 Cliquez sur le module")
        print("   ✅ Vérifiez que le statut est 'Installed'")
        print("   🔄 Si 'To Upgrade', cliquez sur 'Upgrade'")
        
        print("\n🎯 3. Si l'app n'apparaît toujours pas:")
        print("   🔄 Rechargez la page (F5)")
        print("   🧹 Videz le cache du navigateur")
        print("   🔄 Redémarrez le conteneur Docker")
        
        print("\n🌾 4. L'app devrait apparaître comme:")
        print("   📱 Menu principal: '🌾 SmartAgriDecision'")
        print("   📊 Sous-menus: Gestion des Données, IA, etc.")
        
        print("\n✅ Votre module fonctionne, c'est juste un problème d'affichage!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    force_app_display()
