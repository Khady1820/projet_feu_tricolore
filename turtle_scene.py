"""
Module de gestion de la scène graphique
Dessin du carrefour, routes et feu tricolore avec Turtle
STYLE: Routes larges bleues comme sur l'image de référence
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
        self.screen.bgcolor("#E8E8E8")  # Gris clair comme l'image
        self.screen.tracer(0)
        
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
        
        print("✅ Scène Turtle initialisée (Style image - Routes bleues larges)")
    
    def dessiner_carrefour(self):
        """Dessine le carrefour avec routes larges bleues et marquages"""
        drawer = turtle.Turtle()
        drawer.hideturtle()
        drawer.speed(0)
        drawer.penup()
        
        # ========== ROUTE HORIZONTALE (BLEUE) ==========
        drawer.goto(-400, -120)
        drawer.pendown()
        drawer.color("#A8C5DD")  # Bleu clair comme l'image
        drawer.begin_fill()
        for _ in range(2):
            drawer.forward(800)
            drawer.left(90)
            drawer.forward(240)  # ✅ Route très large
            drawer.left(90)
        drawer.end_fill()
        
        # ========== ROUTE VERTICALE (BLEUE) ==========
        drawer.penup()
        drawer.goto(-120, -400)
        drawer.pendown()
        drawer.begin_fill()
        for _ in range(2):
            drawer.forward(240)  # ✅ Route très large
            drawer.left(90)
            drawer.forward(800)
            drawer.left(90)
        drawer.end_fill()
        
        # ========== LIGNE MÉDIANE HORIZONTALE (jaune discontinue) ==========
        # S'arrête avant les passages piétons (au centre du carrefour)
        drawer.penup()
        drawer.goto(-400, 0)
        drawer.setheading(0)
        drawer.pendown()
        drawer.color("yellow")
        drawer.width(3)
        
        # Ligne de gauche jusqu'au carrefour
        for i in range(7):  # S'arrête à -120 (bord route verticale)
            if i % 2 == 0:
                drawer.forward(40)
            else:
                drawer.penup()
                drawer.forward(40)
                drawer.pendown()
        
        # Saut du carrefour (zone des passages piétons)
        drawer.penup()
        drawer.goto(120, 0)  # Reprend après le carrefour
        drawer.pendown()
        
        # Ligne de droite après le carrefour
        for i in range(7):
            if i % 2 == 0:
                drawer.forward(40)
            else:
                drawer.penup()
                drawer.forward(40)
                drawer.pendown()
        
        # ========== LIGNE MÉDIANE VERTICALE (jaune discontinue) ==========
        # S'arrête avant les passages piétons (au centre du carrefour)
        drawer.penup()
        drawer.goto(0, -400)
        drawer.setheading(90)
        drawer.pendown()
        
        # Ligne du bas jusqu'au carrefour
        for i in range(7):  # S'arrête à -120 (bord route horizontale)
            if i % 2 == 0:
                drawer.forward(40)
            else:
                drawer.penup()
                drawer.forward(40)
                drawer.pendown()
        
        # Saut du carrefour
        drawer.penup()
        drawer.goto(0, 120)  # Reprend après le carrefour
        drawer.pendown()
        
        # Ligne du haut après le carrefour
        for i in range(7):
            if i % 2 == 0:
                drawer.forward(40)
            else:
                drawer.penup()
                drawer.forward(40)
                drawer.pendown()
        
        # ========== BORDURES BLANCHES DES ROUTES ==========
        drawer.penup()
        drawer.color("white")
        drawer.width(3)
        
        # Bordure haute route horizontale
        drawer.goto(-400, 120)
        drawer.pendown()
        drawer.goto(400, 120)
        
        # Bordure basse route horizontale
        drawer.penup()
        drawer.goto(-400, -120)
        drawer.pendown()
        drawer.goto(400, -120)
        
        # Bordure gauche route verticale
        drawer.penup()
        drawer.goto(-120, -400)
        drawer.pendown()
        drawer.goto(-120, 400)
        
        # Bordure droite route verticale
        drawer.penup()
        drawer.goto(120, -400)
        drawer.pendown()
        drawer.goto(120, 400)
        
        # ========== PASSAGES PIÉTONS (blancs épais) - DANS LE CARRÉ ==========
        drawer.penup()
        drawer.color("white")
        drawer.width(8)
        
        # Passage piéton Nord (à l'intérieur du carrefour, juste après la bordure)
        for i in range(16):
            drawer.goto(-115 + i*15, 125)  # Changé de 220 à 125 (dans le carré)
            drawer.setheading(90)
            drawer.pendown()
            drawer.forward(30)  # Plus court
            drawer.penup()
        
        # Passage piéton Sud (à l'intérieur du carrefour)
        for i in range(16):
            drawer.goto(-115 + i*15, -155)  # Changé de -240 à -155 (dans le carré)
            drawer.setheading(90)
            drawer.pendown()
            drawer.forward(30)  # Plus court
            drawer.penup()
        
        # Passage piéton Est (à l'intérieur du carrefour)
        for i in range(16):
            drawer.goto(125, -115 + i*15)  # Changé de 220 à 125 (dans le carré)
            drawer.setheading(0)
            drawer.pendown()
            drawer.forward(30)  # Plus court
            drawer.penup()
        
        # Passage piéton Ouest (à l'intérieur du carrefour)
        for i in range(16):
            drawer.goto(-155, -115 + i*15)  # Changé de -240 à -155 (dans le carré)
            drawer.setheading(0)
            drawer.pendown()
            drawer.forward(30)  # Plus court
            drawer.penup()
        
        print("✅ Carrefour dessiné (style image - routes bleues 240px)")
    
    def dessiner_feux_tricolores(self):
        """Dessine 4 feux tricolores (aux coins du carrefour, pas au milieu)"""
        
        # Positions des 4 feux - AUX COINS comme l'image
        positions_feux = {
            # NORD : Feu VERTICAL en bas à gauche du carrefour
            'nord': {'x': -140, 'y': 130, 'vertical': True},
            
            # SUD : Feu VERTICAL en haut à droite du carrefour  
            'sud': {'x': 140, 'y': -130, 'vertical': True},
            
            # EST : Feu HORIZONTAL en haut à gauche du carrefour
            'est': {'x': 130, 'y': 140, 'vertical': False},
            
            # OUEST : Feu HORIZONTAL en bas à droite du carrefour
            'ouest': {'x': -130, 'y': -140, 'vertical': False}
        }
        
        for direction, pos in positions_feux.items():
            x_base = pos['x']
            y_base = pos['y']
            is_vertical = pos['vertical']
            
            # ========== BOÎTIER DU FEU ==========
            boitier = turtle.Turtle()
            boitier.hideturtle()
            boitier.speed(0)
            boitier.penup()
            
            if is_vertical:
                # ===== FEU VERTICAL (Nord/Sud) =====
                boitier.goto(x_base - 10, y_base - 45)
                boitier.pendown()
                boitier.color("black")
                boitier.begin_fill()
                for _ in range(2):
                    boitier.forward(20)
                    boitier.left(90)
                    boitier.forward(90)
                    boitier.left(90)
                boitier.end_fill()
                
                # Lumières verticales (Rouge en haut, Vert en bas)
                lumiere_positions = {
                    'rouge': y_base + 30,
                    'orange': y_base,
                    'vert': y_base - 30
                }
                
                for couleur, y_lumiere in lumiere_positions.items():
                    lumiere = turtle.Turtle()
                    lumiere.shape("circle")
                    lumiere.shapesize(0.8)
                    lumiere.color("gray")
                    lumiere.fillcolor("gray")
                    lumiere.penup()
                    lumiere.goto(x_base, y_lumiere)
                    self.feu_turtles[direction][couleur] = lumiere
            
            else:
                # ===== FEU HORIZONTAL (Est/Ouest) =====
                boitier.goto(x_base - 45, y_base - 10)
                boitier.pendown()
                boitier.color("black")
                boitier.begin_fill()
                for _ in range(2):
                    boitier.forward(90)
                    boitier.left(90)
                    boitier.forward(20)
                    boitier.left(90)
                boitier.end_fill()
                
                # Lumières horizontales (Rouge à gauche, Vert à droite)
                lumiere_positions = {
                    'rouge': x_base - 30,
                    'orange': x_base,
                    'vert': x_base + 30
                }
                
                for couleur, x_lumiere in lumiere_positions.items():
                    lumiere = turtle.Turtle()
                    lumiere.shape("circle")
                    lumiere.shapesize(0.8)
                    lumiere.color("gray")
                    lumiere.fillcolor("gray")
                    lumiere.penup()
                    lumiere.goto(x_lumiere, y_base)
                    self.feu_turtles[direction][couleur] = lumiere
            
            # Allumer rouge par défaut
            self.feu_turtles[direction]['rouge'].color("red")
            self.feu_turtles[direction]['rouge'].fillcolor("red")
        
        print("✅ 4 feux tricolores créés aux COINS du carrefour:")
        print("   - NORD: Vertical en bas-gauche")
        print("   - SUD: Vertical en haut-droite")
        print("   - EST: Horizontal en haut-gauche")
        print("   - OUEST: Horizontal en bas-droite")
    
    def actualiser_feu(self, etat_ns, etat_eo=None):
        """
        Met à jour l'affichage des 4 feux
        
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
        
        # Allumer Nord et Sud
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
        
        # Allumer Est et Ouest
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
        """Fait clignoter les feux orange (mode nuit)"""
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
        self.screen.bgcolor("#E8E8E8")
    
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