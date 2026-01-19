"""
Module de gestion du feu tricolore
Gère les états et les cycles automatiques du feu
"""

from logger import Logger


class TrafficLight:
    """Gestion du feu tricolore"""
    
    # Constantes pour les états du feu
    ROUGE = "ROUGE"
    ORANGE = "ORANGE"
    VERT = "VERT"
    
    def __init__(self, logger):
        """
        Initialise le feu tricolore
        
        Args:
            logger (Logger): Instance du logger pour journalisation
        """
        self.etat_actuel = self.ROUGE
        self.logger = logger
        self.auto_mode = True  # Mode automatique par défaut
        self.running = False
        self.clignotant = False  # Pour le mode nuit
        
        # Log de l'initialisation
        self.logger.log_personnalise(
            "FEU_AUTO", 
            f"Initialisation du feu à l'état {self.etat_actuel}",
            etat_feu=self.etat_actuel
        )
    
    def changer_etat(self, nouvel_etat, manuel=False):
        """
        Change l'état du feu tricolore
        
        Args:
            nouvel_etat (str): Nouvel état (ROUGE, ORANGE, VERT)
            manuel (bool): True si changement manuel, False si automatique
            
        Returns:
            str: Le nouvel état du feu
        """
        ancien_etat = self.etat_actuel
        self.etat_actuel = nouvel_etat
        
        # Journalisation selon le mode
        if manuel:
            self.logger.log_changement_feu_manuel(ancien_etat, nouvel_etat)
        else:
            self.logger.log_changement_feu_auto(ancien_etat, nouvel_etat)
        
        print(f"🚦 Feu: {ancien_etat} → {nouvel_etat} ({'manuel' if manuel else 'auto'})")
        
        return nouvel_etat
    
    def activer_mode_automatique(self):
        """Active le mode automatique du feu"""
        self.auto_mode = True
        self.clignotant = False
        self.database.log_event(
            "SYSTEME",
            "Activation du mode automatique",
            etat_feu=self.etat_actuel
        )
        print("✅ Mode automatique activé")
    
    def desactiver_mode_automatique(self):
        """Désactive le mode automatique (mode manuel)"""
        self.auto_mode = False
        self.clignotant = False
        self.database.log_event(
            "SYSTEME",
            "Activation du mode manuel",
            etat_feu=self.etat_actuel
        )
        print("✅ Mode manuel activé")
    
    def activer_clignotant(self):
        """Active le mode clignotant (mode nuit)"""
        self.clignotant = True
        self.auto_mode = False
        self.etat_actuel = self.ORANGE
        self.database.log_event(
            "FEU_AUTO",
            "Activation du mode clignotant (mode nuit)",
            etat_feu=self.ORANGE
        )
        print("🌙 Mode clignotant activé (mode nuit)")
    
    def get_couleur_rgb(self):
        """
        Retourne la couleur RGB pour l'affichage Turtle
        
        Returns:
            str: Nom de la couleur pour Turtle
        """
        couleurs = {
            self.ROUGE: "red",
            self.ORANGE: "orange",
            self.VERT: "green"
        }
        return couleurs.get(self.etat_actuel, "gray")
    
    def est_rouge(self):
        """Vérifie si le feu est rouge"""
        return self.etat_actuel == self.ROUGE
    
    def est_orange(self):
        """Vérifie si le feu est orange"""
        return self.etat_actuel == self.ORANGE
    
    def est_vert(self):
        """Vérifie si le feu est vert"""
        return self.etat_actuel == self.VERT
    
    def get_etat(self):
        """
        Retourne l'état actuel du feu
        
        Returns:
            str: État actuel (ROUGE, ORANGE, VERT)
        """
        return self.etat_actuel
    
    def __str__(self):
        """Représentation textuelle du feu"""
        mode = "Clignotant" if self.clignotant else ("Auto" if self.auto_mode else "Manuel")
        return f"Feu Tricolore [{self.etat_actuel}] - Mode: {mode}"
    
    def __repr__(self):
        """Représentation pour debug"""
        return f"TrafficLight(etat='{self.etat_actuel}', auto={self.auto_mode}, clignotant={self.clignotant})"


# Test du module
if __name__ == "__main__":
    from database import Database
    
    # Créer une base de données de test
    db = Database("test_traffic_light.db")
    
    # Créer un feu tricolore
    feu = TrafficLight(db)
    
    print("\n🧪 Test du feu tricolore")
    print("=" * 50)
    
    # Test 1: Changement automatique
    print("\n1️⃣ Test changements automatiques:")
    feu.changer_etat(TrafficLight.VERT)
    feu.changer_etat(TrafficLight.ORANGE)
    feu.changer_etat(TrafficLight.ROUGE)
    
    # Test 2: Changement manuel
    print("\n2️⃣ Test changement manuel:")
    feu.desactiver_mode_automatique()
    feu.changer_etat(TrafficLight.VERT, manuel=True)
    
    # Test 3: Mode clignotant
    print("\n3️⃣ Test mode clignotant:")
    feu.activer_clignotant()
    
    # Test 4: Vérifications d'état
    print("\n4️⃣ Test vérifications:")
    print(f"Est rouge? {feu.est_rouge()}")
    print(f"Est orange? {feu.est_orange()}")
    print(f"Est vert? {feu.est_vert()}")
    print(f"Couleur RGB: {feu.get_couleur_rgb()}")
    
    # Affichage final
    print("\n" + "=" * 50)
    print(f"État final: {feu}")
    print(f"Debug: {repr(feu)}")
    
    # Afficher les événements
    print("\n📊 Événements enregistrés:")
    events = db.get_events_by_type("FEU_AUTO")
    for event in events[:5]:  # Afficher les 5 derniers
        print(f"  - {event[1]}: {event[3]}")
    
    print("\n✅ Test terminé")