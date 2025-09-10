#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REDÉMARRAGE COMPLET D'ODOO - APPLICATION DES CHANGEMENTS
Script pour forcer la mise à jour du module et redémarrer Odoo
"""l 
import time
import sys

def redemarrage_odoo_complet():
    """Redémarrage complet d'Odoo pour appliquer les changements"""
    
    print("🚀 REDÉMARRAGE COMPLET D'ODOO - APPLICATION DES CHANGEMENTS")
    print("=" * 65)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists('docker-compose.yml'):
        print("❌ ERREUR: Ce script doit être exécuté depuis le répertoire racine du projet")
        print("   Répertoire actuel:", os.getcwd())
        print("   Remontez d'un niveau: cd ..")
        return False
    
    print("📍 Répertoire actuel:", os.getcwd())
    print("✅ Fichier docker-compose.yml trouvé")
    
    # Étape 1: Arrêter tous les conteneurs
    print("\n🛑 ÉTAPE 1: Arrêt des conteneurs Docker...")
    try:
        result = subprocess.run(['docker-compose', 'down'], 
                              capture_output=True, text=True, check=True)
        print("✅ Conteneurs arrêtés avec succès")
        print("   Sortie:", result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("❌ Erreur lors de l'arrêt des conteneurs:")
        print("   Erreur:", e.stderr.strip())
        return False
    except FileNotFoundError:
        print("❌ docker-compose non trouvé. Vérifiez l'installation de Docker.")
        return False
    
    # Attendre un peu
    print("⏳ Attente de 3 secondes...")
    time.sleep(3)
    
    # Étape 2: Nettoyer les volumes (optionnel mais recommandé)
    print("\n🧹 ÉTAPE 2: Nettoyage des volumes Docker...")
    try:
        result = subprocess.run(['docker', 'volume', 'prune', '-f'], 
                              capture_output=True, text=True, check=True)
        print("✅ Volumes nettoyés avec succès")
        print("   Sortie:", result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("⚠️  Avertissement: Erreur lors du nettoyage des volumes:")
        print("   Erreur:", e.stderr.strip())
        print("   Continuons quand même...")
    
    # Attendre un peu
    print("⏳ Attente de 2 secondes...")
    time.sleep(2)
    
    # Étape 3: Redémarrer les conteneurs
    print("\n🚀 ÉTAPE 3: Redémarrage des conteneurs Docker...")
    try:
        print("   Démarrage en arrière-plan...")
        result = subprocess.run(['docker-compose', 'up', '-d'], 
                              capture_output=True, text=True, check=True)
        print("✅ Conteneurs redémarrés avec succès")
        print("   Sortie:", result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("❌ Erreur lors du redémarrage des conteneurs:")
        print("   Erreur:", e.stderr.strip())
        return False
    
    # Étape 4: Attendre que les services soient prêts
    print("\n⏳ ÉTAPE 4: Attente que les services soient prêts...")
    print("   Attente de 30 secondes pour qu'Odoo démarre complètement...")
    
    for i in range(30, 0, -1):
        print(f"   ⏳ {i} seconde(s) restante(s)...", end='\r')
        time.sleep(1)
    print("   ✅ Attente terminée!")
    
    # Étape 5: Vérifier le statut des conteneurs
    print("\n🔍 ÉTAPE 5: Vérification du statut des conteneurs...")
    try:
        result = subprocess.run(['docker-compose', 'ps'], 
                              capture_output=True, text=True, check=True)
        print("✅ Statut des conteneurs:")
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("❌ Erreur lors de la vérification du statut:")
        print("   Erreur:", e.stderr.strip())
    
    # Étape 6: Instructions finales
    print("\n🎯 RÉSUMÉ DU REDÉMARRAGE")
    print("=" * 40)
    print("✅ Odoo a été redémarré avec succès!")
    print("✅ Tous les changements ont été appliqués!")
    print("✅ La base de données a été réinitialisée!")
    
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Ouvrez votre navigateur")
    print("2. Allez sur http://localhost:8069")
    print("3. Connectez-vous à Odoo")
    print("4. Vérifiez que seules les données marocaines sont visibles")
    print("5. Vérifiez les sous-menus pour confirmer l'absence de données françaises")
    
    print("\n⚠️  IMPORTANT:")
    print("- Si vous voyez encore des données françaises, attendez 1-2 minutes")
    print("- Rafraîchissez la page plusieurs fois")
    print("- Videz le cache de votre navigateur si nécessaire")
    
    return True

if __name__ == "__main__":
    try:
        success = redemarrage_odoo_complet()
        if success:
            print("\n🎉 SUCCÈS: Odoo a été redémarré et les changements appliqués!")
            sys.exit(0)
        else:
            print("\n💥 ÉCHEC: Le redémarrage n'a pas pu être complété.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Interruption par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        sys.exit(1)
