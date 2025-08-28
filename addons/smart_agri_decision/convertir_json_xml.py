#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de conversion JSON vers XML Odoo
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

def convertir_json_vers_xml():
    """Convertit le fichier JSON en XML Odoo"""
    
    print("🔄 Conversion JSON vers XML Odoo...")
    
    # Lecture du fichier JSON
    with open('data/donnees_intenses.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Création de la structure XML
    root = ET.Element("odoo")
    data_element = ET.SubElement(root, "data")
    data_element.set("noupdate", "1")
    
    # Types de sol
    for soil in data['data']['types_sol']:
        record = ET.SubElement(data_element, "record")
        record.set("id", soil['id'])
        record.set("model", "smart_agri_soil_type")
        
        for key, value in soil.items():
            if key != 'id':
                field = ET.SubElement(record, "field")
                field.set("name", key)
                if isinstance(value, (int, float)):
                    field.text = str(value)
                else:
                    field.text = str(value)
    
    # Exploitations
    for exp in data['data']['exploitations']:
        record = ET.SubElement(data_element, "record")
        record.set("id", exp['id'])
        record.set("model", "smart_agri_exploitation")
        
        for key, value in exp.items():
            if key not in ['id', 'parcelles', 'cultures', 'modeles_ia', 'predictions', 'alertes']:
                field = ET.SubElement(record, "field")
                field.set("name", key)
                if key == 'date_creation':
                    field.set("eval", "time.strftime('%Y-01-01')")
                elif isinstance(value, (int, float)):
                    field.text = str(value)
                else:
                    field.text = str(value)
    
    # Parcelles
    for parc in data['data']['parcelles']:
        record = ET.SubElement(data_element, "record")
        record.set("id", parc['id'])
        record.set("model", "smart_agri_parcelle")
        
        for key, value in parc.items():
            if key not in ['id', 'culture_actuelle', 'rendement_moyen', 'qualite_sol']:
                field = ET.SubElement(record, "field")
                field.set("name", key)
                if key == 'exploitation_id':
                    field.set("ref", value)
                elif key == 'soil_type_id':
                    field.set("ref", value)
                elif isinstance(value, (int, float)):
                    field.text = str(value)
                else:
                    field.text = str(value)
    
    # Cultures
    for cult in data['data']['cultures']:
        record = ET.SubElement(data_element, "record")
        record.set("id", cult['id'])
        record.set("model", "smart_agri_culture")
        
        for key, value in cult.items():
            if key not in ['id', 'qualite']:
                field = ET.SubElement(record, "field")
                field.set("name", key)
                if key in ['exploitation_id', 'parcelle_id']:
                    field.set("ref", value)
                elif key in ['date_semis', 'date_recolte']:
                    field.set("eval", f"time.strftime('%Y-{value.split('-')[1]}-{value.split('-')[2]}')")
                elif isinstance(value, (int, float)):
                    field.text = str(value)
                else:
                    field.text = str(value)
    
    # Modèles IA
    for modele in data['data']['modeles_ia']:
        record = ET.SubElement(data_element, "record")
        record.set("id", modele['id'])
        record.set("model", "smart_agri_ai_model")
        
        for key, value in modele.items():
            if key != 'id':
                field = ET.SubElement(record, "field")
                field.set("name", key)
                if isinstance(value, (int, float)):
                    field.text = str(value)
                else:
                    field.text = str(value)
    
    # Prédictions IA
    for pred in data['data']['predictions_ia']:
        record = ET.SubElement(data_element, "record")
        record.set("id", pred['id'])
        record.set("model", "smart_agri_ia_predictions")
        
        for key, value in pred.items():
            if key not in ['id', 'precision']:
                field = ET.SubElement(record, "field")
                field.set("name", key)
                if key in ['exploitation_id', 'parcelle_id', 'culture_id']:
                    field.set("ref", value)
                elif key == 'date_prediction':
                    field.set("eval", f"time.strftime('%Y-{value.split('-')[1]}-{value.split('-')[2]}')")
                elif isinstance(value, (int, float)):
                    field.text = str(value)
                else:
                    field.text = str(value)
    
    # Simulations IA
    for sim in data['data']['simulations_ia']:
        record = ET.SubElement(data_element, "record")
        record.set("id", sim['id'])
        record.set("model", "smart_agri_ia_simulateur")
        
        for key, value in sim.items():
            if key not in ['id', 'precision']:
                field = ET.SubElement(record, "field")
                field.set("name", key)
                if key in ['exploitation_id', 'parcelle_id']:
                    field.set("ref", value)
                elif isinstance(value, (int, float)):
                    field.text = str(value)
                else:
                    field.text = str(value)
    
    # Détections de stress
    for det in data['data']['detections_stress']:
        record = ET.SubElement(data_element, "record")
        record.set("id", det['id'])
        record.set("model", "smart_agri_ia_detection_stress")
        
        for key, value in det.items():
            if key not in ['id', 'precision']:
                field = ET.SubElement(record, "field")
                field.set("name", key)
                if key in ['exploitation_id', 'parcelle_id']:
                    field.set("ref", value)
                elif key == 'date_detection':
                    field.set("eval", f"time.strftime('%Y-{value.split('-')[1]}-{value.split('-')[2]}')")
                elif isinstance(value, (int, float)):
                    field.text = str(value)
                else:
                    field.text = str(value)
    
    # Optimisations des ressources
    for opt in data['data']['optimisations_ressources']:
        record = ET.SubElement(data_element, "record")
        record.set("id", opt['id'])
        record.set("model", "smart_agri_ia_optimisation_ressources")
        
        for key, value in opt.items():
            if key not in ['id', 'precision']:
                field = ET.SubElement(record, "field")
                field.set("name", key)
                if key in ['exploitation_id', 'parcelle_id']:
                    field.set("ref", value)
                elif key == 'date_optimisation':
                    field.set("eval", f"time.strftime('%Y-{value.split('-')[1]}-{value.split('-')[2]}')")
                elif isinstance(value, (int, float)):
                    field.text = str(value)
                else:
                    field.text = str(value)
    
    # Dashboards
    for dash in data['data']['dashboards']:
        record = ET.SubElement(data_element, "record")
        record.set("id", dash['id'])
        record.set("model", "smart_agri_dashboard")
        
        for key, value in dash.items():
            if key not in ['id']:
                field = ET.SubElement(record, "field")
                field.set("name", key)
                if key == 'exploitation_id':
                    field.set("ref", value)
                elif isinstance(value, (int, float)):
                    field.text = str(value)
                else:
                    field.text = str(value)
    
    # Alertes climatiques
    for alerte in data['data']['alertes_climatiques']:
        record = ET.SubElement(data_element, "record")
        record.set("id", alerte['id'])
        record.set("model", "smart_agri_alerte_climatique")
        
        for key, value in alerte.items():
            if key not in ['id', 'precision']:
                field = ET.SubElement(record, "field")
                field.set("name", key)
                if key in ['date_debut', 'date_fin']:
                    field.set("eval", f"time.strftime('%Y-{value.split('-')[1]}-{value.split('-')[2]}')")
                elif isinstance(value, (int, float)):
                    field.text = str(value)
                else:
                    field.text = str(value)
    
    # Écriture du fichier XML
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    
    with open('data/donnees_intenses.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print("✅ Conversion terminée ! Fichier XML créé : data/donnees_intenses.xml")
    print(f"📊 Statistiques : {data['statistiques']['total_exploitations']} exploitations, {data['statistiques']['total_parcelles']} parcelles")
    print(f"🤖 IA : {data['statistiques']['total_modeles_ia']} modèles, {data['statistiques']['total_predictions']} prédictions")
    print(f"💰 ROI IA moyen : {data['statistiques']['roi_ia_moyen']}")

if __name__ == "__main__":
    convertir_json_vers_xml()
