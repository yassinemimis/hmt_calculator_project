"""
Contrôleur pour l'optimisation du choix de pompe
Implémente l'algorithme complet avec système de Score pondéré.
"""
import math
import numpy as np
from models.solution_model import SolutionModel
from utils.interpolation import cubic_interpolation, simple_fsolve


class PumpOptimizer:
    def __init__(self, hmt_calculator, npsh_calculator):
        self.hmt_calc = hmt_calculator
        self.npsh_calc = npsh_calculator
        self.solutions = []

    # ------------------------------------------------------------------
    # Poids selon l'objectif
    # ------------------------------------------------------------------
    OBJECTIVES = {
        "Fonctionnement normal":     {'W1': 4, 'W2': 2, 'W3': 2, 'W4': 2},
        "Économie d'énergie":        {'W1': 4, 'W2': 4, 'W3': 1, 'W4': 1},
        "Précision opérationnelle":  {'W1': 4, 'W2': 1, 'W3': 4, 'W4': 1},
        "Fonctionnement sûr":        {'W1': 4, 'W2': 1, 'W3': 1, 'W4': 4},
    }

    def _get_weights(self, objective):
        return self.OBJECTIVES.get(objective, self.OBJECTIVES["Fonctionnement normal"])

    # ------------------------------------------------------------------
    # Score
    # ------------------------------------------------------------------
    def _compute_score(self, Qf, Hf, npf, Q_nom, HMT, Q_BEP, H_BEP, weights):
        W1, W2, W3, W4 = weights['W1'], weights['W2'], weights['W3'], weights['W4']
        W_sum = W1 + W2 + W3 + W4  # = 10

        # Efficacité (rendement)
        efficacite = npf  # déjà entre 0 et 1

        # Énergie
        err_energie = min(1.0, abs((Hf * Qf) / (HMT * Q_nom) - 1))
        energie = 1.0 - err_energie

        # Précision (point de fonctionnement vs objectif)
        err_precision = (abs(Hf - HMT) / HMT + abs(Qf - Q_nom) / Q_nom) / 2.0
        precision = max(0.0, 1.0 - err_precision)

        # Optimalité (écart au BEP)
        err_optimalite = (abs(Qf - Q_BEP) / Q_BEP + abs(Hf - H_BEP) / H_BEP) / 2.0
        optimalite = max(0.0, 1.0 - err_optimalite)

        score = (W1 * efficacite + W2 * energie + W3 * precision + W4 * optimalite)
        score = max(0.0, score)  # score sur échelle 0-10
        return score, efficacite, energie, precision, optimalite

    # ------------------------------------------------------------------
    # Point principal
    # ------------------------------------------------------------------
    def find_optimal_solutions(self, pumps, diameters, hmt_results,
                               system_curves, Q_nominal,
                               margin_npsh=0.5,
                               objective="Fonctionnement normal",
                               **kwargs):
        """
        Trouve toutes les solutions valides et retourne les 3 meilleures par Score.
        """
        self.solutions = []
        weights = self._get_weights(objective)

        for idx, D in enumerate(diameters):
            result = hmt_results[idx]
            HMT = result['HMT']
            A   = result['A']
            f   = result['f']

            for pump in pumps:
                bep = pump.get_max_efficiency_point()
                Q_BEP    = bep['Qp']
                H_BEP    = bep['Hp']
                idx_bep  = bep['index']
                Hp_max   = float(np.max(pump.Hp))

                # ── 1. Pompe seule ──────────────────────────────────
                if (Hp_max >= HMT and
                    Q_BEP >= Q_nominal and
                    0.7 * H_BEP <= HMT <= 1.2 * H_BEP and
                    Q_BEP <= Q_nominal <= 1.2 * Q_BEP):

                    sol = self._evaluate_configuration(
                        pump, D, 1, 1, 'Seule',
                        A, f, margin_npsh, idx_bep,
                        Q_nominal, HMT, Q_BEP, H_BEP, weights, **kwargs)
                    if sol:
                        self.solutions.append(sol)

                # ── 2. Pompes en série ──────────────────────────────
                if pump.nombre >= 2:
                    for n_serie in range(2, pump.nombre + 1):
                        H_total  = H_BEP * n_serie
                        Hp_max_s = Hp_max * n_serie

                        if (Hp_max_s >= HMT and
                            Q_BEP >= Q_nominal and
                            0.7 * H_BEP <= HMT <= 1.2 * H_BEP and
                            Q_BEP <= Q_nominal <= 1.2 * Q_BEP):

                            sol = self._evaluate_configuration(
                                pump, D, n_serie, 1, 'Série',
                                A, f, margin_npsh, idx_bep,
                                Q_nominal, HMT, Q_BEP, H_BEP, weights, **kwargs)
                            if sol:
                                self.solutions.append(sol)

                # ── 3. Pompes en parallèle ──────────────────────────
                if pump.nombre >= 2:
                    for n_parallel in range(2, pump.nombre + 1):
                        Q_total = Q_BEP * n_parallel

                        if (Hp_max >= HMT and
                            Q_total >= Q_nominal and
                            0.7 * H_BEP <= HMT <= 1.2 * H_BEP and
                            Q_BEP <= Q_nominal <= 1.2 * Q_BEP):

                            sol = self._evaluate_configuration(
                                pump, D, 1, n_parallel, 'Parallèle',
                                A, f, margin_npsh, idx_bep,
                                Q_nominal, HMT, Q_BEP, H_BEP, weights, **kwargs)
                            if sol:
                                self.solutions.append(sol)

                # ── 4. Cas mixte (série + parallèle) ───────────────
                if pump.nombre >= 4:
                    for n_serie in range(2, pump.nombre // 2 + 1):
                        for n_parallel in range(2, pump.nombre // n_serie + 1):
                            if n_serie * n_parallel > pump.nombre:
                                continue

                            H_total  = H_BEP * n_serie
                            Q_total  = Q_BEP * n_parallel
                            Hp_max_m = Hp_max * n_serie

                            if (Hp_max_m >= HMT and
                                Q_total >= Q_nominal and
                                0.7 * H_BEP <= HMT <= 1.2 * H_BEP and
                                Q_BEP <= Q_nominal <= 1.2 * Q_BEP):

                                sol = self._evaluate_configuration(
                                    pump, D, n_serie, n_parallel, 'Mixte',
                                    A, f, margin_npsh, idx_bep,
                                    Q_nominal, HMT, Q_BEP, H_BEP, weights, **kwargs)
                                if sol:
                                    self.solutions.append(sol)

        # Trier par Score décroissant, garder les 3 meilleurs
        self.solutions.sort(key=lambda x: x.score, reverse=True)
        self.solutions = self.solutions[:3]
        return self.solutions

    # ------------------------------------------------------------------
    # Évaluation d'une configuration
    # ------------------------------------------------------------------
    def _evaluate_configuration(self, pump, D, n_serie, n_parallel, config_type,
                                 A, f, margin_npsh, idx_bep,
                                 Q_nominal, HMT, Q_BEP, H_BEP, weights,
                                 **kwargs):
        try:
            Qp = pump.Qp.copy()
            Hp = pump.Hp.copy()

            if config_type in ('Série', 'Mixte'):
                Hp = Hp * n_serie
            if config_type in ('Parallèle', 'Mixte'):
                Qp = Qp * n_parallel

            f_Hp   = cubic_interpolation(Qp, Hp)
            f_np   = cubic_interpolation(pump.Qp, pump.np)
            f_NPSH = cubic_interpolation(pump.Qp, pump.NPSH)

            Hg = self.hmt_calc.pipe.H_geometric

            def system_curve(Q):
                return Hg + A * Q**2

            def intersection(Q):
                return f_Hp(Q) - system_curve(Q)

            Q_initial = Qp[idx_bep]
            Qf = simple_fsolve(intersection, Q_initial)[0]

            if Qf < Qp[0] or Qf > Qp[-1]:
                return None

            # Débit par pompe (pour np et NPSH)
            Q_per_pump = Qf / n_parallel if n_parallel > 1 else Qf

            # Filtrage : le point doit être APRÈS le max de rendement
            if Q_per_pump < pump.Qp[idx_bep]:
                return None

            Hf    = float(f_Hp(Qf))
            npf   = float(f_np(Q_per_pump))
            NPSHr = float(f_NPSH(Q_per_pump))

            # Vérification cavitation
            loss_method = kwargs.get('loss_method', 'Coefficients')
            Kasp = kwargs.get('Kasp', None)
            e    = kwargs.get('e', None)

            NPSHa = self.npsh_calc.calculate_NPSHa(
                Qf, D, f, Kasp=Kasp, e=e, loss_method=loss_method
            )

            if not self.npsh_calc.check_cavitation(NPSHa, NPSHr, margin_npsh):
                return None

            # Score
            score, efficacite, energie, precision, optimalite = self._compute_score(
                Qf, Hf, npf, Q_nominal, HMT, Q_BEP, H_BEP, weights
            )

            # Créer la solution
            solution = SolutionModel()
            solution.diameter      = D
            solution.pump_type     = pump.type
            solution.configuration = config_type
            solution.n_serie       = n_serie
            solution.n_parallel    = n_parallel
            solution.Qf            = Qf
            solution.Hf            = Hf
            solution.efficiency    = npf
            solution.NPSHr         = NPSHr
            solution.NPSHa         = NPSHa
            solution.NPSH_margin   = NPSHa - NPSHr
            solution.score         = score
            solution.score_details = {
                'efficacite': efficacite,
                'energie': energie,
                'precision': precision,
                'optimalite': optimalite,
            }

            return solution

        except Exception:
            return None

    def get_best_solution(self):
        """Retourne la meilleure solution (Score maximal)"""
        return self.solutions[0] if self.solutions else None
