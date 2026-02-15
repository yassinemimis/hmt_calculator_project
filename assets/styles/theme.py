"""
Thème Industrial Engineering - Responsive Design
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect

def get_screen_size():
    """Récupère la taille de l'écran"""
    screen = QApplication.primaryScreen()
    if screen:
        return screen.size()
    return None

def is_small_screen():
    """Vérifie si l'écran est petit (<= 1366x768)"""
    size = get_screen_size()
    if size:
        return size.width() <= 1366 or size.height() <= 768
    return False

def is_very_small_screen():
    """Vérifie si l'écran est très petit (<= 1024x768)"""
    size = get_screen_size()
    if size:
        return size.width() <= 1024 or size.height() <= 768
    return False

def get_font_size():
    """Retourne la taille de police selon l'écran"""
    if is_very_small_screen():
        return 9
    elif is_small_screen():
        return 10
    return 10.5

def get_spacing():
    """Retourne l'espacement selon l'écran"""
    if is_very_small_screen():
        return 8
    elif is_small_screen():
        return 12
    return 16

def get_margin():
    """Retourne les marges selon l'écran"""
    if is_very_small_screen():
        return 10
    elif is_small_screen():
        return 15
    return 20

THEME = {
    'primary': '#1A73E8',
    'primary_dark': '#1557B0',
    'primary_light': '#E8F0FE',
    
    'accent': '#34A853',
    'accent_dark': '#2D8E47',
    'accent_light': '#E6F4EA',
    
    'success': '#34A853',
    'warning': '#F9AB00',
    'danger': '#D93025',
    'info': '#1A73E8',
    
    'bg_main': '#F5F7FA',
    'bg_surface': '#FFFFFF',
    'bg_panel': '#E8EAED',
    'bg_hover': '#F1F3F4',
    
    'text_primary': '#1F1F1F',
    'text_secondary': '#5F6368',
    'text_disabled': '#9AA0A6',
    
    'border': '#DADCE0',
    'divider': '#E0E0E0',
}

def get_stylesheet():
    """Génère le stylesheet adaptatif"""
    font_size = get_font_size()
    
    return f"""
/* ==================== GLOBAL ==================== */
* {{
    font-family: 'Roboto', 'Segoe UI', sans-serif;
}}

QMainWindow {{
    background-color: {THEME['bg_main']};
}}

QWidget {{
    font-size: {font_size}pt;
    color: {THEME['text_primary']};
}}

/* ==================== CARDS / PANELS ==================== */
QGroupBox {{
    background: {THEME['bg_surface']};
    border: 1px solid {THEME['border']};
    border-radius: 6px;
    margin-top: 12px;
    padding: 10px;
    font-weight: 600;
    font-size: {font_size + 0.5}pt;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    top: -6px;
    padding: 3px 10px;
    background: {THEME['primary']};
    color: white;
    border-radius: 3px;
    font-weight: 600;
}}

/* ==================== LABELS ==================== */
QLabel {{
    color: {THEME['text_primary']};
    font-size: {font_size}pt;
    padding: 1px;
}}

QLabel[class="title"] {{
    font-size: {font_size + 6}pt;
    font-weight: 700;
    color: {THEME['primary']};
    padding: 6px 0;
}}

QLabel[class="subtitle"] {{
    font-size: {font_size + 1}pt;
    color: {THEME['text_secondary']};
    padding: 3px 0;
}}

QLabel[class="section-title"] {{
    font-size: {font_size + 2}pt;
    font-weight: 600;
    color: {THEME['primary']};
    padding: 4px 0;
}}

/* ==================== INPUTS ==================== */
QLineEdit {{
    background: white;
    border: 2px solid {THEME['border']};
    border-radius: 4px;
    padding: 6px 8px;
    font-size: {font_size}pt;
    min-height: 22px;
    selection-background-color: {THEME['primary_light']};
}}

QLineEdit:focus {{
    border: 2px solid {THEME['primary']};
    background: {THEME['primary_light']};
}}

QLineEdit:disabled {{
    background: {THEME['bg_panel']};
    color: {THEME['text_disabled']};
}}

/* ==================== COMBOBOX ==================== */
QComboBox {{
    background: white;
    border: 2px solid {THEME['border']};
    border-radius: 4px;
    padding: 6px 8px;
    font-size: {font_size}pt;
    min-height: 22px;
}}

QComboBox:focus {{
    border: 2px solid {THEME['primary']};
    background: {THEME['primary_light']};
}}

QComboBox::drop-down {{
    border: none;
    width: 25px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {THEME['text_secondary']};
    margin-right: 6px;
}}

QComboBox QAbstractItemView {{
    background: white;
    border: 1px solid {THEME['border']};
    selection-background-color: {THEME['primary_light']};
    selection-color: {THEME['text_primary']};
    padding: 3px;
}}

/* ==================== BUTTONS ==================== */
QPushButton {{
    background: {THEME['primary']};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 7px 14px;
    font-weight: 600;
    font-size: {font_size}pt;
    min-height: 28px;
}}

QPushButton:hover {{
    background: {THEME['primary_dark']};
}}

QPushButton:pressed {{
    background: {THEME['primary_dark']};
    padding-top: 8px;
    padding-bottom: 6px;
}}

QPushButton:disabled {{
    background: {THEME['bg_panel']};
    color: {THEME['text_disabled']};
}}

QPushButton[class="success"] {{
    background: {THEME['success']};
}}

QPushButton[class="success"]:hover {{
    background: {THEME['accent_dark']};
}}

QPushButton[class="danger"] {{
    background: {THEME['danger']};
}}

QPushButton[class="danger"]:hover {{
    background: #C5221F;
}}

QPushButton[class="warning"] {{
    background: {THEME['warning']};
    color: {THEME['text_primary']};
}}

QPushButton[class="secondary"] {{
    background: white;
    color: {THEME['primary']};
    border: 2px solid {THEME['primary']};
}}

QPushButton[class="secondary"]:hover {{
    background: {THEME['primary_light']};
}}

/* ==================== TABS ==================== */
QTabWidget::pane {{
    border: none;
    background: transparent;
    top: -1px;
}}

QTabBar {{
    background: transparent;
}}

QTabBar::tab {{
    background: white;
    border: 2px solid {THEME['border']};
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 12px;
    margin-right: 3px;
    color: {THEME['text_secondary']};
    font-weight: 600;
    font-size: {font_size}pt;
    min-width: 80px;
}}

QTabBar::tab:selected {{
    background: {THEME['primary']};
    color: white;
    border-color: {THEME['primary']};
}}

QTabBar::tab:hover:!selected {{
    background: {THEME['bg_hover']};
}}

/* ==================== TABLE ==================== */
QTableWidget {{
    background: white;
    border: 1px solid {THEME['border']};
    border-radius: 6px;
    gridline-color: {THEME['divider']};
    selection-background-color: {THEME['primary_light']};
}}

QTableWidget::item {{
    padding: 5px;
    font-size: {font_size}pt;
}}

QTableWidget::item:selected {{
    background: {THEME['primary_light']};
    color: {THEME['text_primary']};
}}

QHeaderView::section {{
    background: {THEME['bg_panel']};
    color: {THEME['text_primary']};
    padding: 6px;
    border: none;
    border-right: 1px solid {THEME['divider']};
    border-bottom: 2px solid {THEME['primary']};
    font-weight: 600;
    font-size: {font_size}pt;
}}

QHeaderView::section:first {{
    border-top-left-radius: 6px;
}}

QHeaderView::section:last {{
    border-top-right-radius: 6px;
    border-right: none;
}}

/* ==================== TEXT EDIT ==================== */
QTextEdit, QPlainTextEdit {{
    background: white;
    border: 2px solid {THEME['border']};
    border-radius: 6px;
    padding: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: {font_size - 0.5}pt;
    line-height: 1.4;
}}

QTextEdit:focus, QPlainTextEdit:focus {{
    border: 2px solid {THEME['primary']};
}}

/* ==================== SCROLLBAR ==================== */
QScrollBar:vertical {{
    background: {THEME['bg_main']};
    width: 10px;
    border: none;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {THEME['border']};
    border-radius: 5px;
    min-height: 25px;
}}

QScrollBar::handle:vertical:hover {{
    background: {THEME['text_disabled']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: {THEME['bg_main']};
    height: 10px;
    border: none;
}}

QScrollBar::handle:horizontal {{
    background: {THEME['border']};
    border-radius: 5px;
    min-width: 25px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {THEME['text_disabled']};
}}

/* ==================== STATUS BAR ==================== */
QStatusBar {{
    background: {THEME['bg_surface']};
    border-top: 1px solid {THEME['border']};
    color: {THEME['text_secondary']};
    padding: 3px;
    font-size: {font_size - 0.5}pt;
}}

QStatusBar::item {{
    border: none;
}}

/* ==================== MENU BAR ==================== */
QMenuBar {{
    background: {THEME['bg_surface']};
    border-bottom: 1px solid {THEME['border']};
    padding: 3px;
}}

QMenuBar::item {{
    padding: 5px 10px;
    background: transparent;
    color: {THEME['text_primary']};
}}

QMenuBar::item:selected {{
    background: {THEME['primary_light']};
    color: {THEME['primary']};
    border-radius: 3px;
}}

QMenu {{
    background: white;
    border: 1px solid {THEME['border']};
    border-radius: 4px;
    padding: 3px;
}}

QMenu::item {{
    padding: 6px 20px;
    border-radius: 3px;
}}

QMenu::item:selected {{
    background: {THEME['primary_light']};
    color: {THEME['primary']};
}}

/* ==================== RADIO BUTTONS ==================== */
QRadioButton {{
    spacing: 6px;
    color: {THEME['text_primary']};
    font-size: {font_size}pt;
}}

QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border: 2px solid {THEME['border']};
    border-radius: 8px;
    background: white;
}}

QRadioButton::indicator:checked {{
    background: {THEME['primary']};
    border-color: {THEME['primary']};
}}

/* ==================== PROGRESS BAR ==================== */
QProgressBar {{
    border: 2px solid {THEME['border']};
    border-radius: 4px;
    text-align: center;
    background: white;
    height: 20px;
}}

QProgressBar::chunk {{
    background-color: {THEME['primary']};
    border-radius: 2px;
}}

/* ==================== TOOLTIPS ==================== */
QToolTip {{
    background: {THEME['text_primary']};
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 3px;
    font-size: {font_size - 0.5}pt;
}}
"""