"""
Contrôleur pour les calculs économiques
"""

class EconomicCalculator:
    def __init__(self, fluid_model):
        self.fluid = fluid_model
        self.g = 9.81
    
    def calculate_power(self, Qf, Hf, np_pump, nm_motor=0.9):
        """
        Calcule les puissances
        
        Returns:
            dict avec P_hyd, P_pump, P_total (en W et kW)
        """
        # Puissance hydraulique
        P_hyd = self.fluid.density * self.g * Qf * Hf  # W
        
        # Puissance absorbée par la pompe
        P_pump = P_hyd / np_pump  # W
        
        # Puissance électrique totale
        P_total = P_pump / nm_motor  # W
        
        return {
            'P_hyd_W': P_hyd,
            'P_hyd_kW': P_hyd / 1000,
            'P_pump_W': P_pump,
            'P_pump_kW': P_pump / 1000,
            'P_total_W': P_total,
            'P_total_kW': P_total / 1000
        }
    
    def calculate_costs(self, solution, L_total, nm_motor=0.9, 
                       cost_pipe_per_m=1000, cost_pump=50000,
                       cost_kWh=5, hours_per_day=10, days_per_year=250):
        """
        Calcule tous les coûts
        
        Args:
            solution: SolutionModel
            L_total: Longueur totale de conduite (m)
            nm_motor: Rendement moteur
            cost_pipe_per_m: Coût conduite par mètre
            cost_pump: Coût unitaire d'une pompe
            cost_kWh: Coût du kWh
            hours_per_day: Heures de fonctionnement par jour
            days_per_year: Jours de fonctionnement par an
        
        Returns:
            dict avec tous les coûts
        """
        # Puissances
        powers = self.calculate_power(solution.Qf, solution.Hf, 
                                      solution.efficiency, nm_motor)
        
        # Coût de la conduite
        cost_pipe_total = L_total * cost_pipe_per_m
        
        # Coût des pompes
        n_total_pumps = solution.total_pumps  # ✅ Correction
        cost_pumps_total = n_total_pumps * cost_pump
        
        # Coût énergétique annuel
        cost_energy_annual = (powers['P_total_kW'] * hours_per_day * 
                             days_per_year * cost_kWh)
        
        # Coût total (installation + 1 an)
        cost_total = cost_pipe_total + cost_pumps_total + cost_energy_annual
        
        return {
            'powers': powers,
            'nm_motor': nm_motor,
            'n_total_pumps': n_total_pumps,  # ✅ Nom correct
            'cost_pipe': cost_pipe_total,
            'cost_pumps': cost_pumps_total,
            'cost_energy_annual': cost_energy_annual,
            'cost_total': cost_total,
            'hours_per_day': hours_per_day,
            'days_per_year': days_per_year
        }
    
    def calculate_payback_period(self, cost_installation, cost_energy_annual):
        """Calcule la période de retour sur investissement"""
        return cost_installation / cost_energy_annual if cost_energy_annual > 0 else float('inf')
    
    def compare_solutions(self, solutions_with_costs):
        """
        Compare plusieurs solutions sur base économique
        
        Args:
            solutions_with_costs: Liste de tuples (solution, costs_dict)
        
        Returns:
            Solution la plus économique sur différents critères
        """
        if not solutions_with_costs:
            return None
        
        # Meilleure solution par coût total
        best_total = min(solutions_with_costs, 
                        key=lambda x: x[1]['cost_total'])
        
        # Meilleure solution par coût énergétique
        best_energy = min(solutions_with_costs,
                         key=lambda x: x[1]['cost_energy_annual'])
        
        # Meilleure solution par rendement
        best_efficiency = max(solutions_with_costs,
                             key=lambda x: x[0].efficiency)
        
        return {
            'best_total_cost': best_total,
            'best_energy_cost': best_energy,
            'best_efficiency': best_efficiency
        }