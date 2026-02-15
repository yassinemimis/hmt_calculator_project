"""
Configuration - Responsive
"""
import os

# Application
APP_TITLE = "Calculateur HMT Professionnel v2.0"

# Chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SYSTEM_PUMPS_DIR = os.path.join(DATA_DIR, 'system_pumps')
SAMPLE_PUMPS_DIR = os.path.join(DATA_DIR, 'sample_pumps')

# Assets
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
ICONS_DIR = os.path.join(ASSETS_DIR, 'icons')
LOGO_PATH = os.path.join(ICONS_DIR, 'logo.png')
LOGO_SMALL_PATH = os.path.join(ICONS_DIR, 'logo_small.png')
LOGO_ICO_PATH = os.path.join(ICONS_DIR, 'logo.ico')

# Créer les dossiers s'ils n'existent pas
os.makedirs(SYSTEM_PUMPS_DIR, exist_ok=True)
os.makedirs(SAMPLE_PUMPS_DIR, exist_ok=True)
os.makedirs(ICONS_DIR, exist_ok=True)

# Vitesses limites
DEFAULT_VMIN = 0.5
DEFAULT_VMAX = 3.0

# Méthodes
FRICTION_METHODS = ['Colebrook-White', 'Haaland', 'Swamee-Jain']
LOSS_METHODS = ['Coefficients', 'Pourcentage']

# Monnaies
CURRENCIES = ['DZD', 'EUR', 'USD', 'MAD', 'TND']

# Responsive breakpoints
BREAKPOINT_VERY_SMALL = 1024
BREAKPOINT_SMALL = 1366
BREAKPOINT_MEDIUM = 1600
BREAKPOINT_LARGE = 1920