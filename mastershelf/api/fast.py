from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/ingredients > à corriger quand on sera rendu là
@app.get("/ingredients")
def ingredients(
        image: object
    ):      # 1
    """
    Renvoie les ingrédients trouvés dans l'image
    """

    return  {
                "ingredients_list":
                {
                    "ing1": "Ingrédient 1",
                    "ing2": "Ingrédient 2"
                }
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
