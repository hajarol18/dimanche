# -*- coding: utf-8 -*-
"""
StressDetectionModel - Détection automatique de stress climatique et hydrique
Utilise l'IA pour détecter les stress subis par les cultures
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
import xgboost as xgb
import joblib
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class StressDetectionModel:
    """
    Modèle de détection de stress basé sur l'IA
    """
    
    def __init__(self):
        self.model = None
        self.model_type = 'xgboost'  # 'xgboost', 'random_forest', 'isolation_forest'
        self.scaler = StandardScaler()
        self.label_encoder = None
        self.stress_types = {
            'hydrique': 'Stress hydrique - Manque d\'eau',
            'thermique': 'Stress thermique - Température extrême',
            'nutritionnel': 'Stress nutritionnel - Carence en nutriments',
            'salinite': 'Stress de salinité - Excès de sel',
            'ph': 'Stress de pH - Acidité/alcalinité excessive',
            'vent': 'Stress éolien - Vent fort',
            'gel': 'Stress de gel - Température trop basse',
            'chaleur': 'Stress de chaleur - Température trop élevée',
            'aucun': 'Aucun stress détecté'
        }
        self.feature_importance = None
        self.training_metrics = {}
        self.is_trained = False
        
        # Seuils de stress prédéfinis
        self.stress_thresholds = {
            'hydrique': {
                'precipitation_7j': 10,  # mm
                'humidite_sol': 30,      # %
                'indice_vegetation': 0.3
            },
            'thermique': {
                'temperature_max': 35,   # °C
                'temperature_min': 0,    # °C
                'amplitude_thermique': 20 # °C
            },
            'nutritionnel': {
                'azote_sol': 20,        # ppm
                'phosphore_sol': 10,    # ppm
                'potassium_sol': 100    # ppm
            }
        }
    
    def train(self, X, y, model_type='xgboost', test_size=0.2, random_state=42):
        """
        Entraîne le modèle de détection de stress
        
        Args:
            X: Features (données météo, sol, culture)
            y: Target (types de stress)
            model_type: Type de modèle
            test_size: Proportion pour le test
            random_state: Seed pour reproductibilité
        """
        _logger.info(f"Entraînement du modèle de détection de stress ({model_type})...")
        
        self.model_type = model_type
        
        # Encodage des labels pour la classification
        from sklearn.preprocessing import LabelEncoder
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
        self.label_encoder = label_encoder
        
        # Normalisation des features
        X_scaled = self.scaler.fit_transform(X)
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_encoded, test_size=test_size, random_state=random_state
        )
        
        if model_type == 'xgboost':
            self.model = self._train_xgboost(X_train, y_train, X_test, y_test)
        elif model_type == 'random_forest':
            self.model = self._train_random_forest(X_train, y_train, X_test, y_test)
        elif model_type == 'isolation_forest':
            self.model = self._train_isolation_forest(X_train, y_train, X_test, y_test)
        else:
            raise ValueError("Type de modèle non supporté")
        
        # Évaluation
        self._evaluate_model(X_test, y_test)
        
        # Importance des features
        self._calculate_feature_importance(X.columns)
        
        self.is_trained = True
        _logger.info("Modèle de détection de stress entraîné avec succès!")
    
    def _train_xgboost(self, X_train, y_train, X_test, y_test):
        """Entraîne un modèle XGBoost pour la classification"""
        
        params = {
            'n_estimators': 1000,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
            'n_jobs': -1,
            'objective': 'multi:softprob',
            'num_class': len(np.unique(y_train))
        }
        
        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)
        
        return model
    
    def _train_random_forest(self, X_train, y_train, X_test, y_test):
        """Entraîne un modèle Random Forest"""
        
        params = {
            'n_estimators': 500,
            'max_depth': 10,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': 42,
            'n_jobs': -1
        }
        
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        
        return model
    
    def _train_isolation_forest(self, X_train, y_train, X_test, y_test):
        """Entraîne un modèle Isolation Forest pour détecter les anomalies"""
        
        # Isolation Forest pour détecter les stress (anomalies)
        model = IsolationForest(
            contamination=0.1,  # 10% d'anomalies attendues
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train)
        
        return model
    
    def _evaluate_model(self, X_test, y_test):
        """Évalue les performances du modèle"""
        
        if self.model_type == 'isolation_forest':
            # Pour Isolation Forest, on prédit les anomalies
            predictions = self.model.predict(X_test)
            anomaly_scores = self.model.decision_function(X_test)
            
            # Conversion en classification binaire (stress/no stress)
            y_pred_binary = np.where(predictions == -1, 'stress', 'aucun')
            y_test_binary = np.where(y_test == 'aucun', 'aucun', 'stress')
            
            accuracy = accuracy_score(y_test_binary, y_pred_binary)
            
            self.training_metrics = {
                'accuracy': accuracy,
                'anomaly_scores_mean': np.mean(anomaly_scores),
                'anomaly_scores_std': np.std(anomaly_scores)
            }
        else:
            # Pour les modèles de classification standard
            y_pred = self.model.predict(X_test)
            y_pred_proba = self.model.predict_proba(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            
            class_report = classification_report(
                y_test, y_pred, 
                output_dict=True
            )
            
            self.training_metrics = {
                'accuracy': accuracy,
                'classification_report': class_report
            }
        
        _logger.info(f"Précision du modèle: {accuracy:.3f}")
    
    def _calculate_feature_importance(self, feature_names):
        """Calcule l'importance des features"""
        
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
        else:
            self.feature_importance = None
    
    def detect_stress(self, conditions, return_probabilities=True):
        """
        Détecte les stress dans les conditions données
        
        Args:
            conditions: DataFrame avec conditions actuelles
            return_probabilities: Retourner les probabilités
            
        Returns:
            stress_info: Informations sur les stress détectés
        """
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant de détecter les stress")
        
        # Normalisation des conditions
        conditions_scaled = self.scaler.transform(conditions)
        
        if self.model_type == 'isolation_forest':
            # Détection d'anomalies
            anomaly_score = self.model.decision_function(conditions_scaled)[0]
            is_anomaly = self.model.predict(conditions_scaled)[0] == -1
            
            if is_anomaly:
                # Analyse détaillée des stress possibles
                stress_types = self._analyze_stress_types(conditions)
                primary_stress = max(stress_types, key=stress_types.get)
                
                stress_info = {
                    'has_stress': True,
                    'primary_stress': primary_stress,
                    'stress_description': self.stress_types[primary_stress],
                    'anomaly_score': float(anomaly_score),
                    'confidence': min(100, max(0, abs(anomaly_score) * 50)),
                    'all_stress_types': stress_types
                }
            else:
                stress_info = {
                    'has_stress': False,
                    'primary_stress': 'aucun',
                    'stress_description': self.stress_types['aucun'],
                    'anomaly_score': float(anomaly_score),
                    'confidence': 100,
                    'all_stress_types': {'aucun': 100}
                }
        else:
            # Classification standard
            predictions = self.model.predict(conditions_scaled)
            probabilities = self.model.predict_proba(conditions_scaled) if return_probabilities else None
            
            primary_stress = predictions[0]
            confidence = max(probabilities[0]) * 100 if probabilities is not None else 100
            
            stress_info = {
                'has_stress': primary_stress != 'aucun',
                'primary_stress': primary_stress,
                'stress_description': self.stress_types.get(primary_stress, 'Stress inconnu'),
                'confidence': float(confidence),
                'all_probabilities': dict(zip(self.model.classes_, probabilities[0])) if probabilities is not None else {}
            }
        
        return stress_info
    
    def _analyze_stress_types(self, conditions):
        """
        Analyse détaillée des types de stress possibles
        
        Args:
            conditions: Conditions actuelles
            
        Returns:
            dict: Types de stress avec scores
        """
        stress_scores = {}
        
        # Stress hydrique
        if 'precipitation_7j' in conditions.columns and 'humidite_sol' in conditions.columns:
            precip = conditions['precipitation_7j'].iloc[0]
            humidity = conditions['humidite_sol'].iloc[0]
            
            if precip < self.stress_thresholds['hydrique']['precipitation_7j'] or \
               humidity < self.stress_thresholds['hydrique']['humidite_sol']:
                stress_scores['hydrique'] = 100 - min(100, (precip + humidity) / 2)
            else:
                stress_scores['hydrique'] = 0
        
        # Stress thermique
        if 'temperature_max' in conditions.columns and 'temperature_min' in conditions.columns:
            temp_max = conditions['temperature_max'].iloc[0]
            temp_min = conditions['temperature_min'].iloc[0]
            amplitude = temp_max - temp_min
            
            if temp_max > self.stress_thresholds['thermique']['temperature_max']:
                stress_scores['chaleur'] = min(100, (temp_max - 35) * 5)
            elif temp_min < self.stress_thresholds['thermique']['temperature_min']:
                stress_scores['gel'] = min(100, (0 - temp_min) * 10)
            elif amplitude > self.stress_thresholds['thermique']['amplitude_thermique']:
                stress_scores['thermique'] = min(100, (amplitude - 20) * 2)
            else:
                stress_scores['thermique'] = 0
        
        # Stress nutritionnel
        if 'azote_sol' in conditions.columns and 'phosphore_sol' in conditions.columns:
            azote = conditions['azote_sol'].iloc[0]
            phosphore = conditions['phosphore_sol'].iloc[0]
            
            if azote < self.stress_thresholds['nutritionnel']['azote_sol'] or \
               phosphore < self.stress_thresholds['nutritionnel']['phosphore_sol']:
                stress_scores['nutritionnel'] = 100 - min(100, (azote + phosphore) / 2)
            else:
                stress_scores['nutritionnel'] = 0
        
        # Stress de pH
        if 'ph_sol' in conditions.columns:
            ph = conditions['ph_sol'].iloc[0]
            if ph < 5.5 or ph > 8.5:
                stress_scores['ph'] = min(100, abs(ph - 7) * 20)
            else:
                stress_scores['ph'] = 0
        
        # Si aucun stress détecté
        if not stress_scores or max(stress_scores.values()) < 30:
            stress_scores['aucun'] = 100
        
        return stress_scores
    
    def get_stress_recommendations(self, stress_type):
        """
        Retourne les recommandations pour un type de stress
        
        Args:
            stress_type: Type de stress détecté
            
        Returns:
            dict: Recommandations d'action
        """
        recommendations = {
            'hydrique': {
                'action': 'Irrigation d\'urgence',
                'description': 'Augmenter l\'irrigation et surveiller l\'humidité du sol',
                'priority': 'haute',
                'measures': [
                    'Irriguer immédiatement',
                    'Vérifier le système d\'irrigation',
                    'Surveiller l\'humidité du sol',
                    'Considérer le paillage pour retenir l\'humidité'
                ]
            },
            'thermique': {
                'action': 'Protection thermique',
                'description': 'Protéger les cultures des températures extrêmes',
                'priority': 'haute',
                'measures': [
                    'Installer des ombrières',
                    'Utiliser des couvertures thermiques',
                    'Irriguer pour rafraîchir',
                    'Surveiller les prévisions météo'
                ]
            },
            'chaleur': {
                'action': 'Protection contre la chaleur',
                'description': 'Protéger les cultures de la chaleur excessive',
                'priority': 'haute',
                'measures': [
                    'Augmenter l\'irrigation',
                    'Installer des ombrières',
                    'Pulvériser de l\'eau sur les feuilles',
                    'Surveiller les signes de brûlure'
                ]
            },
            'gel': {
                'action': 'Protection contre le gel',
                'description': 'Protéger les cultures du gel',
                'priority': 'critique',
                'measures': [
                    'Installer des chauffages',
                    'Utiliser des couvertures thermiques',
                    'Irriguer avant le gel',
                    'Surveiller les températures nocturnes'
                ]
            },
            'nutritionnel': {
                'action': 'Fertilisation',
                'description': 'Apporter les nutriments manquants',
                'priority': 'moyenne',
                'measures': [
                    'Analyser le sol',
                    'Appliquer les engrais appropriés',
                    'Surveiller l\'état des feuilles',
                    'Planifier la fertilisation future'
                ]
            },
            'ph': {
                'action': 'Correction du pH',
                'description': 'Corriger l\'acidité ou l\'alcalinité du sol',
                'priority': 'moyenne',
                'measures': [
                    'Analyser le pH du sol',
                    'Appliquer de la chaux (si acide)',
                    'Appliquer du soufre (si alcalin)',
                    'Surveiller l\'évolution du pH'
                ]
            },
            'aucun': {
                'action': 'Surveillance continue',
                'description': 'Aucune action immédiate requise',
                'priority': 'faible',
                'measures': [
                    'Continuer la surveillance',
                    'Maintenir les bonnes pratiques',
                    'Préparer les prochaines interventions'
                ]
            }
        }
        
        return recommendations.get(stress_type, recommendations['aucun'])
    
    def get_stress_history(self, data, window_days=30):
        """
        Analyse l'historique des stress sur une période
        
        Args:
            data: DataFrame avec données historiques
            window_days: Fenêtre d'analyse en jours
            
        Returns:
            dict: Analyse de l'historique des stress
        """
        if 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
            recent_data = data[data['date'] >= data['date'].max() - timedelta(days=window_days)]
        else:
            recent_data = data.tail(window_days)
        
        stress_history = []
        
        for _, row in recent_data.iterrows():
            stress_info = self.detect_stress(row.to_frame().T, return_probabilities=False)
            stress_history.append({
                'date': row.get('date', 'Unknown'),
                'stress_type': stress_info['primary_stress'],
                'confidence': stress_info['confidence'],
                'has_stress': stress_info['has_stress']
            })
        
        # Statistiques
        total_days = len(stress_history)
        stress_days = sum(1 for s in stress_history if s['has_stress'])
        stress_frequency = (stress_days / total_days) * 100 if total_days > 0 else 0
        
        # Types de stress les plus fréquents
        stress_types = [s['stress_type'] for s in stress_history if s['has_stress']]
        stress_counts = pd.Series(stress_types).value_counts()
        
        return {
            'total_days': total_days,
            'stress_days': stress_days,
            'stress_frequency': stress_frequency,
            'most_common_stress': stress_counts.index[0] if len(stress_counts) > 0 else 'aucun',
            'stress_distribution': stress_counts.to_dict(),
            'recent_stress': stress_history[-7:] if len(stress_history) >= 7 else stress_history
        }
    
    def get_feature_importance(self, top_n=10):
        """
        Retourne l'importance des features
        
        Args:
            top_n: Nombre de features à retourner
            
        Returns:
            DataFrame avec les features les plus importantes
        """
        if self.feature_importance is None:
            return None
        
        return self.feature_importance.head(top_n)
    
    def save_model(self, filepath):
        """
        Sauvegarde le modèle entraîné
        
        Args:
            filepath: Chemin de sauvegarde
        """
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant d'être sauvegardé")
        
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'scaler': self.scaler,
            'feature_importance': self.feature_importance,
            'training_metrics': self.training_metrics,
            'stress_types': self.stress_types,
            'stress_thresholds': self.stress_thresholds,
            'is_trained': self.is_trained,
            'timestamp': datetime.now().isoformat()
        }
        
        joblib.dump(model_data, filepath)
        _logger.info(f"Modèle de détection de stress sauvegardé: {filepath}")
    
    def load_model(self, filepath):
        """
        Charge un modèle sauvegardé
        
        Args:
            filepath: Chemin du modèle
        """
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.model_type = model_data['model_type']
        self.scaler = model_data['scaler']
        self.feature_importance = model_data['feature_importance']
        self.training_metrics = model_data['training_metrics']
        self.stress_types = model_data['stress_types']
        self.stress_thresholds = model_data['stress_thresholds']
        self.is_trained = model_data['is_trained']
        
        _logger.info(f"Modèle de détection de stress chargé: {filepath}")
    
    def get_model_info(self):
        """
        Retourne les informations du modèle
        
        Returns:
            dict: Informations du modèle
        """
        return {
            'model_type': self.model_type,
            'is_trained': self.is_trained,
            'training_accuracy': self.training_metrics.get('accuracy', 0),
            'feature_count': len(self.feature_importance) if self.feature_importance is not None else 0,
            'stress_types_supported': list(self.stress_types.keys()),
            'top_features': self.get_feature_importance(5).to_dict('records') if self.feature_importance is not None else []
        }
