"""
Calculateur HMT Professionnel - Application PyQt5
Point d'entrée principal
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont

from views.main_window import MainWindow


def main():
    """Fonction principale"""
    # Créer l'application
    app = QApplication(sys.argv)
    app.setApplicationName("Calculateur HMT Professionnel")
    app.setOrganizationName("HMT Solutions")
    app.setFont(QFont("Roboto", 10))
    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()
    
    # Lancer la boucle d'événements
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()