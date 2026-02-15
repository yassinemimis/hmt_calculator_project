"""
Onglet de saisie des données d'entrée - Avec système d'aide
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QLineEdit, QComboBox,
                             QScrollArea, QMessageBox, QFrame, QToolButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
from config import DEFAULT_VMIN, DEFAULT_VMAX, FRICTION_METHODS, LOSS_METHODS
from views.widgets.custom_widgets import Card, SectionHeader, InfoBox, IconButton


class InputTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """Initialize l'interface"""
        # Layout principal avec scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        content_widget = QWidget()
        scroll.setWidget(content_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = SectionHeader(
            "ÉTAPE 1 : Saisie des données du système",
            "Configurez les paramètres environnementaux, géométriques et du fluide"
        )
        layout.addWidget(header)
        
        # Info box
        info = InfoBox(
            "Remplissez tous les champs requis. Utilisez les icônes ℹ�� pour obtenir de l'aide.",
            "info"
        )
        layout.addWidget(info)
        
        # Grid pour organiser les cards
        cards_layout = QGridLayout()
        cards_layout.setSpacing(16)
        
        # Card 1: Environnement
        env_card = self.create_environment_card()
        cards_layout.addWidget(env_card, 0, 0)
        
        # Card 2: Géométrie
        geo_card = self.create_geometry_card()
        cards_layout.addWidget(geo_card, 0, 1)
        
        # Card 3: Fluide
        fluid_card = self.create_fluid_card()
        cards_layout.addWidget(fluid_card, 1, 0)
        
        # Card 4: Fonctionnement
        func_card = self.create_operation_card()
        cards_layout.addWidget(func_card, 1, 1)
        
        # Card 5: Limites
        limits_card = self.create_limits_card()
        cards_layout.addWidget(limits_card, 2, 0)
        
        # Card 6: Méthodes
        methods_card = self.create_methods_card()
        cards_layout.addWidget(methods_card, 2, 1)
        
        layout.addLayout(cards_layout)
        
        # Bouton de validation
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        validate_btn = IconButton("✓  Valider les données et continuer", "")
        validate_btn.setProperty("class", "success")
        validate_btn.setMinimumWidth(280)
        validate_btn.setMinimumHeight(48)
        validate_btn.clicked.connect(self.validate_data)
        button_layout.addWidget(validate_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def create_help_button(self, help_text):
        """Crée un bouton d'aide avec tooltip"""
        help_btn = QToolButton()
        help_btn.setText("ℹ️")
        help_btn.setStyleSheet("""
            QToolButton {
                border: none;
                background: transparent;
                font-size: 14pt;
                padding: 0px;
                margin: 0px;
            }
            QToolButton:hover {
                background: #E8F0FE;
                border-radius: 12px;
            }
        """)
        help_btn.setToolTip(help_text)
        help_btn.setCursor(QCursor(Qt.PointingHandCursor))
        help_btn.clicked.connect(lambda: self.show_help_dialog(help_text))
        return help_btn
    
    def show_help_dialog(self, text):
        """Affiche une boîte de dialogue d'aide détaillée"""
        QMessageBox.information(self, "ℹ️ Aide", text)
    
    def add_field_with_help(self, grid, row, label_text, widget, help_text):
        """Ajoute un champ avec label et bouton d'aide"""
        # Layout horizontal pour label + help
        label_layout = QHBoxLayout()
        label = QLabel(label_text)
        label_layout.addWidget(label)
        
        help_btn = self.create_help_button(help_text)
        label_layout.addWidget(help_btn)
        label_layout.addStretch()
        
        grid.addLayout(label_layout, row, 0)
        grid.addWidget(widget, row, 1)
        
        # Tooltip sur le widget aussi
        widget.setToolTip(help_text)
    
    def create_environment_card(self):
        """Card Environnement avec aide"""
        card = Card("🌍 Données de Site (Environnement)")
        card_layout = card.layout()
        
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(1, 1)
        
        # Patm
        self.patm_input = QLineEdit("101325")
        self.patm_input.setPlaceholderText("Ex: 101325")
        self.add_field_with_help(
            grid, 0,
            "Pression atmosphérique Patm (Pa) :",
            self.patm_input,
            "<b>Pression atmosphérique (Patm)</b><br><br>"
            "Pression de l'air ambiant au niveau du site.<br><br>"
            "<b>Valeur standard :</b> 101325 Pa (au niveau de la mer)<br>"
            "<b>Effet :</b> Diminue avec l'altitude (~12 Pa/m)<br>"
            "<b>Exemple :</b><br>"
            "• Niveau mer : 101325 Pa<br>"
            "• 1000m altitude : ~89875 Pa<br><br>"
            "💡 <i>Vous pouvez calculer automatiquement depuis l'altitude</i>"
        )
        
        # Altitude
        # self.zalt_input = QLineEdit()
        # self.zalt_input.setPlaceholderText("Ex: 1000")
        # self.add_field_with_help(
        #     grid, 1,
        #     "OU Altitude Zalt (m) :",
        #     self.zalt_input,
        #     "<b>Altitude du site (Zalt)</b><br><br>"
        #     "Hauteur au-dessus du niveau de la mer.<br><br>"
        #     "<b>Usage :</b> Permet de calculer automatiquement Patm<br>"
        #     "<b>Formule :</b> Patm = P₀ × (1 - 0.0065×h/288.15)^5.255<br>"
        #     "<b>Exemple :</b><br>"
        #     "• Alger : ~0-200 m<br>"
        #     "• Sétif : ~1100 m<br>"
        #     "• Tamanrasset : ~1400 m<br><br>"
        #     "💡 <i>Cliquez 'Calculer Patm' après saisie</i>"
        # )
        
        # calc_btn = QPushButton("Calculer Patm")
        # calc_btn.setProperty("class", "secondary")
        # calc_btn.clicked.connect(self.calculate_patm_from_altitude)
        # grid.addWidget(calc_btn, 1, 2)
        
        # g
        self.g_input = QLineEdit("9.81")
        self.add_field_with_help(
            grid, 2,
            "Accélération pesanteur g (m/s²) :",
            self.g_input,
            "<b>Accélération de la pesanteur (g)</b><br><br>"
            "Accélération gravitationnelle terrestre.<br><br>"
            "<b>Valeur standard :</b> 9.81 m/s²<br>"
            "<b>Variations :</b> Très faibles selon localisation<br>"
            "• Équateur : ~9.78 m/s²<br>"
            "• Pôles : ~9.83 m/s²<br>"
            "• Algérie : ~9.80-9.81 m/s²<br><br>"
            "💡 <i>Utiliser 9.81 m/s² est suffisant pour la plupart des cas</i>"
        )
        
        card_layout.addLayout(grid)
        return card
    
    def create_geometry_card(self):
        """Card Géométrie avec aide"""
        card = Card("📐 Données de Réseau (Géométrie)")
        card_layout = card.layout()
        
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(1, 1)
        
        # Lasp
        self.lasp_input = QLineEdit("10")
        self.add_field_with_help(
            grid, 0,
            "Longueur aspiration Lasp (m) :",
            self.lasp_input,
            "<b>Longueur d'aspiration (Lasp)</b><br><br>"
            "Distance entre le point de pompage (puits, réservoir) et l'entrée de la pompe.<br><br>"
            "<b>Recommandations :</b><br>"
            "• Minimiser autant que possible (risque cavitation)<br>"
            "• Typiquement : 5-15 m<br>"
            "• Éviter coudes brusques<br><br>"
            "<b>Impact :</b> Plus Lasp est grande, plus les pertes de charge sont importantes"
        )
        
        # Lref
        self.lref_input = QLineEdit("50")
        self.add_field_with_help(
            grid, 1,
            "Longueur refoulement Lref (m) :",
            self.lref_input,
            "<b>Longueur de refoulement (Lref)</b><br><br>"
            "Distance entre la sortie de la pompe et le point d'arrivée.<br><br>"
            "<b>Typiquement :</b> Peut être très variable (10-1000+ m)<br>"
            "<b>Impact :</b> Pertes de charge proportionnelles à la longueur<br><br>"
            "💡 <i>Inclut la longueur horizontale + verticale</i>"
        )
        
        # Zdep
        self.zdep_input = QLineEdit("0")
        self.add_field_with_help(
            grid, 2,
            "Cote départ Zdep (m) :",
            self.zdep_input,
            "<b>Cote du point de départ (Zdep)</b><br><br>"
            "Altitude du niveau d'eau dans le réservoir/puits d'aspiration.<br><br>"
            "<b>Référence :</b> Par rapport à un point de référence (souvent sol)<br>"
            "<b>Exemple :</b><br>"
            "• Puits : niveau d'eau = 0 m (référence)<br>"
            "• Réservoir surélevé : +5 m<br>"
            "• Réservoir enterré : -3 m<br><br>"
            "💡 <i>La différence Zarr - Zdep = Hauteur géométrique</i>"
        )
        
        # Zarr
        self.zarr_input = QLineEdit("20")
        self.add_field_with_help(
            grid, 3,
            "Cote arrivée Zarr (m) :",
            self.zarr_input,
            "<b>Cote du point d'arrivée (Zarr)</b><br><br>"
            "Altitude du point de livraison de l'eau.<br><br>"
            "<b>Calcul :</b> Hauteur géométrique Hg = Zarr - Zdep<br>"
            "<b>Exemple :</b><br>"
            "• Si Zdep = 0 m et Zarr = 20 m → Hg = 20 m<br>"
            "• Château d'eau : généralement 15-40 m<br><br>"
            "💡 <i>Plus Hg est élevée, plus la pompe doit être puissante</i>"
        )
        
        card_layout.addLayout(grid)
        return card
    
    def create_fluid_card(self):
        """Card Fluide avec aide"""
        card = Card("💧 Données de Fluide")
        card_layout = card.layout()
        
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(1, 1)
        
        # Température
        self.temp_input = QLineEdit("20")
        self.temp_input.textChanged.connect(self.update_pv_from_temp)
        self.add_field_with_help(
            grid, 0,
            "Température T (°C) :",
            self.temp_input,
            "<b>Température du fluide (T)</b><br><br>"
            "Température de l'eau à pomper.<br><br>"
            "<b>Impact :</b><br>"
            "• Affecte la viscosité et la pression de vapeur<br>"
            "• Influence le risque de cavitation (NPSH)<br><br>"
            "<b>Valeurs typiques :</b><br>"
            "• Eau froide : 10-15°C<br>"
            "• Eau ambiante : 20-25°C<br>"
            "• Eau tiède : 30-40°C"
        )
        
        # Masse volumique
        self.rho_input = QLineEdit("1000")
        self.add_field_with_help(
            grid, 1,
            "Masse volumique ρ (kg/m³) :",
            self.rho_input,
            "<b>Masse volumique (ρ)</b><br><br>"
            "Densité du fluide pompé.<br><br>"
            "<b>Valeurs :</b><br>"
            "• Eau pure (20°C) : 1000 kg/m³<br>"
            "• Eau salée : 1020-1030 kg/m³<br>"
            "• Eaux usées : 1000-1010 kg/m³<br><br>"
            "💡 <i>Pour l'eau, utiliser 1000 kg/m³ est standard</i>"
        )
        
        # Viscosité dynamique
        self.mu_input = QLineEdit("0.001")
        self.add_field_with_help(
            grid, 2,
            "Viscosité dynamique μ (Pa·s) :",
            self.mu_input,
            "<b>Viscosité dynamique (μ)</b><br><br>"
            "Résistance interne du fluide à l'écoulement.<br><br>"
            "<b>Valeurs pour l'eau :</b><br>"
            "• 0°C : 0.00179 Pa·s<br>"
            "• 10°C : 0.00131 Pa·s<br>"
            "• 20°C : 0.00100 Pa·s<br>"
            "• 30°C : 0.00080 Pa·s<br>"
            "• 40°C : 0.00065 Pa·s<br><br>"
            "<b>Impact :</b> Calcul du nombre de Reynolds et du coefficient de frottement"
        )
        
        # Pression de vapeur
        self.pv_input = QLineEdit("2338")
        self.add_field_with_help(
            grid, 3,
            "Pression vapeur Pv (Pa) :",
            self.pv_input,
            "<b>Pression de vapeur saturante (Pv)</b><br><br>"
            "Pression à laquelle l'eau se vaporise à une température donnée.<br><br>"
            "<b>Valeurs :</b><br>"
            "• 10°C : 1228 Pa<br>"
            "• 20°C : 2338 Pa<br>"
            "• 30°C : 4243 Pa<br>"
            "• 40°C : 7375 Pa<br><br>"
            "<b>Usage :</b> Calcul du NPSH disponible (risque cavitation)<br><br>"
            "⚠️ <i>Critique pour éviter la cavitation de la pompe</i>"
        )
        
        # Rugosité
        self.epsilon_input = QLineEdit("0.00015")
        self.add_field_with_help(
            grid, 4,
            "Rugosité absolue ε (m) :",
            self.epsilon_input,
            "<b>Rugosité absolue (ε)</b><br><br>"
            "Rugosité interne de la conduite.<br><br>"
            "<b>Valeurs typiques :</b><br>"
            "• Acier neuf : 0.00005 m (0.05 mm)<br>"
            "• Acier commercial : 0.00015 m (0.15 mm)<br>"
            "• Fonte : 0.00026 m (0.26 mm)<br>"
            "• PVC : 0.0000015 m (0.0015 mm)<br>"
            "• Béton : 0.0003-0.003 m<br><br>"
            "<b>Impact :</b> Calcul du coefficient de frottement et pertes de charge"
        )
        
        card_layout.addLayout(grid)
        return card
    
    def create_operation_card(self):
        """Card Fonctionnement avec aide"""
        card = Card("⚙️ Données de Fonctionnement")
        card_layout = card.layout()
        
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(1, 1)
        
        # Débit
        self.q_input = QLineEdit("0.05")
        self.add_field_with_help(
            grid, 0,
            "Débit volumique Q (m³/s) :",
            self.q_input,
            "<b>Débit volumique nominal (Q)</b><br><br>"
            "Volume d'eau à pomper par seconde.<br><br>"
            "<b>Conversions :</b><br>"
            "• 1 m³/s = 3600 m³/h = 1000 L/s<br>"
            "• 0.05 m³/s = 180 m³/h = 50 L/s<br><br>"
            "<b>Exemples :</b><br>"
            "• Irrigation petite parcelle : 0.01-0.03 m³/s<br>"
            "• Alimentation village : 0.05-0.15 m³/s<br>"
            "• Station pompage urbain : 0.5-5 m³/s<br><br>"
            "💡 <i>Détermine le dimensionnement complet du système</i>"
        )
        
        card_layout.addLayout(grid)
        return card
    
    def create_limits_card(self):
        """Card Limites avec aide"""
        card = Card("⚡ Limites de Conception")
        card_layout = card.layout()
        
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(1, 1)
        
        # Vmin
        self.vmin_input = QLineEdit(str(DEFAULT_VMIN))
        self.add_field_with_help(
            grid, 0,
            "Vitesse minimale Vmin (m/s) :",
            self.vmin_input,
            "<b>Vitesse minimale admissible (Vmin)</b><br><br>"
            "Vitesse d'écoulement minimale pour éviter la sédimentation.<br><br>"
            "<b>Recommandations :</b><br>"
            "• Eau potable : 0.5-0.7 m/s<br>"
            "• Eau claire : 0.5-0.8 m/s<br>"
            "• Eau chargée : 0.7-1.0 m/s<br><br>"
            "<b>Risque si V < Vmin :</b><br>"
            "• Dépôts de particules<br>"
            "• Réduction progressive du diamètre utile<br>"
            "• Prolifération bactérienne (eau potable)"
        )
        
        # Vmax
        self.vmax_input = QLineEdit(str(DEFAULT_VMAX))
        self.add_field_with_help(
            grid, 1,
            "Vitesse maximale Vmax (m/s) :",
            self.vmax_input,
            "<b>Vitesse maximale admissible (Vmax)</b><br><br>"
            "Vitesse d'écoulement maximale pour éviter l'usure.<br><br>"
            "<b>Recommandations :</b><br>"
            "• Aspiration : 1.0-1.5 m/s (max 2 m/s)<br>"
            "• Refoulement : 1.5-3.0 m/s<br>"
            "• Eau potable : 2.0-2.5 m/s<br>"
            "• Conduites courtes : jusqu'à 3.5 m/s<br><br>"
            "<b>Risque si V > Vmax :</b><br>"
            "• Érosion/usure accélérée<br>"
            "• Bruit et vibrations<br>"
            "• Coups de bélier<br>"
            "• Pertes de charge élevées"
        )
        
        card_layout.addLayout(grid)
        return card
    
    def create_methods_card(self):
        """Card Méthodes avec aide"""
        card = Card("🔬 Méthodes de Calcul")
        card_layout = card.layout()
        
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(1, 1)
        
        # Méthode friction
        friction_layout = QHBoxLayout()
        friction_label = QLabel("Coefficient de frottement :")
        friction_layout.addWidget(friction_label)
        
        friction_help = self.create_help_button(
            "<b>Coefficient de frottement (f)</b><br><br>"
            "Méthodes pour calculer les pertes de charge linéaires.<br><br>"
            "<b>Colebrook-White :</b><br>"
            "• Formule de référence (implicite)<br>"
            "• Précision maximale<br>"
            "• Nécessite résolution itérative<br><br>"
            "<b>Haaland :</b><br>"
            "• Approximation explicite de Colebrook<br>"
            "• Erreur < 2%<br>"
            "• Calcul direct<br><br>"
            "<b>Swamee-Jain :</b><br>"
            "• Approximation simplifiée<br>"
            "• Erreur < 3%<br>"
            "• Rapide et pratique<br><br>"
            "💡 <i>Recommandation : Swamee-Jain pour usage courant</i>"
        )
        friction_layout.addWidget(friction_help)
        friction_layout.addStretch()
        
        grid.addLayout(friction_layout, 0, 0)
        
        self.friction_combo = QComboBox()
        self.friction_combo.addItems(FRICTION_METHODS)
        self.friction_combo.setCurrentText('Swamee-Jain')
        grid.addWidget(self.friction_combo, 0, 1)
        
        # Méthode pertes singulières
        loss_layout = QHBoxLayout()
        loss_label = QLabel("Pertes singulières :")
        loss_layout.addWidget(loss_label)
        
        loss_help = self.create_help_button(
            "<b>Pertes de charge singulières</b><br><br>"
            "Pertes dues aux coudes, vannes, rétrécissements, etc.<br><br>"
            "<b>Méthode Coefficients :</b><br>"
            "• Kasp : Coefficient aspiration (vannes, crépine, etc.)<br>"
            "• Kref : Coefficient refoulement (coudes, clapets, etc.)<br>"
            "• Valeurs typiques : 1.5-3.0<br><br>"
            "<b>Méthode Pourcentage :</b><br>"
            "• Pourcentage des pertes linéaires<br>"
            "• Typiquement : 10-20% (e = 0.1-0.2)<br>"
            "• Plus simple mais moins précis<br><br>"
            "💡 <i>Coefficients si vous connaissez le détail, sinon Pourcentage 10-15%</i>"
        )
        loss_layout.addWidget(loss_help)
        loss_layout.addStretch()
        
        grid.addLayout(loss_layout, 1, 0)
        
        self.loss_combo = QComboBox()
        self.loss_combo.addItems(LOSS_METHODS)
        self.loss_combo.currentTextChanged.connect(self.on_loss_method_changed)
        grid.addWidget(self.loss_combo, 1, 1)
        
        # Params pertes
        self.loss_params_widget = QWidget()
        self.loss_params_layout = QGridLayout(self.loss_params_widget)
        self.loss_params_layout.setContentsMargins(0, 8, 0, 0)
        grid.addWidget(self.loss_params_widget, 2, 0, 1, 2)
        
        self.create_coefficient_inputs()
        
        card_layout.addLayout(grid)
        return card
    
    def create_coefficient_inputs(self):
        """Inputs coefficients avec aide"""
        while self.loss_params_layout.count():
            child = self.loss_params_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Kasp
        kasp_layout = QHBoxLayout()
        kasp_label = QLabel("Kasp (aspiration) :")
        kasp_layout.addWidget(kasp_label)
        
        kasp_help = self.create_help_button(
            "<b>Coefficient Kasp (aspiration)</b><br><br>"
            "Somme des coefficients de pertes singulières côté aspiration.<br><br>"
            "<b>Exemples :</b><br>"
            "• Crépine : 0.5-1.0<br>"
            "• Vanne d'aspiration : 0.2-0.5<br>"
            "• Coude 90° : 0.9<br>"
            "• Élargissement brusque : 0.5-1.0<br><br>"
            "<b>Valeur typique totale : 1.5-3.0</b>"
        )
        kasp_layout.addWidget(kasp_help)
        kasp_layout.addStretch()
        self.loss_params_layout.addLayout(kasp_layout, 0, 0)
        
        self.kasp_input = QLineEdit("1.5")
        self.loss_params_layout.addWidget(self.kasp_input, 0, 1)
        
        # Kref
        kref_layout = QHBoxLayout()
        kref_label = QLabel("Kref (refoulement) :")
        kref_layout.addWidget(kref_label)
        
        kref_help = self.create_help_button(
            "<b>Coefficient Kref (refoulement)</b><br><br>"
            "Somme des coefficients de pertes singulières côté refoulement.<br><br>"
            "<b>Exemples :</b><br>"
            "• Clapet anti-retour : 1.5-2.5<br>"
            "• Vanne de régulation : 0.2-0.5<br>"
            "• Coude 90° : 0.9<br>"
            "• Té : 1.0-1.5<br>"
            "• Sortie réservoir : 1.0<br><br>"
            "<b>Valeur typique totale : 2.0-4.0</b>"
        )
        kref_layout.addWidget(kref_help)
        kref_layout.addStretch()
        self.loss_params_layout.addLayout(kref_layout, 1, 0)
        
        self.kref_input = QLineEdit("2.0")
        self.loss_params_layout.addWidget(self.kref_input, 1, 1)
    
    def create_percentage_input(self):
        """Input pourcentage avec aide"""
        while self.loss_params_layout.count():
            child = self.loss_params_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        perc_layout = QHBoxLayout()
        perc_label = QLabel("Pourcentage e :")
        perc_layout.addWidget(perc_label)
        
        perc_help = self.create_help_button(
            "<b>Pourcentage de pertes singulières (e)</b><br><br>"
            "Pertes singulières exprimées en % des pertes linéaires.<br><br>"
            "<b>Valeurs recommandées :</b><br>"
            "• Réseau simple : e = 0.10 (10%)<br>"
            "• Réseau moyen : e = 0.15 (15%)<br>"
            "• Réseau complexe : e = 0.20-0.30 (20-30%)<br><br>"
            "<b>Formule :</b> Pertes_sing = e × Pertes_linéaires<br><br>"
            "💡 <i>Méthode simple, 10-15% pour la plupart des cas</i>"
        )
        perc_layout.addWidget(perc_help)
        perc_layout.addStretch()
        self.loss_params_layout.addLayout(perc_layout, 0, 0)
        
        self.percentage_input = QLineEdit("0.1")
        self.percentage_input.setPlaceholderText("Ex: 0.1 = 10%")
        self.loss_params_layout.addWidget(self.percentage_input, 0, 1)
    
    def on_loss_method_changed(self, text):
        if text == 'Coefficients':
            self.create_coefficient_inputs()
        else:
            self.create_percentage_input()
    
    # def calculate_patm_from_altitude(self):
    #     try:
    #         zalt = float(self.zalt_input.text())
    #         patm = self.main_window.npsh_calculator.calculate_patm_from_altitude(zalt)
    #         self.patm_input.setText(f"{patm:.2f}")
    #         QMessageBox.information(self, "✓ Succès", 
    #                               f"Pression atmosphérique calculée :\n{patm:.2f} Pa")
    #     except ValueError:
    #         QMessageBox.warning(self, "⚠ Erreur", 
    #                           "Veuillez entrer une altitude valide")
    
    def update_pv_from_temp(self):
   
        try:
            import math
            T = float(self.temp_input.text())
            Pv = 610.78 * math.exp(17.27 * T / (T + 237.3))
            self.pv_input.setText(f"{Pv:.0f}")
        except ValueError:
            pass  
    def validate_data(self):
        try:
            self.update_models()
            
            QMessageBox.information(self, "✓ Validation réussie",
                                  "Toutes les données sont valides.\n"
                                  "Vous pouvez passer à l'étape suivante.")
            
            self.main_window.update_status("✓ Données validées avec succès", 5000)
            self.main_window.tabs.setCurrentIndex(1)
        
        except Exception as e:
            QMessageBox.critical(self, "✗ Erreur de validation",
                               f"Erreur lors de la validation :\n{str(e)}")
    
    def update_models(self):
        """Met à jour les modèles"""
        self.main_window.fluid_model.temperature = float(self.temp_input.text())
        self.main_window.fluid_model.density = float(self.rho_input.text())
        self.main_window.fluid_model.viscosity = float(self.mu_input.text())
        self.main_window.fluid_model.vapor_pressure = float(self.pv_input.text())
        self.main_window.fluid_model.roughness = float(self.epsilon_input.text())
        
        self.main_window.pipe_model.L_aspiration = float(self.lasp_input.text())
        self.main_window.pipe_model.L_refoulement = float(self.lref_input.text())
        self.main_window.pipe_model.Z_depart = float(self.zdep_input.text())
        self.main_window.pipe_model.Z_arrivee = float(self.zarr_input.text())
        
        self.main_window.npsh_calculator.Patm = float(self.patm_input.text())
        self.main_window.npsh_calculator.g = float(self.g_input.text())
        self.main_window.hmt_calculator.g = float(self.g_input.text())
    
    def reset(self):
        """Réinitialise"""
        self.patm_input.setText("101325")
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