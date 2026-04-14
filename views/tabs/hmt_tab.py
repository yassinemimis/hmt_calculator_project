"""
Onglet de calcul HMT (Étape 3)
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGroupBox,
                             QPushButton, QLabel, QLineEdit, QTextEdit,
                             QMessageBox, QGridLayout)
from PyQt5.QtCore import Qt
import math


class HMTTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("ÉTAPE 3 : Choix des diamètres et calcul de la HMT")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2196F3;")
        layout.addWidget(title)

        # ── Section diamètres ─────────────────────────────────────────────
        diam_group  = QGroupBox("Calcul des diamètres")
        diam_layout = QGridLayout()

        calc_btn = QPushButton("Calculer Dmin et Dmax")
        calc_btn.clicked.connect(self.calculate_diameter_range)
        diam_layout.addWidget(calc_btn, 0, 0)

        self.diameter_range_label = QLabel("Cliquez pour calculer la plage")
        self.diameter_range_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        diam_layout.addWidget(self.diameter_range_label, 0, 1)

        diam_layout.addWidget(QLabel("Diamètres à étudier (m, séparés par virgules):"), 1, 0)
        self.diameters_input = QLineEdit("0.1, 0.15, 0.2, 0.25")
        diam_layout.addWidget(self.diameters_input, 1, 1)

        diam_group.setLayout(diam_layout)
        layout.addWidget(diam_group)

        # ── Bouton calcul ─────────────────────────────────────────────────
        calc_hmt_btn = QPushButton("⚙️ CALCULER HMT ET COURBES SYSTÈME")
        calc_hmt_btn.setMinimumHeight(50)
        calc_hmt_btn.setStyleSheet("font-size: 13pt;")
        calc_hmt_btn.clicked.connect(self.calculate_hmt)
        layout.addWidget(calc_hmt_btn)

        # ── Résultats ─────────────────────────────────────────────────────
        res_group  = QGroupBox("Résultats HMT et Courbes du Système")
        res_layout = QVBoxLayout()

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(400)
        res_layout.addWidget(self.results_text)

        res_group.setLayout(res_layout)
        layout.addWidget(res_group)

        layout.addStretch()

    # ─── Calculs ──────────────────────────────────────────────────────────

    def calculate_diameter_range(self):
        try:
            Q    = float(self.main_window.input_tab.q_input.text())
            Vmin = float(self.main_window.input_tab.vmin_input.text())
            Vmax = float(self.main_window.input_tab.vmax_input.text())

            Dmin, Dmax = self.main_window.hmt_calculator.calculate_diameter_range(Q, Vmin, Vmax)

            self.diameter_range_label.setText(
                f"Dmin = {Dmin:.4f} m  ≤  D  ≤  Dmax = {Dmax:.4f} m"
            )

            # Suggérer 6 diamètres régulièrement espacés
            step = (Dmax - Dmin) / 5
            suggested = [Dmin + i * step for i in range(6)]
            self.diameters_input.setText(", ".join(f"{d:.4f}" for d in suggested))

            self.main_window.update_status("Plage de diamètres calculée", 3000)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de calcul :\n{str(e)}")

    def calculate_hmt(self):
        try:
            self.main_window.input_tab.update_models()

            Q            = float(self.main_window.input_tab.q_input.text())
            diameters    = [float(d.strip())
                            for d in self.diameters_input.text().split(",")]
            friction_method = self.main_window.input_tab.friction_combo.currentText()
            kwargs          = self.main_window.input_tab.get_loss_kwargs()
            loss_method     = kwargs.pop('loss_method')   # extraire pour éviter doublon

            self.main_window.hmt_results   = []
            self.main_window.system_curves = {}

            for D in diameters:
                # HMT au débit nominal
                result = self.main_window.hmt_calculator.calculate_HMT(
                    Q, D, friction_method, loss_method, **kwargs)
                result['D'] = D
                self.main_window.hmt_results.append(result)

                # Courbe système avec A(Qs) variable
                curve = self.main_window.hmt_calculator.calculate_system_curve(
                    D, Q, friction_method, loss_method, **kwargs)
                self.main_window.system_curves[D] = curve

            self.display_results()

            QMessageBox.information(self, "Succès",
                                    f"Calculs terminés pour {len(diameters)} diamètre(s).\n"
                                    "Vous pouvez passer à l'optimisation.")
            self.main_window.update_status(
                f"HMT calculée pour {len(diameters)} diamètre(s)", 3000)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de calcul :\n{str(e)}")

    def display_results(self):
        self.results_text.clear()
        self.results_text.append("=" * 100)
        self.results_text.append("RÉSULTATS HMT ET COURBES DU SYSTÈME (A variable)")
        self.results_text.append("=" * 100 + "\n")

        for result in self.main_window.hmt_results:
            D  = result['D']
            out  = f"Diamètre D = {D:.4f} m\n"
            out += "-" * 80 + "\n"
            out += f"  • Vitesse V                    : {result['V']:.4f} m/s\n"
            out += f"  • Nombre de Reynolds Re        : {result['Re']:.2f}\n"
            out += f"  • Coefficient de frottement f  : {result['f']:.6f}\n"
            out += f"  • Coefficient pertes K_T       : {result['K_T']:.6f}\n"
            out += f"  • Coefficient réseau A         : {result['A']:.6f}\n"
            out += f"  • Hauteur géométrique Hg       : {result['Hg']:.4f} m\n"
            out += f"  • Pertes de charge Dh          : {result['Dh']:.4f} m\n"
            out += f"  ► HMT (Q nominal)              : {result['HMT']:.4f} m\n\n"

            curve = self.main_window.system_curves[D]
            out += "  Courbe du système HMTs = f(Qs)  [A(Qs) variable] :\n"
            out += f"  {'Qs (m³/s)':>14}  {'As':>10}  {'HMTs (m)':>10}\n"
            for Qs, As, HMTs in zip(curve['Qs'], curve['As'], curve['HMTs']):
                out += f"  {Qs:>14.4f}  {As:>10.6f}  {HMTs:>10.4f}\n"
            out += "\n"

            self.results_text.append(out)