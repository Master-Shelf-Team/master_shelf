from __future__ import annotations

import html
import json
from pathlib import Path
import requests
import streamlit as st
from PIL import Image
import os
import numpy as np
import ast

st.set_page_config(
    page_title="Master Shelf",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SERVICE_URL = os.environ.get("SERVICE_URL")

DIETS = [
    "", "dietary", "low-carb", "low-sodium", "low-cholesterol", "healthy",
    "vegetarian", "low-calorie", "low-protein", "healthy-2", "inexpensive",
    "low-saturated-fat", "kid-friendly", "low-fat", "pasta-rice-and-grains",
    "comfort-food", "spicy", "kosher", "very-low-carbs", "diabetic",
    "toddler-friendly", "high-protein", "gluten-free", "egg-free",
    "high-calcium", "heirloom-historical", "dairy-free", "infant-baby-friendly"
]

ORIGINS = [
    "", "north-american", "american", "european", "asian", "mexican",
    "australian", "canadian", "southwestern-united-states", "midwestern",
    "south-west-pacific", "thai", "chinese", "southern-united-states",
    "african", "jewish-ashkenazi", "italian", "indian", "tex-mex",
    "central-american", "japanese", "northeastern-united-states", "irish",
    "russian", "caribbean", "californian", "german", "middle-eastern",
    "spanish", "greek", "cuban", "indonesian", "guatemalan",
    "danish", "vietnamese", "british-columbian", "scandinavian", "argentine",
    "south-american", "english", "south-african", "nigerian", "cajun",
    "pacific-northwest", "pakistani"
]

DISHES = [
    "", "vegetables", "salads", "cookies-and-brownies", "beverages", "sandwiches",
    "breads", "pasta", "sweet", "sauces", "quick-breads",
    "salad-dressings", "cocktails", "bisques-cream-soups", "cakes", "bar-cookies",
    "candy", "spaghetti", "savory-sauces", "puddings-and-mousses", "cobblers-and-crisps",
    "clear-soups", "sweet-sauces", "pies-and-tarts", "brownies", "coffee-cakes",
    "pork-loins", "pork-chops", "roast-beef", "barbecue", "ravioli-tortellini",
    "jams-and-preserves", "scones", "savory-pies", "omelets-and-frittatas", "cheesecake",
    "roast", "chili", "granola-and-porridge", "pies", "chowders",
    "pancakes-and-waffles", "shakes", "stews", "cupcakes", "garnishes",
    "rolled-cookies"
]

OCCASIONS = [
    "", "dinner-party", "brunch", "to-go", "potluck", "summer",
    "christmas", "fall", "spring", "winter", "romantic",
    "picnic", "independence-day", "new-years", "thanksgiving", "st-patricks-day",
    "valentines-day", "camping", "barbecue", "wedding", "mardi-gras-carnival",
    "hanukkah", "easter", "super-bowl"
]

MEALS = [
    "", "main-dish", "appetizers", "dinner-party", "desserts", "lunch",
    "brunch", "side-dishes", "one-dish-meal", "beverages", "breakfast",
    "potluck", "snacks", "picnic", "cocktails", "finger-food",
    "frozen-desserts", "barbecue"
]

BASE_DIR = Path(__file__).resolve().parent
ingredients_path = BASE_DIR / "ingredients.txt"

with open(ingredients_path, "r", encoding="utf-8") as f:
    PANTRY_ITEMS = [line.strip() for line in f if line.strip()]

SAMPLE_RECIPES = [
    {
        "title": "Pasta primavera du frigo",
        "time": 25,
        "diet": "Végétarien",
        "origin": "Italienne",
        "match": 94,
        "blurb": "Légumes croquants, un filet d’huile d’olive, et tout ce qui restait au fond du bac.",
        "emoji": "🍝",
    },
    {
        "title": "Bowl miso & légumes rôtis",
        "time": 35,
        "diet": "Vegan",
        "origin": "Japonaise",
        "match": 88,
        "blurb": "Un bouillon umami, des restes de légumes, du riz s’il y en a — sinon des nouilles.",
        "emoji": "🍜",
    },
    {
        "title": "Tacos express aux restes",
        "time": 20,
        "diet": "Omnivore",
        "origin": "Mexicaine",
        "match": 86,
        "blurb": "Tout ce qui est encore beau dans le frigo, une poêle chaude, des tortillas.",
        "emoji": "🌮",
    },
    {
        "title": "Tajine minute aux légumes",
        "time": 45,
        "diet": "Végétarien",
        "origin": "Maghrébine",
        "match": 81,
        "blurb": "Épices douces, pois chiches si tu en as, et un peu de miel ou de citron.",
        "emoji": "🍲",
    },
    {
        "title": "Omelette paysanne",
        "time": 15,
        "diet": "Sans lactose",
        "origin": "Française",
        "match": 79,
        "blurb": "Œufs, herbes, fromage ou pas, et les légumes du bac à verdure.",
        "emoji": "🍳",
    },
    {
        "title": "Curry coco express",
        "time": 30,
        "diet": "Vegan",
        "origin": "Thaïlandaise",
        "match": 77,
        "blurb": "Lait de coco, pâte de curry, et tout le rayon légumes qui demandait à être cuisiné.",
        "emoji": "🍛",
    },
]


def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Outfit:wght@300;400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: "Outfit", sans-serif;
            background-color: C7B383;
        }

        label {
            color: #3d2a1f !important;
        }

        button > div > span > div > p {
                    color: #ffffff;
                }

        .stApp {
            background:
                radial-gradient(1200px 500px at 10% -10%, #f3d7b5 0%, transparent 55%),
                radial-gradient(900px 420px at 100% 0%, #d9e4c8 0%, transparent 50%),
                #F6F0E6;
        }

        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 4rem;
            max-width: 1180px;
        }

        .hero {
            background: linear-gradient(135deg, #3d2a1f 0%, #6b3e2a 55%, #c45c26 140%);
            color: #F6F0E6;
            border-radius: 28px;
            padding: 2.1rem 2.2rem 1.9rem;
            margin-bottom: 1.4rem;
            box-shadow: 0 18px 40px rgba(61, 42, 31, 0.22);
            position: relative;
            overflow: hidden;
        }
        .hero:after {
            content: "🪵";
            position: absolute;
            right: 1.4rem;
            bottom: -0.4rem;
            font-size: 6.5rem;
            opacity: 0.14;
            transform: rotate(-12deg);
        }
        .eyebrow {
            letter-spacing: 0.22em;
            text-transform: uppercase;
            font-size: 0.72rem;
            opacity: 0.78;
            margin-bottom: 0.35rem;
        }
        .hero h1 {
            font-family: "Fraunces", serif;
            font-size: 2.55rem;
            margin: 0 0 0.4rem 0;
            line-height: 1.05;
        }
        .hero p {
            margin: 0;
            max-width: 42rem;
            font-size: 1.05rem;
            opacity: 0.92;
            color: rgba(255, 252, 246, 0.86);
        }

        .panel {
            background: rgba(255, 252, 246, 0.86);
            border: 1px solid rgba(61, 42, 31, 0.08);
            border-radius: 22px;
            padding: 1.15rem 1.2rem 1.05rem;
            box-shadow: 0 10px 28px rgba(44, 36, 22, 0.06);
            height: 100%;
        }
        .panel h3 {
            font-family: "Fraunces", serif;
            margin: 0 0 0.25rem 0;
            color: #3d2a1f;
        }
        .hint {
            color: #6d6254;
            font-size: 0.92rem;
            margin-bottom: 0.85rem;
        }

        .chip-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.6rem; }
        .chip {
            background: #efe3d0;
            color: #3d2a1f;
            border-radius: 999px;
            padding: 0.22rem 0.7rem;
            font-size: 0.8rem;
        }

        .recipe-card {
            background: #fffaf2;
            border: 1px solid rgba(61, 42, 31, 0.08);
            border-radius: 20px;
            padding: 1.05rem 1.1rem;
            height: 100%;
            box-shadow: 0 8px 22px rgba(44, 36, 22, 0.05);
        }
        .recipe-card h4 {
            font-family: "Fraunces", serif;
            margin: 0.15rem 0 0.35rem 0;
            font-size: 1.18rem;
            color: #2C2416;
        }
        .recipe-card h5 {
                    font-family: "Fraunces", serif;
                    margin: 0.15rem 0 0.35rem 0;
                    font-size: 1.18rem;
                    color: #2C2416;
                }
        .meta { color: #6d6254; font-size: 0.86rem; margin-bottom: 0.45rem; }
        .match {
            display: inline-block;
            background: #3d2a1f;
            color: #F6F0E6;
            border-radius: 999px;
            padding: 0.12rem 0.55rem;
            font-size: 0.75rem;
            letter-spacing: 0.04em;
        }
        .recipe-detail { margin-top: 0.6rem; }
        .step-list { list-style: none; padding: 0; margin: 0.7rem 0 0 0; }
        .step-list li {
            display: flex;
            gap: 0.75rem;
            align-items: flex-start;
            padding: 0.7rem 0;
            border-top: 1px solid rgba(61, 42, 31, 0.08);
            color: #2C2416;
            line-height: 1.45;
        }
        .step-num {
            flex: 0 0 1.7rem;
            height: 1.7rem;
            border-radius: 999px;
            background: #C45C26;
            color: #fffaf2;
            font-size: 0.8rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 0.1rem;
        }

        .stButton > button {
            background: #c45c26;
            color: white;
            border: 0;
            border-radius: 999px;
            padding: 0.65rem 1.3rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        .stButton > button:hover {
            background: #a84b1d;
            color: white;
        }

         {
            color: rgba(255, 252, 246, 0.86);
        }

        div[data-testid="stFileUploader"] section {
            background: #fffaf2;
            border-radius: 16px;
        }

        footer { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def filter_recipes(time_max: int, diet: str, origin: str) -> list[dict]:
    out = []
    for recipe in SAMPLE_RECIPES:
        if recipe["time"] > time_max:
            continue
        if diet != "Peu importe" and recipe["diet"] != diet:
            if not (diet == "Végétarien" and recipe["diet"] == "Vegan"):
                continue
        if origin != "Peu importe" and recipe["origin"] != origin:
            continue
        out.append(recipe)
    return out or [r for r in SAMPLE_RECIPES if r["time"] <= time_max][:3]


def recipes_from_api(payload: object) -> list[dict]:
    if isinstance(payload, dict) and isinstance(payload.get("steps"), list):
        return [payload]
    if isinstance(payload, dict):
        for key in ("recipes", "data", "result"):
            if key in payload:
                return recipes_from_api(payload[key])
        return []
    if isinstance(payload, list):
        found: list[dict] = []
        for item in payload:
            found.extend(recipes_from_api(item))
        return found
    return []


def render_recipe(recipe: dict, time_max: int, diet: str, origin: str) -> None:
    title = recipe.get("title") or recipe.get("name") or "Ta recette"
    steps = [str(step).strip() for step in recipe.get("steps") or [] if str(step).strip()]
    ingredients = [str(ingredient).strip() for ingredient in recipe.get("ingredients_raw") or [] if str(ingredient).strip()]
    if not steps:
        st.warning("L'API a répondu, mais sans étapes de recette.")
        return

    items = "".join(
        (
            "<li>"
            f'<span class="step-num">{index}</span>'
            f"<span>{html.escape(step).capitalize()}</span>"
            "</li>"
        )
        for index, step in enumerate(steps, start=1)
    )

    ings = "".join(
            (
                "<li>"
                f'<span class="step-num">&bull;</span>'
                f"<span>{html.escape(ingredient.capitalize())}</span>"
                "</li>"
            )
            for index, ingredient in enumerate(ingredients, start=1)
        )

    st.markdown(
        f"""
        <div class="recipe-card recipe-detail">
          <span class="match">{len(steps)} étapes</span>
          <h4>🍽️ {html.escape(str(title))}</h4>
          <div class="meta">{time_max} min max · {html.escape(diet)} · {html.escape(origin)}</div>
          <h5>🦐 Ingrédients</h5>
          <ul class="step-list">{ings}</ul>
          <h5>➡️ Etapes</h5>
          <ol class="step-list">{items}</ol>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Cuisine à partir du réel</div>
      <h1>Master Shelf</h1>
      <p>Photographie ton frigo. On te propose des recettes qui collent à ce que tu as vraiment,
      au temps que tu as, et à l’envie du moment.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns((1.15, 1), gap="large")

with left:
    st.markdown(
        """
        <div class="panel">
          <h3>Le frigo, en photos</h3>
          <div class="hint">Une photo ou plusieurs : étagères, tiroirs, condiments. Plus c’est lisible, mieux c’est.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    photos = st.file_uploader(
        "Ajouter des photos de frigo",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="fridge_photos",
    )

    if photos:
        st.caption(
            f"{len(photos)} photo{'s' if len(photos) > 1 else ''} "
            f"prête{'s' if len(photos) > 1 else ''} à être "
            f"lue{'s' if len(photos) > 1 else ''}."
        )
        thumbs = st.columns(min(4, len(photos)))
        for i, uploaded in enumerate(photos):
            with thumbs[i % len(thumbs)]:
                uploaded.seek(0)
                image = Image.open(uploaded)
                image.load()
                uploaded.seek(0)
                st.image(image, caption=uploaded.name, use_container_width=True)

with right:
    st.markdown(
        """
        <div class="panel">
          <h3>Tes envies</h3>
          <div class="hint">Ces choix affinent les suggestions. Tu pourras les changer à chaque recherche.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    time_max = st.slider(
        "Temps de recette (minutes)",
        min_value=0,
        max_value=60,
        value=15,
        step=15,
        help="On écarte les plats plus longs que ce plafond.",
    )
    occasion = st.selectbox("Type d'occasion", OCCASIONS, index=0)
    dish = st.selectbox("Type de préparation", DISHES, index=0)
    meal = st.selectbox("Repas de la journée", MEALS, index=0)
    diet = st.selectbox("Régime alimentaire", DIETS, index=0)
    origin = st.selectbox("Provenance du plat", ORIGINS, index=0)

    st.markdown(
        f"""
        <div class="chip-row">
          <span class="chip">⏱ ≤ {time_max} min</span>
          <span class="chip">{occasion}</span>
          <span class="chip">{dish}</span>
          <span class="chip">{meal}</span>
          <span class="chip">{diet}</span>
          <span class="chip">{origin}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
            """
            <div class="panel">
              <h3>Ton garde-manger</h3>
              <div class="hint">Qu'est ce qu'il y a de beau là dedans?</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    pantry_selected = st.multiselect(
    label="Ingrédients de base à disposition (hors frigo) :",
    options=PANTRY_ITEMS,
    default=["butter", "pepper", "vanilla", "bread", "pasta", "onion"],  # Pré-cochés par défaut si besoin
    help="Cherche et sélectionne les ingrédients de ton placard",
    )

st.write("")
go = st.button("Trouver des recettes", type="primary", use_container_width=True)

if go:
    if not photos:
        st.warning("Ajoute au moins une photo de frigo pour lancer la recommandation.")
    else:
        url = f"{SERVICE_URL}/ingredients"

        files = []
        for photo in photos:
            photo.seek(0)
            files.append(
                (
                    "file",
                    (
                        photo.name,
                        photo.getvalue(),
                        photo.type or "application/octet-stream",
                    ),
                )
            )
        payload = {
                        "time_max": str(time_max),
                        "occasion": [occasion],
                        "dish": [dish],
                        "meal": [meal],
                        "diet": [diet],
                        "origin": [origin],
                        "pantry_items": pantry_selected,
                    }
        print(payload)
        form_data = {"data": json.dumps(payload)}

        try:
            with st.spinner("Recherche de recette..."):
                response = requests.post(url, files=files, data=form_data)

            if response.status_code != 200:
                st.error(f"Erreur de l'API : {response.status_code}")
                st.write(response.text)
            else:
                try:
                    payload = response.json()
                except ValueError:
                    st.error("L'API n'a pas renvoyé de JSON.")
                    st.write(response.text)
                else:
                    recipes = recipes_from_api(payload["results"])
                    if not recipes:
                        st.warning("Aucune recette avec des étapes n'a été trouvée dans la réponse.")
                        st.json(payload["results"])
                    else:
                        imagebox = np.array(payload["imagebox"])
                        st.image(imagebox)
                        st.markdown("### Recette")
                        for recipe in recipes:
                            render_recipe(recipe, time_max, diet, origin)
        except requests.exceptions.ConnectionError:
            st.error(
                "Impossible de se connecter à l'API. Vérifiez qu'elle est bien "
                "démarrée."
            )
else:
    st.info("Charge tes photos, règle tes filtres, puis lance la recherche.")
