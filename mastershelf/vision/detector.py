import os
import mlflow
from ultralytics import YOLO
from pathlib import Path

def yolo_predict(image):
    username = Path.home().name

    print("⏳ Chargement du model Yolo ⏳")
    model = YOLO(f"/models/best.pt")
    print("✅ Model Yolo chargé ! ✅")

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
