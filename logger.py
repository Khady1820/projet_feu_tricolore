"""
Module de journalisation des événements
Wrapper autour de la base de données pour faciliter le logging
"""

from datetime import datetime
from database import Database


class Logger:
    """Gestionnaire de journalisation des événements"""
    
    # Types d'actions possibles
    TYPE_SYSTEME = "SYSTEME"
    TYPE_FEU_AUTO = "FEU_AUTO"
    TYPE_FEU_MANUEL = "FEU_MANUEL"
    TYPE_VOITURE = "VOITURE"
    TYPE_SCENARIO = "SCENARIO"
    
    def __init__(self, database=None):
        """
        Initialise le logger
        
        Args:
            database (Database, optional): Instance de la base de données
        """
        self.database = database if database else Database()
        print("✅ Logger initialisé")
    
    # ========== ÉVÉNEMENTS SYSTÈME ==========
    
    def log_demarrage(self, scenario=None):
        """
        Journalise le démarrage de la simulation
        
        Args:
            scenario (str, optional): Nom du scénario actif
        """
        self.database.log_event(
            self.TYPE_SYSTEME,
            "Démarrage de la simulation",
            scenario=scenario
        )
        print("📝 [LOG] Démarrage de la simulation")
    
    def log_pause(self):
        """Journalise la mise en pause"""
        self.database.log_event(
            self.TYPE_SYSTEME,
            "Pause de la simulation"
        )
        print("📝 [LOG] Pause")
    
    def log_reprise(self):
        """Journalise la reprise"""
        self.database.log_event(
            self.TYPE_SYSTEME,
            "Reprise de la simulation"
        )
        print("📝 [LOG] Reprise")
    
    def log_arret(self):
        """Journalise l'arrêt"""
        self.database.log_event(
            self.TYPE_SYSTEME,
            "Arrêt de la simulation"
        )
        print("📝 [LOG] Arrêt")
    
    def log_reinitialisation(self):
        """Journalise la réinitialisation"""
        self.database.log_event(
            self.TYPE_SYSTEME,
            "Réinitialisation de la simulation"
        )
        print("📝 [LOG] Réinitialisation")
    
    def log_initialisation(self, scenario=None):
        """
        Journalise l'initialisation de l'application
        
        Args:
            scenario (str, optional): Nom du scénario initial
        """
        self.database.log_event(
            self.TYPE_SYSTEME,
            "Initialisation de la simulation",
            scenario=scenario
        )
        print("📝 [LOG] Initialisation")
    
    # ========== ÉVÉNEMENTS DU FEU ==========
    
    def log_changement_feu_auto(self, ancien_etat, nouvel_etat, scenario=None):
        """
        Journalise un changement automatique du feu
        
        Args:
            ancien_etat (str): État précédent
            nouvel_etat (str): Nouvel état
            scenario (str, optional): Scénario actif
        """
        action = f"Changement automatique {ancien_etat} -> {nouvel_etat}"
        self.database.log_event(
            self.TYPE_FEU_AUTO,
            action,
            etat_feu=nouvel_etat,
            scenario=scenario
        )
        print(f"📝 [LOG] Feu auto: {ancien_etat} -> {nouvel_etat}")
    
    def log_changement_feu_manuel(self, ancien_etat, nouvel_etat, scenario=None):
        """
        Journalise un changement manuel du feu
        
        Args:
            ancien_etat (str): État précédent
            nouvel_etat (str): Nouvel état
            scenario (str, optional): Scénario actif
        """
        action = f"Changement manuel {ancien_etat} -> {nouvel_etat}"
        self.database.log_event(
            self.TYPE_FEU_MANUEL,
            action,
            etat_feu=nouvel_etat,
            scenario=scenario
        )
        print(f"📝 [LOG] Feu manuel: {ancien_etat} -> {nouvel_etat}")
    
    def log_activation_clignotant(self):
        """Journalise l'activation du mode clignotant"""
        self.database.log_event(
            self.TYPE_FEU_AUTO,
            "Activation du mode clignotant (mode nuit)",
            etat_feu="ORANGE"
        )
        print("📝 [LOG] Mode clignotant activé")
    
    # ========== ÉVÉNEMENTS DES VOITURES ==========
    
    def log_creation_voiture(self, id_voiture, x, y, vitesse, scenario=None):
        """
        Journalise la création d'une voiture
        
        Args:
            id_voiture (int): ID de la voiture
            x (float): Position X
            y (float): Position Y
            vitesse (float): Vitesse initiale
            scenario (str, optional): Scénario actif
        """
        self.database.log_event(
            self.TYPE_VOITURE,
            "Création nouvelle voiture",
            scenario=scenario,
            id_voiture=id_voiture,
            position_x=x,
            position_y=y,
            vitesse=vitesse
        )
        print(f"📝 [LOG] Voiture #{id_voiture} créée")
    
    def log_arret_voiture(self, id_voiture, x, y, etat_feu="ROUGE"):
        """
        Journalise l'arrêt d'une voiture
        
        Args:
            id_voiture (int): ID de la voiture
            x (float): Position X
            y (float): Position Y
            etat_feu (str): État du feu
        """
        self.database.log_event(
            self.TYPE_VOITURE,
            "Arrêt au feu rouge",
            etat_feu=etat_feu,
            id_voiture=id_voiture,
            position_x=round(x, 2),
            position_y=round(y, 2),
            vitesse=0.0
        )
    
    def log_demarrage_voiture(self, id_voiture, x, y, vitesse, etat_feu="VERT"):
        """
        Journalise le démarrage d'une voiture
        
        Args:
            id_voiture (int): ID de la voiture
            x (float): Position X
            y (float): Position Y
            vitesse (float): Vitesse actuelle
            etat_feu (str): État du feu
        """
        self.database.log_event(
            self.TYPE_VOITURE,
            "Redémarrage au feu vert",
            etat_feu=etat_feu,
            id_voiture=id_voiture,
            position_x=round(x, 2),
            position_y=round(y, 2),
            vitesse=vitesse
        )
    
    def log_suppression_voiture(self, id_voiture):
        """
        Journalise la suppression d'une voiture
        
        Args:
            id_voiture (int): ID de la voiture
        """
        self.database.log_event(
            self.TYPE_VOITURE,
            "Suppression voiture (hors écran)",
            id_voiture=id_voiture
        )
        print(f"📝 [LOG] Voiture #{id_voiture} supprimée")
    
    # ========== ÉVÉNEMENTS DES SCÉNARIOS ==========
    
    def log_changement_scenario(self, ancien_scenario, nouveau_scenario):
        """
        Journalise un changement de scénario
        
        Args:
            ancien_scenario (str): Nom de l'ancien scénario
            nouveau_scenario (str): Nom du nouveau scénario
        """
        action = f"Changement de scénario: {ancien_scenario} -> {nouveau_scenario}"
        self.database.log_event(
            self.TYPE_SCENARIO,
            action,
            scenario=nouveau_scenario
        )
        print(f"📝 [LOG] Scénario: {ancien_scenario} -> {nouveau_scenario}")
    
    # ========== MÉTHODES UTILITAIRES ==========
    
    def log_personnalise(self, type_action, action, **kwargs):
        """
        Journalise un événement personnalisé
        
        Args:
            type_action (str): Type d'action
            action (str): Description de l'action
            **kwargs: Paramètres additionnels (etat_feu, scenario, etc.)
        """
        self.database.log_event(type_action, action, **kwargs)
        print(f"📝 [LOG] {type_action}: {action}")
    
    def get_statistiques(self):
        """
        Retourne des statistiques sur les événements
        
        Returns:
            dict: Statistiques des événements
        """
        tous_events = self.database.get_all_events()
        
        stats = {
            'total': len(tous_events),
            'par_type': {}
        }
        
        # Compter par type
        for event in tous_events:
            type_action = event[2]  # Colonne type_action
            stats['par_type'][type_action] = stats['par_type'].get(type_action, 0) + 1
        
        return stats
    
    def afficher_statistiques(self):
        """Affiche les statistiques de journalisation"""
        stats = self.get_statistiques()
        
        print("\n" + "="*60)
        print("📊 STATISTIQUES DE JOURNALISATION")
        print("="*60)
        print(f"Total d'événements: {stats['total']}")
        print("\nRépartition par type:")
        for type_action, count in stats['par_type'].items():
            print(f"  • {type_action}: {count} événements")
        print("="*60 + "\n")
    
    def afficher_derniers_events(self, nombre=10):
        """
        Affiche les derniers événements
        
        Args:
            nombre (int): Nombre d'événements à afficher
        """
        events = self.database.get_all_events()[:nombre]
        
        print("\n" + "="*60)
        print(f"📝 DERNIERS {nombre} ÉVÉNEMENTS")
        print("="*60)
        
        for event in events:
            timestamp = event[1]
            type_action = event[2]
            action = event[3]
            print(f"[{timestamp}] {type_action}: {action}")
        
        print("="*60 + "\n")
    
    def vider_logs(self):
        """Vide tous les logs de la base de données"""
        self.database.clear_database()
        print("🗑️  Tous les logs ont été supprimés")


# Test du module
if __name__ == "__main__":
    print("\n🧪 Test du module logger")
    print("=" * 60)
    
    # Créer un logger
    logger = Logger(Database("test_logger.db"))
    
    print("\n1️⃣ Test des logs système:")
    logger.log_initialisation(scenario="Circulation Normale")
    logger.log_demarrage(scenario="Circulation Normale")
    logger.log_pause()
    logger.log_reprise()
    logger.log_arret()
    logger.log_reinitialisation()
    
    print("\n2️⃣ Test des logs du feu:")
    logger.log_changement_feu_auto("ROUGE", "VERT", "Circulation Normale")
    logger.log_changement_feu_auto("VERT", "ORANGE", "Circulation Normale")
    logger.log_changement_feu_manuel("ORANGE", "ROUGE", "Mode Manuel")
    logger.log_activation_clignotant()
    
    print("\n3️⃣ Test des logs des voitures:")
    logger.log_creation_voiture(1, -350, 25, 3.0, "Circulation Normale")
    logger.log_creation_voiture(2, 25, -350, 3.0, "Circulation Normale")
    logger.log_arret_voiture(1, -100, 25)
    logger.log_demarrage_voiture(1, -100, 25, 3.0)
    logger.log_suppression_voiture(1)
    
    print("\n4️⃣ Test des logs des scénarios:")
    logger.log_changement_scenario("Circulation Normale", "Heure de Pointe")
    logger.log_changement_scenario("Heure de Pointe", "Mode Nuit")
    
    print("\n5️⃣ Test log personnalisé:")
    logger.log_personnalise("TEST", "Événement de test", scenario="Test")
    
    print("\n6️⃣ Affichage des statistiques:")
    logger.afficher_statistiques()
    
    print("\n7️⃣ Affichage des derniers événements:")
    logger.afficher_derniers_events(5)
    
    print("\n" + "="*60)
    print("✅ Test terminé")