"""
Onglet de calcul économique
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
        """Initialize l'interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Titre
        title = QLabel("ÉTAPE 5: Calcul économique")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2196F3;")
        layout.addWidget(title)
        
        # Paramètres économiques
        params_group = QGroupBox("Paramètres économiques")
        params_layout = QGridLayout()
        
        # Rendement moteur
        params_layout.addWidget(QLabel("Rendement moteur nm:"), 0, 0)
        self.nm_input = QLineEdit("0.90")
        params_layout.addWidget(self.nm_input, 0, 1)
        
        # Monnaie
        params_layout.addWidget(QLabel("Monnaie:"), 1, 0)
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
        
        params_layout.addWidget(currency_widget, 1, 1)
        
        # Prix conduite
        params_layout.addWidget(QLabel("Prix conduite (par mètre):"), 2, 0)
        self.cost_pipe_input = QLineEdit("1000")
        params_layout.addWidget(self.cost_pipe_input, 2, 1)
        
        # Prix pompe
        params_layout.addWidget(QLabel("Prix pompe unitaire:"), 3, 0)
        self.cost_pump_input = QLineEdit("50000")
        params_layout.addWidget(self.cost_pump_input, 3, 1)
        
        # Prix kWh
        params_layout.addWidget(QLabel("Prix kWh:"), 4, 0)
        self.cost_kwh_input = QLineEdit("5")
        params_layout.addWidget(self.cost_kwh_input, 4, 1)
        
        # Heures par jour
        params_layout.addWidget(QLabel("Heures de fonctionnement par jour:"), 5, 0)
        self.hours_day_input = QLineEdit("10")
        params_layout.addWidget(self.hours_day_input, 5, 1)
        
        # Jours par an
        params_layout.addWidget(QLabel("Jours de fonctionnement par an:"), 6, 0)
        self.days_year_input = QLineEdit("250")
        params_layout.addWidget(self.days_year_input, 6, 1)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Bouton de calcul
        calculate_btn = QPushButton("💰 CALCULER LES COÛTS")
        calculate_btn.setMinimumHeight(50)
        calculate_btn.setStyleSheet("font-size: 13pt;")
        calculate_btn.clicked.connect(self.calculate_economic)
        layout.addWidget(calculate_btn)
        
        # Zone de résultats
        results_group = QGroupBox("Analyse économique")
        results_layout = QVBoxLayout()
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(300)
        results_layout.addWidget(self.results_text)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        layout.addStretch()
    
    def calculate_economic(self):
        """Calcule les coûts"""
        if not self.main_window.best_solution:
            QMessageBox.warning(self, "Attention",
                              "Veuillez d'abord trouver une solution optimale")
            return
        
        try:
            # Paramètres
            nm = float(self.nm_input.text())
            cost_pipe = float(self.cost_pipe_input.text())
            cost_pump = float(self.cost_pump_input.text())
            cost_kwh = float(self.cost_kwh_input.text())
            hours_day = float(self.hours_day_input.text())
            days_year = float(self.days_year_input.text())
            
            # Monnaie
            selected_currency = self.currency_group.checkedButton().text()
            
            # Longueur totale
            L_total = self.main_window.pipe_model.L_total
            
            # Calcul
            self.main_window.economic_data = self.main_window.economic_calculator.calculate_costs(
                self.main_window.best_solution,
                L_total,
                nm,
                cost_pipe,
                cost_pump,
                cost_kwh,
                hours_day,
                days_year
            )
            
            self.main_window.economic_data['currency'] = selected_currency
            
            # Afficher
            self.display_results()
            
            QMessageBox.information(self, "Succès",
                                  "Calcul économique terminé.\n"
                                  "Vous pouvez voir les résultats finaux.")
            
            self.main_window.update_status("Calcul économique terminé", 3000)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur",
                               f"Erreur lors du calcul économique:\n{str(e)}")
    
    def display_results(self):
        """Affiche les résultats économiques"""
        self.results_text.clear()
        
        data = self.main_window.economic_data
        sol = self.main_window.best_solution
        currency = data['currency']
        
        header = "="*100 + "\n"
        header += "ANALYSE ÉCONOMIQUE DE LA SOLUTION OPTIMALE\n"
        header += "="*100 + "\n\n"
        
        self.results_text.append(header)
        
        output = f"Configuration:\n"
        output += f"  • Type de pompe               : {sol.pump_type}\n"
        output += f"  • Configuration               : {sol.configuration}\n"
        output += f"  • Nombre total de pompes      : {data['n_total_pumps']}\n"
        output += f"  • Diamètre de conduite        : {sol.diameter:.4f} m\n"
        output += f"  • Rendement pompe             : {sol.efficiency*100:.2f}%\n"
        output += f"  • Rendement moteur            : {data['nm_motor']*100:.2f}%\n\n"
        
        powers = data['powers']
        output += f"Puissances:\n"
        output += f"  • Puissance hydraulique (P_hyd)   : {powers['P_hyd_kW']:.2f} kW\n"
        output += f"  • Puissance pompe (Pp)            : {powers['P_pump_kW']:.2f} kW\n"
        output += f"  • Puissance électrique totale     : {powers['P_total_kW']:.2f} kW\n\n"
        
        output += f"Coûts ({currency}):\n"
        output += f"  • Coût conduite                   : {data['cost_pipe']:,.2f} {currency}\n"
        output += f"  • Coût pompes                     : {data['cost_pumps']:,.2f} {currency}\n"
        output += f"  • Coût énergétique annuel         : {data['cost_energy_annual']:,.2f} {currency}/an\n"
        output += f"  ► COÛT TOTAL (installation + 1 an): {data['cost_total']:,.2f} {currency}\n"
        
        self.results_text.append(output)