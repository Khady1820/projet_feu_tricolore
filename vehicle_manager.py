"""
Module de gestion de flotte de véhicules intelligents
Gestionnaire pour créer et gérer plusieurs voitures avec détection de dangers
"""

from vehicles import Vehicle


class VehicleManager:
    """Gestionnaire de flotte de véhicules intelligents"""
    
    def __init__(self, logger):
        """
        Initialise le gestionnaire
        
        Args:
            logger (Logger): Instance du logger
        """
        self.logger = logger
        self.voitures = []
        self.feux_tricolores = []
        self.images_vehicules = {}  # Dictionnaire pour stocker les chemins d'images
    
    def definir_images_vehicules(self, images_dict):
        """
        Définit les images à utiliser pour les véhicules
        
        Args:
            images_dict (dict): Dictionnaire {direction: chemin_image}
                               Par exemple: {'est': 'car_east.gif', 'ouest': 'car_west.gif'}
        """
        self.images_vehicules = images_dict
        print(f"📷 Images de véhicules configurées: {len(images_dict)} directions")
    
    def ajouter_voiture(self, x, y, direction, scenario_config, image_path=None):
        """
        Ajoute une nouvelle voiture intelligente
        
        Args:
            x (float): Position X
            y (float): Position Y
            direction (str): Direction de la voiture
            scenario_config (dict): Configuration du scénario
            image_path (str): Chemin vers l'image (optionnel, sinon utilise images_vehicules)
            
        Returns:
            Vehicle: La voiture créée
        """
        # Si pas d'image fournie, chercher dans le dictionnaire
        if image_path is None and direction in self.images_vehicules:
            image_path = self.images_vehicules[direction]
        
        voiture = Vehicle(x, y, direction, self.logger, scenario_config, image_path)
        self.voitures.append(voiture)
        
        self.logger.log_creation_voiture(
            voiture.id,
            voiture.x,
            voiture.y,
            voiture.vitesse
        )
        
        return voiture
    
    def enregistrer_feux(self, feux_tricolores):
        """
        Enregistre les feux tricolores pour la détection
        
        Args:
            feux_tricolores (list): Liste des objets feux tricolores
        """
        self.feux_tricolores = feux_tricolores
        print(f"🚦 {len(feux_tricolores)} feux tricolores enregistrés")
    
    def mettre_a_jour(self, feu):
        for v in self.vehicules[:]:
            voiture_devant = self.voiture_devant(v)
            etat = feu.etat_ns if v.direction in ["N", "S"] else feu.etat_ew

            if voiture_devant:
                v.arreter()
            elif etat == "ROUGE" and self._zone_arret(v):
                v.arreter()
            elif etat == "ORANGE" and self._zone_arret(v):
                v.ralentir()
            else:
                v.demarrer()
                v.avancer()

            if v.est_hors_ecran():
                v.t.hideturtle()
                self.vehicules.remove(v)
    
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
    
    def get_voitures_en_danger(self):
        """
        Retourne la liste des voitures en situation de danger
        
        Returns:
            list: Liste des voitures en danger
        """
        return [v for v in self.voitures if v.actif and v.en_danger]
    
    def activer_detection_tous(self):
        """Active la détection de dangers pour toutes les voitures"""
        for voiture in self.voitures:
            voiture.activer_detection()
        print("✅ Détection de dangers activée pour toutes les voitures")
    
    def desactiver_detection_tous(self):
        """Désactive la détection de dangers pour toutes les voitures"""
        for voiture in self.voitures:
            voiture.desactiver_detection()
        print("⚠️ Détection de dangers désactivée pour toutes les voitures")
    
    def detruire_toutes(self):
        """Détruit toutes les voitures"""
        for voiture in self.voitures[:]:
            voiture.detruire()
        self.voitures.clear()
        print("🗑️  Toutes les voitures ont été supprimées")
    
    def afficher_statistiques(self):
        """Affiche les statistiques de la flotte"""
        total = len(self.voitures)
        actives = self.get_nombre_voitures()
        en_danger = len(self.get_voitures_en_danger())
        
        print(f"\n📊 Statistiques de la flotte:")
        print(f"   Total voitures: {total}")
        print(f"   Voitures actives: {actives}")
        print(f"   Voitures en danger: {en_danger}")