"""
Onglet d'optimisation et choix de la pompe
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QPushButton, QLabel, QLineEdit, QTextEdit,
                             QMessageBox, QGridLayout)
from PyQt5.QtCore import Qt


class OptimalTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """Initialize l'interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Titre
        title = QLabel("ÉTAPE 4: Choix optimal des pompes")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2196F3;")
        layout.addWidget(title)
        
        # Paramètres NPSH
        npsh_group = QGroupBox("Paramètres NPSH")
        npsh_layout = QGridLayout()
        
        npsh_layout.addWidget(QLabel("Marge de sécurité NPSH (m):"), 0, 0)
        self.npsh_margin_input = QLineEdit("0.5")
        npsh_layout.addWidget(self.npsh_margin_input, 0, 1)
        
        npsh_layout.addWidget(QLabel("Cote surface libre aspiration Zs (m):"), 1, 0)
        self.zs_input = QLineEdit("0")
        npsh_layout.addWidget(self.zs_input, 1, 1)
        
        npsh_group.setLayout(npsh_layout)
        layout.addWidget(npsh_group)
        
        # Bouton de calcul
        optimize_btn = QPushButton("🔍 TROUVER LA SOLUTION OPTIMALE")
        optimize_btn.setMinimumHeight(50)
        optimize_btn.setStyleSheet("font-size: 13pt;")
        optimize_btn.clicked.connect(self.find_optimal_solution)
        layout.addWidget(optimize_btn)
        
        # Zone de résultats
        results_group = QGroupBox("Solutions trouvées")
        results_layout = QVBoxLayout()
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(450)
        results_layout.addWidget(self.results_text)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        layout.addStretch()
    
    def find_optimal_solution(self):
        """Trouve la solution optimale"""
        if not self.main_window.hmt_results:
            QMessageBox.warning(self, "Attention",
                              "Veuillez d'abord calculer la HMT")
            return
        
        if not self.main_window.pumps:
            QMessageBox.warning(self, "Attention",
                              "Veuillez d'abord importer des pompes")
            return
        
        try:
            # Paramètres
            margin_npsh = float(self.npsh_margin_input.text())
            Zs = float(self.zs_input.text())
            Q_nominal = float(self.main_window.input_tab.q_input.text())
            
            # Paramètres de pertes
            loss_method = self.main_window.input_tab.loss_combo.currentText()
            kwargs = {'loss_method': loss_method}
            
            if loss_method == 'Coefficients':
                kwargs['Kasp'] = float(self.main_window.input_tab.kasp_input.text())
                kwargs['Kref'] = float(self.main_window.input_tab.kref_input.text())
            else:
                kwargs['e'] = float(self.main_window.input_tab.percentage_input.text())
            
            # Diamètres
            diameters = [r['D'] for r in self.main_window.hmt_results]
            
            # Optimisation
            self.main_window.solutions = self.main_window.pump_optimizer.find_optimal_solutions(
                self.main_window.pumps,
                diameters,
                self.main_window.hmt_results,
                self.main_window.system_curves,
                Q_nominal,
                margin_npsh,
                Zs,
                **kwargs
            )
            
            if self.main_window.solutions:
                self.main_window.best_solution = self.main_window.solutions[0]
                self.display_results()
                
                QMessageBox.information(self, "Succès",
                                      f"{len(self.main_window.solutions)} solution(s) trouvée(s).\n"
                                      "Vous pouvez passer au calcul économique.")
                
                self.main_window.update_status(
                    f"{len(self.main_window.solutions)} solution(s) trouvée(s)", 3000
                )
            else:
                QMessageBox.warning(self, "Attention",
                                  "Aucune solution valide trouvée.\n"
                                  "Essayez de modifier les paramètres ou d'ajouter d'autres pompes.")
        
        except Exception as e:
            QMessageBox.critical(self, "Erreur",
                               f"Erreur lors de l'optimisation:\n{str(e)}")
    
    def display_results(self):
        """Affiche les solutions trouvées"""
        self.results_text.clear()
        
        header = "="*100 + "\n"
        header += "SOLUTIONS OPTIMALES TROUVÉES (triées par rendement décroissant)\n"
        header += "="*100 + "\n\n"
        
        self.results_text.append(header)
        
        for idx, sol in enumerate(self.main_window.solutions):
            output = f"Solution #{idx+1}\n"
            output += "-" * 80 + "\n"
            output += f"  • Diamètre (D)                : {sol.diameter:.4f} m\n"
            output += f"  • Type de pompe               : {sol.pump_type}\n"
            
            # Configuration détaillée
            config_lines = sol.get_configuration_text().split('\n')
            output += f"  • Configuration               : {config_lines[0]}\n"
            for line in config_lines[1:]:
                output += f"                                  {line}\n"
            
            output += f"  • Nombre total de pompes      : {sol.total_pumps}\n"
            output += f"  • Débit de fonctionnement (Qf): {sol.Qf:.4f} m³/s\n"
            output += f"  • Hauteur de fonctionnement (Hf): {sol.Hf:.4f} m\n"
            output += f"  ► RENDEMENT (np)              : {sol.efficiency:.4f} ({sol.efficiency*100:.2f}%)\n"
            output += f"  • NPSHr                       : {sol.NPSHr:.4f} m\n"
            output += f"  • NPSHa                       : {sol.NPSHa:.4f} m\n"
            output += f"  • Marge NPSH                  : {sol.NPSH_margin:.4f} m\n"
            output += "\n"
            
            self.results_text.append(output)
        
        # Meilleure solution
        best = self.main_window.best_solution
        summary = "="*100 + "\n"
        summary += "🏆 MEILLEURE SOLUTION (Rendement maximal)\n"
        summary += "="*100 + "\n"
        
        if best.configuration == 'Seule':
            config_text = "Pompe seule"
        elif best.configuration == 'Série':
            config_text = f"Série ({best.n_serie} pompes)"
        elif best.configuration == 'Parallèle':
            config_text = f"Parallèle ({best.n_parallel} pompes)"
        elif best.configuration == 'Mixte':
            config_text = f"Mixte ({best.n_parallel} branches × {best.n_serie} pompes)"
        else:
            config_text = best.configuration
        
        summary += f"Diamètre: {best.diameter:.4f} m | Pompe: {best.pump_type}\n"
        summary += f"Configuration: {config_text}\n"
        summary += f"Rendement: {best.efficiency*100:.2f}% | Qf: {best.Qf:.4f} m³/s | Hf: {best.Hf:.4f} m\n"
        
        self.results_text.append(summary)