"""
Module de gestion de l'interface graphique
Interface utilisateur avec Tkinter pour contrôler la simulation
"""

import tkinter as tk
from tkinter import ttk


class SimulationGUI:
    """Interface graphique de contrôle de la simulation"""
    
    def __init__(self, controller):
        """
        Initialise l'interface graphique
        
        Args:
            controller: Instance du contrôleur principal (SimulationFeuTricolore)
        """
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("🚦 Contrôle Simulation - Feu Tricolore Thiès")
        self.root.geometry("450x450")
        self.root.resizable(False, False)
        
        # Style
        self.setup_style()
        
        # Créer l'interface
        self.creer_interface()
        
        print("✅ Interface graphique créée")
    
    def setup_style(self):
        """Configure le style de l'interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurer les couleurs
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabelframe', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
    
    def creer_interface(self):
        """Crée tous les éléments de l'interface"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Créer les sections
        self.creer_titre(main_frame)
        self.creer_section_etat(main_frame)
        self.creer_section_scenario(main_frame)
        self.creer_section_controles(main_frame)
        self.creer_section_manuel(main_frame)
        self.creer_pied_page(main_frame)
    
    def creer_titre(self, parent):
        """Crée le titre de l'application"""
        titre_label = ttk.Label(
            parent, 
            text="🚦 Simulation Feu Tricolore", 
            font=("Arial", 18, "bold")
        )
        titre_label.grid(row=0, column=0, columnspan=2, pady=15)
    
    def creer_section_etat(self, parent):
        """Crée la section d'affichage de l'état"""
        info_frame = ttk.LabelFrame(parent, text="État de la simulation", padding="10")
        info_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Label état de la simulation
        self.label_etat = ttk.Label(
            info_frame, 
            text="État: Arrêté", 
            font=("Arial", 11, "bold"),
            foreground="red"
        )
        self.label_etat.grid(row=0, column=0, pady=3, sticky=tk.W)
        
        # Label état du feu
        self.label_feu = ttk.Label(
            info_frame, 
            text="Feu: ROUGE", 
            font=("Arial", 11)
        )
        self.label_feu.grid(row=1, column=0, pady=3, sticky=tk.W)
        
        # Label nombre de voitures
        self.label_voitures = ttk.Label(
            info_frame,
            text="Voitures: 0",
            font=("Arial", 11)
        )
        self.label_voitures.grid(row=2, column=0, pady=3, sticky=tk.W)
    
    def creer_section_scenario(self, parent):
        """Crée la section de sélection de scénario"""
        scenario_frame = ttk.LabelFrame(parent, text="Scénario", padding="10")
        scenario_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.scenario_var = tk.StringVar(value="Circulation Normale")
        scenarios = ["Circulation Normale", "Heure de Pointe", "Mode Nuit", "Mode Manuel"]
        
        self.scenario_combo = ttk.Combobox(
            scenario_frame,
            textvariable=self.scenario_var,
            values=scenarios,
            state="readonly",
            width=25,
            font=("Arial", 10)
        )
        self.scenario_combo.grid(row=0, column=0, padx=5)
        self.scenario_combo.bind("<<ComboboxSelected>>", self.on_scenario_change)
    
    def creer_section_controles(self, parent):
        """Crée la section des boutons de contrôle"""
        btn_frame = ttk.LabelFrame(parent, text="Contrôles", padding="10")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Bouton Play/Démarrer
        self.btn_play = ttk.Button(
            btn_frame, 
            text="▶ Démarrer", 
            command=self.on_play,
            width=18
        )
        self.btn_play.grid(row=0, column=0, padx=5, pady=5)
        
        # Bouton Pause
        self.btn_pause = ttk.Button(
            btn_frame, 
            text="⏸ Pause", 
            command=self.on_pause,
            width=18,
            state="disabled"
        )
        self.btn_pause.grid(row=0, column=1, padx=5, pady=5)
        
        # Bouton Stop
        self.btn_stop = ttk.Button(
            btn_frame, 
            text="⏹ Stop", 
            command=self.on_stop,
            width=18,
            state="disabled"
        )
        self.btn_stop.grid(row=1, column=0, padx=5, pady=5)
        
        # Bouton Réinitialiser
        self.btn_reset = ttk.Button(
            btn_frame, 
            text="🔄 Réinitialiser", 
            command=self.on_reset,
            width=18
        )
        self.btn_reset.grid(row=1, column=1, padx=5, pady=5)
    
    def creer_section_manuel(self, parent):
        """Crée la section de contrôle manuel du feu"""
        self.manual_frame = ttk.LabelFrame(parent, text="Contrôle Manuel du Feu", padding="10")
        self.manual_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        self.manual_frame.grid_remove()  # Caché par défaut
        
        # Bouton Rouge
        self.btn_rouge = ttk.Button(
            self.manual_frame,
            text="🔴 ROUGE",
            command=lambda: self.on_manuel_feu("ROUGE"),
            width=12
        )
        self.btn_rouge.grid(row=0, column=0, padx=3)
        
        # Bouton Orange
        self.btn_orange = ttk.Button(
            self.manual_frame,
            text="🟠 ORANGE",
            command=lambda: self.on_manuel_feu("ORANGE"),
            width=12
        )
        self.btn_orange.grid(row=0, column=1, padx=3)
        
        # Bouton Vert
        self.btn_vert = ttk.Button(
            self.manual_frame,
            text="🟢 VERT",
            command=lambda: self.on_manuel_feu("VERT"),
            width=12
        )
        self.btn_vert.grid(row=0, column=2, padx=3)
    
    def creer_pied_page(self, parent):
        """Crée le pied de page"""
        footer_label = ttk.Label(
            parent,
            text="Université Iba Der Thiam de Thiès - Licence 3 Info",
            font=("Arial", 8, "italic"),
            foreground="gray"
        )
        footer_label.grid(row=5, column=0, columnspan=2, pady=10)
    
    # ========== CALLBACKS DES BOUTONS ==========
    
    def on_play(self):
        """Callback du bouton Play"""
        if hasattr(self.controller, 'play'):
            self.controller.play()
    
    def on_pause(self):
        """Callback du bouton Pause"""
        if hasattr(self.controller, 'pause'):
            self.controller.pause()
    
    def on_stop(self):
        """Callback du bouton Stop"""
        if hasattr(self.controller, 'stop'):
            self.controller.stop()
    
    def on_reset(self):
        """Callback du bouton Réinitialiser"""
        if hasattr(self.controller, 'reinitialiser'):
            self.controller.reinitialiser()
    
    def on_scenario_change(self, event=None):
        """Callback du changement de scénario"""
        if hasattr(self.controller, 'changer_scenario'):
            self.controller.changer_scenario(self.scenario_var.get())
    
    def on_manuel_feu(self, etat):
        """Callback des boutons de contrôle manuel du feu"""
        if hasattr(self.controller, 'changer_feu_manuel'):
            self.controller.changer_feu_manuel(etat)
    
    # ========== MÉTHODES DE MISE À JOUR ==========
    
    def update_etat(self, texte, couleur="black"):
        """
        Met à jour l'affichage de l'état
        
        Args:
            texte (str): Texte à afficher
            couleur (str): Couleur du texte
        """
        self.label_etat.config(text=texte, foreground=couleur)
    
    def update_feu(self, etat):
        """
        Met à jour l'affichage de l'état du feu
        
        Args:
            etat (str): État du feu (ROUGE, ORANGE, VERT)
        """
        self.label_feu.config(text=f"Feu: {etat}")
    
    def update_voitures(self, nombre):
        """
        Met à jour le compteur de voitures
        
        Args:
            nombre (int): Nombre de voitures actives
        """
        self.label_voitures.config(text=f"Voitures: {nombre}")
    
    def activer_controles_simulation(self):
        """Active les boutons de simulation (Play désactivé, autres activés)"""
        self.btn_play.config(state="disabled")
        self.btn_pause.config(state="normal")
        self.btn_stop.config(state="normal")
        self.scenario_combo.config(state="disabled")
    
    def desactiver_controles_simulation(self):
        """Désactive les boutons de simulation (Play activé, autres désactivés)"""
        self.btn_play.config(state="normal")
        self.btn_pause.config(state="disabled", text="⏸ Pause")
        self.btn_stop.config(state="disabled")
        self.scenario_combo.config(state="readonly")
    
    def afficher_controles_manuels(self):
        """Affiche les boutons de contrôle manuel du feu"""
        self.manual_frame.grid()
    
    def masquer_controles_manuels(self):
        """Masque les boutons de contrôle manuel du feu"""
        self.manual_frame.grid_remove()
    
    def update_pause_button(self, en_pause):
        """
        Met à jour le texte du bouton pause
        
        Args:
            en_pause (bool): True si en pause, False sinon
        """
        if en_pause:
            self.btn_pause.config(text="▶ Reprendre")
        else:
            self.btn_pause.config(text="⏸ Pause")
    
    def get_scenario_selectionne(self):
        """
        Retourne le scénario sélectionné
        
        Returns:
            str: Nom du scénario
        """
        return self.scenario_var.get()
    
    def run(self):
        """Lance la boucle principale de l'interface"""
        self.root.mainloop()
    
    def get_root(self):
        """
        Retourne la fenêtre principale
        
        Returns:
            tk.Tk: Fenêtre principale
        """
        return self.root


# Test du module
if __name__ == "__main__":
    print("\n🧪 Test du module GUI")
    print("=" * 60)
    
    # Créer un contrôleur factice pour le test
    class FakeController:
        def play(self):
            print("▶ Play appelé")
        
        def pause(self):
            print("⏸ Pause appelé")
        
        def stop(self):
            print("⏹ Stop appelé")
        
        def reinitialiser(self):
            print("🔄 Réinitialiser appelé")
        
        def changer_scenario(self, scenario):
            print(f"📊 Scénario changé: {scenario}")
        
        def changer_feu_manuel(self, etat):
            print(f"🚦 Feu manuel: {etat}")
    
    # Créer le contrôleur factice
    fake_controller = FakeController()
    
    # Créer l'interface
    gui = SimulationGUI(fake_controller)
    
    # Test des mises à jour
    print("\n1️⃣ Test des mises à jour d'interface:")
    gui.update_etat("État: Test en cours", "blue")
    gui.update_feu("VERT")
    gui.update_voitures(5)
    
    print("2️⃣ Test activation contrôles:")
    gui.activer_controles_simulation()
    
    print("3️⃣ Test affichage contrôles manuels:")
    gui.afficher_controles_manuels()
    
    print("\n" + "=" * 60)
    print("✅ Interface créée - Testez les boutons")
    print("   Fermez la fenêtre pour terminer le test")
    
    # Lancer l'interface
    gui.run()