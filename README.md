# Master Shelf

Projet de groupe LeWagon pour fin de formation.
Ce projet à pour but d'appliquer nos connaissances , d'apprendre et de mieux comprendre les concepts de Data Science.

## Project overview

L'idée du projet:
- Ne pas savoir quoi cuisiner avec nos ingrédients
- Transformer une photo et une liste d'ingrédients en recettes recommandés
- L'utilisateur envoie seulement une photo et ajoute des ingrédients secondaires à la main , choisis ses préférences.
- L'application renvoie des recettes pour que l'utilisateur n'ait pas besoin de faire les courses pour se faire à manger

## Workflow

- Photo
- Détection ingrédients
- Inventaire
- Préférences
- Filtrage Strict par Query
- Recommandations via un Neareast Neighbors
- Affichage en front

## Features

- Détection d'ingrédients depuis une image
- Gestion d'un inventaire
- Filtrage strict par ingrédients
- Recommandation de recettes via les préférences utilisateur
- Recommandation via un "historique" si pas de préférences utilisateur choisi
- Classement par similarité

## Architecture

- Frontend : Streamlit
- API : FastAPI
- Base de données : BigQuery
- Computer Vision : Yolo
- Recommendation system : Nearest Neighbors

## Dataset

[Food.com Recipes with Ingredients and Tags](https://www.kaggle.com/datasets/realalexanderwei/food-com-recipes-with-ingredients-and-tags/data)

Retravaillé et clean selon nos besoin en amont
