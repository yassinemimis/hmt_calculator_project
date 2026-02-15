"""
Fonctions mathématiques utilitaires
"""
import math

def calculate_velocity(Q, D):
    """Calcule la vitesse d'écoulement"""
    return (4 * Q) / (math.pi * D**2)


def calculate_diameter_from_velocity(Q, V):
    """Calcule le diamètre depuis le débit et la vitesse"""
    return math.sqrt((4 * Q) / (math.pi * V))


def round_to_standard_diameter(D, standard_diameters=None):
    """Arrondit au diamètre normalisé le plus proche"""
    if standard_diameters is None:
        # Diamètres standards DN (mm)
        standard_diameters = [
            0.050, 0.065, 0.080, 0.100, 0.125, 0.150, 0.200, 0.250,
            0.300, 0.350, 0.400, 0.450, 0.500, 0.600, 0.700, 0.800,
            0.900, 1.000
        ]
    
    # Trouver le plus proche
    return min(standard_diameters, key=lambda x: abs(x - D))


def format_number(value, decimals=2):
    """Formate un nombre avec séparateurs de milliers"""
    return f"{value:,.{decimals}f}"


def percentage(value):
    """Convertit un ratio en pourcentage"""
    return value * 100