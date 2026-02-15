"""
Onglet de saisie des données d'entrée
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QLabel, QLineEdit, QPushButton, QComboBox,
                             QGridLayout, QMessageBox, QScrollArea)
from PyQt5.QtCore import Qt
from config import DEFAULT_VMIN, DEFAULT_VMAX, FRICTION_METHODS, LOSS_METHODS


class InputTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """Initialize l'interface"""
        # Scroll area pour le contenu
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        content_widget = QWidget()
        scroll.setWidget(content_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(15)
        
        # Titre
        title = QLabel("ÉTAPE 1: Saisie des données du système")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2196F3;")
        layout.addWidget(title)
        
        # Section 1: Environnement
        env_group = self.create_environment_section()
        layout.addWidget(env_group)
        
        # Section 2: Géométrie
        geo_group = self.create_geometry_section()
        layout.addWidget(geo_group)
        
        # Section 3: Fluide
        fluid_group = self.create_fluid_section()
        layout.addWidget(fluid_group)
        
        # Section 4: Fonctionnement
        func_group = self.create_operation_section()
        layout.addWidget(func_group)
        
        # Section 5: Limites
        limits_group = self.create_limits_section()
        layout.addWidget(limits_group)
        
        # Section 6: Méthodes
        methods_group = self.create_methods_section()
        layout.addWidget(methods_group)
        
        # Bouton de validation
        validate_btn = QPushButton("✓ Valider les données")
        validate_btn.setMinimumHeight(45)
        validate_btn.setProperty("class", "success")
        validate_btn.clicked.connect(self.validate_data)
        layout.addWidget(validate_btn)
        
        layout.addStretch()
    
    def create_environment_section(self):
        """Crée la section environnement"""
        group = QGroupBox("Données de Site (Environnement)")
        grid = QGridLayout()
        
        # Patm
        grid.addWidget(QLabel("Pression atmosphérique Patm (Pa):"), 0, 0)
        self.patm_input = QLineEdit("101325")
        grid.addWidget(self.patm_input, 0, 1)
        
        # OU Altitude
        grid.addWidget(QLabel("OU Altitude Zalt (m):"), 1, 0)
        self.zalt_input = QLineEdit()
        grid.addWidget(self.zalt_input, 1, 1)
        
        calc_patm_btn = QPushButton("Calculer Patm")
        calc_patm_btn.clicked.connect(self.calculate_patm_from_altitude)
        grid.addWidget(calc_patm_btn, 1, 2)
        
        # g
        grid.addWidget(QLabel("Accélération pesanteur g (m/s²):"), 2, 0)
        self.g_input = QLineEdit("9.81")
        grid.addWidget(self.g_input, 2, 1)
        
        group.setLayout(grid)
        return group
    
    def create_geometry_section(self):
        """Crée la section géométrie"""
        group = QGroupBox("Données de Réseau (Géométrie)")
        grid = QGridLayout()
        
        grid.addWidget(QLabel("Longueur aspiration Lasp (m):"), 0, 0)
        self.lasp_input = QLineEdit("10")
        grid.addWidget(self.lasp_input, 0, 1)
        
        grid.addWidget(QLabel("Longueur refoulement Lref (m):"), 1, 0)
        self.lref_input = QLineEdit("50")
        grid.addWidget(self.lref_input, 1, 1)
        
        grid.addWidget(QLabel("Cote départ Zdep (m):"), 2, 0)
        self.zdep_input = QLineEdit("0")
        grid.addWidget(self.zdep_input, 2, 1)
        
        grid.addWidget(QLabel("Cote arrivée Zarr (m):"), 3, 0)
        self.zarr_input = QLineEdit("20")
        grid.addWidget(self.zarr_input, 3, 1)
        
        group.setLayout(grid)
        return group
    
    def create_fluid_section(self):
        """Crée la section fluide"""
        group = QGroupBox("Données de Fluide")
        grid = QGridLayout()
        
        grid.addWidget(QLabel("Température T (°C):"), 0, 0)
        self.temp_input = QLineEdit("20")
        grid.addWidget(self.temp_input, 0, 1)
        
        grid.addWidget(QLabel("Masse volumique ρ (kg/m³):"), 1, 0)
        self.rho_input = QLineEdit("1000")
        grid.addWidget(self.rho_input, 1, 1)
        
        grid.addWidget(QLabel("Viscosité dynamique μ (Pa·s):"), 2, 0)
        self.mu_input = QLineEdit("0.001")
        grid.addWidget(self.mu_input, 2, 1)
        
        grid.addWidget(QLabel("Pression vapeur saturante Pv (Pa):"), 3, 0)
        self.pv_input = QLineEdit("2338")
        grid.addWidget(self.pv_input, 3, 1)
        
        grid.addWidget(QLabel("Rugosité absolue ε (m):"), 4, 0)
        self.epsilon_input = QLineEdit("0.00015")
        grid.addWidget(self.epsilon_input, 4, 1)
        
        group.setLayout(grid)
        return group
    
    def create_operation_section(self):
        """Crée la section fonctionnement"""
        group = QGroupBox("Données de Fonctionnement")
        grid = QGridLayout()
        
        grid.addWidget(QLabel("Débit volumique Q (m³/s):"), 0, 0)
        self.q_input = QLineEdit("0.05")
        grid.addWidget(self.q_input, 0, 1)
        
        group.setLayout(grid)
        return group
    
    def create_limits_section(self):
        """Crée la section limites"""
        group = QGroupBox("Limites de Conception")
        grid = QGridLayout()
        
        grid.addWidget(QLabel("Vitesse minimale Vmin (m/s):"), 0, 0)
        self.vmin_input = QLineEdit(str(DEFAULT_VMIN))
        grid.addWidget(self.vmin_input, 0, 1)
        
        grid.addWidget(QLabel("Vitesse maximale Vmax (m/s):"), 1, 0)
        self.vmax_input = QLineEdit(str(DEFAULT_VMAX))
        grid.addWidget(self.vmax_input, 1, 1)
        
        group.setLayout(grid)
        return group
    
    def create_methods_section(self):
        """Crée la section méthodes"""
        group = QGroupBox("Méthodes de Calcul")
        grid = QGridLayout()
        
        # Méthode de frottement
        grid.addWidget(QLabel("Coefficient de frottement:"), 0, 0)
        self.friction_combo = QComboBox()
        self.friction_combo.addItems(FRICTION_METHODS)
        self.friction_combo.setCurrentText('Swamee-Jain')
        grid.addWidget(self.friction_combo, 0, 1)
        
        # Méthode pertes singulières
        grid.addWidget(QLabel("Pertes singulières:"), 1, 0)
        self.loss_combo = QComboBox()
        self.loss_combo.addItems(LOSS_METHODS)
        self.loss_combo.currentTextChanged.connect(self.on_loss_method_changed)
        grid.addWidget(self.loss_combo, 1, 1)
        
        # Paramètres pertes
        self.loss_params_widget = QWidget()
        self.loss_params_layout = QGridLayout(self.loss_params_widget)
        grid.addWidget(self.loss_params_widget, 2, 0, 1, 2)
        
        self.create_coefficient_inputs()
        
        group.setLayout(grid)
        return group
    
    def create_coefficient_inputs(self):
        """Crée les inputs pour coefficients"""
        # Nettoyer
        while self.loss_params_layout.count():
            child = self.loss_params_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.loss_params_layout.addWidget(QLabel("Kasp (aspiration):"), 0, 0)
        self.kasp_input = QLineEdit("1.5")
        self.loss_params_layout.addWidget(self.kasp_input, 0, 1)
        
        self.loss_params_layout.addWidget(QLabel("Kref (refoulement):"), 0, 2)
        self.kref_input = QLineEdit("2.0")
        self.loss_params_layout.addWidget(self.kref_input, 0, 3)
    
    def create_percentage_input(self):
        """Crée l'input pour pourcentage"""
        # Nettoyer
        while self.loss_params_layout.count():
            child = self.loss_params_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.loss_params_layout.addWidget(QLabel("Pourcentage e (ex: 0.1 pour 10%):"), 0, 0)
        self.percentage_input = QLineEdit("0.1")
        self.loss_params_layout.addWidget(self.percentage_input, 0, 1)
    
    def on_loss_method_changed(self, text):
        """Changement de méthode de pertes"""
        if text == 'Coefficients':
            self.create_coefficient_inputs()
        else:
            self.create_percentage_input()
    
    def calculate_patm_from_altitude(self):
        """Calcule Patm depuis altitude"""
        try:
            zalt = float(self.zalt_input.text())
            patm = self.main_window.npsh_calculator.calculate_patm_from_altitude(zalt)
            self.patm_input.setText(f"{patm:.2f}")
            QMessageBox.information(self, "Succès", 
                                  f"Patm calculé: {patm:.2f} Pa")
        except ValueError:
            QMessageBox.warning(self, "Erreur", 
                              "Veuillez entrer une altitude valide")
    
    def validate_data(self):
        """Valide les données saisies"""
        try:
            # Mettre à jour les modèles
            self.update_models()
            
            QMessageBox.information(self, "✓ Validation réussie",
                                  "Toutes les données sont valides.\n"
                                  "Vous pouvez passer à l'étape suivante.")
            
            self.main_window.update_status("Données validées", 3000)
            self.main_window.tabs.setCurrentIndex(1)
        
        except Exception as e:
            QMessageBox.critical(self, "Erreur de validation",
                               f"Erreur: {str(e)}")
    
    def update_models(self):
        """Met à jour les modèles avec les données saisies"""
        # Fluid model
        self.main_window.fluid_model.temperature = float(self.temp_input.text())
        self.main_window.fluid_model.density = float(self.rho_input.text())
        self.main_window.fluid_model.viscosity = float(self.mu_input.text())
        self.main_window.fluid_model.vapor_pressure = float(self.pv_input.text())
        self.main_window.fluid_model.roughness = float(self.epsilon_input.text())
        
        # Pipe model
        self.main_window.pipe_model.L_aspiration = float(self.lasp_input.text())
        self.main_window.pipe_model.L_refoulement = float(self.lref_input.text())
        self.main_window.pipe_model.Z_depart = float(self.zdep_input.text())
        self.main_window.pipe_model.Z_arrivee = float(self.zarr_input.text())
        
        # NPSH calculator
        self.main_window.npsh_calculator.Patm = float(self.patm_input.text())
        self.main_window.npsh_calculator.g = float(self.g_input.text())
        
        # HMT calculator
        self.main_window.hmt_calculator.g = float(self.g_input.text())
    
    def reset(self):
        """Réinitialise le formulaire"""
        self.patm_input.setText("101325")
        self.zalt_input.clear()
        self.g_input.setText("9.81")
        self.lasp_input.setText("10")
        self.lref_input.setText("50")
        self.zdep_input.setText("0")
        self.zarr_input.setText("20")
        self.temp_input.setText("20")
        self.rho_input.setText("1000")
        self.mu_input.setText("0.001")
        self.pv_input.setText("2338")
        self.epsilon_input.setText("0.00015")
        self.q_input.setText("0.05")
        self.vmin_input.setText(str(DEFAULT_VMIN))
        self.vmax_input.setText(str(DEFAULT_VMAX))