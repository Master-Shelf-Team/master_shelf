from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import cv2
from pathlib import Path
from mastershelf.algo_filter.filtering import final_match
from mastershelf.vision.detector import yolo_predict

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

# http://127.0.0.1:8000/ingredients POST avec TON JPEG > à corriger quand on sera rendu là
@app.post("/ingredients")
def ingredients(
        image: str
    ):      # 1
    """
    Renvoie les ingrédients trouvés dans l'image
    """
    ing_list = yolo_predict(image)

    print(f"🔎 Recherche de la meilleure recette pour la liste d'ingrédients 🔎")

    results = final_match(ing_list)

    print(f"💥 Meilleure recette trouvée ! 💥\n ➡️ Envoie de la réponse au Front")

    return  {
                "steps": results
            }

# http://127.0.0.1:8000/recipe?ingredients=tomato+onion+cheese > à corriger quand on sera rendu là
@app.get("/recipe")
def recipe(
        ingredients: object
    ):      # 1
    """
    Renvoie les étapes de la première recette associée aux ingrédients
    """

    return  {
                "recipe":
                {
                    "step1": "Etape 1",
                    "step2": "Etape 2"
                }
            }


@app.get("/")
def root():
    return {"greeting": "Bienvenue sur notre super API de Master Shelf !"}
