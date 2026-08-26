from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import cv2
from pathlib import Path

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

# http://127.0.0.1:8000/ingredients > à corriger quand on sera rendu là
@app.get("/ingredients")
def ingredients(
        image: str
    ):      # 1
    """
    Renvoie les ingrédients trouvés dans l'image
    """
    username = Path.home().name

    print("Chargement du model Yolo")
    model = YOLO(f"/home/{username}/code/MitriBarbot/master_shelf/models/last.pt")
    print("Model Yolo chargé !")


    if image == None:
        image = f"/home/{username}/code/MitriBarbot/master_shelf/raw_data/sam-test.jpg"

    print(f"Détection d'ingrédient pour l'image :\n{image}")
    # Baisser la confiance (conf) et augmenter le seuil d'intersection (iou)
    results = model.predict(
        source=image,
        conf=0.15,   # Affiche même les détections incertaines
        iou=0.45,    # Évite les boîtes qui se chevauchent trop
        save=True
    )

    ings = []

    class_names = model.names
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Récupérer l'ID de la classe (format float/tensor, converti en int)
            class_id = int(box.cls[0].item())

            # Obtenir le nom de la catégorie correspondante
            category_name = class_names[class_id]

            # Récupérer le score de confiance (optionnel)
            confidence = box.conf[0].item()

            print(f"Objet détecté : {category_name} (Confiance : {confidence:.2f})")

            ings.append(category_name)

    print(ings)

    return  {
                "ingredients_list": ings
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
