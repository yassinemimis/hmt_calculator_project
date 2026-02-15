"""
Modèle pour stocker une solution optimale
"""

class SolutionModel:
    def __init__(self):
        self.diameter = 0.0
        self.pump_type = ""
        self.configuration = ""  # 'Seule', 'Série', 'Parallèle', 'Mixte'
        self.n_serie = 1
        self.n_parallel = 1
        self.Qf = 0.0
        self.Hf = 0.0
        self.efficiency = 0.0
        self.NPSHr = 0.0
        self.NPSHa = 0.0
        self.NPSH_margin = 0.0
    
    @property
    def total_pumps(self):
        return self.n_serie * self.n_parallel
    
    def get_configuration_text(self):
        """Retourne le texte de configuration formaté"""
        if self.configuration == 'Seule':
            return "Pompe seule\n  └─ 1 pompe unique"
        elif self.configuration == 'Série':
            return f"Montage en série\n  └─ {self.n_serie} pompes en série"
        elif self.configuration == 'Parallèle':
            return f"Montage en parallèle\n  └─ {self.n_parallel} pompes en parallèle"
        elif self.configuration == 'Mixte':
            return (f"Montage mixte\n"
                   f"  └─ {self.n_parallel} branches en parallèle\n"
                   f"  └─ Chaque branche contient {self.n_serie} pompes en série")
        return self.configuration
    
    def to_dict(self):
        return {
            'D': self.diameter,
            'pump_type': self.pump_type,
            'config': self.configuration,
            'n_serie': self.n_serie,
            'n_parallel': self.n_parallel,
            'Qf': self.Qf,
            'Hf': self.Hf,
            'np': self.efficiency,
            'NPSHr': self.NPSHr,
            'NPSHa': self.NPSHa,
            'marge_NPSH': self.NPSH_margin
        }