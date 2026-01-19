"""
Module de gestion de la base de données SQLite
Journalisation de tous les événements de la simulation
"""

import sqlite3
from datetime import datetime


class Database:
    """Gestion de la base de données SQLite pour la journalisation"""
    
    def __init__(self, db_name="traffic_simulation.db"):
        """
        Initialise la connexion à la base de données
        
        Args:
            db_name (str): Nom du fichier de base de données
        """
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données avec la table des événements"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Création de la table selon le schéma du projet
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evenements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                type_action TEXT NOT NULL,
                action TEXT NOT NULL,
                etat_feu TEXT,
                scenario TEXT,
                id_voiture INTEGER,
                position_x REAL,
                position_y REAL,
                vitesse REAL
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Base de données '{self.db_name}' initialisée")
    
    def log_event(self, type_action, action, etat_feu=None, scenario=None, 
                  id_voiture=None, position_x=None, position_y=None, vitesse=None):
        """
        Enregistre un événement dans la base de données
        
        Args:
            type_action (str): Type d'action (SYSTEME, FEU_AUTO, FEU_MANUEL, VOITURE)
            action (str): Description de l'action
            etat_feu (str, optional): État du feu (ROUGE, ORANGE, VERT)
            scenario (str, optional): Nom du scénario actif
            id_voiture (int, optional): Identifiant de la voiture
            position_x (float, optional): Position X de la voiture
            position_y (float, optional): Position Y de la voiture
            vitesse (float, optional): Vitesse de la voiture
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Timestamp au format demandé
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO evenements 
            (timestamp, type_action, action, etat_feu, scenario, id_voiture, 
             position_x, position_y, vitesse)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, type_action, action, etat_feu, scenario, 
              id_voiture, position_x, position_y, vitesse))
        
        conn.commit()
        conn.close()
    
    def get_all_events(self):
        """
        Récupère tous les événements de la base de données
        
        Returns:
            list: Liste de tuples contenant tous les événements
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM evenements ORDER BY timestamp DESC')
        events = cursor.fetchall()
        
        conn.close()
        return events
    
    def get_events_by_type(self, type_action):
        """
        Récupère les événements filtrés par type
        
        Args:
            type_action (str): Type d'action à filtrer
            
        Returns:
            list: Liste des événements du type spécifié
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT * FROM evenements WHERE type_action = ? ORDER BY timestamp DESC',
            (type_action,)
        )
        events = cursor.fetchall()
        
        conn.close()
        return events
    
    def clear_database(self):
        """Supprime tous les événements de la base de données"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM evenements')
        
        conn.commit()
        conn.close()
        print("🗑️ Base de données vidée")


# Test du module
if __name__ == "__main__":
    # Test de la classe Database
    db = Database("test_traffic.db")
    
    # Enregistrer quelques événements de test
    db.log_event("SYSTEME", "Test initialisation", scenario="Circulation Normale")
    db.log_event("FEU_AUTO", "Changement ROUGE -> VERT", etat_feu="VERT")
    db.log_event("VOITURE", "Création voiture", id_voiture=1, 
                 position_x=-350, position_y=25, vitesse=3.0)
    
    # Afficher tous les événements
    print("\n📊 Événements enregistrés:")
    events = db.get_all_events()
    for event in events:
        print(event)
    
    print(f"\n✅ Test terminé - {len(events)} événements enregistrés")