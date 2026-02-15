"""
Custom Widgets pour Industrial Engineering UI
"""
from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QWidget)
from PyQt5.QtCore import Qt
from assets.styles.theme import get_color


class Card(QFrame):
    """بطاقة (Card) احترافية"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setStyleSheet(f"""
            QFrame#card {{
                background: white;
                border: 1px solid {get_color('border')};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        if title:
            title_label = QLabel(title)
            title_label.setProperty("class", "section-title")
            layout.addWidget(title_label)
            
            # Divider
            divider = QFrame()
            divider.setFrameShape(QFrame.HLine)
            divider.setStyleSheet(f"background: {get_color('divider')};")
            divider.setMaximumHeight(1)
            layout.addWidget(divider)


class StatCard(QFrame):
    """بطاقة إحصائيات"""
    
    def __init__(self, title, value, unit="", icon="", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 2px solid {get_color('border')};
                border-radius: 10px;
                padding: 16px;
            }}
            QFrame:hover {{
                border-color: {get_color('primary')};
            }}
        """)
        
        layout = QVBoxLayout(self)
        
        # Titre
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {get_color('text_secondary')}; font-size: 9pt;")
        layout.addWidget(title_label)
        
        # Valeur
        value_layout = QHBoxLayout()
        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"color: {get_color('primary')}; font-size: 20pt; font-weight: bold;")
        value_layout.addWidget(value_label)
        
        if unit:
            unit_label = QLabel(unit)
            unit_label.setStyleSheet(f"color: {get_color('text_secondary')}; font-size: 11pt;")
            value_layout.addWidget(unit_label)
        
        value_layout.addStretch()
        layout.addLayout(value_layout)


class SectionHeader(QWidget):
    """En-tête de section"""
    
    def __init__(self, title, subtitle="", parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(4)
        
        # Titre
        title_label = QLabel(title)
        title_label.setProperty("class", "title")
        layout.addWidget(title_label)
        
        # Sous-titre
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setProperty("class", "subtitle")
            layout.addWidget(subtitle_label)
        
        # Ligne de séparation
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {get_color('primary')},
                stop:1 transparent);
            max-height: 3px;
            border-radius: 1px;
        """)
        layout.addWidget(line)


class IconButton(QPushButton):
    """Bouton avec icône"""
    
    def __init__(self, text, icon="", parent=None):
        super().__init__(text, parent)
        if icon:
            self.setText(f"{icon}  {text}")
        self.setMinimumHeight(44)


class InfoBox(QFrame):
    """Boîte d'information (info/warning/success/danger)"""
    
    def __init__(self, text, box_type="info", parent=None):
        super().__init__(parent)
        
        colors = {
            'info': get_color('info'),
            'success': get_color('success'),
            'warning': get_color('warning'),
            'danger': get_color('danger')
        }
        
        bg_colors = {
            'info': get_color('primary_light'),
            'success': get_color('accent_light'),
            'warning': '#FEF7E0',
            'danger': '#FCE8E6'
        }
        
        color = colors.get(box_type, colors['info'])
        bg_color = bg_colors.get(box_type, bg_colors['info'])
        
        self.setStyleSheet(f"""
            QFrame {{
                background: {bg_color};
                border-left: 4px solid {color};
                border-radius: 6px;
                padding: 12px 16px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        
        # Icône
        icons = {
            'info': 'ℹ️',
            'success': '✓',
            'warning': '⚠',
            'danger': '✗'
        }
        
        icon_label = QLabel(icons.get(box_type, 'ℹ️'))
        icon_label.setStyleSheet(f"font-size: 16pt; color: {color};")
        layout.addWidget(icon_label)
        
        # Texte
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(f"color: {get_color('text_primary')};")
        layout.addWidget(text_label, 1)