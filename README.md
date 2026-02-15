# Calculateur HMT Professionnel

Application professionnelle pour le calcul de la Hauteur Manométrique Totale (HMT) des systèmes de pompage.

## 🚀 Fonctionnalités

- ✅ Calcul HMT avec 3 méthodes de coefficient de frottement
- ✅ Optimisation automatique du choix de pompe
- ✅ Vérification NPSH (anti-cavitation)
- ✅ Calcul économique complet
- ✅ Visualisation graphique interactive
- ✅ Export des résultats (TXT, JSON)
- ✅ Interface moderne PyQt5

## 📋 Prérequis

- Python 3.7+
- pip

## 🔧 Installation

```bash
# Cloner le projet
git clone https://github.com/votre-repo/hmt-calculator.git
cd hmt-calculator

# Installer les dépendances
pip install -r requirements.txt
```

## ▶️ Lancement

### Windows
```batch
run.bat
```

### Linux/Mac
```bash
chmod +x run.sh
./run.sh
```

### Manuel
```bash
python main.py
```

## 📚 Utilisation

1. **Données d'entrée** : Saisir les paramètres du système
2. **Pompes** : Importer les pompes disponibles (fichiers JSON)
3. **Calcul HMT** : Choisir les diamètres et calculer
4. **Optimisation** : Trouver la configuration optimale
5. **Économie** : Calculer les coûts
6. **Résultats** : Consulter et exporter les résultats
7. **Graphiques** : Visualiser les courbes

## 📁 Structure du projet

```
hmt_calculator_project/
├── main.py                 # Point d'entrée
├── config.py              # Configuration
├── models/                # Modèles de données
├── controllers/           # Logique métier
├── views/                 # Interface utilisateur
├── utils/                 # Utilitaires
├── assets/                # Ressources (styles, icons)
└── data/                  # Données exemple
```

## 📄 Format fichier pompe (JSON)

```json
{
  "type": "Pompe Centrifuge 100kW",
  "nombre": 4,
  "Qp": [0.01, 0.02, 0.03, 0.04, 0.05],
  "Hp": [30, 32, 33, 32, 30],
  "np": [0.60, 0.70, 0.80, 0.82, 0.78],
  "NPSH": [2.5, 3.0, 3.5, 4.0, 4.5]
}
```

## 🤝 Contribution

Les contributions sont les bienvenues !

## 📝 Licence

MIT License

## 👨‍💻 Auteur

Votre Nom