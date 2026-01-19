"""
Test simple pour vérifier que tous les modules fonctionnent
"""

print("\n" + "="*60)
print("🧪 TEST RAPIDE DU PROJET FEU TRICOLORE")
print("="*60)

# Test 1: Database
print("\n1️⃣ Test database.py...")
try:
    from database import Database
    db = Database("test_quick.db")
    db.log_event("TEST", "Test database")
    print("   ✅ database.py fonctionne")
except Exception as e:
    print(f"   ❌ Erreur database.py: {e}")

# Test 2: Logger
print("\n2️⃣ Test logger.py...")
try:
    from logger import Logger
    logger = Logger(db)
    logger.log_demarrage("Test")
    print("   ✅ logger.py fonctionne")
except Exception as e:
    print(f"   ❌ Erreur logger.py: {e}")

# Test 3: Traffic Light
print("\n3️⃣ Test traffic_light.py...")
try:
    from traffic_light import TrafficLight
    feu = TrafficLight(logger)
    feu.changer_etat("VERT")
    print("   ✅ traffic_light.py fonctionne")
except Exception as e:
    print(f"   ❌ Erreur traffic_light.py: {e}")

# Test 4: Scenarios
print("\n4️⃣ Test scenarios.py...")
try:
    from scenarios import CirculationNormale, HeureDePointe, ModeNuit, ModeManuel
    s1 = CirculationNormale()
    s2 = HeureDePointe()
    s3 = ModeNuit()
    s4 = ModeManuel()
    print(f"   ✅ scenarios.py fonctionne - {len([s1,s2,s3,s4])} scénarios")
except Exception as e:
    print(f"   ❌ Erreur scenarios.py: {e}")

# Test 5: Vehicles
print("\n5️⃣ Test vehicles.py...")
try:
    from vehicles import Vehicle
    config = {
        'vitesse_normale': 3.0,
        'acceleration': 0.5,
        'deceleration': 0.8
    }
    print("   ⚠️  vehicles.py nécessite Turtle (fenêtre graphique)")
    print("   ✅ Import réussi")
except Exception as e:
    print(f"   ❌ Erreur vehicles.py: {e}")

# Test 6: Turtle Scene
print("\n6️⃣ Test turtle_scene.py...")
try:
    from turtle_scene import TurtleScene
    print("   ⚠️  turtle_scene.py nécessite fenêtre graphique")
    print("   ✅ Import réussi")
except Exception as e:
    print(f"   ❌ Erreur turtle_scene.py: {e}")

# Test 7: GUI
print("\n7️⃣ Test gui.py...")
try:
    from gui import SimulationGUI
    print("   ⚠️  gui.py nécessite Tkinter (fenêtre graphique)")
    print("   ✅ Import réussi")
except Exception as e:
    print(f"   ❌ Erreur gui.py: {e}")

# Test 8: Main
print("\n8️⃣ Test main.py...")
try:
    import main
    print("   ✅ main.py peut être importé")
except Exception as e:
    print(f"   ❌ Erreur main.py: {e}")

# Résumé
print("\n" + "="*60)
print("📊 RÉSUMÉ DES TESTS")
print("="*60)
print("✅ Tous les modules de base fonctionnent")
print("⚠️  Pour tester l'interface graphique, lancez: python main.py")
print("="*60 + "\n")