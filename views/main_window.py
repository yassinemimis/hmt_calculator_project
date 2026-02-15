"""
Fenêtre principale - Avec Logo
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget,
                             QStatusBar, QMenuBar, QAction, QMessageBox,
                             QFileDialog, QApplication, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap

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

from assets.styles.theme import get_stylesheet, is_small_screen, is_very_small_screen
from config import APP_TITLE, LOGO_PATH, LOGO_SMALL_PATH, LOGO_ICO_PATH
import os


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
        
        # Charger/créer le logo
        self.ensure_logo_exists()
        
        self.init_ui()
        self.create_menu_bar()
        self.create_status_bar()
        
        # Appliquer le thème responsive
        self.setStyleSheet(get_stylesheet())
        
        # Adapter la taille selon l'écran
        self.adapt_window_size()
        
        # Définir l'icône de la fenêtre
        self.set_window_icon()
    
    def ensure_logo_exists(self):
        """Vérifie et crée le logo si nécessaire"""
        if not os.path.exists(LOGO_PATH):
            try:
                from utils.logo_generator import create_gradient_logo
                create_gradient_logo()
                print("✓ Logo créé automatiquement")
            except Exception as e:
                print(f"⚠ Impossible de créer le logo: {e}")
    
    def set_window_icon(self):
        """Définit l'icône de la fenêtre"""
        try:
            # Essayer d'abord .ico (Windows)
            if os.path.exists(LOGO_ICO_PATH):
                self.setWindowIcon(QIcon(LOGO_ICO_PATH))
            # Sinon PNG
            elif os.path.exists(LOGO_PATH):
                self.setWindowIcon(QIcon(LOGO_PATH))
        except Exception as e:
            print(f"⚠ Erreur chargement icône: {e}")
    
    def adapt_window_size(self):
        """Adapte la taille de la fenêtre selon l'écran"""
        screen = QApplication.primaryScreen()
        if screen:
            screen_size = screen.size()
            screen_geometry = screen.availableGeometry()
            
            if is_very_small_screen():
                self.showMaximized()
            elif is_small_screen():
                width = int(screen_geometry.width() * 0.95)
                height = int(screen_geometry.height() * 0.95)
                self.resize(width, height)
                self.center_window()
            else:
                self.resize(1400, 900)
                self.center_window()
    
    def init_ui(self):
        """Initialize l'interface utilisateur"""
        self.setWindowTitle(APP_TITLE)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Marges adaptatives
        if is_very_small_screen():
            main_layout.setContentsMargins(5, 5, 5, 5)
        elif is_small_screen():
            main_layout.setContentsMargins(8, 8, 8, 8)
        else:
            main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header avec logo (optionnel)
        if not is_very_small_screen():
            header_widget = self.create_header()
            main_layout.addWidget(header_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        main_layout.addWidget(self.tabs)
        
        # Créer les onglets
        self.input_tab = InputTab(self)
        self.pump_tab = PumpTab(self)
        self.hmt_tab = HMTTab(self)
        self.optimal_tab = OptimalTab(self)
        self.economic_tab = EconomicTab(self)
        self.results_tab = ResultsTab(self)
        self.graphs_tab = GraphsTab(self)
        
        # Noms des onglets
        if is_very_small_screen():
            self.tabs.addTab(self.input_tab, "1. Données")
            self.tabs.addTab(self.pump_tab, "2. Pompes")
            self.tabs.addTab(self.hmt_tab, "3. HMT")
            self.tabs.addTab(self.optimal_tab, "4. Optimal")
            self.tabs.addTab(self.economic_tab, "5. Économie")
            self.tabs.addTab(self.results_tab, "6. Résultats")
            self.tabs.addTab(self.graphs_tab, "7. Graphes")
        else:
            self.tabs.addTab(self.input_tab, "📝 1. Données d'entrée")
            self.tabs.addTab(self.pump_tab, "⚙️ 2. Pompes")
            self.tabs.addTab(self.hmt_tab, "📊 3. Calcul HMT")
            self.tabs.addTab(self.optimal_tab, "🎯 4. Optimisation")
            self.tabs.addTab(self.economic_tab, "💰 5. Économie")
            self.tabs.addTab(self.results_tab, "📋 6. Résultats")
            self.tabs.addTab(self.graphs_tab, "📈 7. Graphiques")
    
    def create_header(self):
        """Crée l'en-tête avec logo"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        # Logo
        if os.path.exists(LOGO_SMALL_PATH):
            logo_label = QLabel()
            pixmap = QPixmap(LOGO_SMALL_PATH)
            scaled_pixmap = pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            header_layout.addWidget(logo_label)
        
        # Titre
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(10, 0, 0, 0)
        title_layout.setSpacing(2)
        
        title_label = QLabel("Calculateur HMT Professionnel")
        title_label.setStyleSheet("""
            font-size: 16pt;
            font-weight: bold;
            color: #1A73E8;
        """)
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Analyse hydraulique de systèmes de pompage")
        subtitle_label.setStyleSheet("""
            font-size: 9pt;
            color: #5F6368;
        """)
        title_layout.addWidget(subtitle_label)
        
        header_layout.addWidget(title_widget)
        header_layout.addStretch()
        
        # Version
        version_label = QLabel("v2.0")
        version_label.setStyleSheet("""
            font-size: 9pt;
            color: #9AA0A6;
            padding: 5px 10px;
            background: #F1F3F4;
            border-radius: 12px;
        """)
        header_layout.addWidget(version_label)
        
        return header_widget
    
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
        
        # Menu Affichage
        view_menu = menubar.addMenu('&Affichage')
        
        fullscreen_action = QAction('&Plein écran', self)
        fullscreen_action.setShortcut('F11')
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        maximize_action = QAction('&Maximiser', self)
        maximize_action.triggered.connect(self.showMaximized)
        view_menu.addAction(maximize_action)
        
        restore_action = QAction('&Restaurer', self)
        restore_action.triggered.connect(self.showNormal)
        view_menu.addAction(restore_action)
        
        # Menu Aide
        help_menu = menubar.addMenu('&Aide')
        
        about_action = QAction('&À propos', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        doc_action = QAction('&Documentation', self)
        doc_action.setShortcut('F1')
        doc_action.triggered.connect(self.show_documentation)
        help_menu.addAction(doc_action)
    
    def toggle_fullscreen(self, checked):
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()
    
    def create_status_bar(self):
        """Crée la barre d'état"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        screen = QApplication.primaryScreen()
        if screen:
            size = screen.size()
            self.status_bar.showMessage(
                f'Prêt | Résolution: {size.width()}x{size.height()}', 5000
            )
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            window_geometry = self.frameGeometry()
            center_point = screen_geometry.center()
            window_geometry.moveCenter(center_point)
            self.move(window_geometry.topLeft())
    
    def new_project(self):
        """Crée un nouveau projet"""
        reply = QMessageBox.question(
            self, 'Nouveau projet',
            'Voulez-vous vraiment créer un nouveau projet?\nToutes les données non sauvegardées seront perdues.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.fluid_model = FluidModel()
            self.pipe_model = PipeModel()
            self.hmt_calculator = HMTCalculator(self.fluid_model, self.pipe_model)
            self.npsh_calculator = NPSHCalculator(self.fluid_model, self.pipe_model)
            self.pump_optimizer = PumpOptimizer(self.hmt_calculator, self.npsh_calculator)
            self.economic_calculator = EconomicCalculator(self.fluid_model)
            
            self.pumps.clear()
            self.hmt_results.clear()
            self.system_curves.clear()
            self.solutions.clear()
            self.best_solution = None
            self.economic_data = None
            
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
        
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Exporter les résultats',
            '', 'Fichiers PDF (*.pdf);;Fichiers texte (*.txt);;Fichiers JSON (*.json)'
        )
        
        if filename:
            try:
                if filename.endswith('.pdf'):
                    self.results_tab.export_pdf(filename)
                elif filename.endswith('.json'):
                    self.results_tab.export_json(filename)
                else:
                    self.results_tab.export_txt(filename)
                
                QMessageBox.information(self, 'Succès',
                                      f'Résultats exportés dans:\n{filename}')
                self.status_bar.showMessage(f'Export réussi: {filename}', 5000)
            except Exception as e:
                QMessageBox.critical(self, 'Erreur',
                                   f'Erreur lors de l\'export:\n{str(e)}')
    
    def show_about(self):
        """Affiche À propos avec logo"""
        msg = QMessageBox(self)
        msg.setWindowTitle('À propos')
        
        # Ajouter le logo
        if os.path.exists(LOGO_SMALL_PATH):
            pixmap = QPixmap(LOGO_SMALL_PATH)
            msg.setIconPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        screen = QApplication.primaryScreen()
        screen_info = ""
        if screen:
            size = screen.size()
            screen_info = f"<p><b>Résolution écran:</b> {size.width()}x{size.height()}</p>"
        
        msg.setText(
            '<h2>Calculateur HMT Professionnel</h2>'
            '<p>Version 2.0 - Industrial Engineering Design</p>'
        )
        
        msg.setInformativeText(
            '<p>Calculateur de Hauteur Manométrique Totale.</p>'
            f'{screen_info}'
            '<p><b>Technologies:</b></p>'
            '<ul>'
            '<li>Python 3.8+</li>'
            '<li>PyQt5 (Interface responsive)</li>'
            '<li>NumPy</li>'
            '<li>Matplotlib</li>'
            '<li>ReportLab</li>'
            '</ul>'
            '<p>© 2024 - Tous droits réservés</p>'
        )
        
        msg.exec_()
    
    def show_documentation(self):
        """Affiche la documentation"""
        doc_text = """
        <h2>Documentation - Calculateur HMT</h2>
        
        <h3>Interface Responsive:</h3>
        <p>L'application s'adapte automatiquement à votre écran.</p>
        
        <h3>Raccourcis clavier:</h3>
        <ul>
            <li><b>Ctrl+N:</b> Nouveau projet</li>
            <li><b>Ctrl+E:</b> Exporter résultats</li>
            <li><b>F11:</b> Plein écran</li>
            <li><b>F1:</b> Documentation</li>
            <li><b>Ctrl+Q:</b> Quitter</li>
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