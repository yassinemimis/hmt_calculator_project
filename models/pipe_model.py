"""
Modèle de données pour la conduite
"""

class PipeModel:
    def __init__(self):
        self.L_aspiration = 10.0   # m
        self.L_refoulement = 50.0  # m
        self.Z_depart = 0.0        # m  (cote surface libre aspiration)
        self.Z_arrivee = 20.0      # m  (cote surface libre refoulement)
        self.Z_pompe = 2.0         # m  (cote axe de pompe)
        self.diameter = 0.2        # m

    @property
    def L_total(self):
        return self.L_aspiration + self.L_refoulement

    @property
    def H_geometric(self):
        return self.Z_arrivee - self.Z_depart

    def to_dict(self):
        return {
            'L_aspiration': self.L_aspiration,
            'L_refoulement': self.L_refoulement,
            'Z_depart': self.Z_depart,
            'Z_arrivee': self.Z_arrivee,
            'Z_pompe': self.Z_pompe,
            'diameter': self.diameter
        }
