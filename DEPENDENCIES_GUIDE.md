# 📦 Guide des Dépendances - SmartAgriDecision

## 🚀 Installation Rapide

### Prérequis Système
- **Docker** et **Docker Compose** (recommandé)
- **Python 3.8+** (pour développement local)
- **PostgreSQL 12+** avec **PostGIS 3.0+**
- **Git**

### Option 1: Installation avec Docker (Recommandée)

```bash
# 1. Cloner le repository
git clone https://github.com/hajarol18/dimanche.git
cd dimanche

# 2. Démarrer les services
docker-compose up -d

# 3. Accéder à Odoo
# http://localhost:10020
```

**Avantages :**
- ✅ Installation automatique de toutes les dépendances
- ✅ Base de données PostgreSQL + PostGIS configurée
- ✅ Environnement isolé et reproductible
- ✅ Pas de conflits de versions

### Option 2: Installation Locale (Développement)

#### 1. Installation Python et dépendances

```bash
# Créer un environnement virtuel
python -m venv smartagri_env
source smartagri_env/bin/activate  # Linux/Mac
# ou
smartagri_env\Scripts\activate     # Windows

# Installer les dépendances de base
pip install -r etc/requirements.txt

# Installer les dépendances avancées (pour l'IA)
pip install -r addons/smart_agri_decision/requirements.txt
```

#### 2. Installation PostgreSQL + PostGIS

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql-12 postgresql-12-postgis-3
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows:**
- Télécharger PostgreSQL depuis https://www.postgresql.org/download/windows/
- Installer PostGIS via Stack Builder

**macOS:**
```bash
brew install postgresql postgis
brew services start postgresql
```

#### 3. Configuration de la base de données

```sql
-- Créer la base de données
CREATE DATABASE odoo123;
CREATE USER odoo_user WITH PASSWORD 'odoo_password';
GRANT ALL PRIVILEGES ON DATABASE odoo123 TO odoo_user;

-- Activer PostGIS
\c odoo123
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
```

## 📋 Dépendances Détaillées

### 🔧 Dépendances Système

| Composant | Version | Description |
|-----------|---------|-------------|
| **Docker** | 20.10+ | Conteneurisation |
| **Docker Compose** | 2.0+ | Orchestration |
| **Python** | 3.8+ | Langage principal |
| **PostgreSQL** | 12+ | Base de données |
| **PostGIS** | 3.0+ | Extension géospatiale |

### 🐍 Dépendances Python Principales

#### Core Data Science
```bash
pandas>=2.0.0          # Manipulation de données
numpy>=1.24.0           # Calculs numériques
scipy>=1.10.0           # Calculs scientifiques
```

#### Machine Learning & IA
```bash
scikit-learn>=1.3.0     # ML classique
xgboost>=2.0.0          # Gradient boosting
lightgbm>=4.0.0         # Gradient boosting rapide
catboost>=1.2.0         # Gradient boosting catégoriel
```

#### Deep Learning (Optionnel)
```bash
tensorflow>=2.13.0      # Deep learning
torch>=2.0.0            # PyTorch
keras>=2.13.0           # API haut niveau
```

#### Géospatial & Cartographie
```bash
geopandas>=0.13.0       # Données géospatiales
shapely>=2.0.0          # Géométries
folium>=0.14.0          # Cartes interactives
leaflet>=0.25.0         # Cartes web
```

#### Base de données
```bash
psycopg2-binary>=2.9.0  # Driver PostgreSQL
sqlalchemy>=2.0.0       # ORM
```

#### Météo & Climat
```bash
meteostat>=1.0.0        # Données météo
xarray>=2023.0.0        # Données climatiques
netCDF4>=1.6.0          # Fichiers climatiques
```

## 🛠️ Installation par Étapes

### Étape 1: Vérifier les prérequis
```bash
# Vérifier Docker
docker --version
docker-compose --version

# Vérifier Python
python --version  # Doit être 3.8+

# Vérifier Git
git --version
```

### Étape 2: Cloner et configurer
```bash
# Cloner le repository
git clone https://github.com/hajarol18/dimanche.git
cd dimanche

# Vérifier la structure
ls -la
# Doit contenir: addons/, docker-compose.yml, README.md
```

### Étape 3: Démarrer avec Docker
```bash
# Démarrer les services
docker-compose up -d

# Vérifier les conteneurs
docker-compose ps

# Voir les logs
docker-compose logs -f
```

### Étape 4: Accéder à l'application
- **Odoo** : http://localhost:10020
- **Base de données** : localhost:5432
- **Utilisateur** : hajar / hajar

## 🔧 Configuration Avancée

### Variables d'environnement
```bash
# Créer un fichier .env
cat > .env << EOF
POSTGRES_DB=odoo123
POSTGRES_USER=odoo
POSTGRES_PASSWORD=odoo
ODOO_DB=odoo123
ODOO_USER=hajar
ODOO_PASSWORD=hajar
ODOO_PORT=10020
EOF
```

### Configuration Odoo
```bash
# Fichier de configuration
cat > etc/odoo.conf << EOF
[options]
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
admin_passwd = admin
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
db_name = odoo123
xmlrpc_port = 8069
xmlrpc_interface = 0.0.0.0
EOF
```

## 🧪 Tests et Vérification

### Test de l'installation
```bash
# Exécuter le script de test
python test_ia_final_corrige.py

# Vérifier les modules
python -c "import pandas, numpy, sklearn; print('✅ Dépendances OK')"
```

### Test des fonctionnalités IA
```bash
# Test des modèles IA
python -c "
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
print('✅ IA Libraries OK')
"
```

## 🚨 Résolution de Problèmes

### Problème: Docker ne démarre pas
```bash
# Vérifier les ports
netstat -tulpn | grep :10020
netstat -tulpn | grep :5432

# Redémarrer Docker
sudo systemctl restart docker
```

### Problème: Erreur PostgreSQL
```bash
# Vérifier les logs
docker-compose logs db

# Redémarrer la base
docker-compose restart db
```

### Problème: Module non trouvé
```bash
# Vérifier les addons
docker-compose exec odoo odoo -d odoo123 -i smart_agri_decision

# Mettre à jour la liste
docker-compose exec odoo odoo -d odoo123 -u all
```

### Problème: Dépendances Python manquantes
```bash
# Installer manuellement
pip install -r addons/smart_agri_decision/requirements.txt

# Ou via Docker
docker-compose exec odoo pip install -r /mnt/extra-addons/smart_agri_decision/requirements.txt
```

## 📚 Ressources Utiles

### Documentation
- [Odoo 18 Documentation](https://www.odoo.com/documentation/18.0/)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [Docker Documentation](https://docs.docker.com/)

### APIs et Services
- [Meteostat API](https://dev.meteostat.net/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [PostGIS Functions](https://postgis.net/docs/reference.html)

### Communauté
- [Odoo Community](https://www.odoo.com/community)
- [PostGIS Mailing List](https://lists.osgeo.org/mailman/listinfo/postgis-users)

## 🎯 Prochaines Étapes

1. **Cloner le repository** : `git clone https://github.com/hajarol18/dimanche.git`
2. **Démarrer avec Docker** : `docker-compose up -d`
3. **Accéder à Odoo** : http://localhost:10020
4. **Installer le module** : SmartAgriDecision
5. **Tester les fonctionnalités** : Scripts de test
6. **Commencer le développement IA** : Modèles et algorithmes

---

**🌾 Bon développement avec SmartAgriDecision !** 🤖
