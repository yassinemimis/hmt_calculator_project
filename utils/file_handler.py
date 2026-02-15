"""
Gestionnaire de fichiers (import/export) - Support JSON & CSV
"""
import json
import csv
from models.pump_model import PumpModel


class FileHandler:
    
    @staticmethod
    def load_pump_from_json(filepath):
        """Charge une pompe depuis un fichier JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Valider la structure
            required_keys = ['type', 'nombre', 'Qp', 'Hp', 'np', 'NPSH']
            missing_keys = [key for key in required_keys if key not in data]
            
            if missing_keys:
                raise ValueError(f"Clés manquantes dans le fichier JSON: {', '.join(missing_keys)}")
            
            # Vérifier que ce sont des listes
            for key in ['Qp', 'Hp', 'np', 'NPSH']:
                if not isinstance(data[key], list):
                    raise ValueError(f"'{key}' doit être une liste (array)")
            
            # Vérifier longueurs
            lengths = [len(data[key]) for key in ['Qp', 'Hp', 'np', 'NPSH']]
            if len(set(lengths)) != 1:
                raise ValueError(
                    f"Les tableaux doivent avoir la même longueur.\n"
                    f"Longueurs actuelles: Qp={lengths[0]}, Hp={lengths[1]}, "
                    f"np={lengths[2]}, NPSH={lengths[3]}"
                )
            
            # Vérifier que les listes ne sont pas vides
            if lengths[0] == 0:
                raise ValueError("Les tableaux de données sont vides")
            
            # Créer le modèle
            pump = PumpModel.from_json(data)
            return pump
        
        except json.JSONDecodeError as e:
            raise Exception(f"Fichier JSON invalide: {str(e)}")
        except KeyError as e:
            raise Exception(f"Clé manquante dans le JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Erreur lors du chargement JSON: {str(e)}")
    
    @staticmethod
    def load_pump_from_csv(filepath):
        """
        Charge une pompe depuis un fichier CSV
        
        Format CSV attendu:
        Type,Pompe Centrifuge 100kW
        Nombre,4
        Qp,Hp,np,NPSH
        0.01,30,0.60,2.5
        0.02,32,0.70,3.0
        0.03,33,0.80,3.5
        ...
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                # Lire les métadonnées (premières lignes)
                metadata = {}
                data_started = False
                Qp, Hp, np_vals, NPSH = [], [], [], []
                
                for row in reader:
                    if not row or len(row) == 0:
                        continue
                    
                    # Ligne de métadonnées
                    if not data_started and len(row) >= 2:
                        key = row[0].strip().lower()
                        
                        if key == 'type':
                            metadata['type'] = row[1].strip()
                        elif key == 'nombre':
                            metadata['nombre'] = int(row[1].strip())
                        elif key == 'qp':
                            # Header des données - commencer à lire les données
                            data_started = True
                            continue
                    
                    # Lignes de données
                    elif data_started and len(row) == 4:
                        try:
                            Qp.append(float(row[0].strip()))
                            Hp.append(float(row[1].strip()))
                            np_vals.append(float(row[2].strip()))
                            NPSH.append(float(row[3].strip()))
                        except ValueError:
                            # Ignorer les lignes invalides
                            continue
                
                # Validation
                if 'type' not in metadata:
                    raise ValueError("Métadonnée 'Type' manquante dans le CSV")
                if 'nombre' not in metadata:
                    raise ValueError("Métadonnée 'Nombre' manquante dans le CSV")
                if len(Qp) == 0:
                    raise ValueError("Aucune donnée de pompe trouvée dans le CSV")
                
                # Vérifier longueurs
                if not (len(Qp) == len(Hp) == len(np_vals) == len(NPSH)):
                    raise ValueError(
                        f"Les colonnes doivent avoir la même longueur.\n"
                        f"Qp: {len(Qp)}, Hp: {len(Hp)}, np: {len(np_vals)}, NPSH: {len(NPSH)}"
                    )
                
                # Créer le dictionnaire
                pump_data = {
                    'type': metadata['type'],
                    'nombre': metadata['nombre'],
                    'Qp': Qp,
                    'Hp': Hp,
                    'np': np_vals,
                    'NPSH': NPSH
                }
                
                # Créer le modèle
                pump = PumpModel.from_json(pump_data)
                return pump
        
        except Exception as e:
            raise Exception(f"Erreur lors du chargement CSV: {str(e)}")
    
    @staticmethod
    def save_pump_to_json(pump, filepath):
        """Sauvegarde une pompe dans un fichier JSON"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(pump.to_dict(), f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde JSON: {str(e)}")
    
    @staticmethod
    def save_pump_to_csv(pump, filepath):
        """
        Sauvegarde une pompe dans un fichier CSV
        
        Format:
        Type,<nom>
        Nombre,<nombre>
        Qp,Hp,np,NPSH
        <données>
        """
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                
                # Métadonnées
                writer.writerow(['Type', pump.type])
                writer.writerow(['Nombre', pump.nombre])
                writer.writerow([])  # Ligne vide
                
                # Header
                writer.writerow(['Qp', 'Hp', 'np', 'NPSH'])
                
                # Données
                for i in range(len(pump.Qp)):
                    writer.writerow([
                        pump.Qp[i],
                        pump.Hp[i],
                        pump.np[i],
                        pump.NPSH[i]
                    ])
        
        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde CSV: {str(e)}")
    
    @staticmethod
    def export_results_txt(content, filepath):
        """Exporte les résultats en TXT"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"Erreur lors de l'export TXT: {str(e)}")
    
    @staticmethod
    def export_results_json(data, filepath):
        """Exporte les résultats en JSON"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Erreur lors de l'export JSON: {str(e)}")
    
    @staticmethod
    def export_results_csv(solutions, filepath):
        """Exporte les solutions en CSV"""
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow([
                    'Rang', 'Type Pompe', 'Configuration', 'N_Serie', 'N_Parallele',
                    'Diametre (m)', 'Qf (m³/s)', 'Hf (m)', 'Rendement (%)',
                    'NPSHr (m)', 'NPSHa (m)', 'Marge NPSH (m)'
                ])
                
                # Données
                for idx, sol in enumerate(solutions):
                    writer.writerow([
                        idx + 1,
                        sol.pump_type,
                        sol.configuration,
                        sol.n_serie,
                        sol.n_parallel,
                        f"{sol.diameter:.4f}",
                        f"{sol.Qf:.4f}",
                        f"{sol.Hf:.4f}",
                        f"{sol.efficiency*100:.2f}",
                        f"{sol.NPSHr:.4f}",
                        f"{sol.NPSHa:.4f}",
                        f"{sol.NPSH_margin:.4f}"
                    ])
        
        except Exception as e:
            raise Exception(f"Erreur lors de l'export CSV: {str(e)}")