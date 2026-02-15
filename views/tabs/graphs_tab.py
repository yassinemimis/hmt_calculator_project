"""
Onglet des graphiques
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QMessageBox)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class GraphsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_canvas = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize l'interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Titre
        title = QLabel("ÉTAPE 7: Visualisation graphique")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2196F3;")
        layout.addWidget(title)
        
        # Boutons de sélection
        button_layout = QHBoxLayout()
        
        hmt_btn = QPushButton("📊 Courbes HMT vs D")
        hmt_btn.clicked.connect(lambda: self.plot_graphs('hmt'))
        button_layout.addWidget(hmt_btn)
        
        system_btn = QPushButton("📈 Courbes système")
        system_btn.clicked.connect(lambda: self.plot_graphs('system'))
        button_layout.addWidget(system_btn)
        
        operating_btn = QPushButton("🎯 Point de fonctionnement")
        operating_btn.clicked.connect(lambda: self.plot_graphs('operating'))
        button_layout.addWidget(operating_btn)
        
        comparison_btn = QPushButton("💡 Comparaison solutions")
        comparison_btn.clicked.connect(lambda: self.plot_graphs('comparison'))
        button_layout.addWidget(comparison_btn)
        
        layout.addLayout(button_layout)
        
        # Frame pour les graphiques
        self.plot_frame = QWidget()
        self.plot_layout = QVBoxLayout(self.plot_frame)
        self.plot_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plot_frame)
        
        # Afficher les courbes HMT par défaut
        self.main_window.tabs.currentChanged.connect(self.on_tab_changed)
    
    def on_tab_changed(self, index):
        """Appelé quand on change d'onglet"""
        if index == 6 and self.main_window.hmt_results:  # Index graphiques
            if not self.current_canvas:
                self.plot_graphs('hmt')
    
    def clear_plot(self):
        """Nettoie le graphique actuel"""
        if self.current_canvas:
            self.plot_layout.removeWidget(self.current_canvas)
            self.current_canvas.deleteLater()
            self.current_canvas = None
    
    def plot_graphs(self, graph_type='hmt'):
        """Génère les graphiques selon le type"""
        self.clear_plot()
        
        if graph_type == 'hmt':
            self.plot_hmt_graphs()
        elif graph_type == 'system':
            self.plot_system_curves()
        elif graph_type == 'operating':
            self.plot_operating_point()
        elif graph_type == 'comparison':
            self.plot_comparison()
    
    def plot_hmt_graphs(self):
        """Graphiques HMT de base"""
        if not self.main_window.hmt_results:
            QMessageBox.warning(self, "Attention",
                              "Veuillez d'abord calculer la HMT")
            return
        
        fig = Figure(figsize=(14, 10))
        
        diameters = [r['D'] for r in self.main_window.hmt_results]
        hmts = [r['HMT'] for r in self.main_window.hmt_results]
        velocities = [r['V'] for r in self.main_window.hmt_results]
        reynolds = [r['Re'] for r in self.main_window.hmt_results]
        friction = [r['f'] for r in self.main_window.hmt_results]
        
        # Graphique 1: HMT vs Diamètre
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot(diameters, hmts, 'b-o', linewidth=2, markersize=8)
        ax1.set_xlabel('Diamètre (m)', fontweight='bold')
        ax1.set_ylabel('HMT (m)', fontweight='bold')
        ax1.set_title('HMT en fonction du Diamètre', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Graphique 2: Vitesse vs Diamètre
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot(diameters, velocities, 'r-s', linewidth=2, markersize=8)
        Vmin = float(self.main_window.input_tab.vmin_input.text())
        Vmax = float(self.main_window.input_tab.vmax_input.text())
        ax2.axhline(y=Vmin, color='g', linestyle='--', label=f'Vmin = {Vmin} m/s')
        ax2.axhline(y=Vmax, color='orange', linestyle='--', label=f'Vmax = {Vmax} m/s')
        ax2.set_xlabel('Diamètre (m)', fontweight='bold')
        ax2.set_ylabel('Vitesse (m/s)', fontweight='bold')
        ax2.set_title('Vitesse en fonction du Diamètre', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Graphique 3: Reynolds vs Diamètre
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot(diameters, reynolds, 'g-^', linewidth=2, markersize=8)
        ax3.axhline(y=2300, color='r', linestyle='--', label='Re critique (2300)')
        ax3.set_xlabel('Diamètre (m)', fontweight='bold')
        ax3.set_ylabel('Nombre de Reynolds', fontweight='bold')
        ax3.set_title('Reynolds en fonction du Diamètre', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Graphique 4: Coefficient de frottement
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.plot(diameters, friction, 'm-d', linewidth=2, markersize=8)
        ax4.set_xlabel('Diamètre (m)', fontweight='bold')
        ax4.set_ylabel('Coefficient de frottement', fontweight='bold')
        ax4.set_title('Coefficient de frottement', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        fig.suptitle('Analyses des Résultats HMT', fontsize=16, fontweight='bold')
        fig.tight_layout()
        
        self.current_canvas = FigureCanvas(fig)
        self.plot_layout.addWidget(self.current_canvas)
        self.current_canvas.draw()
    
    def plot_system_curves(self):
        """Courbes du système"""
        if not self.main_window.system_curves:
            QMessageBox.warning(self, "Attention",
                              "Veuillez d'abord calculer la HMT")
            return
        
        fig = Figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        
        for D, curve in self.main_window.system_curves.items():
            ax.plot(curve['Qs'], curve['HMTs'], '-o', linewidth=2, 
                   markersize=6, label=f'D = {D:.4f} m')
        
        ax.set_xlabel('Débit (m³/s)', fontweight='bold', fontsize=12)
        ax.set_ylabel('HMT système (m)', fontweight='bold', fontsize=12)
        ax.set_title('Courbes du système HMTs = f(Qs) pour différents diamètres',
                    fontweight='bold', fontsize=14)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        
        self.current_canvas = FigureCanvas(fig)
        self.plot_layout.addWidget(self.current_canvas)
        self.current_canvas.draw()
    
    def plot_operating_point(self):
        """Point de fonctionnement"""
        if not self.main_window.best_solution:
            QMessageBox.warning(self, "Attention",
                              "Veuillez d'abord trouver la solution optimale")
            return
        
        sol = self.main_window.best_solution
        D = sol.diameter
        
        # Trouver la pompe
        pump = None
        for p in self.main_window.pumps:
            if p.type == sol.pump_type:
                pump = p
                break
        
        if not pump:
            QMessageBox.warning(self, "Erreur", "Pompe non trouvée")
            return
        
        fig = Figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        
        # Courbe pompe
        Qp = np.array(pump.Qp.copy())
        Hp = np.array(pump.Hp.copy())
        
        if sol.configuration == 'Série' or sol.configuration == 'Mixte':
            Hp = Hp * sol.n_serie
        
        if sol.configuration == 'Parallèle' or sol.configuration == 'Mixte':
            Qp = Qp * sol.n_parallel
        
        ax.plot(Qp, Hp, 'b-', linewidth=2, label=f"Courbe pompe ({sol.configuration})")
        
        # Courbe système
        curve = self.main_window.system_curves[D]
        ax.plot(curve['Qs'], curve['HMTs'], 'r-', linewidth=2,
               label=f'Courbe système (D={D:.4f}m)')
        
        # Point de fonctionnement
        ax.plot(sol.Qf, sol.Hf, 'go', markersize=15, 
               label='Point de fonctionnement', zorder=5)
        
        ax.annotate(f"Qf={sol.Qf:.4f} m³/s\nHf={sol.Hf:.2f} m\nη={sol.efficiency*100:.1f}%",
                   xy=(sol.Qf, sol.Hf), xytext=(10, 10),
                   textcoords='offset points', fontsize=10,
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        ax.set_xlabel('Débit (m³/s)', fontweight='bold', fontsize=12)
        ax.set_ylabel('Hauteur (m)', fontweight='bold', fontsize=12)
        ax.set_title('Point de fonctionnement du système', fontweight='bold', fontsize=14)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        
        self.current_canvas = FigureCanvas(fig)
        self.plot_layout.addWidget(self.current_canvas)
        self.current_canvas.draw()
    
    def plot_comparison(self):
        """Comparaison des solutions"""
        if not self.main_window.solutions:
            QMessageBox.warning(self, "Attention",
                              "Veuillez d'abord trouver les solutions optimales")
            return
        
        top_solutions = self.main_window.solutions[:min(5, len(self.main_window.solutions))]
        
        fig = Figure(figsize=(14, 10))
        
        labels = [f"{s.pump_type}\n{s.configuration}\nD={s.diameter:.3f}m" 
                 for s in top_solutions]
        rendements = [s.efficiency*100 for s in top_solutions]
        debits = [s.Qf for s in top_solutions]
        hauteurs = [s.Hf for s in top_solutions]
        npsh_marges = [s.NPSH_margin for s in top_solutions]
        
        # Graphique 1: Rendements
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.bar(range(len(labels)), rendements, color='skyblue', edgecolor='black')
        ax1.set_xticks(range(len(labels)))
        ax1.set_xticklabels(labels, rotation=15, ha='right', fontsize=8)
        ax1.set_ylabel('Rendement (%)', fontweight='bold')
        ax1.set_title('Rendement des solutions', fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Graphique 2: Débits
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.bar(range(len(labels)), debits, color='lightgreen', edgecolor='black')
        ax2.set_xticks(range(len(labels)))
        ax2.set_xticklabels(labels, rotation=15, ha='right', fontsize=8)
        ax2.set_ylabel('Débit (m³/s)', fontweight='bold')
        ax2.set_title('Débit de fonctionnement', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Graphique 3: Hauteurs
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.bar(range(len(labels)), hauteurs, color='salmon', edgecolor='black')
        ax3.set_xticks(range(len(labels)))
        ax3.set_xticklabels(labels, rotation=15, ha='right', fontsize=8)
        ax3.set_ylabel('Hauteur (m)', fontweight='bold')
        ax3.set_title('Hauteur manométrique', fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Graphique 4: Marges NPSH
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.bar(range(len(labels)), npsh_marges, color='gold', edgecolor='black')
        ax4.set_xticks(range(len(labels)))
        ax4.set_xticklabels(labels, rotation=15, ha='right', fontsize=8)
        ax4.set_ylabel('Marge NPSH (m)', fontweight='bold')
        ax4.set_title('Marge de sécurité NPSH', fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')
        
        fig.suptitle('Comparaison des meilleures solutions', fontsize=16, fontweight='bold')
        fig.tight_layout()
        
        self.current_canvas = FigureCanvas(fig)
        self.plot_layout.addWidget(self.current_canvas)
        self.current_canvas.draw()