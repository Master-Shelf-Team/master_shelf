import os
import mlflow
from ultralytics import YOLO
from pathlib import Path

def yolo_predict(image):
    username = Path.home().name

    print("⏳ Chargement du model Yolo ⏳")
    model = YOLO(f"/home/{username}/code/MitriBarbot/master_shelf/models/best.pt")
    print("✅ Model Yolo chargé ! ✅")


    if image == None:
        image = f"/home/{username}/code/MitriBarbot/master_shelf/raw_data/sam-test.jpg"

    print(f"🔎 Détection d'ingrédient pour l'image :\n{image}")
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

            print(f"💥 Objet détecté : {category_name} (Confiance : {confidence:.2f})")

            ings.append(category_name)

    print(ings)
    return {
            "ingredients_list": ings
        }

# Inutilisable en l'état, code à retravailler
def save_model() -> None:
    """
    Persist trained YOLO model locally and on MLflow.
    """
    print("⏳ Enregistrement du model sur MLfLow...")

    # 1. Charger votre modèle avec ses meilleurs poids
    username = Path.home().name
    model = YOLO(f"/home/{username}/code/MitriBarbot/master_shelf/models/best.pt")

    # Récupération du nom du modèle depuis vos variables globales ou d'environnement
    mlflow_model_name = os.environ.get("MLFLOW_MODEL_NAME", "YOLO_Ingredients_Detector")

    # Enregistrement natif du modèle YOLO (Ultralytics) dans MLflow
    mlflow.ultralytics.log_model(
        model=model,
        artifact_path="model",
        registered_model_name=mlflow_model_name
    )

    print("✅ Model enregistré sur MLflow")
    return None
