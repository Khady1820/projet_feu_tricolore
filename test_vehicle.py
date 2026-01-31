"""
Test simple des véhicules avec images
"""

from vehicles import Vehicle
from vehicle_manager import VehicleManager
from logger import Logger
import turtle
import time


if __name__ == "__main__":
    print("\n🚗 TEST DES VÉHICULES AVEC IMAGES")
    print("=" * 60)
    
    # Créer un logger
    logger = Logger()
    
    # Configuration
    config = {
        'vitesse_normale': 3.0,
        'acceleration': 0.5,
        'deceleration': 0.8,
        'distance_securite': 80
    }
    
    # Initialiser l'écran
    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    screen.title("Test Véhicules avec Images")
    screen.bgcolor("white")
    screen.tracer(0)
    
    # Créer le gestionnaire
    manager = VehicleManager(logger)
    
    # DÉFINIR LES IMAGES PAR DIRECTION
    # Les voitures choisiront automatiquement une image aléatoire
    # Si vous voulez des images spécifiques par direction, décommentez ci-dessous:
    
    # manager.definir_images_vehicules({
    #     'est': '4x4noir.gif',
    #     'ouest': 'ambulance.gif',
    #     'nord': 'police.gif',
    #     'sud': 'toyota.gif'
    # })
    
    print("\n1️⃣ Création des voitures...")
    
    # Créer des voitures - elles utiliseront automatiquement des images aléatoires
    voiture1 = manager.ajouter_voiture(-250, 0, 'est', config)
    voiture2 = manager.ajouter_voiture(-200, 0, 'est', config)
    voiture3 = manager.ajouter_voiture(0, -200, 'nord', config)
    voiture4 = manager.ajouter_voiture(200, 0, 'ouest', config)
    voiture5 = manager.ajouter_voiture(0, 200, 'sud', config)
    
    print(f"✅ {manager.get_nombre_voitures()} voitures créées")
    
    print("\n2️⃣ Animation en cours...")
    print("   Les voitures se déplacent et évitent les collisions\n")
    
    # Animation
    for i in range(200):
        # Mise à jour intelligente
        manager.mettre_a_jour_vehicules()
        
        # Nettoyage
        if i % 20 == 0:
            manager.nettoyer_voitures_inactives()
        
        # Statistiques
        if i % 50 == 0 and i > 0:
            manager.afficher_statistiques()
        
        screen.update()
        time.sleep(0.05)
    
    print("\n3️⃣ Statistiques finales:")
    manager.afficher_statistiques()
    
    print("\n4️⃣ Nettoyage...")
    manager.detruire_toutes()
    
    print("\n" + "=" * 60)
    print("✅ Test terminé!")
    print("\n💡 Si vous voyez des rectangles colorés au lieu d'images:")
    print("   → Vos images ne sont pas trouvées")
    print("   → Vérifiez qu'elles sont en format .gif")
    print("   → Placez-les dans un dossier 'images/'")
    print("\n🎯 Fermez la fenêtre pour terminer")
    
    screen.mainloop()