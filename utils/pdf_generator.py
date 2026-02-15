"""
Générateur de rapports PDF
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, 
                                TableStyle, PageBreak, Image)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime
import matplotlib.pyplot as plt
import io


class PDFReportGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4,
                                     rightMargin=2*cm, leftMargin=2*cm,
                                     topMargin=2*cm, bottomMargin=2*cm)
        self.story = []
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Configure les styles personnalisés"""
        # Titre principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1A73E8'),
            spaceAfter=30,
            alignment=1  # Center
        ))
        
        # Titre de section
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1A73E8'),
            spaceAfter=12,
            spaceBefore=20,
            borderWidth=2,
            borderColor=colors.HexColor('#1A73E8'),
            borderPadding=8,
            backColor=colors.HexColor('#E8F0FE')
        ))
        
        # Sous-titre
        self.styles.add(ParagraphStyle(
            name='SubTitle',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34A853'),
            spaceAfter=8,
            spaceBefore=12
        ))
        
        # Texte normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            spaceAfter=6
        ))
    
    def add_header(self, main_window):
        """Ajoute l'en-tête du rapport"""
        # Titre principal
        title = Paragraph(
            "RAPPORT D'ANALYSE HYDRAULIQUE<br/>SYSTÈME DE POMPAGE",
            self.styles['CustomTitle']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Date
        date_text = f"Généré le {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}"
        date_para = Paragraph(date_text, self.styles['CustomBody'])
        self.story.append(date_para)
        self.story.append(Spacer(1, 1*cm))
    
    def add_system_characteristics(self, main_window):
        """Section 1: Caractéristiques du système"""
        self.story.append(Paragraph(
            "1. CARACTÉRISTIQUES DU SYSTÈME",
            self.styles['SectionTitle']
        ))
        
        Q = float(main_window.input_tab.q_input.text())
        Hg = main_window.pipe_model.H_geometric
        Lasp = main_window.pipe_model.L_aspiration
        Lref = main_window.pipe_model.L_refoulement
        T = main_window.fluid_model.temperature
        rho = main_window.fluid_model.density
        
        data = [
            ['Paramètre', 'Valeur', 'Unité'],
            ['Débit nominal (Q)', f'{Q:.4f}', 'm³/s'],
            ['Hauteur géométrique (Hg)', f'{Hg:.4f}', 'm'],
            ['Longueur aspiration', f'{Lasp:.2f}', 'm'],
            ['Longueur refoulement', f'{Lref:.2f}', 'm'],
            ['Longueur totale', f'{Lasp + Lref:.2f}', 'm'],
            ['Température fluide', f'{T:.1f}', '°C'],
            ['Masse volumique', f'{rho:.1f}', 'kg/m³'],
        ]
        
        table = Table(data, colWidths=[8*cm, 4*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A73E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F7FA')])
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 1*cm))
    
    def add_optimal_solution(self, main_window):
        """Section 2: Solution optimale"""
        sol = main_window.best_solution
        
        self.story.append(Paragraph(
            "2. SOLUTION OPTIMALE",
            self.styles['SectionTitle']
        ))
        
        data = [
            ['Paramètre', 'Valeur', 'Unité'],
            ['Débit de fonctionnement (Qf)', f'{sol.Qf:.4f}', 'm³/s'],
            ['Hauteur manométrique (Hf)', f'{sol.Hf:.4f}', 'm'],
            ['Rendement pompe (ηp)', f'{sol.efficiency*100:.2f}', '%'],
        ]
        
        if main_window.economic_data:
            nm = main_window.economic_data['nm_motor']
            P_total = main_window.economic_data['powers']['P_total_kW']
            data.append(['Rendement moteur (ηm)', f'{nm*100:.2f}', '%'])
            data.append(['Puissance électrique totale', f'{P_total:.2f}', 'kW'])
        
        table = Table(data, colWidths=[8*cm, 4*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34A853')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#E6F4EA')])
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 1*cm))
    
    def add_pump_configuration(self, main_window):
        """Section 3: Configuration de la pompe"""
        sol = main_window.best_solution
        
        self.story.append(Paragraph(
            "3. CONFIGURATION DE LA POMPE",
            self.styles['SectionTitle']
        ))
        
        # Configuration text
        if sol.configuration == 'Seule':
            config_desc = "Pompe seule (1 pompe unique)"
        elif sol.configuration == 'Série':
            config_desc = f"Montage en série ({sol.n_serie} pompes en série)"
        elif sol.configuration == 'Parallèle':
            config_desc = f"Montage en parallèle ({sol.n_parallel} pompes en parallèle)"
        elif sol.configuration == 'Mixte':
            config_desc = f"Montage mixte ({sol.n_parallel} branches × {sol.n_serie} pompes/branche)"
        else:
            config_desc = sol.configuration
        
        data = [
            ['Paramètre', 'Valeur'],
            ['Type de pompe', sol.pump_type],
            ['Configuration', config_desc],
            ['Nombre total de pompes', str(sol.total_pumps)],
            ['Diamètre de conduite', f'{sol.diameter:.4f} m ({sol.diameter*1000:.1f} mm)'],
        ]
        
        table = Table(data, colWidths=[8*cm, 7*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F9AB00')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FEF7E0')])
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 1*cm))
    
    def add_npsh_verification(self, main_window):
        """Section 4: Vérification NPSH"""
        sol = main_window.best_solution
        
        self.story.append(Paragraph(
            "4. VÉRIFICATION NPSH (CAVITATION)",
            self.styles['SectionTitle']
        ))
        
        status = "✓ PAS DE RISQUE" if sol.NPSH_margin > 0 else "✗ RISQUE DE CAVITATION"
        status_color = colors.HexColor('#34A853') if sol.NPSH_margin > 0 else colors.HexColor('#EA4335')
        
        data = [
            ['Paramètre', 'Valeur', 'Unité'],
            ['NPSHr (requis)', f'{sol.NPSHr:.4f}', 'm'],
            ['NPSHa (disponible)', f'{sol.NPSHa:.4f}', 'm'],
            ['Marge de sécurité', f'{sol.NPSH_margin:.4f}', 'm'],
            ['Statut', status, '-'],
        ]
        
        table = Table(data, colWidths=[8*cm, 4*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EA4335')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FCE8E6')]),
            ('TEXTCOLOR', (1, 4), (1, 4), status_color),
            ('FONTNAME', (1, 4), (1, 4), 'Helvetica-Bold'),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 1*cm))
    
    def add_economic_analysis(self, main_window):
        """Section 5: Analyse économique"""
        if not main_window.economic_data:
            return
        
        data = main_window.economic_data
        currency = data['currency']
        
        self.story.append(Paragraph(
            "5. ANALYSE ÉCONOMIQUE",
            self.styles['SectionTitle']
        ))
        
        table_data = [
            ['Poste', 'Montant', 'Unité'],
            ['Coût conduite', f"{data['cost_pipe']:,.2f}", currency],
            ['Coût pompes', f"{data['cost_pumps']:,.2f}", currency],
            ['Coût énergétique annuel', f"{data['cost_energy_annual']:,.2f}", f'{currency}/an'],
            ['COÛT TOTAL (installation + 1 an)', f"{data['cost_total']:,.2f}", currency],
        ]
        
        table = Table(table_data, colWidths=[8*cm, 4*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A73E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#E8F0FE')]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#BBDEFB')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 1*cm))
    
    def add_hmt_details(self, main_window):
        """Section 6: Détails des calculs HMT"""
        if not main_window.hmt_results:
            return
        
        self.story.append(PageBreak())
        
        self.story.append(Paragraph(
            "6. DÉTAILS DES CALCULS HMT",
            self.styles['SectionTitle']
        ))
        
        for result in main_window.hmt_results:
            D = result['D']
            
            self.story.append(Paragraph(
                f"Diamètre D = {D:.4f} m ({D*1000:.1f} mm)",
                self.styles['SubTitle']
            ))
            
            data = [
                ['Paramètre', 'Valeur', 'Unité'],
                ['Vitesse (V)', f"{result['V']:.4f}", 'm/s'],
                ['Reynolds (Re)', f"{result['Re']:.2f}", '-'],
                ['Coefficient frottement (f)', f"{result['f']:.6f}", '-'],
                ['Pertes singulières (K_T)', f"{result['K_T']:.6f}", '-'],
                ['Coefficient réseau (A)', f"{result['A']:.6f}", '-'],
                ['Hauteur géométrique (Hg)', f"{result['Hg']:.4f}", 'm'],
                ['Pertes de charge (Δh)', f"{result['Dh']:.4f}", 'm'],
                ['HMT', f"{result['HMT']:.4f}", 'm'],
            ]
            
            table = Table(data, colWidths=[8*cm, 4*cm, 3*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9334E6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3E5F5')]),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E1BEE7')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ]))
            
            self.story.append(table)
            self.story.append(Spacer(1, 0.5*cm))
    
    def add_graph(self, main_window):
        """Ajoute un graphique au PDF"""
        try:
            sol = main_window.best_solution
            D = sol.diameter
            
            # Trouver la pompe
            pump = None
            for p in main_window.pumps:
                if p.type == sol.pump_type:
                    pump = p
                    break
            
            if not pump:
                return
            
            # Créer le graphique
            import numpy as np
            fig, ax = plt.subplots(figsize=(6, 4))
            
            # Courbe pompe
            Qp = np.array(pump.Qp.copy())
            Hp = np.array(pump.Hp.copy())
            
            if sol.configuration == 'Série' or sol.configuration == 'Mixte':
                Hp = Hp * sol.n_serie
            if sol.configuration == 'Parallèle' or sol.configuration == 'Mixte':
                Qp = Qp * sol.n_parallel
            
            ax.plot(Qp, Hp, '-', color='#1A73E8', linewidth=2, label='Courbe pompe')
            
            # Courbe système
            curve = main_window.system_curves[D]
            ax.plot(curve['Qs'], curve['HMTs'], '-', color='#34A853', 
                   linewidth=2, label='Courbe système')
            
            # Point de fonctionnement
            ax.plot(sol.Qf, sol.Hf, 'o', color='#EA4335', markersize=12,
                   label='Point fonctionnement')
            
            ax.set_xlabel('Débit (m³/s)', fontweight='bold')
            ax.set_ylabel('Hauteur (m)', fontweight='bold')
            ax.set_title('Point de Fonctionnement du Système', fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Sauvegarder dans un buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            # Ajouter au PDF
            self.story.append(PageBreak())
            self.story.append(Paragraph(
                "7. GRAPHIQUE - POINT DE FONCTIONNEMENT",
                self.styles['SectionTitle']
            ))
            
            img = Image(img_buffer, width=15*cm, height=10*cm)
            self.story.append(img)
            
        except Exception as e:
            print(f"Erreur lors de la création du graphique: {e}")
    
    def add_footer(self):
        """Ajoute le pied de page"""
        self.story.append(Spacer(1, 1*cm))
        
        footer_text = f"""
        <para align=center>
        ───────────────────────────────────────────────────────────────<br/>
        Rapport généré par le <b>Calculateur HMT Professionnel</b> - Version 2.0<br/>
        {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}<br/>
        ───────────────────────────────────────────────────────────────
        </para>
        """
        
        self.story.append(Paragraph(footer_text, self.styles['CustomBody']))
    
    def generate(self, main_window):
        """Génère le PDF complet"""
        self.add_header(main_window)
        self.add_system_characteristics(main_window)
        self.add_optimal_solution(main_window)
        self.add_pump_configuration(main_window)
        self.add_npsh_verification(main_window)
        self.add_economic_analysis(main_window)
        self.add_hmt_details(main_window)
        self.add_graph(main_window)
        self.add_footer()
        
        # Construire le PDF
        self.doc.build(self.story)