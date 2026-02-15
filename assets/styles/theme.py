"""
Industrial Engineering Theme - Complete Design System
"""

THEME = {
    # Primary Colors
    'primary': '#1A73E8',
    'primary_dark': '#1557B0',
    'primary_light': '#E8F0FE',
    
    # Accent Colors
    'accent': '#34A853',
    'accent_dark': '#2D8E47',
    'accent_light': '#E6F4EA',
    
    # Status Colors
    'success': '#34A853',
    'warning': '#F9AB00',
    'danger': '#D93025',
    'info': '#1A73E8',
    
    # Background
    'bg_main': '#F5F7FA',
    'bg_surface': '#FFFFFF',
    'bg_panel': '#E8EAED',
    'bg_hover': '#F1F3F4',
    
    # Text
    'text_primary': '#1F1F1F',
    'text_secondary': '#5F6368',
    'text_disabled': '#9AA0A6',
    
    # Borders & Dividers
    'border': '#DADCE0',
    'divider': '#E0E0E0',
    
    # Shadows
    'shadow_light': 'rgba(0, 0, 0, 0.08)',
    'shadow_medium': 'rgba(0, 0, 0, 0.12)',
}

STYLESHEET = f"""
/* ==================== GLOBAL ==================== */
* {{
    font-family: 'Roboto', 'Segoe UI', sans-serif;
}}

QMainWindow {{
    background-color: {THEME['bg_main']};
}}

QWidget {{
    font-size: 10pt;
    color: {THEME['text_primary']};
}}

/* ==================== CARDS / PANELS ==================== */
QGroupBox {{
    background: {THEME['bg_surface']};
    border: 1px solid {THEME['border']};
    border-radius: 8px;
    margin-top: 16px;
    padding: 16px;
    font-weight: 600;
    font-size: 11pt;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    top: -8px;
    padding: 4px 12px;
    background: {THEME['primary']};
    color: white;
    border-radius: 4px;
    font-weight: 600;
}}

/* ==================== LABELS ==================== */
QLabel {{
    color: {THEME['text_primary']};
    font-size: 10pt;
    padding: 2px;
}}

QLabel[class="title"] {{
    font-size: 18pt;
    font-weight: 700;
    color: {THEME['primary']};
    padding: 8px 0;
}}

QLabel[class="subtitle"] {{
    font-size: 11pt;
    color: {THEME['text_secondary']};
    padding: 4px 0;
}}

QLabel[class="section-title"] {{
    font-size: 12pt;
    font-weight: 600;
    color: {THEME['primary']};
    padding: 6px 0;
}}

/* ==================== INPUTS ==================== */
QLineEdit {{
    background: white;
    border: 2px solid {THEME['border']};
    border-radius: 6px;
    padding: 10px 12px;
    font-size: 10pt;
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
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 10pt;
}}

QComboBox:focus {{
    border: 2px solid {THEME['primary']};
    background: {THEME['primary_light']};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {THEME['text_secondary']};
    margin-right: 8px;
}}

QComboBox QAbstractItemView {{
    background: white;
    border: 1px solid {THEME['border']};
    selection-background-color: {THEME['primary_light']};
    selection-color: {THEME['text_primary']};
    padding: 4px;
}}

/* ==================== BUTTONS ==================== */
QPushButton {{
    background: {THEME['primary']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 10pt;
    min-height: 36px;
}}

QPushButton:hover {{
    background: {THEME['primary_dark']};
}}

QPushButton:pressed {{
    background: {THEME['primary_dark']};
    padding-top: 12px;
    padding-bottom: 8px;
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
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 12px 20px;
    margin-right: 4px;
    color: {THEME['text_secondary']};
    font-weight: 600;
    font-size: 10pt;
    min-width: 120px;
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
    border-radius: 8px;
    gridline-color: {THEME['divider']};
    selection-background-color: {THEME['primary_light']};
}}

QTableWidget::item {{
    padding: 8px;
}}

QTableWidget::item:selected {{
    background: {THEME['primary_light']};
    color: {THEME['text_primary']};
}}

QHeaderView::section {{
    background: {THEME['bg_panel']};
    color: {THEME['text_primary']};
    padding: 10px;
    border: none;
    border-right: 1px solid {THEME['divider']};
    border-bottom: 2px solid {THEME['primary']};
    font-weight: 600;
}}

QHeaderView::section:first {{
    border-top-left-radius: 8px;
}}

QHeaderView::section:last {{
    border-top-right-radius: 8px;
    border-right: none;
}}

/* ==================== TEXT EDIT ==================== */
QTextEdit, QPlainTextEdit {{
    background: white;
    border: 2px solid {THEME['border']};
    border-radius: 8px;
    padding: 12px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9.5pt;
    line-height: 1.6;
}}

QTextEdit:focus, QPlainTextEdit:focus {{
    border: 2px solid {THEME['primary']};
}}

/* ==================== SCROLLBAR ==================== */
QScrollBar:vertical {{
    background: {THEME['bg_main']};
    width: 12px;
    border: none;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {THEME['border']};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {THEME['text_disabled']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: {THEME['bg_main']};
    height: 12px;
    border: none;
}}

QScrollBar::handle:horizontal {{
    background: {THEME['border']};
    border-radius: 6px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {THEME['text_disabled']};
}}

/* ==================== STATUS BAR ==================== */
QStatusBar {{
    background: {THEME['bg_surface']};
    border-top: 1px solid {THEME['border']};
    color: {THEME['text_secondary']};
    padding: 4px;
}}

QStatusBar::item {{
    border: none;
}}

/* ==================== MENU BAR ==================== */
QMenuBar {{
    background: {THEME['bg_surface']};
    border-bottom: 1px solid {THEME['border']};
    padding: 4px;
}}

QMenuBar::item {{
    padding: 6px 12px;
    background: transparent;
    color: {THEME['text_primary']};
}}

QMenuBar::item:selected {{
    background: {THEME['primary_light']};
    color: {THEME['primary']};
    border-radius: 4px;
}}

QMenu {{
    background: white;
    border: 1px solid {THEME['border']};
    border-radius: 6px;
    padding: 4px;
}}

QMenu::item {{
    padding: 8px 24px;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background: {THEME['primary_light']};
    color: {THEME['primary']};
}}

/* ==================== RADIO BUTTONS ==================== */
QRadioButton {{
    spacing: 8px;
    color: {THEME['text_primary']};
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {THEME['border']};
    border-radius: 9px;
    background: white;
}}

QRadioButton::indicator:checked {{
    background: {THEME['primary']};
    border-color: {THEME['primary']};
}}

QRadioButton::indicator:checked::after {{
    content: "";
    width: 8px;
    height: 8px;
    border-radius: 4px;
    background: white;
}}

/* ==================== TOOLTIPS ==================== */
QToolTip {{
    background: {THEME['text_primary']};
    color: white;
    border: none;
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 9pt;
}}
"""

def get_stylesheet():
    return STYLESHEET

# الألوان لاستخدامها في الكود
def get_color(color_name):
    return THEME.get(color_name, '#000000')