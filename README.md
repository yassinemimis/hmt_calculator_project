# 🚀 Calculateur HMT Professionnel

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)

Application professionnelle pour le calcul de la **Hauteur Manométrique Totale (HMT)** des systèmes de pompage avec interface PyQt5 moderne.

![Industrial Engineering Design](https://img.shields.io/badge/Design-Industrial%20Engineering-1A73E8)

---

## ✨ Fonctionnalités

- ✅ **Calcul HMT** avec 3 méthodes de coefficient de frottement
  - Colebrook-White
  - Haaland
  - Swamee-Jain
- ✅ **Optimisation automatique** du choix de pompe
  - Pompe seule
  - Montage en série
  - Montage en parallèle
  - Montage mixte
- ✅ **Vérification NPSH** (anti-cavitation)
- ✅ **Calcul économique** complet
- ✅ **Visualisation graphique** interactive avec Matplotlib
- ✅ **Export multi-format**
  - TXT (rapport texte)
  - JSON (données structurées)
  - CSV (tableaux)
  - PDF (rapport professionnel)
- ✅ **Import pompes** JSON et CSV
- ✅ **Interface moderne** PyQt5 avec thème Industrial Engineering

---

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

---

## 🔧 Installation

### Méthode 1 : Installation avec pip (recommandée)

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/hmt-calculator.git
cd hmt-calculator

# Installer avec pip
pip install .

# Ou en mode développement
pip install -e .

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