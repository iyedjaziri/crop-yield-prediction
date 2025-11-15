# Rapport Métier: Système de Prédiction de Rendement Agricole

## 1. Résumé Exécutif
Ce projet vise à fournir aux agriculteurs un outil d'aide à la décision permettant de prédire les rendements agricoles et de recommander les cultures les plus rentables en fonction des conditions climatiques et des intrants (pesticides).

**Impact Attendu :**
- Optimisation des ressources (pesticides, eau).
- Maximisation des profits par la sélection des cultures adaptées.
- Réduction des risques liés aux aléas climatiques.

## 2. Méthodologie Technique
Nous avons consolidé des données historiques de rendement, de précipitations, de température et d'utilisation de pesticides.
- **Données :** Fusion sur la base "Année + Pays".
- **Modélisation :** Comparaison de plusieurs algorithmes (Ridge Regression vs Random Forest).
- **Optimisation :** Recherche systématique des meilleurs hyperparamètres (GridSearch).

## 3. Résultats et Performance
Le modèle retenu est le **Random Forest Regressor**.

### Métriques Clés
| Métrique | Valeur | Interprétation Business |
| :--- | :--- | :--- |
| **R² (Coefficient de Détermination)** | **0.94** | Le modèle explique **94%** des variations de rendement. C'est un score excellent, indiquant une très haute fiabilité des prédictions. |
| **RMSE (Erreur Quadratique Moyenne)** | **~20,000 hg/ha** | En moyenne, nos prédictions s'écartent de la réalité de cette valeur. Compte tenu des rendements moyens élevés, cette marge d'erreur est acceptable pour la planification stratégique. |
| **Profitability Proxy** | **Variable** | Indicateur personnalisé estimant le profit potentiel (Rendement * Prix - Coût Pesticides). Le modèle permet d'identifier les cultures maximisant cet indicateur. |

### MLflow Tracking
Nous avons utilisé MLflow pour tracer chaque expérience.
- **Ce que vous verrez dans MLflow :**
    - Comparaison des modèles (Ridge vs Random Forest).
    - Hyperparamètres utilisés (nombre d'arbres, profondeur).
    - Courbes d'apprentissage et métriques de performance.
    - L'artefact du modèle final prêt pour le déploiement.

## 4. Facteurs d'Influence (Feature Importance)
Les principaux facteurs influençant le rendement identifiés par le modèle sont :
1.  **Type de Culture (Item)** : Le choix de la culture est le facteur déterminant n°1.
2.  **Pesticides** : Une corrélation forte a été observée, mais avec des rendements décroissants au-delà d'un certain seuil.
3.  **Précipitations & Température** : Facteurs climatiques critiques, variant selon la région.

## 5. Prochaines Étapes
- **Déploiement :** L'API est conteneurisée (Docker) et prête pour la production.
- **Monitoring :** Surveillance continue de la performance du modèle pour détecter toute dérive (Data Drift).
- **Amélioration :** Intégration de données de sol plus granulaires et de prix de marché en temps réel.
