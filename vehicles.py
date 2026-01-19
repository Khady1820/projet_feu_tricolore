"""
Module de gestion des véhicules
Animation et comportement des voitures avec Turtle
"""

import turtle
import random


class Vehicle:
    """Représentation et animation d'un véhicule"""
    
    # Compteur de classe pour générer des IDs uniques
    compteur_id = 0
    
    def __init__(self, x, y, direction, logger, scenario_config):
        """
        Initialise un véhicule
        
        Args:
            x (float): Position X initiale
            y (float): Position Y initiale
            direction (str): 'horizontal' ou 'vertical'
            logger (Logger): Instance du logger
            scenario_config (dict): Configuration du scénario actuel
        """
        # ID unique pour chaque voiture
        Vehicle.compteur_id += 1
        self.id = Vehicle.compteur_id
        
        # Position et direction
        self.x = x
        self.y = y
        self.direction = direction
        
        # Vitesse et accélération
        self.vitesse = scenario_config['vitesse_normale']
        self.vitesse_max = scenario_config['vitesse_normale']
        self.acceleration = scenario_config['acceleration']
        self.deceleration = scenario_config['deceleration']
        
        # Logger pour journalisation
        self.logger = logger
        
        # État
        self.actif = True
        self.arretee = False
        
        # Création du turtle pour la voiture
        self.turtle = turtle.Turtle()
        self.turtle.shape("square")
        self.turtle.shapesize(0.8, 1.5)
        self.turtle.color(self._couleur_aleatoire())
        self.turtle.penup()
        self.turtle.goto(x, y)

        
        # Orientation selon la direction
        if direction == 'horizontal':
            self.turtle.setheading(0)  # Vers la droite
        else:
            self.turtle.setheading(90)  # Vers le haut
        
        print(f"🚗 Voiture #{self.id} créée à ({x}, {y}) - Direction: {direction}")
    
    def _couleur_aleatoire(self):
        """
        Génère une couleur aléatoire pour la voiture
        
        Returns:
            str: Nom de la couleur
        """
        couleurs = [
            'blue', 'purple', 'brown', 'pink', 
            'cyan', 'magenta', 'navy', 'teal',
            'maroon', 'olive', 'coral', 'tomato'
        ]
        return random.choice(couleurs)
    
    def avancer(self):
        """Fait avancer la voiture selon sa vitesse et direction"""
        if self.vitesse > 0:
            if self.direction == 'horizontal':
                self.x += self.vitesse
                self.turtle.goto(self.x, self.y)
            else:  # vertical
                self.y += self.vitesse
                self.turtle.goto(self.x, self.y)
    
    def arreter(self):
        """Arrête progressivement la voiture (freinage)"""
        if self.vitesse > 0:
            self.vitesse = max(0, self.vitesse - self.deceleration)
            
            # Journaliser seulement quand la voiture s'arrête complètement
            if self.vitesse == 0 and not self.arretee:
                self.arretee = True
                self.logger.log_arret_voiture(
                    self.id,
                    self.x,
                    self.y
                )
    
    def demarrer(self):
        """Redémarre progressivement la voiture (accélération)"""
        if self.vitesse < self.vitesse_max:
            # Journaliser au premier démarrage
            if self.vitesse == 0:
                self.logger.log_demarrage_voiture(
                    self.id,
                    self.x,
                    self.y,
                    self.vitesse
                )
                self.arretee = False
            
            self.vitesse = min(self.vitesse_max, self.vitesse + self.acceleration)
    
    def ralentir(self):
        """Ralentit la voiture (feu orange)"""
        if self.vitesse > self.vitesse_max * 0.5:
            self.vitesse = max(self.vitesse_max * 0.5, self.vitesse - self.deceleration * 0.5)
    
    def est_avant_feu(self, position_feu, marge=30):
        """
        Vérifie si la voiture est avant le feu tricolore
        
        Args:
            position_feu (float): Position du feu sur l'axe concerné
            marge (int): Distance de détection avant le feu
            
        Returns:
            bool: True si la voiture est dans la zone avant le feu
        """
        if self.direction == 'horizontal':
            return self.x < position_feu and self.x > position_feu - marge
        else:  # vertical
            return self.y < position_feu and self.y > position_feu - marge
    
    def est_hors_ecran(self, limite=400):
        """
        Vérifie si la voiture est sortie de l'écran
        
        Args:
            limite (int): Limite de l'écran en pixels
            
        Returns:
            bool: True si hors écran
        """
        return abs(self.x) > limite or abs(self.y) > limite
    
    def detruire(self):
        """Supprime la voiture de l'écran et la désactive"""
        self.turtle.hideturtle()
        self.actif = False
        print(f"🗑️  Voiture #{self.id} supprimée (hors écran)")
    
    def get_position(self):
        """
        Retourne la position actuelle
        
        Returns:
            tuple: (x, y)
        """
        return (self.x, self.y)
    
    def get_vitesse(self):
        """
        Retourne la vitesse actuelle
        
        Returns:
            float: Vitesse
        """
        return self.vitesse
    
    def __str__(self):
        """Représentation textuelle de la voiture"""
        return f"Voiture #{self.id} [{self.direction}] à ({int(self.x)}, {int(self.y)}) - Vitesse: {self.vitesse:.1f}"
    
    def __repr__(self):
        """Représentation pour debug"""
        return f"Vehicle(id={self.id}, pos=({self.x:.1f}, {self.y:.1f}), v={self.vitesse:.1f}, dir='{self.direction}')"


class VehicleManager:
    """Gestionnaire de flotte de véhicules"""
    
    def __init__(self, logger):
        """
        Initialise le gestionnaire
        
        Args:
            logger (Logger): Instance du logger
        """
        self.logger = logger
        self.voitures = []
    
    def ajouter_voiture(self, x, y, direction, scenario_config):
        """
        Ajoute une nouvelle voiture
        
        Args:
            x (float): Position X
            y (float): Position Y
            direction (str): Direction de la voiture
            scenario_config (dict): Configuration du scénario
            
        Returns:
            Vehicle: La voiture créée
        """
        voiture = Vehicle(x, y, direction, self.logger, scenario_config)
        self.voitures.append(voiture)
        
        self.logger.log_creation_voiture(
            voiture.id,
            voiture.x,
            voiture.y,
            voiture.vitesse
        )
        
        return voiture
    
    def supprimer_voiture(self, voiture):
        """
        Supprime une voiture de la flotte
        
        Args:
            voiture (Vehicle): Voiture à supprimer
        """
        if voiture in self.voitures:
            voiture.detruire()
            self.voitures.remove(voiture)
    
    def nettoyer_voitures_inactives(self):
        """Supprime toutes les voitures inactives ou hors écran"""
        for voiture in self.voitures[:]:
            if not voiture.actif or voiture.est_hors_ecran():
                self.supprimer_voiture(voiture)
    
    def get_nombre_voitures(self):
        """
        Retourne le nombre de voitures actives
        
        Returns:
            int: Nombre de voitures
        """
        return len([v for v in self.voitures if v.actif])
    
    def detruire_toutes(self):
        """Détruit toutes les voitures"""
        for voiture in self.voitures[:]:
            voiture.detruire()
        self.voitures.clear()
        print("🗑️  Toutes les voitures ont été supprimées")


# Test du module
if __name__ == "__main__":
    from logger import Logger
    import time
    
    print("\n🧪 Test du module vehicles")
    print("=" * 60)
    
    # Créer un logger de test
    logger = Logger()
    
    # Configuration de test
    config_test = {
        'vitesse_normale': 3.0,
        'acceleration': 0.5,
        'deceleration': 0.8
    }
    
    # Initialiser l'écran Turtle
    screen = turtle.Screen()
    screen.setup(width=600, height=600)
    screen.title("Test Vehicles")
    screen.bgcolor("lightgray")
    screen.tracer(0)
    
    print("\n1️⃣ Création de voitures de test:")
    
    # Créer quelques voitures
    voiture1 = Vehicle(-200, 0, 'horizontal', logger, config_test)
    voiture2 = Vehicle(0, -200, 'vertical', logger, config_test)
    
    print(f"\n   {voiture1}")
    print(f"   {voiture2}")
    
    print("\n2️⃣ Simulation de mouvement (5 secondes):")
    print("   Les voitures vont avancer...")
    
    # Simuler le mouvement
    for i in range(50):
        voiture1.avancer()
        voiture2.avancer()
        screen.update()
        time.sleep(0.1)
    
    print(f"\n   Voiture 1 après mouvement: {voiture1}")
    print(f"   Voiture 2 après mouvement: {voiture2}")
    
    print("\n3️⃣ Test arrêt et redémarrage:")
    
    # Test arrêt
    for i in range(5):
        voiture1.arreter()
        print(f"   Freinage {i+1}: vitesse = {voiture1.vitesse:.2f}")
    
    # Test redémarrage
    for i in range(10):
        voiture1.demarrer()
        print(f"   Accélération {i+1}: vitesse = {voiture1.vitesse:.2f}")
    
    print("\n4️⃣ Nettoyage:")
    voiture1.detruire()
    voiture2.detruire()
    
    print("\n" + "=" * 60)
    print("✅ Test terminé - Fermez la fenêtre Turtle pour continuer")
    
    screen.mainloop()