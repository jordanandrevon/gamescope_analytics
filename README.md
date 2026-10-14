\# GameScope Analytics



\## 1. Présentation du projet



GameScope Analytics est un projet d'analyse de données consacré au catalogue de jeux vidéo disponible sur Steam.



L'objectif est de collecter des données publiques, de les nettoyer et de les structurer afin de produire des indicateurs utiles à la compréhension du catalogue et de la popularité des jeux.



\*\*Problématique métier :\*\* comment analyser le catalogue Steam afin d'identifier les jeux les plus populaires, les tendances par genre et les titres bénéficiant des meilleurs retours des joueurs ?



\## 2. Sources de données



Les données proviennent de l'API publique \*\*SteamSpy\*\* :



\- Documentation et accès : https://steamspy.com/api.php

\- Périmètre : catalogue de jeux Steam.

\- Indicateurs utilisés : genres, prix, évaluations positives et négatives, estimations du nombre de propriétaires et joueurs simultanés.



Les valeurs de propriétaires fournies par SteamSpy sont des \*\*estimations\*\*, et non des chiffres de ventes réels. Les joueurs simultanés représentent un indicateur d'activité, pas le nombre total de joueurs.



\## 3. Architecture du projet



Le pipeline de données suit les étapes suivantes :



1\. \*\*Collecte :\*\* récupération des données depuis SteamSpy avec Python.

2\. \*\*Préparation :\*\* nettoyage, contrôle des valeurs, suppression des doublons et transformation des données.

3\. \*\*Stockage et analyse :\*\* importation des données dans BigQuery et exécution de requêtes SQL.

4\. \*\*Visualisation :\*\* création d'un tableau de bord interactif avec Looker Studio.



```text

API SteamSpy

&#x20;   ↓

Python : collecte et nettoyage

&#x20;   ↓

Fichiers CSV

&#x20;   ↓

Google BigQuery

&#x20;   ↓

Requêtes SQL

&#x20;   ↓

Looker Studio

```



\## 4. Technologies utilisées



\- \*\*Python\*\* : collecte et préparation des données.

\- \*\*Pandas\*\* : manipulation et nettoyage des données.

\- \*\*Jupyter Notebook\*\* : exploration et documentation des analyses.

\- \*\*Google BigQuery\*\* : stockage et interrogation des données avec SQL.

\- \*\*Looker Studio\*\* : visualisation des indicateurs.

\- \*\*Git et GitHub\*\* : versionnement et partage du projet.



\## 5. Structure du dépôt



\- `collecte\_steamspy.py` : script de collecte des données.

\- `GameScopeAnalitycs.ipynb` : notebook d'exploration et d'analyse.

\- `gamescope\_catalogue\_jeux.csv` : jeu de données nettoyé utilisé pour l'analyse.

\- `lancer\_collecte.bat` : fichier de lancement de la collecte sous Windows.

\- `.gitignore` : liste des fichiers exclus du versionnement.



\## 6. Analyses SQL



Les analyses réalisées dans BigQuery portent notamment sur :



\- La répartition des jeux selon les combinaisons de genres.

\- Les jeux ayant les estimations de propriétaires les plus élevées.

\- Les jeux ayant la plus forte proportion d'avis positifs, avec un minimum d'avis afin de limiter les résultats peu représentatifs.



Les résultats doivent être interprétés en tenant compte des limites des données et du caractère estimatif de certains indicateurs.



\## 7. Installation et exécution



\### Prérequis



\- Python installé sur Windows.

\- Git.

\- Les bibliothèques Python nécessaires au script.

\- Un projet Google Cloud configuré pour BigQuery, avec les droits nécessaires.



\### Récupérer le projet



```bash

git clone https://github.com/jordanandrevon/gamescope\_analytics.git

cd gamescope\_analytics

```



\### Installer les dépendances



Les dépendances exactes seront précisées dans un fichier `requirements.txt` après vérification des imports du projet.



\### Lancer la collecte



Sous Windows, le fichier `lancer\_collecte.bat` permet de démarrer le script de collecte. Son chemin Python doit être adapté à l'environnement de l'ordinateur utilisé.



\## 8. Automatisation et qualité des données



Le projet prévoit une exécution automatisée de la collecte, une journalisation des événements et des erreurs, ainsi qu'un mécanisme de reprise évitant de retraiter les jeux déjà collectés.



Les contrôles de qualité comprennent notamment :



\- La vérification de l'unicité de l'identifiant `appid`.

\- Le contrôle des valeurs manquantes.

\- La conversion des types et la préparation des indicateurs.

\- La distinction entre données observées et données estimées.



\## 9. Tableau de bord



Le tableau de bord Looker Studio présentera les principaux indicateurs du catalogue et permettra d'explorer les résultats à l'aide de visualisations et de filtres interactifs.



Le lien du tableau de bord sera ajouté ici une fois sa publication et ses droits d'accès vérifiés.



\## 10. Limites



\- Les estimations de propriétaires ne constituent pas des données de ventes officielles.

\- Les résultats dépendent du périmètre de collecte et de la disponibilité de l'API.

\- Les genres peuvent être fournis sous forme de combinaisons de plusieurs catégories.

\- Les résultats décrivent le périmètre étudié et ne représentent pas nécessairement l'ensemble du marché du jeu vidéo.



\## 11. Auteur



Projet réalisé dans le cadre de la formation Data Analyst.



