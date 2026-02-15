"""
Fenêtre principale de l'application PyQt5
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QTabWidget, QStatusBar, QMenuBar, QAction,
                             QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from views.tabs.input_tab import InputTab
from views.tabs.pump_tab import PumpTab
from views.tabs.hmt_tab import HMTTab
from views.tabs.optimal_tab import OptimalTab
from views.tabs.economic_tab import EconomicTab
from views.tabs.results_tab import ResultsTab
from views.tabs.graphs_tab import GraphsTab

from models.fluid_model import FluidModel
from models.pipe_model import PipeModel
from controllers.hmt_calculator import HMTCalculator
from controllers.npsh_calculator import NPSHCalculator
from controllers.pump_optimizer import PumpOptimizer
from controllers.economic_calculator import EconomicCalculator

from assets.styles.theme import get_stylesheet
from config import APP_TITLE, WINDOW_SIZE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Modèles
        self.fluid_model = FluidModel()
        self.pipe_model = PipeModel()
        
        # Contrôleurs
        self.hmt_calculator = HMTCalculator(self.fluid_model, self.pipe_model)
        self.npsh_calculator = NPSHCalculator(self.fluid_model, self.pipe_model)
        self.pump_optimizer = PumpOptimizer(self.hmt_calculator, self.npsh_calculator)
        self.economic_calculator = EconomicCalculator(self.fluid_model)
        
        # Données
        self.pumps = []
        self.hmt_results = []
        self.system_curves = {}
        self.solutions = []
        self.best_solution = None
        self.economic_data = None
        
        self.init_ui()
        self.create_menu_bar()
        self.create_status_bar()
        
        # Appliquer le thème
        self.setStyleSheet(get_stylesheet())
    
    def init_ui(self):
        """Initialize l'interface utilisateur"""
        self.setWindowTitle(APP_TITLE)
        
        # Taille de la fenêtre
        width, height = map(int, WINDOW_SIZE.split('x'))
        self.resize(width, height)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        layout.addWidget(self.tabs)
        
        # Créer les onglets
        self.input_tab = InputTab(self)
        self.pump_tab = PumpTab(self)
        self.hmt_tab = HMTTab(self)
        self.optimal_tab = OptimalTab(self)
        self.economic_tab = EconomicTab(self)
        self.results_tab = ResultsTab(self)
        self.graphs_tab = GraphsTab(self)
        
        # Ajouter les onglets
        self.tabs.addTab(self.input_tab, "📝 1. Données d'entrée")
        self.tabs.addTab(self.pump_tab, "⚙️ 2. Pompes")
        self.tabs.addTab(self.hmt_tab, "📊 3. Calcul HMT")
        self.tabs.addTab(self.optimal_tab, "🎯 4. Optimisation")
        self.tabs.addTab(self.economic_tab, "💰 5. Économie")
        self.tabs.addTab(self.results_tab, "📋 6. Résultats")
        self.tabs.addTab(self.graphs_tab, "📈 7. Graphiques")
        
        # Centrer la fenêtre
        self.center_window()
    
    def create_menu_bar(self):
        """Crée la barre de menu"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu('&Fichier')
        
        new_action = QAction('&Nouveau projet', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        export_action = QAction('&Exporter résultats', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction('&Quitter', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menu Aide
        help_menu = menubar.addMenu('&Aide')
        
        about_action = QAction('&À propos', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        doc_action = QAction('&Documentation', self)
        doc_action.setShortcut('F1')
        doc_action.triggered.connect(self.show_documentation)
        help_menu.addAction(doc_action)
    
    def create_status_bar(self):
        """Crée la barre d'état"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Prêt', 3000)
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        frame_geometry = self.frameGeometry()
        from PyQt5.QtWidgets import QDesktopWidget
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
    
    def new_project(self):
        """Crée un nouveau projet"""
        reply = QMessageBox.question(
            self, 'Nouveau projet',
            'Voulez-vous vraiment créer un nouveau projet?\nToutes les données non sauvegardées seront perdues.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Réinitialiser tous les modèles
            self.fluid_model = FluidModel()
            self.pipe_model = PipeModel()
            self.hmt_calculator = HMTCalculator(self.fluid_model, self.pipe_model)
            self.npsh_calculator = NPSHCalculator(self.fluid_model, self.pipe_model)
            self.pump_optimizer = PumpOptimizer(self.hmt_calculator, self.npsh_calculator)
            self.economic_calculator = EconomicCalculator(self.fluid_model)
            
            # Vider les données
            self.pumps.clear()
            self.hmt_results.clear()
            self.system_curves.clear()
            self.solutions.clear()
            self.best_solution = None
            self.economic_data = None
            
            # Réinitialiser les onglets
            self.input_tab.reset()
            self.pump_tab.update_pump_table()
            
            self.status_bar.showMessage('Nouveau projet créé', 3000)
            self.tabs.setCurrentIndex(0)
    
    def export_results(self):
        """Exporte les résultats"""
        if not self.best_solution:
            QMessageBox.warning(self, 'Attention', 
                              'Aucun résultat à exporter.\nVeuillez d\'abord effectuer les calculs.')
            return
        
        # Dialogue de sauvegarde
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Exporter les résultats',
            '', 'Fichiers texte (*.txt);;Fichiers JSON (*.json);;Tous les fichiers (*.*)'
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    self.results_tab.export_json(filename)
                else:
                    self.results_tab.export_txt(filename)
                
                QMessageBox.information(self, 'Succès', 
                                      f'Résultats exportés dans:\n{filename}')
                self.status_bar.showMessage(f'Résultats exportés: {filename}', 5000)
            except Exception as e:
                QMessageBox.critical(self, 'Erreur', 
                                   f'Erreur lors de l\'export:\n{str(e)}')
    
    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        QMessageBox.about(
            self, 'À propos',
            '<h2>Calculateur HMT Professionnel</h2>'
            '<p>Version 2.0</p>'
            '<p>Calculateur de Hauteur Manométrique Totale pour systèmes de pompage.</p>'
            '<p><b>Développé avec:</b></p>'
            '<ul>'
            '<li>Python 3.x</li>'
            '<li>PyQt5</li>'
            '<li>NumPy</li>'
            '<li>Matplotlib</li>'
            '</ul>'
            '<p>© 2024 - Tous droits réservés</p>'
        )
    
    def show_documentation(self):
        """Affiche la documentation"""
        doc_text = """
        <h2>Documentation - Calculateur HMT</h2>
        
        <h3>Étapes d'utilisation:</h3>
        <ol>
            <li><b>Données d'entrée:</b> Saisir les paramètres du système (fluide, géométrie, etc.)</li>
            <li><b>Pompes:</b> Importer ou créer les pompes disponibles</li>
            <li><b>Calcul HMT:</b> Choisir les diamètres et calculer les HMT</li>
            <li><b>Optimisation:</b> Trouver la configuration optimale</li>
            <li><b>Économie:</b> Calculer les coûts</li>
            <li><b>Résultats:</b> Voir et exporter les résultats finaux</li>
            <li><b>Graphiques:</b> Visualiser les courbes</li>
        </ol>
        
        <h3>Raccourcis clavier:</h3>
        <ul>
            <li><b>Ctrl+N:</b> Nouveau projet</li>
            <li><b>Ctrl+E:</b> Exporter résultats</li>
            <li><b>Ctrl+Q:</b> Quitter</li>
            <li><b>F1:</b> Documentation</li>
        </ul>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle('Documentation')
        msg.setTextFormat(Qt.RichText)
        msg.setText(doc_text)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
    
    def update_status(self, message, duration=3000):
        """Met à jour la barre d'état"""
        self.status_bar.showMessage(message, duration)