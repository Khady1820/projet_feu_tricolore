"""
Module de gestion d'un véhicule individuel intelligent
Animation et comportement d'une voiture avec Turtle
Support des images et détection de dangers
"""

import turtle
import random
import os


class Vehicle:
    """Représentation et animation d'un véhicule intelligent"""
    
    # Compteur de classe pour générer des IDs uniques
    compteur_id = 0
    
    # Dictionnaire des images enregistrées (CORRIGÉ: doit être un dict, pas un set)
    images_enregistrees = {}
    
    # Liste des images disponibles
    images_disponibles = [
        "v2.gif"
    ]
    
    def __init__(self, x, y, direction, logger, scenario_config, image_path=None):
        """
        Initialise un véhicule
        
        Args:
            x (float): Position X initiale
            y (float): Position Y initiale
            direction (str): 'nord', 'sud', 'est', 'ouest'
            logger (Logger): Instance du logger
            scenario_config (dict): Configuration du scénario actuel
            image_path (str): Chemin vers l'image du véhicule (optionnel)
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
        
        # Paramètres de sécurité
        self.distance_securite = scenario_config.get('distance_securite', 50)
        self.detection_active = True
        self.en_danger = False
        
        # Création du turtle pour la voiture
        self.turtle = turtle.Turtle()
        self.turtle.penup()
        
        # Charger l'image ou utiliser une forme par défaut
        self.image_path = image_path
        
        # Si aucun chemin fourni, choisir une image aléatoire
        if image_path is None:
            image_path = random.choice(Vehicle.images_disponibles)
        
        # Charger l'image
        if self._charger_image(image_path):
            print(f"✅ Image utilisée: {image_path}")
        else:
            # Forme rectangulaire par défaut si échec
            self.turtle.shape("square")
            self.turtle.shapesize(0.8, 1.5)
            self.turtle.color(self._couleur_aleatoire())
            print(f"⚠️ Utilisation de la forme par défaut pour voiture #{self.id}")
        
        self.turtle.goto(x, y)
        
        # Orientation selon la direction (4 directions)
        if direction == 'est':  # Vient de l'ouest, va vers l'est
            self.turtle.setheading(0)  # Vers la droite
        elif direction == 'ouest':  # Vient de l'est, va vers l'ouest
            self.turtle.setheading(180)  # Vers la gauche
        elif direction == 'nord':  # Vient du sud, va vers le nord
            self.turtle.setheading(90)  # Vers le haut
        elif direction == 'sud':  # Vient du nord, va vers le bas
            self.turtle.setheading(270)  # Vers le bas
        
        print(f"🚗 Voiture #{self.id} créée à ({x}, {y}) - Direction: {direction}")
    
    def _charger_image(self, image_path):
        """
        Charge une image pour représenter le véhicule
        
        Args:
            image_path (str): Chemin vers l'image (GIF)
            
        Returns:
            bool: True si l'image a été chargée, False sinon
        """
        try:
            # Si le chemin n'existe pas, essayer dans différents dossiers
            chemins_possibles = [
                image_path,                          # Chemin direct
                os.path.join('images', image_path),  # Dans dossier images/
                os.path.join('..', 'images', image_path),  # Un niveau au-dessus
                os.path.join('.', image_path),       # Dossier courant
            ]
            
            # Chercher le fichier
            chemin_trouve = None
            for chemin in chemins_possibles:
                if os.path.exists(chemin):
                    chemin_trouve = chemin
                    break
            
            if chemin_trouve is None:
                print(f"⚠️ Image non trouvée: {image_path}")
                print(f"   Chemins testés: {chemins_possibles}")
                return False
            
            # Enregistrer la forme dans Turtle si pas déjà fait
            if chemin_trouve not in Vehicle.images_enregistrees:
                screen = turtle.Screen()
                screen.register_shape(chemin_trouve)
                Vehicle.images_enregistrees[chemin_trouve] = True
                print(f"📝 Image enregistrée: {chemin_trouve}")
            
            # Appliquer la forme
            self.turtle.shape(chemin_trouve)
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement de l'image: {e}")
            return False
    
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
    
    def detecter_danger(self, autres_voitures, feux_tricolores=None):
        """
        Détecte les dangers autour du véhicule
        
        Args:
            autres_voitures (list): Liste des autres véhicules
            feux_tricolores (list): Liste des feux tricolores (optionnel)
            
        Returns:
            dict: Informations sur les dangers détectés
        """
        dangers = {
            'collision_imminente': False,
            'feu_rouge': False,
            'distance_min': 200,
            'voiture_proche': None
        }
        
        # Détection de collision avec d'autres voitures
        for autre in autres_voitures:
            if autre.id != self.id and autre.actif:
                # Vérifier si la voiture est dans la même direction
                if autre.direction == self.direction:
                    distance = self._calculer_distance(autre)
                    
                    # Mettre à jour la distance minimale
                    if distance < dangers['distance_min']:
                        dangers['distance_min'] = distance
                        dangers['voiture_proche'] = autre
                    
                    # Vérifier si collision imminente
                    if distance < self.distance_securite:
                        # Vérifier si l'autre voiture est devant nous
                        if self._est_devant(autre):
                            dangers['collision_imminente'] = True
        
        # Détection de feux rouges
        if feux_tricolores:
            for feu in feux_tricolores:
                if self._detecter_feu_rouge(feu):
                    dangers['feu_rouge'] = True
                    break
        
        return dangers
    
    def _calculer_distance(self, autre_voiture):
        """
        Calcule la distance avec une autre voiture
        
        Args:
            autre_voiture (Vehicle): L'autre véhicule
            
        Returns:
            float: Distance entre les deux voitures
        """
        dx = self.x - autre_voiture.x
        dy = self.y - autre_voiture.y
        return (dx**2 + dy**2)**0.5
    
    def _est_devant(self, autre_voiture):
        """
        Vérifie si une autre voiture est devant nous
        
        Args:
            autre_voiture (Vehicle): L'autre véhicule
            
        Returns:
            bool: True si l'autre voiture est devant
        """
        if self.direction == 'est':
            return autre_voiture.x > self.x
        elif self.direction == 'ouest':
            return autre_voiture.x < self.x
        elif self.direction == 'nord':
            return autre_voiture.y > self.y
        elif self.direction == 'sud':
            return autre_voiture.y < self.y
        return False
    
    def _detecter_feu_rouge(self, feu):
        """
        Détecte si un feu rouge est devant
        
        Args:
            feu: Objet feu tricolore
            
        Returns:
            bool: True si feu rouge devant
        """
        try:
            # Vérifier si le feu est rouge
            if hasattr(feu, 'etat') and feu.etat == 'rouge':
                # Vérifier si on approche du feu
                if hasattr(feu, 'x') and hasattr(feu, 'y'):
                    distance_x = abs(self.x - feu.x)
                    distance_y = abs(self.y - feu.y)
                    
                    if self.direction == 'est' and self.x < feu.x and distance_x < self.distance_securite:
                        return True
                    elif self.direction == 'ouest' and self.x > feu.x and distance_x < self.distance_securite:
                        return True
                    elif self.direction == 'nord' and self.y < feu.y and distance_y < self.distance_securite:
                        return True
                    elif self.direction == 'sud' and self.y > feu.y and distance_y < self.distance_securite:
                        return True
        except:
            pass
        
        return False
    
    def reagir_aux_dangers(self, dangers):
        """
        Réagit aux dangers détectés
        
        Args:
            dangers (dict): Dictionnaire des dangers détectés
        """
        # Si collision imminente ou feu rouge, arrêter
        if dangers['collision_imminente'] or dangers['feu_rouge']:
            if not self.en_danger:
                self.en_danger = True
                if dangers['collision_imminente']:
                    print(f"⚠️ Voiture #{self.id} détecte un danger - Distance: {dangers['distance_min']:.1f}px")
                if dangers['feu_rouge']:
                    print(f"🚦 Voiture #{self.id} s'arrête au feu rouge")
            self.arreter()
        else:
            # Aucun danger, peut rouler
            if self.en_danger:
                self.en_danger = False
                print(f"✅ Voiture #{self.id} reprend sa route")
            self.demarrer()
    
    def avancer(self):
        """Fait avancer la voiture selon sa vitesse et direction"""
        if self.vitesse > 0:
            if self.direction == 'est':
                self.x += self.vitesse
                self.turtle.goto(self.x, self.y)
            elif self.direction == 'ouest':
                self.x -= self.vitesse
                self.turtle.goto(self.x, self.y)
            elif self.direction == 'nord':
                self.y += self.vitesse
                self.turtle.goto(self.x, self.y)
            elif self.direction == 'sud':
                self.y -= self.vitesse
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
        if self.direction == 'est':
            return self.x < position_feu and self.x > position_feu - marge
        elif self.direction == 'ouest':
            return self.x > position_feu and self.x < position_feu + marge
        elif self.direction == 'nord':
            return self.y < position_feu and self.y > position_feu - marge
        elif self.direction == 'sud':
            return self.y > position_feu and self.y < position_feu + marge
    
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
    
    def activer_detection(self):
        """Active la détection de dangers"""
        self.detection_active = True
    
    def desactiver_detection(self):
        """Désactive la détection de dangers"""
        self.detection_active = False
    
    def __str__(self):
        """Représentation textuelle de la voiture"""
        danger_str = " [DANGER]" if self.en_danger else ""
        return f"Voiture #{self.id} [{self.direction}] à ({int(self.x)}, {int(self.y)}) - Vitesse: {self.vitesse:.1f}{danger_str}"
    
    def __repr__(self):
        """Représentation pour debug"""
        return f"Vehicle(id={self.id}, pos=({self.x:.1f}, {self.y:.1f}), v={self.vitesse:.1f}, dir='{self.direction}')"