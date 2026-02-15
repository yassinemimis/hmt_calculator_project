"""
Onglet des résultats finaux
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTextEdit, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from utils.file_handler import FileHandler
import datetime
from utils.pdf_generator import PDFReportGenerator
from views.widgets.custom_widgets import IconButton

class ResultsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """Initialize l'interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Titre
        title = QLabel("ÉTAPE 6: Résultats Finaux")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2196F3;")
        layout.addWidget(title)
        
        # Zone de texte pour les résultats
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(500)
        layout.addWidget(self.results_text)
        
        # Boutons d'export
        button_layout = QHBoxLayout()

        export_txt_btn = IconButton("📄  Exporter TXT", "")
        export_txt_btn.setProperty("class", "secondary")
        export_txt_btn.clicked.connect(self.export_txt_dialog)
        button_layout.addWidget(export_txt_btn)

        export_json_btn = IconButton("📊  Exporter JSON", "")
        export_json_btn.setProperty("class", "secondary")
        export_json_btn.clicked.connect(self.export_json_dialog)
        button_layout.addWidget(export_json_btn)

        export_pdf_btn = IconButton("📄  Générer PDF", "")
        export_pdf_btn.clicked.connect(self.export_pdf_dialog)
        button_layout.addWidget(export_pdf_btn)

        generate_full_btn = IconButton("🖨️  Rapport Complet TXT", "")
        generate_full_btn.setProperty("class", "secondary")
        generate_full_btn.clicked.connect(self.generate_full_report)
        button_layout.addWidget(generate_full_btn)

        button_layout.addStretch()

        layout.addLayout(button_layout)
                
        # Auto-update des résultats
        self.main_window.tabs.currentChanged.connect(self.on_tab_changed)
    
    def on_tab_changed(self, index):
        """Appelé quand on change d'onglet"""
        if index == 5:  # Index de l'onglet résultats
            self.update_results()
    
    def update_results(self):
        """Met à jour l'affichage des résultats finaux"""
        if not self.main_window.best_solution:
            self.results_text.setPlainText(
                "Aucune solution calculée pour le moment.\n\n"
                "Veuillez suivre les étapes:\n"
                "1. Saisir les données d'entrée\n"
                "2. Importer les pompes\n"
                "3. Calculer la HMT\n"
                "4. Trouver la solution optimale\n"
                "5. Calculer les coûts économiques"
            )
            return
        
        self.results_text.clear()
        
        sol = self.main_window.best_solution
        
        # En-tête
        header = "╔" + "="*118 + "╗\n"
        header += "║" + " "*30 + "RAPPORT FINAL - SYSTÈME DE POMPAGE" + " "*53 + "║\n"
        header += "╚" + "="*118 + "╝\n\n"
        
        self.results_text.append(header)
        
        # Section 1: Caractéristiques du système
        section1 = self.build_system_characteristics()
        self.results_text.append(section1)
        
        # Section 2: Solution optimale
        section2 = self.build_optimal_solution()
        self.results_text.append(section2)
        
        # Section 3: Configuration de la pompe
        section3 = self.build_pump_configuration()
        self.results_text.append(section3)
        
        # Section 4: Vérification NPSH
        section4 = self.build_npsh_verification()
        self.results_text.append(section4)
        
        # Section 5: Analyse économique
        if self.main_window.economic_data:
            section5 = self.build_economic_analysis()
            self.results_text.append(section5)
        
        # Pied de page
        footer = self.build_footer()
        self.results_text.append(footer)
    
    def build_system_characteristics(self):
        """Construit la section caractéristiques du système"""
        Q = float(self.main_window.input_tab.q_input.text())
        Hg = self.main_window.pipe_model.H_geometric
        Lasp = self.main_window.pipe_model.L_aspiration
        Lref = self.main_window.pipe_model.L_refoulement
        T = self.main_window.fluid_model.temperature
        rho = self.main_window.fluid_model.density
        
        section = "┌─ CARACTÉRISTIQUES DU SYSTÈME ─────────────────────────────────────────────────────────────┐\n"
        section += f"│ Débit nominal (Q)                    : {Q:.4f} m³/s\n"
        section += f"│ Hauteur géométrique (Hg)             : {Hg:.4f} m\n"
        section += f"│ Longueur aspiration                  : {Lasp:.2f} m\n"
        section += f"│ Longueur refoulement                 : {Lref:.2f} m\n"
        section += f"│ Température fluide                   : {T:.1f} °C\n"
        section += f"│ Masse volumique                      : {rho:.1f} kg/m³\n"
        section += "└────────────────────────────────────────────────────────────────────────────────────────────┘\n\n"
        
        return section
    
    def build_optimal_solution(self):
        """Construit la section solution optimale"""
        sol = self.main_window.best_solution
        
        section = "┌─ SOLUTION OPTIMALE ────────────────────────────────────────────────────────────────────────┐\n"
        section += f"│ Qf    : Débit de fonctionnement     : {sol.Qf:.4f} m³/s\n"
        section += f"│ Hf    : Hauteur manométrique totale : {sol.Hf:.4f} m\n"
        section += f"│ npf   : Rendement de la pompe       : {sol.efficiency:.4f} ({sol.efficiency*100:.2f}%)\n"
        
        if self.main_window.economic_data:
            nm = self.main_window.economic_data['nm_motor']
            P_total_kW = self.main_window.economic_data['powers']['P_total_kW']
            section += f"│ nm    : Rendement du moteur         : {nm:.4f} ({nm*100:.2f}%)\n"
            section += f"│ Ptotal: Puissance électrique totale : {P_total_kW:.2f} kW\n"
        
        section += "└────────────────────────────────────────────────────────────────────────────────────────────┘\n\n"
        
        return section
    
    def build_pump_configuration(self):
        """Construit la section configuration de la pompe"""
        sol = self.main_window.best_solution
        
        section = "┌─ CONFIGURATION DE LA POMPE ────────────────────────────────────────────────────────────────┐\n"
        section += f"│ Type de pompe                        : {sol.pump_type}\n"
        
        # Configuration détaillée
        if sol.configuration == 'Seule':
            section += f"│ Configuration                        : Pompe seule\n"
            section += f"│   └─ 1 pompe unique\n"
        elif sol.configuration == 'Série':
            section += f"│ Configuration                        : Montage en série\n"
            section += f"│   └─ {sol.n_serie} pompes en série\n"
        elif sol.configuration == 'Parallèle':
            section += f"│ Configuration                        : Montage en parallèle\n"
            section += f"│   └─ {sol.n_parallel} pompes en parallèle\n"
        elif sol.configuration == 'Mixte':
            section += f"│ Configuration                        : Montage mixte\n"
            section += f"│   └─ {sol.n_parallel} branches en parallèle\n"
            section += f"│   └─ Chaque branche contient {sol.n_serie} pompes en série\n"
        
        if self.main_window.economic_data:
            n_total = self.main_window.economic_data['n_total_pumps']
            section += f"│ Nombre total de pompes               : {n_total}\n"
        
        section += f"│ Diamètre de conduite                : {sol.diameter:.4f} m ({sol.diameter*1000:.1f} mm)\n"
        section += "└────────────────────────────────────────────────────────────────────────────────────────────┘\n\n"
        
        return section
    
    def build_npsh_verification(self):
        """Construit la section vérification NPSH"""
        sol = self.main_window.best_solution
        
        section = "┌─ VÉRIFICATION NPSH (CAVITATION) ──────────────────────────────────────────────────────────┐\n"
        section += f"│ NPSHr (requis)                       : {sol.NPSHr:.4f} m\n"
        section += f"│ NPSHa (disponible)                   : {sol.NPSHa:.4f} m\n"
        section += f"│ Marge de sécurité                    : {sol.NPSH_margin:.4f} m\n"
        
        if sol.NPSH_margin > 0:
            section += f"│ Statut                               : ✓ PAS DE RISQUE DE CAVITATION\n"
        else:
            section += f"│ Statut                               : ✗ RISQUE DE CAVITATION!\n"
        
        section += "└────────────────────────────────────────────────────────────────────────────────────────────┘\n\n"
        
        return section
    
    def build_economic_analysis(self):
        """Construit la section analyse économique"""
        data = self.main_window.economic_data
        currency = data['currency']
        
        section = "┌─ ANALYSE ÉCONOMIQUE ───────────────────────────────────────────────────────────────────────┐\n"
        section += f"│ Coût de la conduite                  : {data['cost_pipe']:>15,.2f} {currency}\n"
        section += f"│ Coût des pompes                      : {data['cost_pumps']:>15,.2f} {currency}\n"
        section += f"│ Coût énergétique annuel              : {data['cost_energy_annual']:>15,.2f} {currency}/an\n"
        section += f"│ ─────────────────────────────────────────────────────────────────────────────────────────\n"
        section += f"│ COÛT TOTAL (installation + 1 an)     : {data['cost_total']:>15,.2f} {currency}\n"
        section += "└────────────────────────────────────────────────────────────────────────────────────────────┘\n\n"
        
        return section
    
    def build_footer(self):
        """Construit le pied de page"""
        footer = "\n" + "─"*120 + "\n"
        footer += "Rapport généré par le Calculateur HMT Professionnel - Version 2.0 (PyQt5)\n"
        footer += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return footer
    
    def export_txt_dialog(self):
        """Dialogue d'export TXT"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter en TXT",
            f"rapport_hmt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Fichiers texte (*.txt);;Tous les fichiers (*.*)"
        )
        
        if filename:
            self.export_txt(filename)
    
    def export_txt(self, filename):
        """Exporte les résultats en TXT"""
        try:
            content = self.results_text.toPlainText()
            FileHandler.export_results_txt(content, filename)
            QMessageBox.information(self, "Succès",
                                  f"Résultats exportés dans:\n{filename}")
            self.main_window.update_status(f"Export TXT réussi: {filename}", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Erreur",
                               f"Erreur lors de l'export:\n{str(e)}")
    
    def export_json_dialog(self):
        """Dialogue d'export JSON"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter en JSON",
            f"rapport_hmt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "Fichiers JSON (*.json);;Tous les fichiers (*.*)"
        )
        
        if filename:
            self.export_json(filename)
    
    def export_json(self, filename):
        """Exporte les résultats en JSON"""
        try:
            data = {
                'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'solution_optimale': self.main_window.best_solution.to_dict(),
                'parametres_systeme': {
                    'Q': float(self.main_window.input_tab.q_input.text()),
                    'Lasp': self.main_window.pipe_model.L_aspiration,
                    'Lref': self.main_window.pipe_model.L_refoulement,
                    'Zdep': self.main_window.pipe_model.Z_depart,
                    'Zarr': self.main_window.pipe_model.Z_arrivee,
                    'T': self.main_window.fluid_model.temperature,
                    'rho': self.main_window.fluid_model.density,
                    'mu': self.main_window.fluid_model.viscosity,
                    'Pv': self.main_window.fluid_model.vapor_pressure,
                    'Patm': self.main_window.npsh_calculator.Patm,
                    'g': self.main_window.hmt_calculator.g
                }
            }
            
            if self.main_window.economic_data:
                data['analyse_economique'] = {
                    'currency': self.main_window.economic_data['currency'],
                    'powers_kW': {
                        'P_hyd': self.main_window.economic_data['powers']['P_hyd_kW'],
                        'P_pump': self.main_window.economic_data['powers']['P_pump_kW'],
                        'P_total': self.main_window.economic_data['powers']['P_total_kW']
                    },
                    'costs': {
                        'pipe': self.main_window.economic_data['cost_pipe'],
                        'pumps': self.main_window.economic_data['cost_pumps'],
                        'energy_annual': self.main_window.economic_data['cost_energy_annual'],
                        'total': self.main_window.economic_data['cost_total']
                    }
                }
            
            FileHandler.export_results_json(data, filename)
            QMessageBox.information(self, "Succès",
                                  f"Résultats exportés en JSON dans:\n{filename}")
            self.main_window.update_status(f"Export JSON réussi: {filename}", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Erreur",
                               f"Erreur lors de l'export:\n{str(e)}")
    
    def generate_full_report(self):
        """Génère un rapport complet détaillé"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Générer rapport complet",
            f"rapport_complet_hmt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Fichiers texte (*.txt);;Tous les fichiers (*.*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    # En-tête
                    f.write("="*120 + "\n")
                    f.write("                          RAPPORT COMPLET - SYSTÈME DE POMPAGE\n")
                    f.write("="*120 + "\n\n")
                    
                    f.write(f"Date de génération: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    # 1. Données d'entrée
                    f.write(self.build_input_data_section())
                    
                    # 2. Pompes disponibles
                    f.write(self.build_pumps_section())
                    
                    # 3. Calculs HMT
                    f.write(self.build_hmt_calculations_section())
                    
                    # 4. Solutions trouvées
                    f.write(self.build_solutions_section())
                    
                    # 5. Solution finale
                    f.write(self.build_final_solution_section())
                    
                    # Fin
                    f.write("\n" + "="*120 + "\n")
                    f.write("FIN DU RAPPORT\n")
                    f.write("="*120 + "\n")
                
                QMessageBox.information(self, "Succès",
                                      f"Rapport complet généré dans:\n{filename}")
                self.main_window.update_status(f"Rapport complet généré: {filename}", 5000)
            
            except Exception as e:
                QMessageBox.critical(self, "Erreur",
                                   f"Erreur lors de la génération:\n{str(e)}")
    
    def build_input_data_section(self):
        """Section données d'entrée pour rapport complet"""
        section = "\n1. DONNÉES D'ENTRÉE\n"
        section += "-" * 120 + "\n\n"
        
        section += "1.1 Données de site:\n"
        section += f"  • Pression atmosphérique (Patm)  : {self.main_window.npsh_calculator.Patm:.2f} Pa\n"
        section += f"  • Accélération pesanteur (g)     : {self.main_window.hmt_calculator.g:.2f} m/s²\n\n"
        
        section += "1.2 Données de réseau:\n"
        section += f"  • Longueur aspiration (Lasp)     : {self.main_window.pipe_model.L_aspiration:.2f} m\n"
        section += f"  • Longueur refoulement (Lref)    : {self.main_window.pipe_model.L_refoulement:.2f} m\n"
        section += f"  • Cote départ (Zdep)             : {self.main_window.pipe_model.Z_depart:.2f} m\n"
        section += f"  • Cote arrivée (Zarr)            : {self.main_window.pipe_model.Z_arrivee:.2f} m\n"
        section += f"  • Hauteur géométrique (Hg)       : {self.main_window.pipe_model.H_geometric:.2f} m\n\n"
        
        section += "1.3 Données de fluide:\n"
        section += f"  • Température (T)                : {self.main_window.fluid_model.temperature:.1f} °C\n"
        section += f"  • Masse volumique (ρ)            : {self.main_window.fluid_model.density:.1f} kg/m³\n"
        section += f"  • Viscosité dynamique (μ)        : {self.main_window.fluid_model.viscosity:.6f} Pa·s\n"
        section += f"  • Pression vapeur saturante (Pv) : {self.main_window.fluid_model.vapor_pressure:.2f} Pa\n"
        section += f"  • Rugosité absolue (ε)           : {self.main_window.fluid_model.roughness:.6f} m\n\n"
        
        section += "1.4 Données de fonctionnement:\n"
        Q = float(self.main_window.input_tab.q_input.text())
        Vmin = float(self.main_window.input_tab.vmin_input.text())
        Vmax = float(self.main_window.input_tab.vmax_input.text())
        section += f"  • Débit volumique (Q)            : {Q:.4f} m³/s\n"
        section += f"  • Vitesse minimale (Vmin)        : {Vmin:.2f} m/s\n"
        section += f"  • Vitesse maximale (Vmax)        : {Vmax:.2f} m/s\n\n"
        
        return section
    
    def build_pumps_section(self):
        """Section pompes disponibles"""
        section = "\n2. POMPES DISPONIBLES\n"
        section += "-" * 120 + "\n\n"
        
        for idx, pump in enumerate(self.main_window.pumps):
            section += f"Pompe #{idx+1}:\n"
            section += f"  • Type                           : {pump.type}\n"
            section += f"  • Nombre disponible              : {pump.nombre}\n"
            section += f"  • Points de données              : {len(pump.Qp)}\n\n"
        
        return section
    
    def build_hmt_calculations_section(self):
        """Section calculs HMT"""
        section = "\n3. CALCULS HMT POUR CHAQUE DIAMÈTRE\n"
        section += "-" * 120 + "\n\n"
        
        for result in self.main_window.hmt_results:
            section += f"Diamètre D = {result['D']:.4f} m:\n"
            section += f"  • Vitesse (V)                    : {result['V']:.4f} m/s\n"
            section += f"  • Reynolds (Re)                  : {result['Re']:.2f}\n"
            section += f"  • Coefficient frottement (f)     : {result['f']:.6f}\n"
            section += f"  • Coeff. pertes singulières (K_T): {result['K_T']:.6f}\n"
            section += f"  • Coefficient global réseau (A)  : {result['A']:.6f}\n"
            section += f"  • Pertes de charge (Dh)          : {result['Dh']:.4f} m\n"
            section += f"  • HMT                            : {result['HMT']:.4f} m\n\n"
        
        return section
    
    def build_solutions_section(self):
        """Section solutions trouvées"""
        section = "\n4. SOLUTIONS TROUVÉES (top 10)\n"
        section += "-" * 120 + "\n\n"
        
        for idx, sol in enumerate(self.main_window.solutions[:10]):
            section += f"Solution #{idx+1}:\n"
            section += f"  • Diamètre                       : {sol.diameter:.4f} m\n"
            section += f"  • Type de pompe                  : {sol.pump_type}\n"
            section += f"  • Configuration                  : {sol.configuration}\n"
            section += f"  • Nombre total de pompes         : {sol.total_pumps}\n"
            section += f"  • Débit fonctionnement (Qf)      : {sol.Qf:.4f} m³/s\n"
            section += f"  • Hauteur fonctionnement (Hf)    : {sol.Hf:.4f} m\n"
            section += f"  • Rendement (np)                 : {sol.efficiency:.4f} ({sol.efficiency*100:.2f}%)\n"
            section += f"  • NPSHa                          : {sol.NPSHa:.4f} m\n"
            section += f"  • NPSHr                          : {sol.NPSHr:.4f} m\n"
            section += f"  • Marge NPSH                     : {sol.NPSH_margin:.4f} m\n\n"
        
        return section
    
    def build_final_solution_section(self):
        """Section solution finale"""
        sol = self.main_window.best_solution
        
        section = "\n5. SOLUTION FINALE (OPTIMALE)\n"
        section += "-" * 120 + "\n\n"
        
        section += f"Configuration de montage:\n"
        
        if sol.configuration == 'Seule':
            section += f"  • Type: Pompe seule\n"
            section += f"  • Description: 1 pompe unique\n\n"
        elif sol.configuration == 'Série':
            section += f"  • Type: Montage en série\n"
            section += f"  • Description: {sol.n_serie} pompes en série\n\n"
        elif sol.configuration == 'Parallèle':
            section += f"  • Type: Montage en parallèle\n"
            section += f"  • Description: {sol.n_parallel} pompes en parallèle\n\n"
        elif sol.configuration == 'Mixte':
            section += f"  • Type: Montage mixte\n"
            section += f"  • Description: {sol.n_parallel} branches en parallèle\n"
            section += f"                 Chaque branche contient {sol.n_serie} pompes en série\n\n"
        
        section += f"Performances:\n"
        section += f"Qf    : {sol.Qf:.4f} m³/s\n"
        section += f"Hf    : {sol.Hf:.4f} m\n"
        section += f"npf   : {sol.efficiency:.4f} ({sol.efficiency*100:.2f}%)\n"
        
        if self.main_window.economic_data:
            data = self.main_window.economic_data
            section += f"nm    : {data['nm_motor']:.4f} ({data['nm_motor']*100:.2f}%)\n"
            section += f"Ptotal: {data['powers']['P_total_kW']:.2f} kW\n\n"
            
            section += "\n6. ANALYSE ÉCONOMIQUE\n"
            section += "-" * 120 + "\n\n"
            
            section += f"Coûts ({data['currency']}):\n"
            section += f"  • Coût conduite                  : {data['cost_pipe']:,.2f}\n"
            section += f"  • Coût pompes ({data['n_total_pumps']} unités)      : {data['cost_pumps']:,.2f}\n"
            section += f"  • Coût énergétique annuel        : {data['cost_energy_annual']:,.2f}\n"
            section += f"  • COÛT TOTAL                     : {data['cost_total']:,.2f}\n\n"
        
        return section
    def export_pdf_dialog(self):
        """Dialogue d'export PDF"""
        if not self.main_window.best_solution:
            QMessageBox.warning(self, "⚠ Attention",
                            "Aucune solution disponible pour générer le PDF")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Générer rapport PDF",
            f"rapport_hmt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            "Fichiers PDF (*.pdf);;Tous les fichiers (*.*)"
        )
        
        if filename:
            self.export_pdf(filename)

    def export_pdf(self, filename):
        """Génère le rapport PDF"""
        try:
            pdf = PDFReportGenerator(filename)
            pdf.generate(self.main_window)
            
            QMessageBox.information(self, "✓ Succès",
                                f"Rapport PDF généré avec succès :\n{filename}")
            self.main_window.update_status(f"✓ Export PDF réussi : {filename}", 5000)
        except Exception as e:
            QMessageBox.critical(self, "✗ Erreur",
                            f"Erreur lors de la génération du PDF :\n{str(e)}")