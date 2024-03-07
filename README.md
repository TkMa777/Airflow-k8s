# Agrégation de Données avec Airflow sur Kubernetes

## Description

Ce projet implémente un flux de travail automatisé qui utilise Apache Airflow pour extraire, analyser et agréger des données de vente à partir d'un fichier CSV dans un environnement Kubernetes. Le DAG (`Directed Acyclic Graph`) défini dans Airflow va chercher les données, calculer les prix de vente moyens, maximums et le nombre de modèles uniques par marque, puis sauvegarder cette information pour une utilisation future.

## Fonctionnalités

- **Extraction de données :** Télécharge les dernières données de vente à partir d'une source externe spécifiée.
- **Analyse de données :** Effectue des calculs statistiques pour obtenir des insights sur les données.
- **Agrégation de données :** Groupe les données par marque pour une meilleure compréhension des performances de vente.
- **Extensibilité :** Facilement adaptable pour inclure d'autres sources de données ou analyses.

## Prérequis

- Un cluster Kubernetes opérationnel.
- Helm installé et configuré pour gérer les déploiements dans Kubernetes.
- Accès à un dépôt Git contenant les définitions de DAG nécessaires.

## Installation

1. Clonez le dépôt du projet:
   ```sh
   git clone https://github.com/TkMa777/k8s-Airflow.git

## Appliquez la configuration Kubernetes pour ServiceAccount et RoleBinding:

`kubectl apply -f dashboard-adminuser.yaml`

`kubectl apply -f dashboard-clusterrole.yaml`

`kubectl apply -f dashboard-secret.yaml`

## Définissez les clés secrètes pour k8s dashboard:

`kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')`

## Helm pour installer ou mettre à niveau Airflow dans le cluster Kubernetes en utilisant le fichier values.yaml pour la configuration:

`helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f values.yaml`




