"""
Onglet d'optimisation et choix de la pompe
Affiche les 3 meilleures solutions avec Score, permet à l'utilisateur de choisir.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QPushButton, QLabel, QLineEdit, QTextEdit,
                             QMessageBox, QGridLayout, QComboBox,
                             QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt
from controllers.pump_optimizer import PumpOptimizer


class OptimalTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._radio_buttons = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("ÉTAPE 4: Choix optimal des pompes")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2196F3;")
        layout.addWidget(title)

        # ── Paramètres NPSH ──────────────────────────────────────────
        npsh_group = QGroupBox("Paramètres NPSH")
        npsh_layout = QGridLayout()

        npsh_layout.addWidget(QLabel("Marge de sécurité NPSH (m):"), 0, 0)
        self.npsh_margin_input = QLineEdit("0.5")
        npsh_layout.addWidget(self.npsh_margin_input, 0, 1)

        npsh_group.setLayout(npsh_layout)
        layout.addWidget(npsh_group)

        # ── Objectif de fonctionnement ───────────────────────────────
        obj_group = QGroupBox("Objectif de fonctionnement")
        obj_layout = QGridLayout()

        obj_layout.addWidget(QLabel("Objectif:"), 0, 0)
        self.objective_combo = QComboBox()
        self.objective_combo.addItems(list(PumpOptimizer.OBJECTIVES.keys()))
        obj_layout.addWidget(self.objective_combo, 0, 1)

        # Description des poids
        self.weights_label = QLabel()
        self.weights_label.setStyleSheet("color: #555; font-size: 9pt;")
        obj_layout.addWidget(self.weights_label, 1, 0, 1, 2)
        self.objective_combo.currentTextChanged.connect(self._update_weights_label)
        self._update_weights_label(self.objective_combo.currentText())

        obj_group.setLayout(obj_layout)
        layout.addWidget(obj_group)

        # ── Bouton calcul ────────────────────────────────────────────
        optimize_btn = QPushButton("🔍 TROUVER LES 3 MEILLEURES SOLUTIONS")
        optimize_btn.setMinimumHeight(50)
        optimize_btn.setStyleSheet("font-size: 13pt;")
        optimize_btn.clicked.connect(self.find_optimal_solution)
        layout.addWidget(optimize_btn)

        # ── Zone résultats ───────────────────────────────────────────
        results_group = QGroupBox("Top 3 — Solutions valides (triées par Score)")
        results_layout = QVBoxLayout()

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(350)
        results_layout.addWidget(self.results_text)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        # ── Sélection manuelle ───────────────────────────────────────
        self.select_group = QGroupBox("Choisir la solution finale")
        select_layout = QVBoxLayout()

        self.select_label = QLabel("Sélectionnez une solution parmi les résultats :")
        select_layout.addWidget(self.select_label)

        self.radio_container = QWidget()
        self.radio_layout = QVBoxLayout(self.radio_container)
        self.radio_layout.setContentsMargins(0, 0, 0, 0)
        self.radio_group = QButtonGroup(self)
        select_layout.addWidget(self.radio_container)

        confirm_btn = QPushButton("✓ Confirmer le choix")
        confirm_btn.setMinimumHeight(40)
        confirm_btn.clicked.connect(self.confirm_selection)
        select_layout.addWidget(confirm_btn)

        self.select_group.setLayout(select_layout)
        self.select_group.setVisible(False)
        layout.addWidget(self.select_group)

        layout.addStretch()

    # ------------------------------------------------------------------ helpers

    def _update_weights_label(self, objective):
        w = PumpOptimizer.OBJECTIVES.get(objective, {})
        txt = (f"Poids → Efficacité: {w.get('W1',0)}  |  "
               f"Énergie: {w.get('W2',0)}  |  "
               f"Précision: {w.get('W3',0)}  |  "
               f"Optimalité: {w.get('W4',0)}  "
               f"(total = 10)")
        self.weights_label.setText(txt)

    def _clear_radio_buttons(self):
        for rb in self._radio_buttons:
            self.radio_layout.removeWidget(rb)
            rb.deleteLater()
        self._radio_buttons.clear()

    # ------------------------------------------------------------------ calcul

    def find_optimal_solution(self):
        if not self.main_window.hmt_results:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord calculer la HMT")
            return
        if not self.main_window.pumps:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord importer des pompes")
            return

        try:
            margin_npsh = float(self.npsh_margin_input.text())
            Q_nominal   = float(self.main_window.input_tab.q_input.text())
            objective   = self.objective_combo.currentText()

            loss_method = self.main_window.input_tab.loss_combo.currentText()
            kwargs = {'loss_method': loss_method}
            if loss_method == 'Coefficients':
                kwargs['Kasp'] = float(self.main_window.input_tab.kasp_input.text())
                kwargs['Kref'] = float(self.main_window.input_tab.kref_input.text())
            else:
                kwargs['e'] = float(self.main_window.input_tab.percentage_input.text())

            diameters = [r['D'] for r in self.main_window.hmt_results]

            self.main_window.solutions = self.main_window.pump_optimizer.find_optimal_solutions(
                self.main_window.pumps,
                diameters,
                self.main_window.hmt_results,
                self.main_window.system_curves,
                Q_nominal,
                margin_npsh,
                objective,
                **kwargs
            )

            if self.main_window.solutions:
                # Par défaut : la meilleure solution
                self.main_window.best_solution = self.main_window.solutions[0]
                self.display_results()
                self._build_radio_buttons()
                self.select_group.setVisible(True)

                self.main_window.update_status(
                    f"{len(self.main_window.solutions)} solution(s) trouvée(s)", 3000)
            else:
                self.select_group.setVisible(False)
                QMessageBox.warning(self, "Attention",
                                    "Aucune solution valide trouvée.\n"
                                    "Modifiez les paramètres ou ajoutez d'autres pompes.")

        except Exception as e:
            QMessageBox.critical(self, "Erreur",
                                 f"Erreur lors de l'optimisation:\n{str(e)}")

    # ------------------------------------------------------------------ affichage

    def display_results(self):
        self.results_text.clear()
        header = "=" * 100 + "\n"
        header += "TOP 3 — SOLUTIONS OPTIMALES (triées par Score décroissant)\n"
        header += "=" * 100 + "\n\n"
        self.results_text.append(header)

        for idx, sol in enumerate(self.main_window.solutions):
            d = sol.score_details
            output  = f"🏅 Solution #{idx+1}\n"
            output += "-" * 80 + "\n"
            output += f"  • Diamètre (D)                    : {sol.diameter:.4f} m\n"
            output += f"  • Type de pompe                   : {sol.pump_type}\n"

            config_lines = sol.get_configuration_text().split('\n')
            output += f"  • Configuration                   : {config_lines[0]}\n"
            for line in config_lines[1:]:
                output += f"                                      {line}\n"

            output += f"  • Nombre total de pompes          : {sol.total_pumps}\n"
            output += f"  • Qf                              : {sol.Qf:.4f} m³/s\n"
            output += f"  • Hf                              : {sol.Hf:.4f} m\n"
            output += f"  • Rendement (ηp)                  : {sol.efficiency*100:.2f}%\n"
            output += f"  • NPSHr / NPSHa                   : {sol.NPSHr:.3f} / {sol.NPSHa:.3f} m\n"
            output += f"  • Marge NPSH                      : {sol.NPSH_margin:.3f} m\n"
            output += f"  ── Détail Score ──\n"
            output += f"     Efficacité  : {d.get('efficacite',0)*100:.1f}%\n"
            output += f"     Énergie     : {d.get('energie',0)*100:.1f}%\n"
            output += f"     Précision   : {d.get('precision',0)*100:.1f}%\n"
            output += f"     Optimalité  : {d.get('optimalite',0)*100:.1f}%\n"
            output += f"  ► SCORE GLOBAL                    : {sol.score:.4f} / 10\n\n"

            self.results_text.append(output)

    def _build_radio_buttons(self):
        self._clear_radio_buttons()
        solutions = self.main_window.solutions
        for idx, sol in enumerate(solutions):
            label = (f"Solution #{idx+1} — Score: {sol.score:.3f}  |  "
                     f"{sol.pump_type}  |  {sol.get_configuration_text().split(chr(10))[0]}  |  "
                     f"D={sol.diameter:.4f} m")
            rb = QRadioButton(label)
            if idx == 0:
                rb.setChecked(True)
            self.radio_group.addButton(rb, idx)
            self.radio_layout.addWidget(rb)
            self._radio_buttons.append(rb)

    def confirm_selection(self):
        selected_id = self.radio_group.checkedId()
        if selected_id < 0 or selected_id >= len(self.main_window.solutions):
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner une solution.")
            return

        self.main_window.best_solution = self.main_window.solutions[selected_id]
        sol = self.main_window.best_solution

        QMessageBox.information(self, "✓ Sélection confirmée",
                                f"Solution #{selected_id+1} sélectionnée :\n"
                                f"  Pompe   : {sol.pump_type}\n"
                                f"  Config  : {sol.configuration}\n"
                                f"  Score   : {sol.score:.4f}\n\n"
                                "Vous pouvez passer au calcul économique.")
        self.main_window.update_status(
            f"Solution #{selected_id+1} confirmée (Score={sol.score:.3f})", 5000)
        self.main_window.tabs.setCurrentIndex(4)
