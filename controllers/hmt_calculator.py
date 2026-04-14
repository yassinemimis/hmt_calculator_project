"""
Contrôleur pour les calculs HMT
"""
import math
import numpy as np


class HMTCalculator:
    def __init__(self, fluid_model, pipe_model):
        self.fluid = fluid_model
        self.pipe = pipe_model
        self.g = 9.81

    def calculate_reynolds(self, velocity, diameter):
        """Calcule le nombre de Reynolds"""
        return (self.fluid.density * velocity * diameter) / self.fluid.viscosity

    def calculate_friction_factor(self, Re, D, epsilon, method='Swamee-Jain'):
        """Calcule le coefficient de frottement"""
        if Re < 2300:  # Écoulement laminaire
            return 64 / Re

        if method == 'Colebrook-White':
            f = 0.02
            for _ in range(50):
                f_new = (-2 * math.log10((epsilon / (3.7 * D)) +
                         (2.51 / (Re * math.sqrt(f)))))**-2
                if abs(f_new - f) < 1e-8:
                    break
                f = f_new
            return f

        elif method == 'Haaland':
            return (-1.8 * math.log10((epsilon / (3.7 * D))**1.11 +
                    (6.9 / Re)))**-2

        else:  # Swamee-Jain
            return 0.25 / (math.log10((epsilon / (3.7 * D)) +
                   (5.74 / Re**0.9)))**2

    def calculate_singular_losses(self, f, L, D, method='Coefficients',
                                  Kasp=1.5, Kref=2.0, percentage=0.1):
        """Calcule les pertes singulières K_T"""
        if method == 'Coefficients':
            return Kasp + Kref
        else:  # Pourcentage
            return percentage * (f * L / D)

    def calculate_HMT(self, Q, D, friction_method='Swamee-Jain',
                      loss_method='Coefficients', **kwargs):
        """Calcule la HMT pour un débit et diamètre donnés"""
        # Vitesse
        V = (4 * Q) / (math.pi * D**2)

        # Reynolds
        Re = self.calculate_reynolds(V, D)

        # Coefficient de frottement
        f = self.calculate_friction_factor(Re, D, self.fluid.roughness,
                                           friction_method)

        # Pertes singulières
        K_T = self.calculate_singular_losses(f, self.pipe.L_total, D,
                                             loss_method, **kwargs)

        # Coefficient global
        A = (8 / (self.g * math.pi**2 * D**4)) * ((f * self.pipe.L_total / D) + K_T)

        # Pertes de charge
        Dh = A * Q**2

        # HMT
        HMT = self.pipe.H_geometric + Dh

        return {
            'D': D,
            'V': V,
            'Re': Re,
            'f': f,
            'K_T': K_T,
            'A': A,
            'Dh': Dh,
            'HMT': HMT,
            'Hg': self.pipe.H_geometric
        }

    def calculate_system_curve(self, D, Q_nominal, friction_method='Swamee-Jain',
                               loss_method='Coefficients', **kwargs):
        """
        Génère la courbe du système HMTs = f(Qs)
        A est VARIABLE : recalculé pour chaque Qs car fs dépend de Qs.
        """
        Hg = self.pipe.H_geometric
        Q_factors = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
        Qs_list = [q * Q_nominal for q in Q_factors]
        HMTs_list = []
        As_list = []

        for Qs in Qs_list:
            Vs = (4 * Qs) / (math.pi * D**2)
            Re_s = self.calculate_reynolds(Vs, D)
            fs = self.calculate_friction_factor(Re_s, D, self.fluid.roughness,
                                                friction_method)
            K_T = self.calculate_singular_losses(fs, self.pipe.L_total, D,
                                                 loss_method, **kwargs)
            A_s = (8 / (self.g * math.pi**2 * D**4)) * ((fs * self.pipe.L_total / D) + K_T)
            HMTs = Hg + A_s * Qs**2
            HMTs_list.append(HMTs)
            As_list.append(A_s)

        return {
            'Qs': Qs_list,
            'HMTs': HMTs_list,
            'As': As_list,
            'Hg': Hg
        }

    def calculate_diameter_range(self, Q, Vmin, Vmax):
        """Calcule les diamètres min et max admissibles"""
        Dmin = math.sqrt((4 * Q) / (math.pi * Vmax))
        Dmax = math.sqrt((4 * Q) / (math.pi * Vmin))
        return Dmin, Dmax
