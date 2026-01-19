"""
Module de gestion du feu tricolore
Gère les états et les cycles automatiques du feu avec coordination Nord/Sud et Est/Ouest
"""

from logger import Logger


class TrafficLight:
    """Gestion du feu tricolore avec alternance Nord/Sud et Est/Ouest"""
    
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
        # États actuels pour chaque axe
        self.etat_nord_sud = self.ROUGE
        self.etat_est_ouest = self.ROUGE
        
        self.logger = logger
        self.auto_mode = True
        self.running = False
        self.clignotant = False
        
        # Axe actuellement prioritaire (commence par Nord/Sud)
        self.axe_prioritaire = "NS"  # "NS" = Nord/Sud, "EO" = Est/Ouest
        
        # Log de l'initialisation
        self.logger.log_personnalise(
            "FEU_AUTO", 
            f"Initialisation: Nord/Sud={self.etat_nord_sud}, Est/Ouest={self.etat_est_ouest}",
            etat_feu=self.etat_nord_sud
        )
    
    def changer_etat(self, nouvel_etat, manuel=False, axe=None):
        """
        Change l'état du feu tricolore
        
        Args:
            nouvel_etat (str): Nouvel état (ROUGE, ORANGE, VERT)
            manuel (bool): True si changement manuel
            axe (str): "NS" pour Nord/Sud, "EO" pour Est/Ouest, None pour les deux
            
        Returns:
            tuple: (etat_nord_sud, etat_est_ouest)
        """
        if axe == "NS" or axe is None:
            ancien_ns = self.etat_nord_sud
            self.etat_nord_sud = nouvel_etat
            
            # Gérer l'alternance automatique
            if not manuel and self.auto_mode:
                if nouvel_etat == self.VERT:
                    self.etat_est_ouest = self.ROUGE
                    self.axe_prioritaire = "NS"
                elif nouvel_etat == self.ROUGE:
                    # Préparer le passage à Est/Ouest
                    pass
        
        if axe == "EO" or (axe is None and self.auto_mode):
            # En mode auto, inverser l'état
            if self.auto_mode and axe is None:
                if nouvel_etat == self.VERT:
                    self.etat_est_ouest = self.ROUGE
                elif nouvel_etat == self.ROUGE:
                    self.etat_est_ouest = self.VERT
            else:
                self.etat_est_ouest = nouvel_etat
        
        # Journalisation
        if manuel:
            self.logger.log_changement_feu_manuel(
                f"{ancien_ns if axe=='NS' else 'ROUGE'}", 
                nouvel_etat
            )
        else:
            action = f"Nord/Sud: {self.etat_nord_sud}, Est/Ouest: {self.etat_est_ouest}"
            self.logger.log_personnalise("FEU_AUTO", action, etat_feu=nouvel_etat)
        
        return (self.etat_nord_sud, self.etat_est_ouest)
    
    def alterner_priorite(self):
        """Alterne la priorité entre Nord/Sud et Est/Ouest"""
        if self.axe_prioritaire == "NS":
            # Passer la priorité à Est/Ouest
            self.etat_nord_sud = self.ROUGE
            self.etat_est_ouest = self.VERT
            self.axe_prioritaire = "EO"
            print("🔄 Priorité → Est/Ouest (VERT) | Nord/Sud (ROUGE)")
        else:
            # Passer la priorité à Nord/Sud
            self.etat_nord_sud = self.VERT
            self.etat_est_ouest = self.ROUGE
            self.axe_prioritaire = "NS"
            print("🔄 Priorité → Nord/Sud (VERT) | Est/Ouest (ROUGE)")
        
        return (self.etat_nord_sud, self.etat_est_ouest)
    
    def get_etat_pour_direction(self, direction):
        """
        Retourne l'état du feu pour une direction donnée
        
        Args:
            direction (str): 'horizontal' ou 'vertical'
            
        Returns:
            str: État du feu (ROUGE, ORANGE, VERT)
        """
        if direction == 'vertical':
            return self.etat_nord_sud
        else:  # horizontal
            return self.etat_est_ouest
    
    def activer_mode_automatique(self):
        """Active le mode automatique du feu"""
        self.auto_mode = True
        self.clignotant = False
        self.logger.log_personnalise(
            "SYSTEME",
            "Activation du mode automatique",
            etat_feu=self.etat_nord_sud
        )
        print("✅ Mode automatique activé")
    
    def desactiver_mode_automatique(self):
        """Désactive le mode automatique (mode manuel)"""
        self.auto_mode = False
        self.clignotant = False
        self.logger.log_personnalise(
            "SYSTEME",
            "Activation du mode manuel",
            etat_feu=self.etat_nord_sud
        )
        print("✅ Mode manuel activé")
    
    def activer_clignotant(self):
        """Active le mode clignotant (mode nuit)"""
        self.clignotant = True
        self.auto_mode = False
        self.etat_nord_sud = self.ORANGE
        self.etat_est_ouest = self.ORANGE
        self.logger.log_activation_clignotant()
        print("🌙 Mode clignotant activé (mode nuit)")
    
    def get_couleur_rgb(self):
        """
        Retourne la couleur RGB pour l'affichage Turtle
        
        Returns:
            tuple: (couleur_nord_sud, couleur_est_ouest)
        """
        couleurs = {
            self.ROUGE: "red",
            self.ORANGE: "orange",
            self.VERT: "green"
        }
        return (couleurs.get(self.etat_nord_sud, "gray"), 
                couleurs.get(self.etat_est_ouest, "gray"))
    
    def est_rouge(self, direction='vertical'):
        """Vérifie si le feu est rouge pour une direction"""
        if direction == 'vertical':
            return self.etat_nord_sud == self.ROUGE
        else:
            return self.etat_est_ouest == self.ROUGE
    
    def est_orange(self, direction='vertical'):
        """Vérifie si le feu est orange pour une direction"""
        if direction == 'vertical':
            return self.etat_nord_sud == self.ORANGE
        else:
            return self.etat_est_ouest == self.ORANGE
    
    def est_vert(self, direction='vertical'):
        """Vérifie si le feu est vert pour une direction"""
        if direction == 'vertical':
            return self.etat_nord_sud == self.VERT
        else:
            return self.etat_est_ouest == self.VERT
    
    def get_etat(self, direction='vertical'):
        """
        Retourne l'état actuel du feu pour une direction
        
        Args:
            direction (str): 'vertical' ou 'horizontal'
            
        Returns:
            str: État actuel (ROUGE, ORANGE, VERT)
        """
        if direction == 'vertical':
            return self.etat_nord_sud
        else:
            return self.etat_est_ouest
    
    def __str__(self):
        """Représentation textuelle du feu"""
        mode = "Clignotant" if self.clignotant else ("Auto" if self.auto_mode else "Manuel")
        return f"Feux Tricolores [NS: {self.etat_nord_sud} | EO: {self.etat_est_ouest}] - Mode: {mode}"
    
    def __repr__(self):
        """Représentation pour debug"""
        return f"TrafficLight(ns='{self.etat_nord_sud}', eo='{self.etat_est_ouest}', auto={self.auto_mode})"


# Test du module
if __name__ == "__main__":
    from logger import Logger
    
    # Créer un logger de test
    logger = Logger()
    
    # Créer un feu tricolore
    feu = TrafficLight(logger)
    
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
    print("\n📊 Statistiques:")
    logger.afficher_statistiques()
    
    print("\n✅ Test terminé")