# Prédiction de Rendement Agricole

[![CI/CD Pipeline](https://github.com/USERNAME/REPO/actions/workflows/ci_cd.yaml/badge.svg)](https://github.com/USERNAME/REPO/actions/workflows/ci_cd.yaml)

Ce projet offre une solution complète de Machine Learning pour prédire les rendements agricoles en fonction de facteurs environnementaux et d'intrants.

## 🚀 Fonctionnalités

### API REST (FastAPI)
L'API expose les points de terminaison suivants :
- `GET /health` : Vérifie si le service est opérationnel.
- `POST /predict` : Prédit le rendement en hg/ha.
    - **Input** : Année, Précipitations, Pesticides, Température, Région, Culture.

### Interface Utilisateur (Streamlit)
Une application web interactive permettant aux utilisateurs de saisir des paramètres et de visualiser les prédictions de rendement instantanément.

### MLOps
- **Tracking** : Suivi des expériences et des modèles avec **MLflow**.
- **Pipeline** : Prétraitement des données et entraînement de modèles (Random Forest, Ridge).

## 🛠️ Installation et Exécution

### Prérequis
- Python 3.12+
- [Poetry](https://python-poetry.org/)
- Docker (optionnel)

### Développement Local (avec Poetry)
1.  **Installation des dépendances** :
    ```bash
    poetry install
    ```
2.  **Entraînement du modèle** :
    ```bash
    poetry run python src/train_model.py
    ```
3.  **Lancer l'API** :
    ```bash
    poetry run uvicorn src.app:app --reload
    ```
    Documentation API disponible sur `http://localhost:8000/docs`.
4.  **Lancer l'Application Web** :
    ```bash
    poetry run streamlit run src/streamlit_app.py
    ```

### Via Docker
1.  **Construire l'image** :
    ```bash
    docker build -t crop-yield-prediction .
    ```
2.  **Lancer le conteneur** :
    ```bash
    docker run -p 8000:8000 crop-yield-prediction
    ```

## 🔄 CI/CD

Le projet intègre un pipeline d'intégration et de déploiement continu via **GitHub Actions** :
- **Tests** : Exécution automatique des tests unitaires (`pytest`).
- **Build** : Construction de l'image Docker.
- **Deploy** : Push de l'image sur Docker Hub (sur la branche `main`).

Pour plus de détails, consultez la [Documentation CI/CD](docs/CI_CD.md).
