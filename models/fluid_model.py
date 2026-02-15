"""
Modèle de données pour le fluide
"""

class FluidModel:
    def __init__(self):
        self.temperature = 20.0  # °C
        self.density = 1000.0    # kg/m³
        self.viscosity = 0.001   # Pa·s
        self.vapor_pressure = 2338.0  # Pa
        self.roughness = 0.00015  # m
    
    def set_water_properties(self, temp):
        """Définit les propriétés de l'eau à une température donnée"""
        self.temperature = temp
        self.density = 1000 - 0.05 * (temp - 20)  # Approximation
        self.viscosity = 0.001 * (1 - 0.03 * (temp - 20))  # Approximation
        
        # Pression de vapeur (formule d'Antoine simplifiée)
        import math
        self.vapor_pressure = math.exp(20.386 - 5132 / (temp + 273.15))
    
    def to_dict(self):
        return {
            'temperature': self.temperature,
            'density': self.density,
            'viscosity': self.viscosity,
            'vapor_pressure': self.vapor_pressure,
            'roughness': self.roughness
        }
    
    def from_dict(self, data):
        self.temperature = data.get('temperature', 20.0)
        self.density = data.get('density', 1000.0)
        self.viscosity = data.get('viscosity', 0.001)
        self.vapor_pressure = data.get('vapor_pressure', 2338.0)
        self.roughness = data.get('roughness', 0.00015)