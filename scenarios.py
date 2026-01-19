"""
Module de gestion des scénarios de circulation
Définit les 4 scénarios selon le cahier des charges
"""

from abc import ABC, abstractmethod


class Scenario(ABC):
    """Classe abstraite pour les scénarios de circulation"""
    
    def __init__(self, nom):
        """
        Initialise un scénario
        
        Args:
            nom (str): Nom du scénario
        """
        self.nom = nom
    
    @abstractmethod
    def get_durees_feu(self):
        """
        Retourne les durées du feu tricolore
        
        Returns:
            dict: Dictionnaire avec clés 'vert', 'orange', 'rouge' (en secondes)
        """
        pass
    
    @abstractmethod
    def get_config_voitures(self):
        """
        Retourne la configuration des voitures
        
        Returns:
            dict: Configuration avec nombre_max, vitesse_normale, intervalle_spawn, etc.
        """
        pass
    
    def __str__(self):
        """Représentation textuelle du scénario"""
        return f"Scénario: {self.nom}"


class CirculationNormale(Scenario):
    """Scénario 1 : Circulation normale"""
    
    def __init__(self):
        super().__init__("Circulation Normale")
    
    def get_durees_feu(self):
        """
        Durées standard pour circulation normale
        
        Returns:
            dict: Vert=5s, Orange=2s, Rouge=5s
        """
        return {
            'vert': 5.0,    # 5 secondes
            'orange': 2.0,  # 2 secondes
            'rouge': 5.0    # 5 secondes
        }
    
    def get_config_voitures(self):
        """
        Configuration pour nombre modéré de voitures
        
        Returns:
            dict: Configuration de base
        """
        return {
            'nombre_max': 8,           # Nombre modéré
            'vitesse_normale': 3.0,    # Vitesse normale
            'intervalle_spawn': 3.0,   # Nouvelle voiture toutes les 3 secondes
            'acceleration': 0.5,       # Accélération progressive
            'deceleration': 0.8        # Freinage fluide
        }


class HeureDePointe(Scenario):
    """Scénario 2 : Heure de pointe"""
    
    def __init__(self):
        super().__init__("Heure de Pointe")
    
    def get_durees_feu(self):
        """
        Durées adaptées pour heure de pointe
        
        Returns:
            dict: Vert prolongé, Orange réduit, Rouge raccourci
        """
        return {
            'vert': 8.0,    # Vert prolongé (8 secondes)
            'orange': 1.5,  # Orange réduit (1.5 secondes)
            'rouge': 3.0    # Rouge raccourci (3 secondes)
        }
    
    def get_config_voitures(self):
        """
        Configuration pour trafic dense
        
        Returns:
            dict: Nombre élevé, apparition fréquente
        """
        return {
            'nombre_max': 15,          # Nombre élevé de voitures
            'vitesse_normale': 2.5,    # Vitesse légèrement réduite
            'intervalle_spawn': 1.5,   # Apparition fréquente (1.5s)
            'acceleration': 0.3,       # Démarrage plus lent
            'deceleration': 1.0        # Freinage normal
        }


class ModeNuit(Scenario):
    """Scénario 3 : Faible circulation (mode nuit)"""
    
    def __init__(self):
        super().__init__("Mode Nuit")
    
    def get_durees_feu(self):
        """
        Durées pour mode nuit (feu clignotant)
        
        Returns:
            dict: Feu orange clignotant uniquement
        """
        return {
            'vert': 0.0,     # Pas de vert
            'orange': 1.0,   # Clignotement orange (1s on/off)
            'rouge': 0.0     # Pas de rouge
        }
    
    def get_config_voitures(self):
        """
        Configuration pour faible circulation
        
        Returns:
            dict: Très peu de voitures, vitesse réduite
        """
        return {
            'nombre_max': 3,           # Très peu de voitures
            'vitesse_normale': 2.0,    # Vitesse réduite
            'intervalle_spawn': 6.0,   # Apparition rare (6 secondes)
            'acceleration': 0.4,       # Accélération normale
            'deceleration': 0.6        # Freinage doux
        }


class ModeManuel(Scenario):
    """Scénario 4 : Mode manuel"""
    
    def __init__(self):
        super().__init__("Mode Manuel")
    
    def get_durees_feu(self):
        """
        Durées pour mode manuel (changement par utilisateur)
        
        Returns:
            dict: Durées très longues car contrôle manuel
        """
        return {
            'vert': 999.0,   # Durée infinie (changement manuel uniquement)
            'orange': 999.0,
            'rouge': 999.0
        }
    
    def get_config_voitures(self):
        """
        Configuration standard pour mode manuel
        
        Returns:
            dict: Configuration normale
        """
        return {
            'nombre_max': 10,          # Nombre modéré
            'vitesse_normale': 3.0,    # Vitesse normale
            'intervalle_spawn': 2.5,   # Apparition régulière
            'acceleration': 0.5,       # Accélération normale
            'deceleration': 0.8        # Freinage normal
        }


# Fonction utilitaire pour obtenir tous les scénarios
def get_tous_scenarios():
    """
    Retourne la liste de tous les scénarios disponibles
    
    Returns:
        list: Liste des classes de scénarios
    """
    return [
        CirculationNormale,
        HeureDePointe,
        ModeNuit,
        ModeManuel
    ]


def get_scenario_par_nom(nom):
    """
    Retourne une instance de scénario par son nom
    
    Args:
        nom (str): Nom du scénario
        
    Returns:
        Scenario: Instance du scénario ou None si non trouvé
    """
    scenarios_map = {
        "Circulation Normale": CirculationNormale,
        "Heure de Pointe": HeureDePointe,
        "Mode Nuit": ModeNuit,
        "Mode Manuel": ModeManuel
    }
    
    scenario_class = scenarios_map.get(nom)
    return scenario_class() if scenario_class else None


# Test du module
if __name__ == "__main__":
    print("\n🧪 Test des scénarios de circulation")
    print("=" * 60)
    
    # Tester chaque scénario
    scenarios = [
        CirculationNormale(),
        HeureDePointe(),
        ModeNuit(),
        ModeManuel()
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}️⃣ {scenario}")
        print("-" * 60)
        
        # Afficher les durées du feu
        durees = scenario.get_durees_feu()
        print(f"   Durées du feu:")
        print(f"      🟢 Vert   : {durees['vert']}s")
        print(f"      🟠 Orange : {durees['orange']}s")
        print(f"      🔴 Rouge  : {durees['rouge']}s")
        
        # Afficher la config des voitures
        config = scenario.get_config_voitures()
        print(f"   Configuration voitures:")
        print(f"      🚗 Nombre max      : {config['nombre_max']}")
        print(f"      ⚡ Vitesse normale : {config['vitesse_normale']}")
        print(f"      ⏱️  Intervalle spawn: {config['intervalle_spawn']}s")
        print(f"      🚀 Accélération    : {config['acceleration']}")
        print(f"      🛑 Décélération    : {config['deceleration']}")
    
    # Test de la fonction utilitaire
    print("\n" + "=" * 60)
    print("🔍 Test fonction get_scenario_par_nom():")
    
    test_scenario = get_scenario_par_nom("Heure de Pointe")
    if test_scenario:
        print(f"   ✅ Scénario trouvé: {test_scenario.nom}")
    else:
        print("   ❌ Scénario non trouvé")
    
    # Liste tous les scénarios
    print("\n📋 Liste de tous les scénarios disponibles:")
    for scenario_class in get_tous_scenarios():
        instance = scenario_class()
        print(f"   • {instance.nom}")
    
    print("\n" + "=" * 60)
    print("✅ Test terminé")