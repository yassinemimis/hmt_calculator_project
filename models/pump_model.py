"""
Modèle de données pour la pompe
"""
import numpy as np

class PumpModel:
    def __init__(self, pump_type, nombre, Qp, Hp, np_vals, NPSH):
        self.type = pump_type
        self.nombre = nombre
        # ✅ تحويل مباشر إلى numpy array
        self.Qp = np.array(Qp) if not isinstance(Qp, np.ndarray) else Qp
        self.Hp = np.array(Hp) if not isinstance(Hp, np.ndarray) else Hp
        self.np = np.array(np_vals) if not isinstance(np_vals, np.ndarray) else np_vals
        self.NPSH = np.array(NPSH) if not isinstance(NPSH, np.ndarray) else NPSH
    
    @classmethod
    def from_json(cls, data):
        """Crée une pompe depuis un dictionnaire JSON"""
        return cls(
            pump_type=data['type'],
            nombre=data['nombre'],
            Qp=data['Qp'],
            Hp=data['Hp'],
            np_vals=data['np'],  # ✅ Correction: np est un mot-clé Python
            NPSH=data['NPSH']
        )
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'type': self.type,
            'nombre': self.nombre,
            'Qp': self.Qp.tolist() if isinstance(self.Qp, np.ndarray) else self.Qp,
            'Hp': self.Hp.tolist() if isinstance(self.Hp, np.ndarray) else self.Hp,
            'np': self.np.tolist() if isinstance(self.np, np.ndarray) else self.np,
            'NPSH': self.NPSH.tolist() if isinstance(self.NPSH, np.ndarray) else self.NPSH
        }
    
    def get_max_efficiency_point(self):
        """Retourne le point de rendement maximal"""
        idx_max = np.argmax(self.np)
        return {
            'Qp': float(self.Qp[idx_max]),
            'Hp': float(self.Hp[idx_max]),
            'np': float(self.np[idx_max]),
            'NPSH': float(self.NPSH[idx_max]),
            'index': int(idx_max)
        }
    
    def __repr__(self):
        return f"PumpModel(type='{self.type}', nombre={self.nombre}, points={len(self.Qp)})"