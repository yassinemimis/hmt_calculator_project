"""
Contrôleur pour les calculs économiques (simplifié selon algorithme)
Coût = C_conduite_totale + C_pompe_configuration
"""

class EconomicCalculator:
    def __init__(self, fluid_model):
        self.fluid = fluid_model
        self.g = 9.81

    def calculate_power(self, Qf, Hf, np_pump, nm_motor=0.9):
        """
        Calcule les puissances (informatif uniquement)
        Returns: dict avec P_hyd, P_pump, P_total (en W et kW)
        """
        P_hyd   = self.fluid.density * self.g * Qf * Hf   # W
        P_pump  = P_hyd / np_pump                          # W
        P_total = P_pump / nm_motor                        # W
        return {
            'P_hyd_W':    P_hyd,
            'P_hyd_kW':   P_hyd / 1000,
            'P_pump_W':   P_pump,
            'P_pump_kW':  P_pump / 1000,
            'P_total_W':  P_total,
            'P_total_kW': P_total / 1000,
        }

    def calculate_costs(self, solution, L_total,
                        cost_pipe_per_m=1000,
                        cost_pump_config=50000,
                        nm_motor=0.9):
        """
        Calcule les coûts selon l'algorithme :
            C_conduite_totale = L * C_conduite
            C_système = C_pompe_configuration + C_conduite_totale

        Args:
            solution        : SolutionModel
            L_total         : Longueur totale de conduite (m)
            cost_pipe_per_m : Prix du mètre de conduite
            cost_pump_config: Prix de la configuration de pompage (toutes pompes)
            nm_motor        : Rendement moteur (pour calcul puissance informatif)

        Returns:
            dict avec les coûts
        """
        powers = self.calculate_power(solution.Qf, solution.Hf,
                                      solution.efficiency, nm_motor)

        cost_pipe_total = L_total * cost_pipe_per_m
        cost_systeme    = cost_pump_config + cost_pipe_total

        return {
            'powers':          powers,
            'nm_motor':        nm_motor,
            'n_total_pumps':   solution.total_pumps,
            'cost_pipe':       cost_pipe_total,
            'cost_pump_config': cost_pump_config,
            'cost_systeme':    cost_systeme,
        }
