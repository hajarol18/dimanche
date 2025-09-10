#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vérification finale - Confirmation de la suppression complète des données françaises
"""

import os
import xml.etree.ElementTree as ET
import glob

def verification_finale_maroc():
    """Vérifie que toutes les données françaises ont été supprimées"""
    
    print("🔍 VÉRIFICATION FINALE - SUPPRESSION COMPLÈTE DES DONNÉES FRANÇAISES")
    print("=" * 80)
    
    # 1. Recherche de tous les fichiers XML dans le projet
    fichiers_xml = []
    for pattern in ["data/*.xml", "views/*.xml", "*.xml"]:
        fichiers_xml.extend(glob.glob(pattern))
    
    fichiers_xml = list(set(fichiers_xml))  # Suppression des doublons
    fichiers_xml.sort()
    
    print(f"📁 FICHIERS XML TROUVÉS ({len(fichiers_xml)}) :")
    for fichier in fichiers_xml:
        if os.path.exists(fichier):
            print(f"   📄 {fichier}")
    
    # 2. Mots-clés français à détecter
    mots_cles_francais = [
        # Régions françaises
        "Provence", "Nouvelle-Aquitaine", "Hauts-de-France", "Auvergne", "Occitanie", "Bretagne",
        "Île-de-France", "Grand Est", "Centre-Val de Loire", "Bourgogne-Franche-Comté", "Normandie",
        "Pays de la Loire", "Corse",
        
        # Villes françaises
        "Paris", "Lyon", "Marseille", "Bordeaux", "Lille", "Toulouse", "Nice", "Nantes", "Strasbourg",
        "Montpellier", "Rennes", "Reims", "Saint-Étienne", "Le Havre", "Toulon", "Grenoble", "Dijon",
        
        # Coordonnées françaises
        "48.8580", "2.3580", "45.7640", "4.8357", "43.2965", "5.3698", "44.8378", "-0.5792",
        "50.6292", "3.0573", "43.6047", "1.4442", "43.7102", "7.7521", "48.8566", "2.3522",
        
        # Exploitations françaises
        "Coopérative du Soleil", "Domaine des Coteaux", "EARL des Grands Champs", 
        "Ferme de la Vallée", "GAEC des Trois Chênes", "Ferme de la Vallée Verte",
        
        # Codes français
        "SOL004", "COT002", "GRA005", "FERME001", "VAL001", "TRO003",
        
        # Noms français
        "Pierre Durand", "Sophie Moreau", "Jean Dupont", "Marie Martin", "Paul Bernard",
        
        # Départements françaises
        "Bouches-du-Rhône", "Gironde", "Nord", "Rhône", "Haute-Garonne", "Finistère", "Seine",
        "Loire-Atlantique", "Bas-Rhin", "Hérault", "Ille-et-Vilaine", "Marne", "Loire", "Isère",
        
        # Autres références françaises
        "France", "français", "française", "françaises", "français", "hexagone", "métropole"
    ]
    
    # 3. Mots-clés marocains à vérifier
    mots_cles_marocains = [
        # Régions marocaines
        "Casablanca-Settat", "Souss-Massa", "Fès-Meknès", "Rabat-Salé-Kénitra", 
        "Tanger-Tétouan-Al Hoceïma", "Marrakech-Safi", "Drâa-Tafilalet", "Béni Mellal-Khénifra",
        "Oriental", "Guelmim-Oued Noun", "Laâyoune-Sakia El Hamra", "Dakhla-Oued Ed-Dahab",
        
        # Villes marocaines
        "Casablanca", "Rabat", "Agadir", "Meknès", "Mohammedia", "El Jadida", "Fès", "Marrakech",
        "Tanger", "Tétouan", "Oujda", "Béni Mellal", "Kénitra", "Safi", "Essaouira", "Ifrane",
        
        # Coordonnées marocaines
        "33.9716", "-6.8498", "32.2540", "-8.5102", "30.4278", "-9.5981", "33.8935", "-5.5473",
        "33.5731", "-7.5898", "33.5951", "-7.6328", "34.0209", "-6.8416", "31.6295", "-7.9811",
        
        # Exploitations marocaines
        "Exploitation Doukkala", "Domaine Souss Massa", "Coopérative Meknès", "Ferme du Blé d'Or",
        "Verger des Pommes d'Or", "Maraîchage Bio Excellence",
        
        # Codes marocains
        "DK001", "SM002", "MK003", "RB001", "CS001", "MH001",
        
        # Noms marocains
        "Ahmed Benali", "Fatima Alaoui", "Mohammed Alami", "Amina Tazi", "Coopérative Al Baraka",
        "Fatima Zahra",
        
        # Types de sol marocains
        "Sol Tirs", "Sol Hamri", "Sol Rmel", "Sol Limoneux", "Sol Argileux",
        
        # Cultures marocaines
        "Blé Dur", "Orge", "Orangers Valencia", "Arganiers", "Oliviers", "Vigne", "Pommes Golden",
        "Poires", "Tomates Bio", "Salades Bio", "Carottes Bio"
    ]
    
    # 4. Analyse de chaque fichier
    total_fichiers_verifies = 0
    total_donnees_francaises_trouvees = 0
    total_donnees_marocaines_trouvees = 0
    fichiers_avec_francais = []
    
    print(f"\n🔍 ANALYSE DÉTAILLÉE DES FICHIERS...")
    print("-" * 60)
    
    for fichier in fichiers_xml:
        if os.path.exists(fichier):
            try:
                print(f"\n📄 Analyse de {fichier}...")
                
                # Lecture du fichier
                with open(fichier, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                # Vérification des données françaises
                donnees_francaises_trouvees = []
                for mot_cle in mots_cles_francais:
                    if mot_cle.lower() in contenu.lower():
                        donnees_francaises_trouvees.append(mot_cle)
                        total_donnees_francaises_trouvees += 1
                
                # Vérification des données marocaines
                donnees_marocaines_trouvees = []
                for mot_cle in mots_cles_marocains:
                    if mot_cle in contenu:
                        donnees_marocaines_trouvees.append(mot_cle)
                        total_donnees_marocaines_trouvees += 1
                
                # Affichage des résultats
                if donnees_francaises_trouvees:
                    print(f"   ⚠️  DONNÉES FRANÇAISES DÉTECTÉES : {', '.join(donnees_francaises_trouvees)}")
                    fichiers_avec_francais.append(fichier)
                else:
                    print(f"   ✅ Aucune donnée française détectée")
                
                if donnees_marocaines_trouvees:
                    print(f"   🇲🇦 DONNÉES MAROCAINES DÉTECTÉES : {len(donnees_marocaines_trouvees)} références")
                    if len(donnees_marocaines_trouvees) <= 5:
                        print(f"      Exemples : {', '.join(donnees_marocaines_trouvees)}")
                    else:
                        print(f"      Exemples : {', '.join(donnees_marocaines_trouvees[:5])}...")
                
                total_fichiers_verifies += 1
                
            except Exception as e:
                print(f"   ❌ Erreur lors de l'analyse : {e}")
    
    # 5. Affichage du résumé final
    print("\n" + "=" * 80)
    print("📋 RÉSUMÉ DE LA VÉRIFICATION FINALE")
    print("=" * 80)
    
    print(f"📁 Fichiers vérifiés : {total_fichiers_verifies}")
    print(f"🇫🇷 Données françaises trouvées : {total_donnees_francaises_trouvees}")
    print(f"🇲🇦 Données marocaines trouvées : {total_donnees_marocaines_trouvees}")
    
    if total_donnees_francaises_trouvees == 0:
        print("\n🎉 SUCCÈS TOTAL : Aucune donnée française détectée !")
        print("✅ Le module est maintenant 100% marocain")
        print("🇲🇦 Prêt pour la production marocaine")
    else:
        print(f"\n⚠️  ATTENTION : {total_donnees_francaises_trouvees} données françaises encore présentes")
        print("🔧 Fichiers nécessitant un nettoyage supplémentaire :")
        for fichier in fichiers_avec_francais:
            print(f"   - {fichier}")
    
    # 6. Vérification des données dans Odoo
    print(f"\n🔍 VÉRIFICATION DES DONNÉES ODOO :")
    print("-" * 40)
    
    if total_donnees_francaises_trouvees == 0:
        print("✅ Toutes les données françaises ont été supprimées des fichiers")
        print("✅ Le module peut être mis à jour dans Odoo")
        print("✅ L'interface devrait maintenant afficher uniquement des données marocaines")
    else:
        print("⚠️  Données françaises encore présentes dans certains fichiers")
        print("🔧 Nécessite un nettoyage supplémentaire avant mise à jour")
    
    # 7. Recommandations finales
    print(f"\n🎯 RECOMMANDATIONS FINALES :")
    print("-" * 40)
    
    if total_donnees_francaises_trouvees == 0:
        print("   ✅ Module prêt pour la production - 100% marocain")
        print("   ✅ Mettre à jour le module dans Odoo")
        print("   ✅ Vérifier l'affichage dans l'interface")
        print("   ✅ Tester les fonctionnalités marocaines")
        print("   ✅ Valider la suppression complète")
    else:
        print("   🔧 Nettoyer les données françaises restantes")
        print("   🔧 Vérifier les références dans les modèles")
        print("   🔧 Relancer la vérification après nettoyage")
        print("   🔧 Ne pas mettre à jour le module avant nettoyage complet")
    
    # 8. Création du rapport de vérification finale
    rapport_final = f"""# RAPPORT DE VÉRIFICATION FINALE - SmartAgriDecision

## 📅 Date de la vérification
{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🔍 Résumé de la vérification
- **Fichiers vérifiés** : {total_fichiers_verifies}
- **Données françaises trouvées** : {total_donnees_francaises_trouvees}
- **Données marocaines trouvées** : {total_donnees_marocaines_trouvees}
- **Statut** : {'100% MAROCAIN' if total_donnees_francaises_trouvees == 0 else 'DONNÉES FRANÇAISES PRÉSENTES'}

## 📁 Fichiers analysés
{chr(10).join([f"- {fichier}" for fichier in fichiers_xml])}

## 🗑️ Données françaises détectées
{chr(10).join([f"- {mot_cle}" for mot_cle in mots_cles_francais if any(mot_cle.lower() in open(f, 'r', encoding='utf-8').read().lower() for f in fichiers_xml if os.path.exists(f))])}

## 🇲🇦 Données marocaines détectées
{chr(10).join([f"- {mot_cle}" for mot_cle in mots_cles_marocains if any(mot_cle in open(f, 'r', encoding='utf-8').read() for f in fichiers_xml if os.path.exists(f))])}

## ⚠️ Fichiers avec données françaises
{chr(10).join([f"- {fichier}" for fichier in fichiers_avec_francais])}

## 🎯 Résultat final
{'✅ SUCCÈS : Le module est maintenant 100% marocain' if total_donnees_francaises_trouvees == 0 else '⚠️ ATTENTION : Données françaises encore présentes'}

## 🔧 Actions recommandées
{chr(10).join(['1. Mettre à jour le module dans Odoo', '2. Vérifier l\'affichage dans l\'interface', '3. Tester les fonctionnalités marocaines', '4. Valider la suppression complète'] if total_donnees_francaises_trouvees == 0 else ['1. Nettoyer les données françaises restantes', '2. Vérifier les références dans les modèles', '3. Relancer la vérification après nettoyage', '4. Ne pas mettre à jour le module avant nettoyage complet'])}

---
*Rapport généré automatiquement par le script de vérification finale*
"""
    
    with open("RAPPORT_VERIFICATION_FINALE.md", "w", encoding="utf-8") as f:
        f.write(rapport_final)
    
    print(f"\n📋 Rapport de vérification finale créé : RAPPORT_VERIFICATION_FINALE.md")
    
    return total_donnees_francaises_trouvees == 0

if __name__ == "__main__":
    try:
        verification_finale_maroc()
    except Exception as e:
        print(f"❌ Erreur lors de la vérification : {e}")
        import traceback
        traceback.print_exc()
