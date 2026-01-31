"""
Simulation de Feu Tricolore - Ville de Thiès
Application principale avec interface graphique

Projet POO2 - Licence 3 Informatique
Université Iba Der Thiam de Thiès
"""

import time
import random

# Imports des modules du projet
from database import Database
from logger import Logger
from traffic_light import TrafficLight
from scenarios import CirculationNormale, HeureDePointe, ModeNuit, ModeManuel
from vehicle_manager import VehicleManager  # ← CHANGÉ: Utiliser VehicleManager
from turtle_scene import TurtleScene
from gui import SimulationGUI

DISTANCE_SECURITE = 45  # Distance de sécurité entre les voiture
class SimulationFeuTricolore:
    """Application principale de simulation"""
    
    def __init__(self):
        """Initialise l'application complète""" 
        print("\n" + "="*60)
        print("🚦 SIMULATION FEU TRICOLORE - VILLE DE THIÈS")         
        print("="*60)
        
        # Initialisation des composants
        self.database = Database()
        self.logger = Logger(self.database)
        self.traffic_light = TrafficLight(self.logger)
        self.scenario = CirculationNormale()
        self.scene = TurtleScene()
        
        # ========== NOUVEAU: Gestionnaire de véhicules intelligents ==========
        self.vehicle_manager = VehicleManager(self.logger)
        
        # IMAGES: Images orientées automatiquement pour chaque direction
        # Après avoir lancé orienter_images.py, décommentez:
        self.vehicle_manager.definir_images_vehicules({
            'est': 'images/.gif',
            'ouest': 'images/.gif',
            'nord': 'images/v2_small2.gif',
            'sud': 'images/v2_small.gif'
        })
        # =====================================================================
        
        # Variables de simulation
        self.voitures = []  # Gardé pour compatibilité
        self.running = False
        self.paused = False
        self.temps_dernier_spawn = time.time()
        self.temps_clignotement = time.time()
        self.etat_clignotant = False
        self.index_etat_feu = 0
        self.temps_debut_etat = time.time()
        
        # Interface graphique (GUI séparée)
        self.gui = SimulationGUI(self)
        
        # Dessiner la légende sur la scène
        self.scene.dessiner_legende()
        
        # IMPORTANT: Initialiser l'affichage des feux au départ
        self.scene.actualiser_feu(self.traffic_light.etat_nord_sud, self.traffic_light.etat_est_ouest)
        self.scene.update()
        
        # Log du démarrage
        self.logger.log_initialisation(scenario=self.scenario.nom)
        
        print("\n✅ Application initialisée avec succès")
        print(f"📊 Scénario actif: {self.scenario.nom}")
        
        # CRÉER DES VOITURES INITIALES
        self.creer_voitures_initiales()
        
        # Démarrer la boucle d'animation principale (sur le thread principal)
        self.demarrer_animation_principale()
    
    def creer_voitures_initiales(self):
        """Crée quelques voitures au démarrage pour montrer le carrefour animé"""
        print("\n🚗 Création des voitures initiales...")
        config = self.scenario.get_config_voitures()
        
        # Créer 8 voitures au départ (2 par direction)
        positions = [
            # Direction EST (vient de l'ouest, va vers l'est)
            (-350, 25, 'est'),
            (-250, 25, 'est'),
            
            # Direction OUEST (vient de l'est, va vers l'ouest)
            (350, -25, 'ouest'),
            (250, -25, 'ouest'),
            
            # Direction NORD (vient du sud, va vers le nord)
            (25, -350, 'nord'),
            (25, -250, 'nord'),
            
            # Direction SUD (vient du nord, va vers le sud)
            (-25, 350, 'sud'),
            (-25, 250, 'sud'),
        ]
        
        for x, y, direction in positions:
            # ========== NOUVEAU: Utiliser VehicleManager ==========
            voiture = self.vehicle_manager.ajouter_voiture(x, y, direction, config)
            # IMPORTANT: Voitures IMMOBILES au départ
            voiture.vitesse = 0  # ✅ Changé de 2.0 à 0 - immobile jusqu'au Play
            self.voitures.append(voiture)  # Garder dans la liste pour compatibilité
            # ====================================================
            
            print(f"   🚗 Voiture #{voiture.id} créée à ({x}, {y}) - {direction} - IMMOBILE")
        
        # Mettre à jour le compteur
        self.gui.update_voitures(self.vehicle_manager.get_nombre_voitures())
        self.scene.update()
        
        print(f"✅ {self.vehicle_manager.get_nombre_voitures()} voitures créées et prêtes à rouler")
    
    def demarrer_animation_principale(self):
        """Démarre la boucle d'animation principale (appelée par ontimer)"""
        print("🎬 Boucle d'animation principale démarrée")
        # Démarrer la boucle d'animation avec ontimer
        self.animer()
    
    def animer(self):
        """Boucle d'animation principale - appelée toutes les 50ms"""
        try:
            # Gérer les voitures selon le mode
            if self.running and not self.paused:
                # Mode simulation active
                self.gerer_simulation()
            else:
                # Mode démo : juste faire bouger les voitures
                self.gerer_voitures_demo()
            
            # Rafraîchir l'écran
            self.scene.update()
            
        except Exception as e:
            print(f"⚠️ Erreur animation: {e}")
        
        # Programmer le prochain appel (50ms = 20 FPS)
        self.scene.get_screen().ontimer(self.animer, 50)
    
    def gerer_voitures_demo(self):
        """Gère les voitures en mode démo (avant Play) - IMMOBILES"""
        # ✅ Les voitures restent IMMOBILES jusqu'au clic sur "Play"
        # Ne rien faire - les voitures gardent leur vitesse = 0
        pass

    def voiture_devant(self, voiture):
        for autre in self.vehicle_manager.voitures:
            if autre == voiture or not autre.actif:
                continue

            if voiture.direction == autre.direction:
                if voiture.direction == 'est' and autre.x > voiture.x and abs(autre.y - voiture.y) < 10:
                    return autre
                if voiture.direction == 'ouest' and autre.x < voiture.x and abs(autre.y - voiture.y) < 10:
                    return autre
                if voiture.direction == 'nord' and autre.y > voiture.y and abs(autre.x - voiture.x) < 10:
                    return autre
                if voiture.direction == 'sud' and autre.y < voiture.y and abs(autre.x - voiture.x) < 10:
                    return autre
        return None   

    def creer_voiture_demo(self):
        """Crée une voiture en mode démo"""
        config = self.scenario.get_config_voitures()
        
        # Choisir aléatoirement une direction
        directions = ['est', 'ouest', 'nord', 'sud']
        direction = random.choice(directions)
        
        # Positions de spawn selon la direction
        positions_spawn = {
            'est': (-350, 25),      # Vient de l'ouest
            'ouest': (350, -25),     # Vient de l'est
            'nord': (25, -350),      # Vient du sud
            'sud': (-25, 350),       # Vient du nord
        }
        
        x, y = positions_spawn[direction]
        
        # ========== NOUVEAU: Utiliser VehicleManager ==========
        voiture = self.vehicle_manager.ajouter_voiture(x, y, direction, config)
        voiture.vitesse = 1.5
        self.voitures.append(voiture)
        # ====================================================
        
        # Mise à jour sécurisée de l'interface
        try:
            self.gui.update_voitures(self.vehicle_manager.get_nombre_voitures())
        except:
            pass  # Ignorer les erreurs si l'interface est fermée
    
    def changer_scenario(self, nom_scenario):
        """
        Change le scénario de circulation
        
        Args:
            nom_scenario (str): Nom du scénario
        """
        ancien_scenario = self.scenario.nom
        
        # Mapper le nom au scénario
        scenarios_map = {
            "Circulation Normale": CirculationNormale(),
            "Heure de Pointe": HeureDePointe(),
            "Mode Nuit": ModeNuit(),
            "Mode Manuel": ModeManuel()
        }
        
        self.scenario = scenarios_map[nom_scenario]
        
        # Afficher/masquer les contrôles manuels
        if nom_scenario == "Mode Manuel":
            self.gui.afficher_controles_manuels()
            self.traffic_light.desactiver_mode_automatique()
        else:
            self.gui.masquer_controles_manuels()
            self.traffic_light.activer_mode_automatique()
        
        # Activer le clignotant pour le mode nuit
        if nom_scenario == "Mode Nuit":
            self.traffic_light.activer_clignotant()
        
        self.logger.log_changement_scenario(ancien_scenario, nom_scenario)
        
        print(f"📊 Scénario changé: {ancien_scenario} → {nom_scenario}")
    
    def changer_feu_manuel(self, etat):
        """
        Change manuellement l'état du feu (Mode Manuel)
        
        Args:
            etat (str): État du feu (ROUGE, ORANGE, VERT)
        """
        if isinstance(self.scenario, ModeManuel) and self.running:
            # En mode manuel, changer les deux axes ensemble
            self.traffic_light.etat_nord_sud = etat
            self.traffic_light.etat_est_ouest = etat
            self.scene.actualiser_feu(etat, etat)
            try:
                self.gui.update_feu(f"NS:{etat} | EO:{etat}")
            except:
                pass
            self.scene.update()
            
            # Logger
            self.logger.log_personnalise(
                "FEU_MANUEL",
                f"Changement manuel → {etat}",
                etat_feu=etat
            )
            
            print(f"🚦 Changement manuel: {etat}")
    
    def play(self):
        """Démarre la simulation complète"""
        if not self.running:
            self.running = True
            self.paused = False
            
            # ========== NOUVEAU: Enregistrer les feux pour détection ==========
            # Les voitures pourront détecter automatiquement les feux rouges
            self.vehicle_manager.enregistrer_feux([self.traffic_light])
            # ================================================================
            
            # Mettre à jour l'interface
            try:
                self.gui.update_etat("État: En cours", "green")
                self.gui.activer_controles_simulation()
            except:
                pass
            
            self.logger.log_demarrage(scenario=self.scenario.nom)
            
            print("\n▶ Simulation démarrée")
            
            # Initialiser les variables de simulation
            self.temps_dernier_spawn = time.time()
            self.index_etat_feu = 0
            self.temps_debut_etat = time.time()
            
            # Initialiser le feu selon le scénario
            if isinstance(self.scenario, ModeNuit):
                self.traffic_light.activer_clignotant()
                self.temps_clignotement = time.time()
                self.etat_clignotant = False
            elif not isinstance(self.scenario, ModeManuel):
                # Commencer par le feu VERT pour Nord/Sud
                self.traffic_light.etat_nord_sud = TrafficLight.VERT
                self.traffic_light.etat_est_ouest = TrafficLight.ROUGE
                self.scene.actualiser_feu(TrafficLight.VERT, TrafficLight.ROUGE)
                try:
                    self.gui.update_feu("NS:VERT | EO:ROUGE")
                except:
                    pass
    
    def pause(self):
        """Met en pause la simulation"""
        self.paused = not self.paused
        
        if self.paused:
            self.gui.update_etat("État: En pause", "orange")
            self.gui.update_pause_button(True)
            self.logger.log_pause()
            print("⏸ Simulation en pause")
        else:
            self.gui.update_etat("État: En cours", "green")
            self.gui.update_pause_button(False)
            self.logger.log_reprise()
            print("▶ Simulation reprise")
    
    def stop(self):
        """Arrête la simulation"""
        self.running = False
        self.paused = False
        
        # Mettre à jour l'interface
        self.gui.update_etat("État: Arrêté", "red")
        self.gui.desactiver_controles_simulation()
        
        self.logger.log_arret()
        print("⏹ Simulation arrêtée")
    
    def reinitialiser(self):
        """Réinitialise complètement la simulation"""
        self.stop()
        
        # ========== NOUVEAU: Utiliser VehicleManager pour nettoyer ==========
        self.vehicle_manager.detruire_toutes()
        self.voitures.clear()
        # ==================================================================
        
        # Réinitialiser les feux à ROUGE partout
        self.traffic_light.etat_nord_sud = TrafficLight.ROUGE
        self.traffic_light.etat_est_ouest = TrafficLight.ROUGE
        self.scene.actualiser_feu(TrafficLight.ROUGE, TrafficLight.ROUGE)
        
        # Mettre à jour l'interface
        try:
            self.gui.update_feu(f"NS:ROUGE | EO:ROUGE")
            self.gui.update_voitures(0)
            self.gui.update_etat("État: Réinitialisé", "blue")
        except:
            pass
        
        self.logger.log_reinitialisation()
        
        self.scene.update()
        print("🔄 Simulation réinitialisée")
        
        # Recréer les voitures initiales
        self.creer_voitures_initiales()
    
    def creer_voiture(self):
        """Crée une nouvelle voiture durant la simulation"""
        config = self.scenario.get_config_voitures()
        
        # Choisir aléatoirement une direction
        directions = ['est', 'ouest', 'nord', 'sud']
        direction = random.choice(directions)
        
        # Positions de spawn selon la direction
        positions_spawn = {
            'est': (-350, 25),      # Vient de l'ouest
            'ouest': (350, -25),     # Vient de l'est
            'nord': (25, -350),      # Vient du sud
            'sud': (-25, 350),       # Vient du nord
        }
        
        x, y = positions_spawn[direction]
        
        # ========== NOUVEAU: Utiliser VehicleManager ==========
        voiture = self.vehicle_manager.ajouter_voiture(x, y, direction, config)
        self.voitures.append(voiture)
        # ====================================================
        
        # Mettre à jour le compteur dans l'interface
        self.gui.update_voitures(self.vehicle_manager.get_nombre_voitures())
        
        print(f"🚗 Voiture #{voiture.id} créée à ({voiture.x}, {voiture.y}) - Direction: {direction}")
    
    def gerer_voitures(self):
        """
        ========== NOUVELLE VERSION INTELLIGENTE ==========
        Gère le comportement des voitures avec détection automatique des dangers
        Les voitures s'arrêtent AVANT les passages piétons
        """
        # Positions des feux - Les voitures doivent s'arrêter AVANT les passages piétons
        positions_feux = {
            'est': 100,      # ✅ S'arrête avant passage piéton (125)
            'ouest': -100,   # ✅ S'arrête avant passage piéton (-125)
            'nord': 100,     # ✅ S'arrête avant passage piéton (125)
            'sud': -100,     # ✅ S'arrête avant passage piéton (-125)
        }
        
        for voiture in self.vehicle_manager.voitures[:]:
            if not voiture.actif:
                continue
            
            # Récupérer l'état du feu SPÉCIFIQUE à cette direction
            etat_feu_voiture = self.traffic_light.get_etat_pour_direction(voiture.direction)
            
            # Vérifier si la voiture est avant le feu
            position_feu = positions_feux[voiture.direction]
            
            if voiture.direction == 'est':
                est_avant_feu = voiture.x < position_feu and voiture.x > position_feu - 40
            elif voiture.direction == 'ouest':
                est_avant_feu = voiture.x > position_feu and voiture.x < position_feu + 40
            elif voiture.direction == 'nord':
                est_avant_feu = voiture.y < position_feu and voiture.y > position_feu - 40
            else:  # 'sud'
                est_avant_feu = voiture.y > position_feu and voiture.y < position_feu + 40
            
            # ========== NOUVEAU: Détection intelligente des dangers ==========
            if voiture.detection_active:
                # Détecter les dangers (collisions + feux rouges)
                dangers = voiture.detecter_danger(self.vehicle_manager.voitures, [self.traffic_light])
                
                # Comportement selon l'état du feu ET les dangers détectés
                if est_avant_feu:
                    if etat_feu_voiture == TrafficLight.ROUGE or dangers['collision_imminente']:
                        voiture.arreter()
                    elif etat_feu_voiture == TrafficLight.VERT and not dangers['collision_imminente']:
                        voiture.demarrer()
                    elif etat_feu_voiture == TrafficLight.ORANGE:
                        if voiture.vitesse > 0:
                            voiture.arreter()
                else:
                    # Après le feu, vérifier quand même les collisions
                    if dangers['collision_imminente']:
                        voiture.arreter()
                    else:
                        voiture.demarrer()
            else:
                # Mode simple (sans détection)
                if est_avant_feu:
                    if etat_feu_voiture == TrafficLight.ROUGE:
                        voiture.arreter()
                    elif etat_feu_voiture == TrafficLight.VERT:
                        voiture.demarrer()
                    elif etat_feu_voiture == TrafficLight.ORANGE:
                        if voiture.vitesse > 0:
                            voiture.arreter()
                else:
                    voiture.demarrer()
            # ================================================================
            voiture_devant = self.voiture_devant(voiture)

            if voiture_devant:
                if voiture.direction in ['est', 'ouest']:
                    distance = abs(voiture_devant.x - voiture.x)
                else:
                    distance = abs(voiture_devant.y - voiture.y)

                if distance < DISTANCE_SECURITE:
                    voiture.arreter()
                    continue
            # Faire avancer la voiture
            voiture.avancer()
             
            # Supprimer si hors écran
            if voiture.est_hors_ecran():
                self.vehicle_manager.supprimer_voiture(voiture)
                if voiture in self.voitures:
                    self.voitures.remove(voiture)
                try:
                    self.gui.update_voitures(self.vehicle_manager.get_nombre_voitures())
                except:
                    pass
    
    def gerer_simulation(self):
        """Gère la simulation complète (feu + voitures) quand Play est activé"""
        durees = self.scenario.get_durees_feu()
        config = self.scenario.get_config_voitures()
        temps_actuel = time.time()
         
        # Mode nuit (clignotant)
        if isinstance(self.scenario, ModeNuit):
            if temps_actuel - self.temps_clignotement >= 1.0:
                self.etat_clignotant = not self.etat_clignotant
                self.scene.clignoter_orange(self.etat_clignotant)
                self.temps_clignotement = temps_actuel
            
            if (temps_actuel - self.temps_dernier_spawn >= config['intervalle_spawn'] 
                and self.vehicle_manager.get_nombre_voitures() < config['nombre_max']):
                self.creer_voiture()
                self.temps_dernier_spawn = temps_actuel
            
            self.gerer_voitures()
            return
        
        # Mode manuel
        if isinstance(self.scenario, ModeManuel):
            if (temps_actuel - self.temps_dernier_spawn >= config['intervalle_spawn'] 
                and self.vehicle_manager.get_nombre_voitures() < config['nombre_max']):
                self.creer_voiture()
                self.temps_dernier_spawn = temps_actuel
            
            self.gerer_voitures()
            return
        
       # Mode automatique avec ALTERNANCE Nord/Sud <-> Est/Ouest
        cycle_complet = [
            # Phase 1 : Nord/Sud a la priorité
            ("VERT_NS", durees['vert']),      # NS=VERT, EO=ROUGE
            ("ORANGE_NS", durees['orange']),  # NS=ORANGE, EO=ROUGE
            ("ROUGE_TOUS", 1.5),              # SÉCURITÉ: Tout rouge 1.5s
            
            # Phase 2: Est/Ouest a la priorité
            ("VERT_EO", durees['vert']),      # NS=ROUGE, EO=VERT
            ("ORANGE_EO", durees['orange']),  # NS=ROUGE, EO=ORANGE
            ("ROUGE_TOUS", 1.5),              # SÉCURITÉ: Tout rouge 1.5s
            
        ]
        
        phase, duree = cycle_complet[self.index_etat_feu]

        if temps_actuel - self.temps_debut_etat >= duree:
            # Passer à l'état suivant
            self.index_etat_feu = (self.index_etat_feu + 1) % len(cycle_complet)
            phase, duree = cycle_complet[self.index_etat_feu]
            
            # Appliquer le changement selon la phase
            if phase == "VERT_NS":
                self.traffic_light.etat_nord_sud = TrafficLight.VERT
                self.traffic_light.etat_est_ouest = TrafficLight.ROUGE
                print("🟢 Nord/Sud VERT | Est/Ouest ROUGE")
            
            elif phase == "ORANGE_NS":
                self.traffic_light.etat_nord_sud = TrafficLight.ORANGE
                self.traffic_light.etat_est_ouest = TrafficLight.ROUGE
                print("🟠 Nord/Sud ORANGE | Est/Ouest ROUGE")
            
            elif phase == "VERT_EO":
                self.traffic_light.etat_nord_sud = TrafficLight.ROUGE
                self.traffic_light.etat_est_ouest = TrafficLight.VERT
                print("🔴 Nord/Sud ROUGE | Est/Ouest VERT 🟢")
            
            elif phase == "ORANGE_EO":
                self.traffic_light.etat_nord_sud = TrafficLight.ROUGE
                self.traffic_light.etat_est_ouest = TrafficLight.ORANGE
                print("🔴 Nord/Sud ROUGE | Est/Ouest ORANGE 🟠")
            
            elif phase == "ROUGE_TOUS":
                # PHASE DE SÉCURITÉ: Tout le monde s'arrête
                self.traffic_light.etat_nord_sud = TrafficLight.ROUGE
                self.traffic_light.etat_est_ouest = TrafficLight.ROUGE
                print("🔴 SÉCURITÉ: Tous les feux ROUGES 🔴")
            
            # Mettre à jour l'affichage
            self.scene.actualiser_feu(self.traffic_light.etat_nord_sud, self.traffic_light.etat_est_ouest)
            try:
                self.gui.update_feu(f"NS:{self.traffic_light.etat_nord_sud} | EO:{self.traffic_light.etat_est_ouest}")
            except:
                pass
            
            self.temps_debut_etat = temps_actuel
        
        # Création de nouvelles voitures
        if (temps_actuel - self.temps_dernier_spawn >= config['intervalle_spawn'] 
            and self.vehicle_manager.get_nombre_voitures() < config['nombre_max']):
            self.creer_voiture()
            self.temps_dernier_spawn = temps_actuel
        
        # Gérer les voitures existantes
        self.gerer_voitures()
    
    def run(self):
        """Lance l'application"""
        print("\n🚀 Lancement de l'interface utilisateur...")
        print("👁️  Les voitures sont déjà visibles sur le carrefour")
        print("▶️  Cliquez sur 'Démarrer' pour activer le feu et la simulation complète")
        print("\n🎨 IMAGES DE VÉHICULES:")
        print("   → Les voitures utiliseront des images si disponibles")
        print("   → Placez vos fichiers .gif dans le dossier 'images/'")
        print("   → Sinon, des rectangles colorés seront utilisés\n")
        self.gui.run()


# ==================== POINT D'ENTRÉE ====================
if __name__ == "__main__":
    try:
        app = SimulationFeuTricolore()
        app.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n👋 Fin de la simulation")
        print("="*60)