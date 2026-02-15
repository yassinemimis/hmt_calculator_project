"""
Onglet de gestion des pompes - Support JSON & CSV
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QFileDialog,
                             QMessageBox, QHeaderView, QLabel, QDialog,
                             QLineEdit, QGridLayout, QDialogButtonBox, QMenu)
from PyQt5.QtCore import Qt
from utils.file_handler import FileHandler
from models.pump_model import PumpModel
from views.widgets.custom_widgets import Card, SectionHeader, InfoBox, IconButton


class PumpTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = SectionHeader(
            "ÉTAPE 2 : Introduction des données des pompes",
            "Importez des fichiers JSON/CSV ou créez les pompes manuellement"
        )
        layout.addWidget(header)
        
        # Info
        info = InfoBox(
            "Formats supportés : JSON et CSV. Vous pouvez aussi ajouter des pompes manuellement.",
            "info"
        )
        layout.addWidget(info)
        
        # Card Actions
        actions_card = Card("Actions")
        actions_layout = actions_card.layout()
        
        buttons_layout = QHBoxLayout()
        
        # Bouton Import avec menu déroulant
        import_btn = IconButton("📁  Importer Fichier", "")
        import_btn.clicked.connect(self.show_import_menu)
        buttons_layout.addWidget(import_btn)
        
        # Bouton Export avec menu déroulant
        export_btn = IconButton("💾  Exporter Pompe", "")
        export_btn.setProperty("class", "secondary")
        export_btn.clicked.connect(self.show_export_menu)
        buttons_layout.addWidget(export_btn)
        
        add_btn = IconButton("➕  Ajouter Manuellement", "")
        add_btn.setProperty("class", "secondary")
        add_btn.clicked.connect(self.add_pump_manually)
        buttons_layout.addWidget(add_btn)
        
        actions_layout.addLayout(buttons_layout)
        layout.addWidget(actions_card)
        
        # Card Table
        table_card = Card("Pompes Disponibles")
        table_layout = table_card.layout()
        
        self.pump_table = QTableWidget()
        self.pump_table.setColumnCount(4)
        self.pump_table.setHorizontalHeaderLabels([
            'ID', 'Type de pompe', 'Nombre disponible', 'Points de données'
        ])
        
        header_table = self.pump_table.horizontalHeader()
        header_table.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header_table.setSectionResizeMode(1, QHeaderView.Stretch)
        header_table.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header_table.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        self.pump_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.pump_table.setAlternatingRowColors(True)
        self.pump_table.setMinimumHeight(300)
        
        table_layout.addWidget(self.pump_table)
        layout.addWidget(table_card)
        
        # Boutons de gestion
        manage_layout = QHBoxLayout()
        
        delete_btn = IconButton("🗑️  Supprimer la sélection", "")
        delete_btn.setProperty("class", "danger")
        delete_btn.clicked.connect(self.delete_selected_pump)
        manage_layout.addWidget(delete_btn)
        
        manage_layout.addStretch()
        
        validate_btn = IconButton("✓  Valider et continuer", "")
        validate_btn.setProperty("class", "success")
        validate_btn.setMinimumWidth(250)
        validate_btn.setMinimumHeight(48)
        validate_btn.clicked.connect(self.validate_pumps)
        manage_layout.addWidget(validate_btn)
        
        layout.addLayout(manage_layout)
        layout.addStretch()
    
    def show_import_menu(self):
        """Affiche un menu pour choisir JSON ou CSV"""
        menu = QMenu(self)
        
        json_action = menu.addAction("📄 Importer JSON")
        json_action.triggered.connect(self.import_pump_json)
        
        csv_action = menu.addAction("📊 Importer CSV")
        csv_action.triggered.connect(self.import_pump_csv)
        
        # Afficher le menu au centre du bouton
        sender = self.sender()
        menu.exec_(sender.mapToGlobal(sender.rect().bottomLeft()))
    
    def show_export_menu(self):
        """Affiche un menu pour exporter en JSON ou CSV"""
        selected_rows = self.pump_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "⚠ Attention",
                              "Veuillez sélectionner une pompe à exporter")
            return
        
        menu = QMenu(self)
        
        json_action = menu.addAction("📄 Exporter en JSON")
        json_action.triggered.connect(self.export_pump_json)
        
        csv_action = menu.addAction("📊 Exporter en CSV")
        csv_action.triggered.connect(self.export_pump_csv)
        
        sender = self.sender()
        menu.exec_(sender.mapToGlobal(sender.rect().bottomLeft()))
    
    def import_pump_json(self):
        """Importe un fichier JSON"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner un fichier JSON de pompe",
            "", "Fichiers JSON (*.json);;Tous les fichiers (*.*)"
        )
        
        if filename:
            try:
                pump = FileHandler.load_pump_from_json(filename)
                self.main_window.pumps.append(pump)
                self.update_pump_table()
                
                QMessageBox.information(self, "✓ Succès",
                                      f"Pompe '{pump.type}' importée depuis JSON avec succès !")
                self.main_window.update_status(f"✓ Pompe JSON importée : {pump.type}", 3000)
            
            except Exception as e:
                QMessageBox.critical(self, "✗ Erreur",
                                   f"Erreur lors de l'import JSON :\n{str(e)}")
    
    def import_pump_csv(self):
        """Importe un fichier CSV"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner un fichier CSV de pompe",
            "", "Fichiers CSV (*.csv);;Tous les fichiers (*.*)"
        )
        
        if filename:
            try:
                pump = FileHandler.load_pump_from_csv(filename)
                self.main_window.pumps.append(pump)
                self.update_pump_table()
                
                QMessageBox.information(self, "✓ Succès",
                                      f"Pompe '{pump.type}' importée depuis CSV avec succès !")
                self.main_window.update_status(f"✓ Pompe CSV importée : {pump.type}", 3000)
            
            except Exception as e:
                QMessageBox.critical(self, "✗ Erreur",
                                   f"Erreur lors de l'import CSV :\n{str(e)}")
    
    def export_pump_json(self):
        """Exporte la pompe sélectionnée en JSON"""
        selected_rows = self.pump_table.selectedIndexes()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        pump = self.main_window.pumps[row]
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter la pompe en JSON",
            f"{pump.type.replace(' ', '_')}.json",
            "Fichiers JSON (*.json);;Tous les fichiers (*.*)"
        )
        
        if filename:
            try:
                FileHandler.save_pump_to_json(pump, filename)
                QMessageBox.information(self, "✓ Succès",
                                      f"Pompe exportée en JSON :\n{filename}")
                self.main_window.update_status(f"✓ Export JSON réussi", 3000)
            except Exception as e:
                QMessageBox.critical(self, "✗ Erreur",
                                   f"Erreur lors de l'export JSON :\n{str(e)}")
    
    def export_pump_csv(self):
        """Exporte la pompe sélectionnée en CSV"""
        selected_rows = self.pump_table.selectedIndexes()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        pump = self.main_window.pumps[row]
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter la pompe en CSV",
            f"{pump.type.replace(' ', '_')}.csv",
            "Fichiers CSV (*.csv);;Tous les fichiers (*.*)"
        )
        
        if filename:
            try:
                FileHandler.save_pump_to_csv(pump, filename)
                QMessageBox.information(self, "✓ Succès",
                                      f"Pompe exportée en CSV :\n{filename}")
                self.main_window.update_status(f"✓ Export CSV réussi", 3000)
            except Exception as e:
                QMessageBox.critical(self, "✗ Erreur",
                                   f"Erreur lors de l'export CSV :\n{str(e)}")
    
    def add_pump_manually(self):
        dialog = AddPumpDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            pump_data = dialog.get_pump_data()
            try:
                pump = PumpModel.from_json(pump_data)
                self.main_window.pumps.append(pump)
                self.update_pump_table()
                
                QMessageBox.information(self, "✓ Succès",
                                      f"Pompe '{pump.type}' ajoutée avec succès !")
                self.main_window.update_status(f"✓ Pompe ajoutée : {pump.type}", 3000)
            
            except Exception as e:
                QMessageBox.critical(self, "✗ Erreur",
                                   f"Erreur lors de l'ajout :\n{str(e)}")
    
    def delete_selected_pump(self):
        selected_rows = self.pump_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "⚠ Attention",
                              "Veuillez sélectionner une pompe à supprimer")
            return
        
        row = selected_rows[0].row()
        pump_type = self.pump_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, '❓ Confirmation',
            f'Voulez-vous vraiment supprimer la pompe :\n"{pump_type}" ?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            del self.main_window.pumps[row]
            self.update_pump_table()
            self.main_window.update_status("✓ Pompe supprimée", 3000)
    
    def update_pump_table(self):
        self.pump_table.setRowCount(0)
        
        for idx, pump in enumerate(self.main_window.pumps):
            row = self.pump_table.rowCount()
            self.pump_table.insertRow(row)
            
            self.pump_table.setItem(row, 0, QTableWidgetItem(str(idx + 1)))
            self.pump_table.setItem(row, 1, QTableWidgetItem(pump.type))
            self.pump_table.setItem(row, 2, QTableWidgetItem(str(pump.nombre)))
            self.pump_table.setItem(row, 3, QTableWidgetItem(str(len(pump.Qp))))
            
            for col in [0, 2, 3]:
                self.pump_table.item(row, col).setTextAlignment(Qt.AlignCenter)
    
    def validate_pumps(self):
        if not self.main_window.pumps:
            QMessageBox.warning(self, "⚠ Attention",
                              "Veuillez importer au moins une pompe")
            return
        
        QMessageBox.information(self, "✓ Validation réussie",
                              f"{len(self.main_window.pumps)} pompe(s) enregistrée(s).\n"
                              "Vous pouvez passer à l'étape suivante.")
        
        self.main_window.update_status(
            f"✓ {len(self.main_window.pumps)} pompe(s) validée(s)", 3000
        )
        self.main_window.tabs.setCurrentIndex(2)


class AddPumpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter une pompe manuellement")
        self.setModal(True)
        self.resize(650, 450)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header = QLabel("Saisie des caractéristiques de la pompe")
        header.setProperty("class", "section-title")
        layout.addWidget(header)
        
        form_layout = QGridLayout()
        form_layout.setSpacing(12)
        form_layout.setColumnStretch(1, 1)
        
        form_layout.addWidget(QLabel("Type de pompe :"), 0, 0)
        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Ex: Pompe Centrifuge 100kW")
        form_layout.addWidget(self.type_input, 0, 1)
        
        form_layout.addWidget(QLabel("Nombre disponible :"), 1, 0)
        self.nombre_input = QLineEdit("1")
        form_layout.addWidget(self.nombre_input, 1, 1)
        
        form_layout.addWidget(QLabel("Qp (m³/s) :"), 2, 0)
        self.qp_input = QLineEdit()
        self.qp_input.setPlaceholderText("Ex: 0.01, 0.02, 0.03, 0.04, 0.05")
        form_layout.addWidget(self.qp_input, 2, 1)
        
        form_layout.addWidget(QLabel("Hp (m) :"), 3, 0)
        self.hp_input = QLineEdit()
        self.hp_input.setPlaceholderText("Ex: 30, 32, 33, 32, 30")
        form_layout.addWidget(self.hp_input, 3, 1)
        
        form_layout.addWidget(QLabel("np (rendement) :"), 4, 0)
        self.np_input = QLineEdit()
        self.np_input.setPlaceholderText("Ex: 0.60, 0.70, 0.80, 0.82, 0.78")
        form_layout.addWidget(self.np_input, 4, 1)
        
        form_layout.addWidget(QLabel("NPSH (m) :"), 5, 0)
        self.npsh_input = QLineEdit()
        self.npsh_input.setPlaceholderText("Ex: 2.5, 3.0, 3.5, 4.0, 4.5")
        form_layout.addWidget(self.npsh_input, 5, 1)
        
        layout.addLayout(form_layout)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_pump_data(self):
        return {
            'type': self.type_input.text(),
            'nombre': int(self.nombre_input.text()),
            'Qp': [float(x.strip()) for x in self.qp_input.text().split(',')],
            'Hp': [float(x.strip()) for x in self.hp_input.text().split(',')],
            'np': [float(x.strip()) for x in self.np_input.text().split(',')],
            'NPSH': [float(x.strip()) for x in self.npsh_input.text().split(',')]
        }