"""
Onglet de calcul HMT
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QPushButton, QLabel, QLineEdit, QTextEdit,
                             QMessageBox, QGridLayout)
from PyQt5.QtCore import Qt
import math


class HMTTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """Initialize l'interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Titre
        title = QLabel("ÉTAPE 3: Choix des diamètres et calcul de la HMT")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2196F3;")
        layout.addWidget(title)
        
        # Section diamètres
        diameter_group = QGroupBox("Calcul des diamètres")
        diameter_layout = QGridLayout()
        
        calc_btn = QPushButton("Calculer Dmin et Dmax")
        calc_btn.clicked.connect(self.calculate_diameter_range)
        diameter_layout.addWidget(calc_btn, 0, 0)
        
        self.diameter_range_label = QLabel("Cliquez pour calculer la plage")
        self.diameter_range_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        diameter_layout.addWidget(self.diameter_range_label, 0, 1)
        
        diameter_layout.addWidget(
            QLabel("Diamètres à étudier (m, séparés par virgules):"), 1, 0
        )
        self.diameters_input = QLineEdit("0.1, 0.15, 0.2, 0.25")
        diameter_layout.addWidget(self.diameters_input, 1, 1)
        
        diameter_group.setLayout(diameter_layout)
        layout.addWidget(diameter_group)
        
        # Bouton de calcul
        calculate_btn = QPushButton("⚙️ CALCULER HMT ET COURBES SYSTÈME")
        calculate_btn.setMinimumHeight(50)
        calculate_btn.setStyleSheet("font-size: 13pt;")
        calculate_btn.clicked.connect(self.calculate_hmt)
        layout.addWidget(calculate_btn)
        
        # Zone de résultats
        results_group = QGroupBox("Résultats HMT")
        results_layout = QVBoxLayout()
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(400)
        results_layout.addWidget(self.results_text)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        layout.addStretch()
    
    def calculate_diameter_range(self):
        """Calcule les diamètres min et max admissibles"""
        try:
            Q = float(self.main_window.input_tab.q_input.text())
            Vmin = float(self.main_window.input_tab.vmin_input.text())
            Vmax = float(self.main_window.input_tab.vmax_input.text())
            
            Dmin, Dmax = self.main_window.hmt_calculator.calculate_diameter_range(
                Q, Vmin, Vmax
            )
            
            self.diameter_range_label.setText(
                f"Dmin = {Dmin:.4f} m  ≤  D  ≤  Dmax = {Dmax:.4f} m"
            )
            
            # Suggérer des diamètres
            suggested = []
            step = (Dmax - Dmin) / 5
            for i in range(6):
                suggested.append(Dmin + i * step)
            
            self.diameters_input.setText(
                ", ".join([f"{d:.4f}" for d in suggested])
            )
            
            self.main_window.update_status("Plage de diamètres calculée", 3000)
        
        except Exception as e:
            QMessageBox.critical(self, "Erreur",
                               f"Erreur de calcul:\n{str(e)}")
    
    def calculate_hmt(self):
        """Calcule HMT et courbes système"""
        try:
            # Mettre à jour les modèles
            self.main_window.input_tab.update_models()
            
            # Récupérer les paramètres
            Q = float(self.main_window.input_tab.q_input.text())
            diameters_str = self.diameters_input.text()
            diameters = [float(d.strip()) for d in diameters_str.split(",")]
            
            # Méthode de calcul
            friction_method = self.main_window.input_tab.friction_combo.currentText()
            loss_method = self.main_window.input_tab.loss_combo.currentText()
            
            # Paramètres pertes
            kwargs = {}
            if loss_method == 'Coefficients':
                kwargs['Kasp'] = float(self.main_window.input_tab.kasp_input.text())
                kwargs['Kref'] = float(self.main_window.input_tab.kref_input.text())
            else:
                kwargs['percentage'] = float(
                    self.main_window.input_tab.percentage_input.text()
                )
            
            # Calculer pour chaque diamètre
            self.main_window.hmt_results = []
            self.main_window.system_curves = {}
            
            for D in diameters:
                # Calcul HMT
                result = self.main_window.hmt_calculator.calculate_HMT(
                    Q, D, friction_method, loss_method, **kwargs
                )
                result['D'] = D
                self.main_window.hmt_results.append(result)
                
                # Courbe système
                curve = self.main_window.hmt_calculator.calculate_system_curve(
                    D, Q, result['A'], friction_method=friction_method,
                    loss_method=loss_method, **kwargs
                )
                self.main_window.system_curves[D] = curve
            
            # Afficher les résultats
            self.display_results()
            
            QMessageBox.information(self, "Succès",
                                  f"Calculs terminés pour {len(diameters)} diamètre(s).\n"
                                  "Vous pouvez passer à l'optimisation.")
            
            self.main_window.update_status(
                f"HMT calculée pour {len(diameters)} diamètre(s)", 3000
            )
        
        except Exception as e:
            QMessageBox.critical(self, "Erreur",
                               f"Erreur de calcul:\n{str(e)}")
    
    def display_results(self):
        """Affiche les résultats HMT"""
        self.results_text.clear()
        
        header = "="*100 + "\n"
        header += "RÉSULTATS DES CALCULS HMT ET COURBES DU SYSTÈME\n"
        header += "="*100 + "\n\n"
        
        self.results_text.append(header)
        
        for result in self.main_window.hmt_results:
            D = result['D']
            output = f"Diamètre D = {D:.4f} m\n"
            output += "-" * 80 + "\n"
            output += f"  • Vitesse d'écoulement (V)           : {result['V']:.4f} m/s\n"
            output += f"  • Nombre de Reynolds (Re)             : {result['Re']:.2f}\n"
            output += f"  • Coefficient de frottement (f)       : {result['f']:.6f}\n"
            output += f"  • Coefficient pertes singulières (K_T): {result['K_T']:.6f}\n"
            output += f"  • Coefficient global du réseau (A)    : {result['A']:.6f}\n"
            output += f"  • Hauteur géométrique (Hg)            : {result['Hg']:.4f} m\n"
            output += f"  • Pertes de charge (Dh)               : {result['Dh']:.4f} m\n"
            output += f"  ► HAUTEUR MANOMÉTRIQUE TOTALE (HMT)   : {result['HMT']:.4f} m\n\n"
            
            # Courbe système
            curve = self.main_window.system_curves[D]
            output += "  Courbe du système HMTs = f(Qs):\n"
            for Qs, HMTs in zip(curve['Qs'], curve['HMTs']):
                output += f"    Qs = {Qs:.4f} m³/s  →  HMTs = {HMTs:.4f} m\n"
            output += "\n"
            
            self.results_text.append(output)