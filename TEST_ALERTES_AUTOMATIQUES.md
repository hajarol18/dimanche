# 🧪 TEST DES ALERTES CLIMATIQUES AUTOMATIQUES

## 🎯 OBJECTIF
Vérifier que les alertes se créent **AUTOMATIQUEMENT** selon la logique métier corrigée.

## 📱 ÉTAPES DE TEST DANS ODOO

### **1. 🌍 Aller dans "Météo & Climat" → "Import Meteostat"**

### **2. ➕ Créer un nouvel import avec :**
- **Nom** : `Test Alertes Automatiques`
- **Exploitation** : Sélectionner une exploitation existante
- **Station ID** : `TEST001`
- **Latitude** : `31.7917` (Maroc)
- **Longitude** : `-7.0926`
- **Date début** : `2025-01-01`
- **Date fin** : `2025-01-31`
- **Scénario climatique** : `🔥 RCP 8.5 - Pessimiste (+4.8°C en 2100)`
- **Paramètres** : `🌤️ Tous les paramètres`

### **3. 💾 Sauvegarder l'import**

### **4. 🚀 Cliquer sur "Créer Alertes Climatiques"**

### **5. ✅ VÉRIFIER QUE :**
- Les alertes sont créées **AUTOMATIQUEMENT**
- Elles apparaissent dans "Météo & Climat" → "Alertes Climatiques"
- **AUCUNE** intervention manuelle n'est nécessaire

## 🎯 RÉSULTAT ATTENDU

**✅ SUCCÈS :** Alertes créées automatiquement selon le scénario RCP 8.5
**❌ ÉCHEC :** Aucune alerte créée ou création manuelle requise

## 🔍 POINTS DE VÉRIFICATION

1. **Alertes créées automatiquement** ✅
2. **Niveau d'alerte approprié** (orange/rouge pour RCP 8.5) ✅
3. **Types d'alerte** : sécheresse, canicule ✅
4. **Lien avec l'exploitation** ✅
5. **Source** : "Import Météo Automatique" ✅

## 🚨 SI ÇA NE MARCHE PAS

Le problème est dans la logique métier et nécessite une correction immédiate.
