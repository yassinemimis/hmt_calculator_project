"""
Onglet de saisie des données d'entrée — Responsive PyQt5
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QLabel, QLineEdit, QPushButton, QComboBox,
                             QGridLayout, QMessageBox, QScrollArea,
                             QSizePolicy, QFrame, QSpacerItem)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from config import DEFAULT_VMIN, DEFAULT_VMAX, FRICTION_METHODS, LOSS_METHODS


class InputTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Scroll principal
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content_widget = QWidget()
        content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        scroll.setWidget(content_widget)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

        layout = QVBoxLayout(content_widget)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # ── Titre ────────────────────────────────────────────────────
        title = QLabel("ÉTAPE 1 : Saisie des données du système")
        title.setStyleSheet(
            "font-size: 15pt; font-weight: bold; color: #2196F3; "
            "padding-bottom: 4px;"
        )
        title.setWordWrap(True)
        layout.addWidget(title)

        # ── Ligne 1 : Environnement + Géométrie (côte à côte) ────────
        row1 = QHBoxLayout()
        row1.setSpacing(12)
        env_group  = self.create_environment_section()
        geo_group  = self.create_geometry_section()
        env_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        geo_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        row1.addWidget(env_group, 1)
        row1.addWidget(geo_group, 1)
        layout.addLayout(row1)

        # ── Ligne 2 : Fluide + (Fonctionnement + Limites empilés) ────
        row2 = QHBoxLayout()
        row2.setSpacing(12)

        fluid_group = self.create_fluid_section()
        fluid_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        row2.addWidget(fluid_group, 1)

        right_col = QVBoxLayout()
        right_col.setSpacing(12)
        func_group   = self.create_operation_section()
        limits_group = self.create_limits_section()
        func_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        limits_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        right_col.addWidget(func_group)
        right_col.addWidget(limits_group)
        right_col.addStretch()
        row2.addLayout(right_col, 1)

        layout.addLayout(row2)

        # ── Ligne 3 : Méthodes (pleine largeur) ──────────────────────
        methods_group = self.create_methods_section()
        methods_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(methods_group)

        # ── Bouton valider ────────────────────────────────────────────
        validate_btn = QPushButton("✓  Valider les données")
        validate_btn.setMinimumHeight(44)
        validate_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        validate_btn.setStyleSheet(
            "font-size: 12pt; font-weight: bold; "
            "background-color: #4CAF50; color: white; "
            "border-radius: 6px; padding: 6px 20px;"
        )
        validate_btn.clicked.connect(self.validate_data)
        layout.addWidget(validate_btn)

        layout.addStretch()

    # ── Helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _make_field(label_text, default="", placeholder=""):
        """Retourne (QLabel, QLineEdit) stylisés et responsives."""
        lbl = QLabel(label_text)
        lbl.setWordWrap(True)
        lbl.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        field = QLineEdit(default)
        if placeholder:
            field.setPlaceholderText(placeholder)
        field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        field.setMinimumHeight(32)
        return lbl, field

    @staticmethod
    def _grid_setup(group):
        """Crée un QGridLayout responsive dans un QGroupBox."""
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)      # colonne valeur s'étire
        grid.setSpacing(8)
        group.setLayout(grid)
        return grid

    # ── Sections ──────────────────────────────────────────────────────

    def create_environment_section(self):
        group = QGroupBox("🌍  Environnement")
        grid  = self._grid_setup(group)

        lbl, self.patm_input = self._make_field("Pression atm. Pa (Pa):", "101325")
        grid.addWidget(lbl, 0, 0)
        grid.addWidget(self.patm_input, 0, 1)

        lbl2, self.zalt_input = self._make_field("OU Altitude Zalt (m):", "", "optionnel")
        grid.addWidget(lbl2, 1, 0)

        alt_row = QHBoxLayout()
        alt_row.addWidget(self.zalt_input)
        calc_btn = QPushButton("Calculer")
        calc_btn.setFixedWidth(80)
        calc_btn.setMinimumHeight(32)
        calc_btn.clicked.connect(self.calculate_patm_from_altitude)
        alt_row.addWidget(calc_btn)
        grid.addLayout(alt_row, 1, 1)

        lbl3, self.g_input = self._make_field("Pesanteur g (m/s²):", "9.81")
        grid.addWidget(lbl3, 2, 0)
        grid.addWidget(self.g_input, 2, 1)

        return group

    def create_geometry_section(self):
        group = QGroupBox("📐  Réseau (Géométrie)")
        grid  = self._grid_setup(group)

        fields = [
            ("L_asp — Aspiration (m):",   "lasp_input",   "10"),
            ("L_ref — Refoulement (m):",  "lref_input",   "50"),
            ("Z_dep — Cote départ (m):",  "zdep_input",   "0"),
            ("Z_arr — Cote arrivée (m):", "zarr_input",   "20"),
            ("Z_pompe — Axe pompe (m):",  "zpompe_input", "2"),
        ]
        for row, (label, attr, default) in enumerate(fields):
            lbl, field = self._make_field(label, default)
            setattr(self, attr, field)
            grid.addWidget(lbl, row, 0)
            grid.addWidget(field, row, 1)

        return group

    def create_fluid_section(self):
        group = QGroupBox("💧  Fluide")
        grid  = self._grid_setup(group)

        fields = [
            ("Température T (°C):",          "temp_input",    "20"),
            ("Masse volumique ρ (kg/m³):",   "rho_input",     "1000"),
            ("Viscosité dynamique μ (Pa·s):","mu_input",      "0.001"),
            ("Pression vapeur Pv (Pa):",     "pv_input",      "2338"),
            ("Rugosité absolue ε (m):",      "epsilon_input", "0.00015"),
        ]
        for row, (label, attr, default) in enumerate(fields):
            lbl, field = self._make_field(label, default)
            setattr(self, attr, field)
            grid.addWidget(lbl, row, 0)
            grid.addWidget(field, row, 1)

        return group

    def create_operation_section(self):
        group = QGroupBox("⚙️  Fonctionnement")
        grid  = self._grid_setup(group)

        lbl, self.q_input = self._make_field("Débit volumique Q (m³/s):", "0.05")
        grid.addWidget(lbl, 0, 0)
        grid.addWidget(self.q_input, 0, 1)

        return group

    def create_limits_section(self):
        group = QGroupBox("🚦  Limites de Conception")
        grid  = self._grid_setup(group)

        lbl1, self.vmin_input = self._make_field("V_min (m/s):", str(DEFAULT_VMIN))
        lbl2, self.vmax_input = self._make_field("V_max (m/s):", str(DEFAULT_VMAX))

        grid.addWidget(lbl1, 0, 0)
        grid.addWidget(self.vmin_input, 0, 1)
        grid.addWidget(lbl2, 1, 0)
        grid.addWidget(self.vmax_input, 1, 1)

        return group

    def create_methods_section(self):
        group = QGroupBox("🔧  Méthodes de Calcul")
        grid  = QGridLayout()
        grid.setColumnStretch(1, 1)
        grid.setSpacing(8)
        group.setLayout(grid)

        # Frottement
        grid.addWidget(QLabel("Coefficient de frottement:"), 0, 0)
        self.friction_combo = QComboBox()
        self.friction_combo.addItems(FRICTION_METHODS)
        self.friction_combo.setCurrentText('Swamee-Jain')
        self.friction_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.friction_combo.setMinimumHeight(32)
        grid.addWidget(self.friction_combo, 0, 1)

        # Pertes singulières
        grid.addWidget(QLabel("Pertes singulières:"), 1, 0)
        self.loss_combo = QComboBox()
        self.loss_combo.addItems(LOSS_METHODS)
        self.loss_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.loss_combo.setMinimumHeight(32)
        self.loss_combo.currentTextChanged.connect(self.on_loss_method_changed)
        grid.addWidget(self.loss_combo, 1, 1)

        # Zone paramètres pertes
        self.loss_params_widget = QWidget()
        self.loss_params_layout = QGridLayout(self.loss_params_widget)
        self.loss_params_layout.setColumnStretch(1, 1)
        self.loss_params_layout.setColumnStretch(3, 1)
        self.loss_params_layout.setContentsMargins(0, 4, 0, 0)
        grid.addWidget(self.loss_params_widget, 2, 0, 1, 2)

        self.create_coefficient_inputs()
        return group

    # ── Pertes ────────────────────────────────────────────────────────

    def create_coefficient_inputs(self):
        self._clear_loss_params()

        lbl1 = QLabel("Kasp (aspiration):")
        self.kasp_input = QLineEdit("1.5")
        self.kasp_input.setMinimumHeight(32)
        self.kasp_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        lbl2 = QLabel("Kref (refoulement):")
        self.kref_input = QLineEdit("2.0")
        self.kref_input.setMinimumHeight(32)
        self.kref_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.loss_params_layout.addWidget(lbl1,            0, 0)
        self.loss_params_layout.addWidget(self.kasp_input, 0, 1)
        self.loss_params_layout.addWidget(lbl2,            0, 2)
        self.loss_params_layout.addWidget(self.kref_input, 0, 3)

    def create_percentage_input(self):
        self._clear_loss_params()

        lbl = QLabel("Pourcentage e (ex: 0.1 pour 10%):")
        self.percentage_input = QLineEdit("0.1")
        self.percentage_input.setMinimumHeight(32)
        self.percentage_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.loss_params_layout.addWidget(lbl,                    0, 0)
        self.loss_params_layout.addWidget(self.percentage_input,  0, 1)

    def _clear_loss_params(self):
        while self.loss_params_layout.count():
            child = self.loss_params_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_loss_method_changed(self, text):
        if text == 'Coefficients':
            self.create_coefficient_inputs()
        else:
            self.create_percentage_input()

    # ── Actions ───────────────────────────────────────────────────────

    def calculate_patm_from_altitude(self):
        try:
            zalt = float(self.zalt_input.text())
            patm = self.main_window.npsh_calculator.calculate_patm_from_altitude(zalt)
            self.patm_input.setText(f"{patm:.2f}")
            QMessageBox.information(self, "Succès", f"Pa calculé : {patm:.2f} Pa")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une altitude valide")

    def validate_data(self):
        try:
            self.update_models()
            QMessageBox.information(self, "✓ Validation réussie",
                                    "Toutes les données sont valides.\n"
                                    "Vous pouvez passer à l'étape suivante.")
            self.main_window.update_status("Données validées", 3000)
            self.main_window.tabs.setCurrentIndex(1)
        except Exception as e:
            QMessageBox.critical(self, "Erreur de validation", f"Erreur : {str(e)}")

    def update_models(self):
        fm = self.main_window.fluid_model
        fm.temperature    = float(self.temp_input.text())
        fm.density        = float(self.rho_input.text())
        fm.viscosity      = float(self.mu_input.text())
        fm.vapor_pressure = float(self.pv_input.text())
        fm.roughness      = float(self.epsilon_input.text())

        pm = self.main_window.pipe_model
        pm.L_aspiration  = float(self.lasp_input.text())
        pm.L_refoulement = float(self.lref_input.text())
        pm.Z_depart      = float(self.zdep_input.text())
        pm.Z_arrivee     = float(self.zarr_input.text())
        pm.Z_pompe       = float(self.zpompe_input.text())

        self.main_window.npsh_calculator.Patm = float(self.patm_input.text())
        self.main_window.npsh_calculator.g    = float(self.g_input.text())
        self.main_window.hmt_calculator.g     = float(self.g_input.text())

    def get_loss_kwargs(self):
        loss_method = self.loss_combo.currentText()
        kwargs = {'loss_method': loss_method}
        if loss_method == 'Coefficients':
            kwargs['Kasp'] = float(self.kasp_input.text())
            kwargs['Kref'] = float(self.kref_input.text())
        else:
            kwargs['percentage'] = float(self.percentage_input.text())
        return kwargs

    def reset(self):
        self.patm_input.setText("101325")
        self.zalt_input.clear()
        self.g_input.setText("9.81")
        self.lasp_input.setText("10")
        self.lref_input.setText("50")
        self.zdep_input.setText("0")
        self.zarr_input.setText("20")
        self.zpompe_input.setText("2")
        self.temp_input.setText("20")
        self.rho_input.setText("1000")
        self.mu_input.setText("0.001")
        self.pv_input.setText("2338")
        self.epsilon_input.setText("0.00015")
        self.q_input.setText("0.05")
        self.vmin_input.setText(str(DEFAULT_VMIN))
        self.vmax_input.setText(str(DEFAULT_VMAX))