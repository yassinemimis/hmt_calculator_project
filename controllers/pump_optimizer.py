"""
Contrôleur pour l'optimisation du choix de pompe
"""
import numpy as np
from models.solution_model import SolutionModel
from utils.interpolation import cubic_interpolation, simple_fsolve

class PumpOptimizer:
    def __init__(self, hmt_calculator, npsh_calculator):
        self.hmt_calc = hmt_calculator
        self.npsh_calc = npsh_calculator
        self.solutions = []
    
    def find_optimal_solutions(self, pumps, diameters, hmt_results, 
                              system_curves, Q_nominal, margin_npsh=0.5, 
                              Zs=0, **kwargs):
        """
        Trouve toutes les solutions optimales
        
        Args:
            pumps: Liste de PumpModel
            diameters: Liste des diamètres à tester
            hmt_results: Résultats HMT pour chaque diamètre
            system_curves: Courbes du système pour chaque diamètre
            Q_nominal: Débit nominal
            margin_npsh: Marge de sécurité NPSH
            Zs: Cote surface libre aspiration
        """
        self.solutions = []
        
        for idx, D in enumerate(diameters):
            result = hmt_results[idx]
            HMT = result['HMT']
            A = result['A']
            f = result['f']
            
            for pump in pumps:
                # Trouver le point de rendement maximal
                max_eff_point = pump.get_max_efficiency_point()
                Qp_max_np = max_eff_point['Qp']
                Hp_max_np = max_eff_point['Hp']
                idx_max_np = max_eff_point['index']
                
                # 1. Pompe seule
                if (0.8 * HMT <= Hp_max_np <= 1.2 * HMT and 
                    Q_nominal <= Qp_max_np <= 1.2 * Q_nominal):
                    
                    solution = self._evaluate_configuration(
                        pump, D, 1, 1, 'Seule', A, f, Zs, 
                        margin_npsh, idx_max_np, **kwargs
                    )
                    if solution:
                        self.solutions.append(solution)
                
                # 2. Pompes en série
                if pump.nombre >= 2:
                    for n_serie in range(2, pump.nombre + 1):
                        Hp_total = Hp_max_np * n_serie
                        
                        if (0.8 * HMT <= Hp_total <= 1.2 * HMT and
                            Q_nominal <= Qp_max_np <= 1.2 * Q_nominal):
                            
                            solution = self._evaluate_configuration(
                                pump, D, n_serie, 1, 'Série', A, f, Zs,
                                margin_npsh, idx_max_np, **kwargs
                            )
                            if solution:
                                self.solutions.append(solution)
                
                # 3. Pompes en parallèle
                if pump.nombre >= 2:
                    for n_parallel in range(2, pump.nombre + 1):
                        Qp_total = Qp_max_np * n_parallel
                        
                        if (0.8 * HMT <= Hp_max_np <= 1.2 * HMT and
                            Q_nominal <= Qp_total <= 1.2 * Q_nominal):
                            
                            solution = self._evaluate_configuration(
                                pump, D, 1, n_parallel, 'Parallèle', A, f, Zs,
                                margin_npsh, idx_max_np, **kwargs
                            )
                            if solution:
                                self.solutions.append(solution)
                
                # 4. Cas mixte (série + parallèle)
                if pump.nombre >= 4:
                    for n_serie in range(2, pump.nombre // 2 + 1):
                        for n_parallel in range(2, pump.nombre // n_serie + 1):
                            if n_serie * n_parallel > pump.nombre:
                                continue
                            
                            Hp_total = Hp_max_np * n_serie
                            Qp_total = Qp_max_np * n_parallel
                            
                            if (0.8 * HMT <= Hp_total <= 1.2 * HMT and
                                Q_nominal <= Qp_total <= 1.2 * Q_nominal):
                                
                                solution = self._evaluate_configuration(
                                    pump, D, n_serie, n_parallel, 'Mixte', 
                                    A, f, Zs, margin_npsh, idx_max_np, **kwargs
                                )
                                if solution:
                                    self.solutions.append(solution)
        
        # Trier par rendement décroissant
        self.solutions.sort(key=lambda x: x.efficiency, reverse=True)
        
        return self.solutions
    
    def _evaluate_configuration(self, pump, D, n_serie, n_parallel, config_type,
                               A, f, Zs, margin_npsh, idx_max_np, **kwargs):
        """Évalue une configuration de pompe"""
        try:
            # Adapter les courbes selon la configuration
            Qp = pump.Qp.copy()
            Hp = pump.Hp.copy()
            
            if config_type == 'Série' or config_type == 'Mixte':
                Hp = Hp * n_serie
            
            if config_type == 'Parallèle' or config_type == 'Mixte':
                Qp = Qp * n_parallel
            
            # Créer les fonctions d'interpolation
            f_Hp = cubic_interpolation(Qp, Hp)
            f_np = cubic_interpolation(pump.Qp, pump.np)
            f_NPSH = cubic_interpolation(pump.Qp, pump.NPSH)
            
            # Courbe du système
            Hg = self.hmt_calc.pipe.H_geometric
            
            def system_curve(Q):
                return Hg + A * Q**2
            
            # Trouver le point de fonctionnement
            def intersection(Q):
                return f_Hp(Q) - system_curve(Q)
            
            Q_initial = Qp[idx_max_np]
            Qf = simple_fsolve(intersection, Q_initial)[0]
            
            # Vérifier validité
            if Qf < Qp[0] or Qf > Qp[-1]:
                return None
            
            # Pour les configurations parallèles/mixtes, 
            # le débit par pompe est Qf/n_parallel
            Q_per_pump = Qf / n_parallel if n_parallel > 1 else Qf
            
            # Vérifier que le point est après le max de rendement
            if Q_per_pump < pump.Qp[idx_max_np]:
                return None
            
            Hf = float(f_Hp(Qf))
            npf = float(f_np(Q_per_pump))
            NPSHr = float(f_NPSH(Q_per_pump))
            
            # Calculer NPSHa
            loss_method = kwargs.get('loss_method', 'Coefficients')
            Kasp = kwargs.get('Kasp', 1.5)
            e = kwargs.get('e', 0.1)
            
            NPSHa = self.npsh_calc.calculate_NPSHa(
                Qf, D, f, Zs, Kasp, e, loss_method
            )
            
            # Vérifier cavitation
            if not self.npsh_calc.check_cavitation(NPSHa, NPSHr, margin_npsh):
                return None
            
            # Créer la solution
            solution = SolutionModel()
            solution.diameter = D
            solution.pump_type = pump.type
            solution.configuration = config_type
            solution.n_serie = n_serie
            solution.n_parallel = n_parallel
            solution.Qf = Qf
            solution.Hf = Hf
            solution.efficiency = npf
            solution.NPSHr = NPSHr
            solution.NPSHa = NPSHa
            solution.NPSH_margin = NPSHa - NPSHr
            
            return solution
        
        except Exception as e:
            # En cas d'erreur, ignorer cette configuration
            return None
    
    def get_best_solution(self):
        """Retourne la meilleure solution (rendement maximal)"""
        if self.solutions:
            return self.solutions[0]
        return None