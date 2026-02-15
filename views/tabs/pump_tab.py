"""
Onglet de gestion des pompes - Avec bibliothèque système
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QFileDialog,
                             QMessageBox, QHeaderView, QLabel, QDialog,
                             QLineEdit, QGridLayout, QDialogButtonBox, QMenu,
                             QProgressDialog, QListWidget, QListWidgetItem,
                             QAbstractItemView, QCheckBox)
from PyQt5.QtCore import Qt
from utils.file_handler import FileHandler
from models.pump_model import PumpModel
from views.widgets.custom_widgets import Card, SectionHeader, InfoBox, IconButton
from config import SYSTEM_PUMPS_DIR
import os
import glob


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
            "Choisissez dans la bibliothèque ou importez vos propres pompes"
        )
        layout.addWidget(header)
        
        # Info
        info = InfoBox(
            "Sélectionnez des pompes de la bibliothèque système ou importez vos propres fichiers JSON/CSV.",
            "info"
        )
        layout.addWidget(info)
        
        # Card Actions
        actions_card = Card("Actions")
        actions_layout = actions_card.layout()
        
        buttons_layout = QHBoxLayout()
        
        # Bouton Bibliothèque (NOUVEAU)
        library_btn = IconButton("📚  Bibliothèque Système", "")
        library_btn.setToolTip("Choisir des pompes depuis la bibliothèque")
        library_btn.clicked.connect(self.show_library_dialog)
        buttons_layout.addWidget(library_btn)
        
        # Bouton Import externe
        import_btn = IconButton("📁  Importer Fichier(s)", "")
        import_btn.setProperty("class", "secondary")
        import_btn.setToolTip("Importer des fichiers JSON/CSV externes")
        import_btn.clicked.connect(self.import_pumps_multi)
        buttons_layout.addWidget(import_btn)
        
        # Bouton Ajouter manuellement
        add_btn = IconButton("➕  Ajouter Manuellement", "")
        add_btn.setProperty("class", "secondary")
        add_btn.clicked.connect(self.add_pump_manually)
        buttons_layout.addWidget(add_btn)
        
        actions_layout.addLayout(buttons_layout)
        
        # Deuxième ligne de boutons
        buttons_layout2 = QHBoxLayout()
        
        # Bouton Export
        export_btn = IconButton("💾  Exporter vers Bibliothèque", "")
        export_btn.setProperty("class", "secondary")
        export_btn.setToolTip("Sauvegarder une pompe dans la bibliothèque système")
        export_btn.clicked.connect(self.export_to_library)
        buttons_layout2.addWidget(export_btn)
        
        # Bouton Export externe
        export_ext_btn = IconButton("📤  Exporter Externe", "")
        export_ext_btn.setProperty("class", "secondary")
        export_ext_btn.clicked.connect(self.show_export_menu)
        buttons_layout2.addWidget(export_ext_btn)
        
        actions_layout.addLayout(buttons_layout2)
        layout.addWidget(actions_card)
        
        # Card Table
        table_card = Card("Pompes Sélectionnées pour le Projet")
        table_layout = table_card.layout()
        
        self.pump_table = QTableWidget()
        self.pump_table.setColumnCount(5)
        self.pump_table.setHorizontalHeaderLabels([
            'ID', 'Type de pompe', 'Nombre disponible', 'Points', 'Source'
        ])
        
        header_table = self.pump_table.horizontalHeader()
        header_table.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header_table.setSectionResizeMode(1, QHeaderView.Stretch)
        header_table.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header_table.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header_table.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        self.pump_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.pump_table.setAlternatingRowColors(True)
        self.pump_table.setMinimumHeight(300)
        
        table_layout.addWidget(self.pump_table)
        layout.addWidget(table_card)
        
        # Boutons de gestion
        manage_layout = QHBoxLayout()
        
        delete_btn = IconButton("🗑️  Supprimer sélection", "")
        delete_btn.setProperty("class", "danger")
        delete_btn.clicked.connect(self.delete_selected_pump)
        manage_layout.addWidget(delete_btn)
        
        clear_all_btn = IconButton("🗑️  Tout supprimer", "")
        clear_all_btn.setProperty("class", "danger")
        clear_all_btn.clicked.connect(self.clear_all_pumps)
        manage_layout.addWidget(clear_all_btn)
        
        manage_layout.addStretch()
        
        validate_btn = IconButton("✓  Valider et continuer", "")
        validate_btn.setProperty("class", "success")
        validate_btn.setMinimumWidth(250)
        validate_btn.setMinimumHeight(48)
        validate_btn.clicked.connect(self.validate_pumps)
        manage_layout.addWidget(validate_btn)
        
        layout.addLayout(manage_layout)
        layout.addStretch()
    
    def show_library_dialog(self):
        """Affiche la boîte de dialogue de la bibliothèque"""
        dialog = PumpLibraryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_pumps = dialog.get_selected_pumps()
            
            if selected_pumps:
                added_count = 0
                for pump in selected_pumps:
                    self.main_window.pumps.append(pump)
                    added_count += 1
                
                self.update_pump_table()
                
                QMessageBox.information(
                    self, "✓ Succès",
                    f"{added_count} pompe(s) ajoutée(s) depuis la bibliothèque !"
                )
                self.main_window.update_status(
                    f"✓ {added_count} pompe(s) chargée(s)", 3000
                )
    
    def import_pumps_multi(self):
        """Importe plusieurs fichiers JSON/CSV externes"""
        filenames, _ = QFileDialog.getOpenFileNames(
            self, 
            "Sélectionner un ou plusieurs fichiers de pompes",
            "", 
            "Tous les fichiers supportés (*.json *.csv);;Fichiers JSON (*.json);;Fichiers CSV (*.csv);;Tous les fichiers (*.*)"
        )
        
        if not filenames:
            return
        
        # Progress dialog pour plusieurs fichiers
        if len(filenames) > 1:
            progress = QProgressDialog(
                "Importation des pompes...", 
                "Annuler", 
                0, 
                len(filenames), 
                self
            )
            progress.setWindowModality(Qt.WindowModal)
            progress.setMinimumDuration(0)
        else:
            progress = None
        
        imported_count = 0
        failed_files = []
        
        for idx, filename in enumerate(filenames):
            if progress:
                progress.setValue(idx)
                progress.setLabelText(f"Importation de {os.path.basename(filename)}...")
                
                if progress.wasCanceled():
                    break
            
            try:
                if filename.lower().endswith('.json'):
                    pump = FileHandler.load_pump_from_json(filename)
                elif filename.lower().endswith('.csv'):
                    pump = FileHandler.load_pump_from_csv(filename)
                else:
                    pump = FileHandler.load_pump_from_json(filename)
                
                self.main_window.pumps.append(pump)
                imported_count += 1
                
            except Exception as e:
                failed_files.append({
                    'file': os.path.basename(filename),
                    'error': str(e)
                })
        
        if progress:
            progress.setValue(len(filenames))
        
        self.update_pump_table()
        
        if imported_count > 0 and len(failed_files) == 0:
            QMessageBox.information(
                self, "✓ Succès",
                f"{imported_count} pompe(s) importée(s) avec succès !"
            )
            self.main_window.update_status(
                f"✓ {imported_count} pompe(s) importée(s)", 3000
            )
        elif imported_count > 0 and len(failed_files) > 0:
            error_msg = f"{imported_count} pompe(s) importée(s).\n\n"
            error_msg += f"⚠ {len(failed_files)} erreur(s):\n"
            for failed in failed_files[:3]:
                error_msg += f"• {failed['file']}\n"
            
            QMessageBox.warning(self, "⚠ Importation partielle", error_msg)
        else:
            QMessageBox.critical(self, "✗ Erreur", 
                               "Aucune pompe n'a pu être importée")
    
    def export_to_library(self):
        """Exporte une pompe vers la bibliothèque système"""
        selected_rows = self.pump_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "⚠ Attention",
                              "Veuillez sélectionner une pompe à sauvegarder")
            return
        
        row = selected_rows[0].row()
        pump = self.main_window.pumps[row]
        
        # Demander confirmation
        reply = QMessageBox.question(
            self, '❓ Confirmation',
            f'Sauvegarder "{pump.type}" dans la bibliothèque système ?\n\n'
            'Elle sera disponible pour tous vos futurs projets.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Générer nom de fichier
                safe_name = pump.type.replace(' ', '_').replace('/', '_')
                filename = os.path.join(SYSTEM_PUMPS_DIR, f"{safe_name}.json")
                
                # Vérifier si existe déjà
                if os.path.exists(filename):
                    overwrite = QMessageBox.question(
                        self, '❓ Fichier existant',
                        f'Une pompe "{pump.type}" existe déjà.\nÉcraser ?',
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.No
                    )
                    if overwrite == QMessageBox.No:
                        return
                
                FileHandler.save_pump_to_json(pump, filename)
                
                QMessageBox.information(
                    self, "✓ Succès",
                    f'Pompe "{pump.type}" sauvegardée dans la bibliothèque !'
                )
                self.main_window.update_status("✓ Pompe ajoutée à la bibliothèque", 3000)
                
            except Exception as e:
                QMessageBox.critical(self, "✗ Erreur",
                                   f"Erreur lors de la sauvegarde:\n{str(e)}")
    
    def show_export_menu(self):
        """Menu export externe"""
        selected_rows = self.pump_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "⚠ Attention",
                              "Veuillez sélectionner une pompe")
            return
        
        menu = QMenu(self)
        json_action = menu.addAction("📄 Exporter JSON")
        json_action.triggered.connect(self.export_pump_json)
        
        csv_action = menu.addAction("📊 Exporter CSV")
        csv_action.triggered.connect(self.export_pump_csv)
        
        sender = self.sender()
        menu.exec_(sender.mapToGlobal(sender.rect().bottomLeft()))
    
    def export_pump_json(self):
        selected_rows = self.pump_table.selectedIndexes()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        pump = self.main_window.pumps[row]
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter en JSON",
            f"{pump.type.replace(' ', '_')}.json",
            "Fichiers JSON (*.json)"
        )
        
        if filename:
            try:
                FileHandler.save_pump_to_json(pump, filename)
                QMessageBox.information(self, "✓ Succès", "Export JSON réussi")
            except Exception as e:
                QMessageBox.critical(self, "✗ Erreur", str(e))
    
    def export_pump_csv(self):
        selected_rows = self.pump_table.selectedIndexes()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        pump = self.main_window.pumps[row]
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter en CSV",
            f"{pump.type.replace(' ', '_')}.csv",
            "Fichiers CSV (*.csv)"
        )
        
        if filename:
            try:
                FileHandler.save_pump_to_csv(pump, filename)
                QMessageBox.information(self, "✓ Succès", "Export CSV réussi")
            except Exception as e:
                QMessageBox.critical(self, "✗ Erreur", str(e))
    
    def add_pump_manually(self):
        dialog = AddPumpDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            pump_data = dialog.get_pump_data()
            try:
                pump = PumpModel.from_json(pump_data)
                self.main_window.pumps.append(pump)
                self.update_pump_table()
                
                QMessageBox.information(self, "✓ Succès",
                                      f"Pompe '{pump.type}' ajoutée !")
                self.main_window.update_status(f"✓ Pompe ajoutée", 3000)
            except Exception as e:
                QMessageBox.critical(self, "✗ Erreur", str(e))
    
    def delete_selected_pump(self):
        selected_rows = self.pump_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "⚠ Attention",
                              "Sélectionnez une pompe")
            return
        
        row = selected_rows[0].row()
        pump_type = self.pump_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, '❓ Confirmation',
            f'Supprimer "{pump_type}" ?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            del self.main_window.pumps[row]
            self.update_pump_table()
            self.main_window.update_status("✓ Pompe supprimée", 3000)
    
    def clear_all_pumps(self):
        if not self.main_window.pumps:
            return
        
        reply = QMessageBox.question(
            self, '❓ Confirmation',
            f'Supprimer TOUTES les pompes ({len(self.main_window.pumps)}) ?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            count = len(self.main_window.pumps)
            self.main_window.pumps.clear()
            self.update_pump_table()
            self.main_window.update_status(f"✓ {count} pompe(s) supprimée(s)", 3000)
    
    def update_pump_table(self):
        self.pump_table.setRowCount(0)
        
        for idx, pump in enumerate(self.main_window.pumps):
            row = self.pump_table.rowCount()
            self.pump_table.insertRow(row)
            
            self.pump_table.setItem(row, 0, QTableWidgetItem(str(idx + 1)))
            self.pump_table.setItem(row, 1, QTableWidgetItem(pump.type))
            self.pump_table.setItem(row, 2, QTableWidgetItem(str(pump.nombre)))
            self.pump_table.setItem(row, 3, QTableWidgetItem(str(len(pump.Qp))))
            
            # Source
            source = getattr(pump, 'source', 'Externe')
            self.pump_table.setItem(row, 4, QTableWidgetItem(source))
            
            for col in [0, 2, 3, 4]:
                self.pump_table.item(row, col).setTextAlignment(Qt.AlignCenter)
    
    def validate_pumps(self):
        if not self.main_window.pumps:
            QMessageBox.warning(self, "⚠ Attention",
                              "Veuillez sélectionner au moins une pompe")
            return
        
        QMessageBox.information(self, "✓ Validation réussie",
                              f"{len(self.main_window.pumps)} pompe(s) validée(s).")
        
        self.main_window.update_status(
            f"✓ {len(self.main_window.pumps)} pompe(s) validée(s)", 3000
        )
        self.main_window.tabs.setCurrentIndex(2)


class PumpLibraryDialog(QDialog):
    """Dialogue de sélection depuis la bibliothèque"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bibliothèque de Pompes Système")
        self.setModal(True)
        self.resize(700, 500)
        self.selected_pumps = []
        self.init_ui()
        self.load_library()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("📚 Sélectionnez les pompes pour votre projet")
        header.setProperty("class", "section-title")
        layout.addWidget(header)
        
        info = InfoBox(
            "Cochez les pompes que vous souhaitez utiliser. Vous pouvez en sélectionner plusieurs.",
            "info"
        )
        layout.addWidget(info)
        
        # Liste avec checkboxes
        self.pump_list = QListWidget()
        self.pump_list.setAlternatingRowColors(True)
        self.pump_list.setMinimumHeight(300)
        layout.addWidget(self.pump_list)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("Tout sélectionner")
        select_all_btn.clicked.connect(self.select_all)
        button_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("Tout désélectionner")
        deselect_all_btn.clicked.connect(self.deselect_all)
        button_layout.addWidget(deselect_all_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Boutons OK/Cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def load_library(self):
        """Charge les pompes de la bibliothèque"""
        self.pump_list.clear()
        self.library_pumps = []
        
        # Chercher tous les fichiers JSON dans le dossier système
        json_files = glob.glob(os.path.join(SYSTEM_PUMPS_DIR, "*.json"))
        
        if not json_files:
            item = QListWidgetItem("⚠ Aucune pompe dans la bibliothèque")
            item.setFlags(Qt.NoItemFlags)
            self.pump_list.addItem(item)
            return
        
        for filepath in sorted(json_files):
            try:
                pump = FileHandler.load_pump_from_json(filepath)
                pump.source = "Bibliothèque"  # Marquer la source
                self.library_pumps.append(pump)
                
                # Créer item avec checkbox
                item_text = f"{pump.type} ({pump.nombre} disponibles, {len(pump.Qp)} points)"
                item = QListWidgetItem(item_text)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                item.setData(Qt.UserRole, pump)
                
                self.pump_list.addItem(item)
                
            except Exception as e:
                print(f"Erreur chargement {filepath}: {e}")
    
    def select_all(self):
        for i in range(self.pump_list.count()):
            item = self.pump_list.item(i)
            if item.flags() & Qt.ItemIsUserCheckable:
                item.setCheckState(Qt.Checked)
    
    def deselect_all(self):
        for i in range(self.pump_list.count()):
            item = self.pump_list.item(i)
            if item.flags() & Qt.ItemIsUserCheckable:
                item.setCheckState(Qt.Unchecked)
    
    def get_selected_pumps(self):
        """Retourne les pompes sélectionnées"""
        selected = []
        for i in range(self.pump_list.count()):
            item = self.pump_list.item(i)
            if item.checkState() == Qt.Checked:
                pump = item.data(Qt.UserRole)
                if pump:
                    selected.append(pump)
        return selected


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