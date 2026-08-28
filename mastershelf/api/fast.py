from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import cv2
from pathlib import Path
from mastershelf.algo_filter.filtering import final_match, get_matching_recipes
from mastershelf.vision.detector import yolo_predict
from PIL import Image
import io
import json
import ast

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

@app.post("/ingredients")
async def ingredients(
    file: UploadFile = File(...),
    data: str = Form(
        ...
    ),  # Correspond à la clé du dictionnaire côté client
):

    # 1. Lire le contenu du fichier envoyé par le front
    """
    Renvoie les ingrédients trouvés dans l'image
    """
    contents = await file.read()

    # 2. Convertir en image PIL
    image = Image.open(io.BytesIO(contents))

    ing_list = yolo_predict(image)

    print(f"🔎 Recherche de la meilleure recette pour la liste d'ingrédients 🔎")

    try:
        # Si la chaîne contient le dictionnaire complet ('{"contraintes": ...}')
        parsed = ast.literal_eval(data)
        if isinstance(parsed, dict) and "contraintes" in parsed:
            contraintes_dict = json.loads(parsed["contraintes"])
        else:
            contraintes_dict = (
                json.loads(parsed) if isinstance(parsed, str) else parsed
            )
    except Exception:
        contraintes_dict = json.loads(data)

    pantry_items = contraintes_dict["pantry_items"]

    print("Dict final récuperé :", contraintes_dict)
    print("Pantry items :", pantry_items)

    results = get_matching_recipes(ing_list, pantry_items)

    print(f"💥 Meilleure recette trouvée ! 💥\n ➡️ Envoie de la réponse au Front")

    return  results

@app.get("/")
def root():
    return {"greeting": "Bienvenue sur notre super API de Master Shelf !"}
