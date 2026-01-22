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
        
        # 4 feux (un pour chaque direction)
        self.feu_turtles = {
            'nord': {},
            'sud': {},
            'est': {},
            'ouest': {}
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
        """Dessine 4 feux tricolores (un pour chaque direction)"""
        
        # Positions des 4 feux - EN DEHORS de la route, à droite de chaque voie
        positions_feux = {
            # Voitures allant vers le NORD (montant ↑) → feu à DROITE sur le trottoir EST
            'nord': {'x': 70, 'y': -100, 'vertical': True},
            
            # Voitures allant vers le SUD (descendant ↓) → feu à DROITE sur le trottoir OUEST
            'sud': {'x': -70, 'y': 100, 'vertical': True},
            
            # Voitures allant vers l'EST (→) → feu à DROITE sur le trottoir SUD (corrigé)
            'est': {'x': -130, 'y': -70, 'vertical': False},
            
            # Voitures allant vers l'OUEST (←) → feu à DROITE sur le trottoir NORD (corrigé)
            'ouest': {'x': 130, 'y': 70, 'vertical': False}
        }
        
        for direction, pos in positions_feux.items():
            x_base = pos['x']
            y_base = pos['y']
            is_vertical = pos['vertical']
            
            # ========== POTEAU DU FEU ==========
            poteau = turtle.Turtle()
            poteau.hideturtle()
            poteau.speed(0)
            poteau.penup()
            poteau.goto(x_base, y_base - 20)
            poteau.pendown()
            poteau.color("dimgray")
            poteau.width(6)
            poteau.setheading(90)
            poteau.forward(15)
            
            # ========== BOÎTIER DU FEU ==========
            boitier = turtle.Turtle()
            boitier.hideturtle()
            boitier.speed(0)
            boitier.penup()
            
            if is_vertical:
                # Boîtier vertical (pour feux EST/OUEST)
                boitier.goto(x_base - 12, y_base)
                boitier.pendown()
                boitier.color("black")
                boitier.begin_fill()
                for _ in range(2):
                    boitier.forward(24)
                    boitier.left(90)
                    boitier.forward(75)
                    boitier.left(90)
                boitier.end_fill()
                
                # Bordure dorée
                boitier.penup()
                boitier.goto(x_base - 13, y_base - 1)
                boitier.pendown()
                boitier.color("gold")
                boitier.width(3)
                for _ in range(2):
                    boitier.forward(26)
                    boitier.left(90)
                    boitier.forward(77)
                    boitier.left(90)
                
                # Lumières verticales
                lumiere_positions = {
                    'rouge': y_base + 60,
                    'orange': y_base + 37,
                    'vert': y_base + 14
                }
                
                for couleur, y_lumiere in lumiere_positions.items():
                    lumiere = turtle.Turtle()
                    lumiere.shape("circle")
                    lumiere.shapesize(1.1)
                    lumiere.color("gray")
                    lumiere.fillcolor("gray")
                    lumiere.penup()
                    lumiere.goto(x_base, y_lumiere)
                    self.feu_turtles[direction][couleur] = lumiere
                    
            else:
                # Boîtier horizontal (pour feux NORD/SUD)
                boitier.goto(x_base, y_base - 12)
                boitier.pendown()
                boitier.color("black")
                boitier.begin_fill()
                for _ in range(2):
                    boitier.forward(75)
                    boitier.left(90)
                    boitier.forward(24)
                    boitier.left(90)
                boitier.end_fill()
                
                # Bordure dorée
                boitier.penup()
                boitier.goto(x_base - 1, y_base - 13)
                boitier.pendown()
                boitier.color("gold")
                boitier.width(3)
                for _ in range(2):
                    boitier.forward(77)
                    boitier.left(90)
                    boitier.forward(26)
                    boitier.left(90)
                
                # Lumières horizontales
                lumiere_positions = {
                    'rouge': x_base + 14,
                    'orange': x_base + 37,
                    'vert': x_base + 60
                }
                
                for couleur, x_lumiere in lumiere_positions.items():
                    lumiere = turtle.Turtle()
                    lumiere.shape("circle")
                    lumiere.shapesize(1.1)
                    lumiere.color("gray")
                    lumiere.fillcolor("gray")
                    lumiere.penup()
                    lumiere.goto(x_lumiere, y_base)
                    self.feu_turtles[direction][couleur] = lumiere
            
            # Allumer rouge par défaut
            self.feu_turtles[direction]['rouge'].color("red")
            self.feu_turtles[direction]['rouge'].fillcolor("red")
        
        print("✅ 4 feux tricolores créés - À DROITE de chaque voie:")
        print("   - NORD (↑): feu à droite (côté EST)")
        print("   - SUD (↓): feu à droite (côté OUEST)")
        print("   - EST (→): feu à droite (côté SUD)")
        print("   - OUEST (←): feu à droite (côté NORD)")
        
    
    def actualiser_feu(self, etat_ns, etat_eo=None):
        """
        Met à jour l'affichage des 4 feux avec synchronisation Nord/Sud et Est/Ouest
        
        Args:
            etat_ns (str): État des feux Nord et Sud
            etat_eo (str, optional): État des feux Est et Ouest
        """
        if etat_eo is None:
            if etat_ns == "VERT":
                etat_eo = "ROUGE"
            elif etat_ns == "ROUGE":
                etat_eo = "VERT"
            else:
                etat_eo = "ROUGE"
        
        # Éteindre toutes les lumières
        for direction in ['nord', 'sud', 'est', 'ouest']:
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
                self.feu_turtles[direction]['vert'].color("lime")
                self.feu_turtles[direction]['vert'].fillcolor("lime")
        
        # Allumer Est et Ouest avec etat_eo
        for direction in ['est', 'ouest']:
            if etat_eo == "ROUGE":
                self.feu_turtles[direction]['rouge'].color("red")
                self.feu_turtles[direction]['rouge'].fillcolor("red")
            elif etat_eo == "ORANGE":
                self.feu_turtles[direction]['orange'].color("orange")
                self.feu_turtles[direction]['orange'].fillcolor("orange")
            elif etat_eo == "VERT":
                self.feu_turtles[direction]['vert'].color("lime")
                self.feu_turtles[direction]['vert'].fillcolor("lime")
    
    def clignoter_orange(self, visible):
        """Fait clignoter les feux orange (mode nuit) sur les 4 feux"""
        if visible:
            for direction in ['nord', 'sud', 'est', 'ouest']:
                self.feu_turtles[direction]['orange'].color("orange")
                self.feu_turtles[direction]['orange'].fillcolor("orange")
        else:
            for direction in ['nord', 'sud', 'est', 'ouest']:
                self.feu_turtles[direction]['orange'].color("gray")
                self.feu_turtles[direction]['orange'].fillcolor("gray")
    
    def update(self):
        """Rafraîchit l'écran"""
        self.screen.update()
    
    def clear_screen(self):
        """Efface tout l'écran"""
        self.screen.clear()
        self.screen.bgcolor("lightgray")
    
    def get_screen(self):
        """Retourne l'objet Screen de Turtle"""
        return self.screen
    
    def fermer(self):
        """Ferme la fenêtre Turtle"""
        self.screen.bye()
    
    def ajouter_texte(self, x, y, texte, taille=12, couleur="black"):
        """Ajoute du texte sur la scène"""
        writer = turtle.Turtle()
        writer.hideturtle()
        writer.penup()
        writer.goto(x, y)
        writer.color(couleur)
        writer.write(texte, align="center", font=("Arial", taille, "bold"))
    
    def dessiner_legende(self):
        """Dessine une légende pour l'utilisateur"""
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
        
        self.ajouter_texte(-280, 300, "Feu Tricolore - Thiès", 10, "black")
        self.ajouter_texte(-280, 280, "🔴 Rouge = Arrêt", 8, "darkred")
        self.ajouter_texte(-280, 260, "🟠 Orange = Ralentir", 8, "orange")
        self.ajouter_texte(-280, 240, "🟢 Vert = Passer", 8, "darkgreen")