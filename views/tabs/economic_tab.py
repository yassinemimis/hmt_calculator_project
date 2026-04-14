"""
Onglet de calcul économique (simplifié selon algorithme)
Calcule uniquement : C_conduite_totale + C_pompe_configuration
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QPushButton, QLabel, QLineEdit, QTextEdit,
                             QMessageBox, QGridLayout, QRadioButton,
                             QButtonGroup)
from PyQt5.QtCore import Qt
from config import CURRENCIES


class EconomicTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("ÉTAPE 5: Calcul économique")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2196F3;")
        layout.addWidget(title)

        # ── Paramètres ───────────────────────────────────────────────
        params_group = QGroupBox("Paramètres économiques")
        params_layout = QGridLayout()

        # Monnaie
        params_layout.addWidget(QLabel("Monnaie:"), 0, 0)
        currency_widget = QWidget()
        currency_layout = QHBoxLayout(currency_widget)
        currency_layout.setContentsMargins(0, 0, 0, 0)
        self.currency_group = QButtonGroup()
        for idx, currency in enumerate(CURRENCIES):
            rb = QRadioButton(currency)
            if currency == 'DZD':
                rb.setChecked(True)
            self.currency_group.addButton(rb, idx)
            currency_layout.addWidget(rb)
        currency_layout.addStretch()
        params_layout.addWidget(currency_widget, 0, 1)

        # Prix conduite par mètre
        params_layout.addWidget(QLabel("Prix conduite C_conduite (par mètre):"), 1, 0)
        self.cost_pipe_input = QLineEdit("1000")
        params_layout.addWidget(self.cost_pipe_input, 1, 1)

        # Prix de la configuration de pompage (toutes pompes)
        params_layout.addWidget(QLabel("Prix configuration pompage C_pompe:"), 2, 0)
        self.cost_pump_input = QLineEdit("50000")
        params_layout.addWidget(self.cost_pump_input, 2, 1)

        # Rendement moteur (informatif pour puissances)
        params_layout.addWidget(QLabel("Rendement moteur ηm (informatif):"), 3, 0)
        self.nm_input = QLineEdit("0.90")
        params_layout.addWidget(self.nm_input, 3, 1)

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # ── Bouton calcul ─────────────────────────────────────────────
        calculate_btn = QPushButton("💰 CALCULER LES COÛTS")
        calculate_btn.setMinimumHeight(50)
        calculate_btn.setStyleSheet("font-size: 13pt;")
        calculate_btn.clicked.connect(self.calculate_economic)
        layout.addWidget(calculate_btn)

        # ── Résultats ─────────────────────────────────────────────────
        results_group = QGroupBox("Analyse économique")
        results_layout = QVBoxLayout()
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(300)
        results_layout.addWidget(self.results_text)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        layout.addStretch()

    # ------------------------------------------------------------------ calcul

    def calculate_economic(self):
        if not self.main_window.best_solution:
            QMessageBox.warning(self, "Attention",
                                "Veuillez d'abord sélectionner une solution optimale")
            return

        try:
            nm          = float(self.nm_input.text())
            cost_pipe   = float(self.cost_pipe_input.text())
            cost_pump   = float(self.cost_pump_input.text())
            currency    = self.currency_group.checkedButton().text()
            L_total     = self.main_window.pipe_model.L_total

            self.main_window.economic_data = \
                self.main_window.economic_calculator.calculate_costs(
                    self.main_window.best_solution,
                    L_total,
                    cost_pipe_per_m=cost_pipe,
                    cost_pump_config=cost_pump,
                    nm_motor=nm
                )
            self.main_window.economic_data['currency'] = currency

            self.display_results()

            QMessageBox.information(self, "Succès",
                                    "Calcul économique terminé.\n"
                                    "Vous pouvez voir les résultats finaux.")
            self.main_window.update_status("Calcul économique terminé", 3000)

        except Exception as e:
            QMessageBox.critical(self, "Erreur",
                                 f"Erreur lors du calcul économique:\n{str(e)}")

    # ------------------------------------------------------------------ affichage

    def display_results(self):
        self.results_text.clear()
        data     = self.main_window.economic_data
        sol      = self.main_window.best_solution
        currency = data['currency']

        header  = "=" * 100 + "\n"
        header += "ANALYSE ÉCONOMIQUE DE LA SOLUTION SÉLECTIONNÉE\n"
        header += "=" * 100 + "\n\n"
        self.results_text.append(header)

        output  = "Configuration :\n"
        output += f"  • Type de pompe               : {sol.pump_type}\n"
        output += f"  • Configuration               : {sol.configuration}\n"
        output += f"  • Nombre total de pompes      : {data['n_total_pumps']}\n"
        output += f"  • Diamètre de conduite        : {sol.diameter:.4f} m\n"
        output += f"  • Rendement pompe             : {sol.efficiency*100:.2f}%\n"
        output += f"  • Rendement moteur            : {data['nm_motor']*100:.2f}%\n\n"

        powers  = data['powers']
        output += "Puissances (informatif) :\n"
        output += f"  • Puissance hydraulique (P_hyd)  : {powers['P_hyd_kW']:.2f} kW\n"
        output += f"  • Puissance pompe (Pp)           : {powers['P_pump_kW']:.2f} kW\n"
        output += f"  • Puissance électrique totale    : {powers['P_total_kW']:.2f} kW\n\n"

        output += f"Coûts ({currency}) :\n"
        output += f"  • C_conduite_totale              : {data['cost_pipe']:,.2f} {currency}\n"
        output += f"  • C_pompe (configuration)        : {data['cost_pump_config']:,.2f} {currency}\n"
        output += f"  ► C_SYSTÈME TOTAL                : {data['cost_systeme']:,.2f} {currency}\n\n"

        output += f"  Score de la solution             : {sol.score:.4f} / 10\n"

        self.results_text.append(output)
