"""
Contrôleur pour les calculs NPSH (Net Positive Suction Head)
"""
import math

class NPSHCalculator:
    def __init__(self, fluid_model, pipe_model):
        self.fluid = fluid_model
        self.pipe = pipe_model
        self.g = 9.81
        self.Patm = 101325  # Pa
    
    def set_atmospheric_pressure(self, Patm):
        """Définit la pression atmosphérique"""
        self.Patm = Patm
    
    def calculate_patm_from_altitude(self, altitude):
        """Calcule la pression atmosphérique depuis l'altitude"""
        Patm = 101325 * (1 - 0.0065 * altitude / 288.15) ** 5.255
        self.Patm = Patm
        return Patm
    
    def calculate_aspiration_losses(self, Q, D, f, Kasp=None, e=None, 
                                    loss_method='Coefficients'):
        """Calcule les pertes de charge à l'aspiration"""
        if loss_method == 'Coefficients' and Kasp is not None:
            Dhasp = (8 / (self.g * math.pi**2 * D**4)) * \
                    (f * self.pipe.L_aspiration / D + Kasp) * Q**2
        elif loss_method == 'Pourcentage' and e is not None:
            Dhasp = (8 / (self.g * math.pi**2 * D**4)) * \
                    (f * self.pipe.L_aspiration / D + e * (f * self.pipe.L_aspiration / D)) * Q**2
        else:
            raise ValueError("Méthode ou paramètres invalides")
        
        return Dhasp
    
    def calculate_NPSHa(self, Q, D, f, Zs=0, Kasp=None, e=None, 
                       loss_method='Coefficients'):
        """Calcule le NPSH disponible (NPSHa)"""
        # Pertes à l'aspiration
        Dhasp = self.calculate_aspiration_losses(Q, D, f, Kasp, e, loss_method)
        
        # NPSHa = (Patm - Pv)/(rho*g) + Zs - Dhasp
        NPSHa = ((self.Patm - self.fluid.vapor_pressure) / 
                (self.fluid.density * self.g)) + Zs - Dhasp
        
        return NPSHa
    
    def check_cavitation(self, NPSHa, NPSHr, margin=0.5):
        """Vérifie si la cavitation est évitée"""
        return NPSHa >= (NPSHr + margin)
    
    def get_npsh_margin(self, NPSHa, NPSHr):
        """Retourne la marge de sécurité NPSH"""
        return NPSHa - NPSHr