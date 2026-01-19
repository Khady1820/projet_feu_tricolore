"""
Module de gestion de la scène graphique
Dessin du carrefour, routes et feu tricolore avec Turtle
"""

import turtle


class TurtleScene:
    """Gestion de la scène graphique avec Turtle"""
    
    def __init__(self, largeur=800, hauteur=800):
        """
        Initialise la scène Turtle
        
        Args:
            largeur (int): Largeur de la fenêtre
            hauteur (int): Hauteur de la fenêtre
        """
        self.screen = turtle.Screen()
        self.screen.setup(width=largeur, height=hauteur)
        self.screen.title("Simulation Feu Tricolore - Ville de Thiès")
        self.screen.bgcolor("lightgray")
        self.screen.tracer(0)  # Désactive le rafraîchissement automatique pour performance
        
        self.feu_turtles = {
            'nord': {},    # Feu pour direction Nord
            'sud': {},     # Feu pour direction Sud
            'est': {},     # Feu pour direction Est
            'ouest': {}    # Feu pour direction Ouest
        }
        
        # Dessiner la scène
        self.dessiner_carrefour()
        self.dessiner_feux_tricolores()
        
        print("✅ Scène Turtle initialisée")
    
    def dessiner_carrefour(self):
        """Dessine le carrefour avec routes et marquages au sol"""
        drawer = turtle.Turtle()
        drawer.hideturtle()
        drawer.speed(0)
        drawer.penup()
        
        # ========== ROUTE HORIZONTALE ==========
        drawer.goto(-400, -50)
        drawer.pendown()
        drawer.color("black")
        drawer.begin_fill()
        for _ in range(2):
            drawer.forward(800)
            drawer.left(90)
            drawer.forward(100)
            drawer.left(90)
        drawer.end_fill()
        
        # ========== ROUTE VERTICALE ==========
        drawer.penup()
        drawer.goto(-50, -400)
        drawer.pendown()
        drawer.begin_fill()
        for _ in range(2):
            drawer.forward(100)
            drawer.left(90)
            drawer.forward(800)
            drawer.left(90)
        drawer.end_fill()
        
        # ========== LIGNE MÉDIANE HORIZONTALE (jaune) ==========
        drawer.penup()
        drawer.goto(-400, 0)
        drawer.setheading(0)
        drawer.pendown()
        drawer.color("yellow")
        drawer.width(3)
        
        # Ligne discontinue
        for i in range(20):
            if i % 2 == 0:
                drawer.forward(40)
            else:
                drawer.penup()
                drawer.forward(40)
                drawer.pendown()
        
        # ========== LIGNE MÉDIANE VERTICALE (jaune) ==========
        drawer.penup()
        drawer.goto(0, -400)
        drawer.setheading(90)
        drawer.pendown()
        
        for i in range(20):
            if i % 2 == 0:
                drawer.forward(40)
            else:
                drawer.penup()
                drawer.forward(40)
                drawer.pendown()
        
        # ========== MARQUAGES AU SOL (passages piétons) ==========
        drawer.penup()
        drawer.color("white")
        drawer.width(5)
        
        # Passage piéton Nord (haut de la route verticale)
        for i in range(6):
            drawer.goto(-45 + i*15, 120)
            drawer.setheading(90)
            drawer.pendown()
            drawer.forward(15)
            drawer.penup()
        
        # Passage piéton Sud (bas de la route verticale)
        for i in range(6):
            drawer.goto(-45 + i*15, -135)
            drawer.setheading(90)
            drawer.pendown()
            drawer.forward(15)
            drawer.penup()
        
        # Passage piéton Est (droite de la route horizontale)
        for i in range(6):
            drawer.goto(120, -45 + i*15)
            drawer.setheading(0)
            drawer.pendown()
            drawer.forward(15)
            drawer.penup()
        
        # Passage piéton Ouest (gauche de la route horizontale)
        for i in range(6):
            drawer.goto(-135, -45 + i*15)
            drawer.setheading(0)
            drawer.pendown()
            drawer.forward(15)
            drawer.penup()
        
        print("✅ Carrefour dessiné")
    
    def dessiner_feux_tricolores(self):
        """Dessine 4 feux tricolores bien positionnés pour chaque direction"""
        
        # Positions stratégiques des 4 feux DEVANT chaque flux de voitures
        # Format: (x_support, y_support, orientation)
        positions_feux = {
            # Feu NORD : pour voitures montant (y positif), à gauche de la route
            'nord': {'x': -60, 'y': 60, 'vertical': True},
            
            # Feu SUD : pour voitures descendant (y négatif), à droite de la route  
            'sud': {'x': 60, 'y': -140, 'vertical': True},
            
            # Feu EST : pour voitures vers la droite (x positif), en haut de la route
            'est': {'x': 120, 'y': 60, 'vertical': False},
            
            # Feu OUEST : pour voitures vers la gauche (x négatif), en bas de la route
            'ouest': {'x': -140, 'y': -60, 'vertical': False}
        }
        
        for direction, pos in positions_feux.items():
            x_base = pos['x']
            y_base = pos['y']
            is_vertical = pos['vertical']
            
            # ========== SUPPORT DU FEU ==========
            support = turtle.Turtle()
            support.hideturtle()
            support.speed(0)
            support.penup()
            
            if is_vertical:
                # Feu vertical (3 lumières empilées verticalement)
                support.goto(x_base - 12, y_base)
                support.pendown()
                support.color("black")
                support.begin_fill()
                for _ in range(2):
                    support.forward(24)
                    support.left(90)
                    support.forward(75)
                    support.left(90)
                support.end_fill()
                
                # Bordure jaune
                support.penup()
                support.goto(x_base - 13, y_base - 1)
                support.pendown()
                support.color("gold")
                support.width(2)
                for _ in range(2):
                    support.forward(26)
                    support.left(90)
                    support.forward(77)
                    support.left(90)
                
                # Créer les 3 lumières (verticales)
                positions_lumiere = {
                    'rouge': y_base + 60,   # En haut
                    'orange': y_base + 35,  # Au milieu
                    'vert': y_base + 10     # En bas
                }
                
                for couleur, y_pos in positions_lumiere.items():
                    light = turtle.Turtle()
                    light.shape("circle")
                    light.shapesize(1.0)
                    light.color("gray")
                    light.fillcolor("gray")
                    light.penup()
                    light.goto(x_base, y_pos)
                    self.feu_turtles[direction][couleur] = light
            
            else:
                # Feu horizontal (3 lumières alignées horizontalement)
                support.goto(x_base, y_base - 12)
                support.pendown()
                support.color("black")
                support.begin_fill()
                for _ in range(2):
                    support.forward(75)
                    support.left(90)
                    support.forward(24)
                    support.left(90)
                support.end_fill()
                
                # Bordure jaune
                support.penup()
                support.goto(x_base - 1, y_base - 13)
                support.pendown()
                support.color("gold")
                support.width(2)
                for _ in range(2):
                    support.forward(77)
                    support.left(90)
                    support.forward(26)
                    support.left(90)
                
                # Créer les 3 lumières (horizontales)
                positions_lumiere = {
                    'rouge': x_base + 10,    # À gauche
                    'orange': x_base + 35,   # Au milieu
                    'vert': x_base + 60      # À droite
                }
                
                for couleur, x_pos in positions_lumiere.items():
                    light = turtle.Turtle()
                    light.shape("circle")
                    light.shapesize(1.0)
                    light.color("gray")
                    light.fillcolor("gray")
                    light.penup()
                    light.goto(x_pos, y_base)
                    self.feu_turtles[direction][couleur] = light
            
            # Allumer le rouge par défaut
            self.feu_turtles[direction]['rouge'].color("red")
            self.feu_turtles[direction]['rouge'].fillcolor("red")
        
        print("✅ 4 feux tricolores repositionnés et ordonnés")
    
    def actualiser_feu(self, etat_ns, etat_eo=None):
        """
        Met à jour l'affichage des 4 feux avec gestion des priorités
        
        Args:
            etat_ns (str): État des feux Nord/Sud (ROUGE, ORANGE, VERT)
            etat_eo (str, optional): État des feux Est/Ouest. Si None, inverse de NS
        """
        # Si pas d'état spécifié pour Est/Ouest, utiliser l'inverse
        if etat_eo is None:
            if etat_ns == "VERT":
                etat_eo = "ROUGE"
            elif etat_ns == "ROUGE":
                etat_eo = "VERT"
            else:  # ORANGE
                etat_eo = "ROUGE"  # Sécurité : Est/Ouest reste rouge pendant l'orange
        
        # Réinitialiser toutes les lumières
        for direction in self.feu_turtles:
            for lumiere in self.feu_turtles[direction].values():
                lumiere.color("gray")
                lumiere.fillcolor("gray")
        
        # Allumer Nord et Sud avec etat_ns
        for direction in ['nord', 'sud']:
            if etat_ns == "ROUGE":
                self.feu_turtles[direction]['rouge'].color("red")
                self.feu_turtles[direction]['rouge'].fillcolor("red")
            elif etat_ns == "ORANGE":
                self.feu_turtles[direction]['orange'].color("orange")
                self.feu_turtles[direction]['orange'].fillcolor("orange")
            elif etat_ns == "VERT":
                self.feu_turtles[direction]['vert'].color("green")
                self.feu_turtles[direction]['vert'].fillcolor("green")
        
        # Allumer Est et Ouest avec etat_eo
        for direction in ['est', 'ouest']:
            if etat_eo == "ROUGE":
                self.feu_turtles[direction]['rouge'].color("red")
                self.feu_turtles[direction]['rouge'].fillcolor("red")
            elif etat_eo == "ORANGE":
                self.feu_turtles[direction]['orange'].color("orange")
                self.feu_turtles[direction]['orange'].fillcolor("orange")
            elif etat_eo == "VERT":
                self.feu_turtles[direction]['vert'].color("green")
                self.feu_turtles[direction]['vert'].fillcolor("green")
        
        print(f"🚦 Feux: Nord/Sud={etat_ns} | Est/Ouest={etat_eo}")
    
    def clignoter_orange(self, visible):
        """
        Fait clignoter les feux orange (mode nuit) sur les 4 feux
        
        Args:
            visible (bool): True pour allumer, False pour éteindre
        """
        if visible:
            for direction in self.feu_turtles:
                self.feu_turtles[direction]['orange'].color("orange")
                self.feu_turtles[direction]['orange'].fillcolor("orange")
        else:
            for direction in self.feu_turtles:
                self.feu_turtles[direction]['orange'].color("gray")
                self.feu_turtles[direction]['orange'].fillcolor("gray")
    
    def update(self):
        """Rafraîchit l'écran (appeler à chaque frame)"""
        self.screen.update()
    
    def clear_screen(self):
        """Efface tout l'écran"""
        self.screen.clear()
        self.screen.bgcolor("lightgray")
    
    def get_screen(self):
        """
        Retourne l'objet Screen de Turtle
        
        Returns:
            turtle.Screen: L'écran Turtle
        """
        return self.screen
    
    def fermer(self):
        """Ferme la fenêtre Turtle"""
        self.screen.bye()
    
    def ajouter_texte(self, x, y, texte, taille=12, couleur="black"):
        """
        Ajoute du texte sur la scène
        
        Args:
            x (float): Position X
            y (float): Position Y
            texte (str): Texte à afficher
            taille (int): Taille de police
            couleur (str): Couleur du texte
        """
        writer = turtle.Turtle()
        writer.hideturtle()
        writer.penup()
        writer.goto(x, y)
        writer.color(couleur)
        writer.write(texte, align="center", font=("Arial", taille, "bold"))
    
    def dessiner_legende(self):
        """Dessine une légende pour l'utilisateur"""
        # Fond blanc pour la légende
        legend_box = turtle.Turtle()
        legend_box.hideturtle()
        legend_box.speed(0)
        legend_box.penup()
        legend_box.goto(-380, 320)
        legend_box.pendown()
        legend_box.color("white")
        legend_box.begin_fill()
        for _ in range(2):
            legend_box.forward(200)
            legend_box.right(90)
            legend_box.forward(80)
            legend_box.right(90)
        legend_box.end_fill()
        
        # Bordure
        legend_box.penup()
        legend_box.goto(-380, 320)
        legend_box.pendown()
        legend_box.color("black")
        legend_box.width(2)
        for _ in range(2):
            legend_box.forward(200)
            legend_box.right(90)
            legend_box.forward(80)
            legend_box.right(90)
        
        # Texte de la légende
        self.ajouter_texte(-280, 300, "Feu Tricolore - Thiès", 10, "black")
        self.ajouter_texte(-280, 280, "🔴 Rouge = Arrêt", 8, "darkred")
        self.ajouter_texte(-280, 260, "🟠 Orange = Ralentir", 8, "orange")
        self.ajouter_texte(-280, 240, "🟢 Vert = Passer", 8, "darkgreen")


# Test du module
if __name__ == "__main__":
    import time
    
    print("\n🧪 Test du module turtle_scene")
    print("=" * 60)
    
    # Créer la scène
    print("\n1️⃣ Création de la scène...")
    scene = TurtleScene()
    
    # Ajouter une légende
    print("2️⃣ Ajout de la légende...")
    scene.dessiner_legende()
    scene.update()
    
    # Test des différents états du feu
    print("\n3️⃣ Test des états du feu:")
    
    etats = ["ROUGE", "ORANGE", "VERT"]
    
    for i in range(3):
        for etat in etats:
            print(f"   Feu: {etat}")
            scene.actualiser_feu(etat)
            scene.update()
            time.sleep(1.5)
    
    # Test du clignotement (mode nuit)
    print("\n4️⃣ Test du mode clignotant (5 secondes):")
    for i in range(10):
        scene.clignoter_orange(i % 2 == 0)
        scene.update()
        time.sleep(0.5)
    
    # Remettre au rouge
    scene.actualiser_feu("ROUGE")
    scene.update()
    
    print("\n" + "=" * 60)
    print("✅ Test terminé - Fermez la fenêtre pour continuer")
    
    # Garder la fenêtre ouverte
    scene.get_screen().mainloop()