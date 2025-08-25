# 🌾 SmartAgriDecision - Module Odoo 18

## 📋 Description

**SmartAgriDecision** est un module Odoo 18 innovant d'aide à la décision agricole basé sur l'Intelligence Artificielle et les données spatiales. Ce module permet aux agriculteurs de gérer leurs exploitations, analyser les données météorologiques, obtenir des prédictions IA et planifier leurs cultures et interventions.

## 🚀 Fonctionnalités Principales

### 🌱 Gestion Agricole
- **Exploitations** : Gestion complète des exploitations agricoles
- **Parcelles** : Géolocalisation et gestion des parcelles avec PostGIS
- **Cultures** : Planification et suivi des cultures par parcelle
- **Intrants** : Gestion des semences, engrais, pesticides, eau
- **Interventions** : Planning des interventions agricoles

### 🌤️ Données Climatiques
- **Météo** : Suivi des conditions météorologiques
- **Import Meteostat** : Import automatique des données climatiques
- **Alertes Climatiques** : Surveillance des conditions menaçantes
- **Tendances Climatiques** : Analyse des tendances à long terme

### 🤖 Intelligence Artificielle
- **Prédictions IA** : Modèles prédictifs pour les cultures
- **Analyse des données** : Traitement avancé des données agricoles
- **Recommandations** : Suggestions basées sur l'IA

## 🛠️ Technologies Utilisées

- **Odoo 18** : Plateforme ERP moderne
- **PostgreSQL + PostGIS** : Base de données géospatiale
- **Python** : Logique métier et IA
- **Docker** : Déploiement conteneurisé
- **Meteostat** : API de données climatiques

## 📦 Installation

### Prérequis
- Docker et Docker Compose
- Git

### Déploiement Rapide
```bash
# Cloner le repository
git clone https://github.com/hajarol18/dimanche.git
cd dimanche

# Démarrer les services
docker-compose up -d

# Accéder à Odoo
# http://localhost:10018
```

### Installation du Module
1. Ouvrir http://localhost:10018
2. Aller dans **Applications**
3. Mettre à jour la liste des applications
4. Rechercher "Smart Agri Decision"
5. Installer le module

## 🏗️ Architecture

```
smart_agri_decision/
├── models/                     # Modèles Python
│   ├── smart_agri_exploitation.py
│   ├── smart_agri_parcelle.py
│   ├── smart_agri_culture.py
│   ├── smart_agri_meteo.py
│   ├── smart_agri_intrants.py
│   ├── smart_agri_meteostat_import.py
│   ├── smart_agri_alerte_climatique.py
│   └── smart_agri_tendance_climatique.py
├── views/                      # Vues XML
│   ├── actions.xml            # Actions centralisées
│   ├── main_menu.xml          # Structure des menus
│   ├── exploitation_views.xml
│   ├── parcelle_views.xml
│   ├── culture_views.xml
│   ├── meteo_views.xml
│   ├── intrants_views.xml
│   ├── meteostat_import_views.xml
│   ├── alerte_climatique_views.xml
│   └── tendance_climatique_views.xml
├── security/                   # Sécurité
│   ├── ir.model.access.csv    # Droits d'accès
│   └── security_data.xml      # Groupes et règles
├── data/                       # Données
│   └── visibility.xml         # Visibilité du module
└── __manifest__.py            # Manifeste du module
```

## 🔐 Sécurité

- **Droits d'accès** : Gestion fine des permissions utilisateur
- **Groupes de sécurité** : Séparation des rôles (utilisateur, manager, admin)
- **Validation des données** : Contrôles de saisie et validation

## 📊 Utilisation

### Menu Principal
- **Gestion** : Exploitations, parcelles, cultures, intrants
- **Données Climatiques** : Météo, Meteostat, alertes, tendances
- **Intelligence Artificielle** : Prédictions et analyses
- **Configuration** : Types de sol et paramètres

### Workflow Typique
1. **Créer une exploitation** avec ses informations
2. **Définir les parcelles** avec géolocalisation
3. **Planifier les cultures** par parcelle
4. **Importer les données météo** depuis Meteostat
5. **Surveiller les alertes** climatiques
6. **Analyser les tendances** à long terme
7. **Planifier les interventions** basées sur l'IA

## 🌍 Compatibilité

- **Odoo** : Version 18.0+
- **PostgreSQL** : Version 13+
- **PostGIS** : Version 3.0+
- **Docker** : Version 20.10+

## 🤝 Contribution

Ce projet est développé dans le cadre d'un stage académique. Les contributions sont les bienvenues !

### Comment contribuer
1. Fork le repository
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📝 Licence

Ce projet est sous licence LGPL-3. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Hajar** - Développeur stagiaire

## 📞 Support

Pour toute question ou problème :
- Créer une issue sur GitHub
- Contacter l'auteur via le repository

## 🎯 Roadmap

- [ ] Intégration avec d'autres APIs météo
- [ ] Modèles IA plus avancés
- [ ] Interface mobile responsive
- [ ] API REST pour intégrations externes
- [ ] Tableaux de bord avancés
- [ ] Export des données en formats variés

---

**🌱 L'agriculture intelligente de demain commence aujourd'hui !**
