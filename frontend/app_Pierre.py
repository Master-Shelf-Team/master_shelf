from __future__ import annotations

import json

import requests
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Master Shelf",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DIETS = [
    "Peu importe",
    "Omnivore",
    "Végétarien",
    "Vegan",
    "Sans gluten",
    "Sans lactose",
    "Halal",
    "Pescétarien",
    "Keto",
]

ORIGINS = [
    "Peu importe",
    "Française",
    "Italienne",
    "Espagnole",
    "Maghrébine",
    "Libanaise",
    "Indienne",
    "Japonaise",
    "Chinoise",
    "Thaïlandaise",
    "Mexicaine",
    "Américaine",
]

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

        .stButton > button {
            background: #C45C26;
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
        min_value=10,
        max_value=120,
        value=40,
        step=5,
        help="On écarte les plats plus longs que ce plafond.",
    )
    diet = st.selectbox("Régime alimentaire", DIETS, index=0)
    origin = st.selectbox("Provenance du plat", ORIGINS, index=0)

    st.markdown(
        f"""
        <div class="chip-row">
          <span class="chip">⏱ ≤ {time_max} min</span>
          <span class="chip">{diet}</span>
          <span class="chip">{origin}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
go = st.button("Trouver des recettes", type="primary", use_container_width=True)

if go:
    if not photos:
        st.warning("Ajoute au moins une photo de frigo pour lancer la recommandation.")
    else:
        recipes = filter_recipes(time_max, diet, origin)
        url = "http://localhost:8000/votre-endpoint-api"

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
        data = {
            "contraintes": json.dumps(
                {
                    "time_max": time_max,
                    "diet": diet,
                    "origin": origin,
                }
            )
        }

        try:
            with st.spinner("Envoi en cours..."):
                response = requests.post(url, files=files, data=data)

            if response.status_code == 200:
                st.success("Photos envoyées avec succès.")
                try:
                    st.json(response.json())
                except ValueError:
                    st.write(response.text)
            else:
                st.error(f"Erreur de l'API : {response.status_code}")
                st.write(response.text)
        except requests.exceptions.ConnectionError:
            st.error(
                "Impossible de se connecter à l'API. Vérifiez qu'elle est bien "
                "démarrée."
            )

        st.markdown("### Suggestions")
        st.caption(
                "Aperçu d’interface : les cartes ci-dessous sont des exemples. "
                "Le modèle de recommandation viendra se brancher ici."
            )
            
        rows = [recipes[i : i + 3] for i in range(0, len(recipes), 3)]
        for row in rows:
            cols = st.columns(3, gap="medium")
            for col, recipe in zip(cols, row):
                with col:
                    st.markdown(
                        f"""
                        <div class="recipe-card">
                          <span class="match">{recipe["match"]}% match</span>
                          <h4>{recipe["emoji"]} {recipe["title"]}</h4>
                          <div class="meta">{recipe["time"]} min · {recipe["diet"]} · {recipe["origin"]}</div>
                          <p>{recipe["blurb"]}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
else:
    st.info("Charge tes photos, règle tes filtres, puis lance la recherche.")
