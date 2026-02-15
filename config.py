"""
Configuration globale de l'application
"""

# Constantes physiques
G_STANDARD = 9.81  # m/s²
PATM_STANDARD = 101325  # Pa
TEMP_STANDARD = 20  # °C

# Limites par défaut
DEFAULT_VMIN = 0.5  # m/s
DEFAULT_VMAX = 3.0  # m/s

# Paramètres de calcul
FRICTION_METHODS = ['Colebrook-White', 'Haaland', 'Swamee-Jain']
LOSS_METHODS = ['Coefficients', 'Pourcentage']

# Interface utilisateur
WINDOW_SIZE = "1400x900"
APP_TITLE = "Calculateur HMT - Version Professionnelle"

# Couleurs (Theme)
COLORS = {
    'primary': '#2196F3',
    'secondary': '#FFC107',
    'success': '#4CAF50',
    'danger': '#F44336',
    'warning': '#FF9800',
    'info': '#00BCD4',
    'background': '#f0f0f0',
    'text': '#212121'
}

# Formats d'export
EXPORT_FORMATS = ['txt', 'json', 'csv', 'pdf']

# NPSH
DEFAULT_NPSH_MARGIN = 0.5  # m

# Économique
CURRENCIES = ['DZD', 'EUR', 'USD']