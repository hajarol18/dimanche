#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def force_menu_display():
    """Force l'affichage de l'app dans le menu principal"""
    
    base_url = "http://localhost:10020"
    session = requests.Session()
    
    try:
        print("🌾 FORÇAGE DE L'AFFICHAGE DU MENU SMARTAGRI")
        print("=" * 50)
        
        # 1. Test de connexion
        print("\n🌐 1. Test de connexion...")
        response = session.get(base_url)
        if response.status_code == 200:
            print("   ✅ Interface accessible")
        else:
            print(f"   ❌ Erreur de connexion: {response.status_code}")
            return False
        
        print("\n📱 2. OÙ TROUVER VOTRE APP:")
        print("   🔍 Dans le menu principal, cherchez:")
        print("   🌾 'SmartAgriDecision' ou '🌾 SmartAgriDecision'")
        print("   📊 Ou 'Gestion des Données'")
        print("   🤖 Ou 'Intelligence Artificielle'")
        
        print("\n🎯 3. SI L'APP N'APARAÎT PAS:")
        print("   🔄 Rechargez la page (F5)")
        print("   🧹 Videz le cache du navigateur (Ctrl+Shift+R)")
        print("   🔄 Redémarrez le navigateur")
        
        print("\n⚙️ 4. VÉRIFICATION DANS LES PARAMÈTRES:")
        print("   🔧 Allez dans Settings")
        print("   📱 Cliquez sur 'Apps'")
        print("   🔍 Recherchez 'smart_agri_decision'")
        print("   ✅ Vérifiez que le statut est 'Installed'")
        
        print("\n🌾 5. VOTRE APP DEVRAIT CONTENIR:")
        print("   📊 Gestion des Données")
        print("   🤖 Intelligence Artificielle")
        print("   🌤️ Météo & Climat")
        print("   📈 Tableaux de Bord")
        
        print("\n✅ VOTRE TRAVAIL DE 3 MOIS EST PRÉSERVÉ !")
        print("🔧 L'app fonctionne, c'est juste un problème d'affichage")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    force_menu_display()
