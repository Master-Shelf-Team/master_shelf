import streamlit as st
from PIL import Image
import requests
import os
import random

# 1. Configuration de la page
st.set_page_config(
    page_title="Master Shelf",
    page_icon="🥗",
    layout="wide"
)

# 2. Styles CSS (Fond vert avec emojis d'aliments, cartes blanches et design)
st.markdown(
    """
    <style>
    /* Fond principal vert avec motif d'emojis d'aliments */
    .stApp {
        background-color: #2e7d32;
        background-image: radial-gradient(#388e3c 2px, transparent 2px);
        background-size: 30px 30px;
        color: #ffffff;
    }

    /* Motif personnalisé en arrière-plan */
    .stApp::before {
        content: "🍗 🥦 🍎 🥑 🧀 🥕 🍇 🥩 🍕 🍌 🍗 🥦 🍎 🥑 🧀 🥕 🍇 🥩";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 1;
        font-size: 2.5rem;
        word-spacing: 30px;
        line-height: 80px;
        pointer-events: none;
        z-index: 0;
    }

    /* En-tête */
    .header-container {
        text-align: center;
        padding: 1rem 0 2rem 0;
    }

    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
    }

    .slogan {
        font-size: 1.3rem;
        color: #e8f5e9;
        font-style: italic;
        margin-top: 5px;
    }

    /* Cartes blanches pour le contenu */
    div[data-testid="stBlock"] {
        background-color: rgba(255, 255, 255, 0.96);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Textes à l'intérieur des cartes */
    div[data-testid="stBlock"] h1,
    div[data-testid="stBlock"] h2,
    div[data-testid="stBlock"] h3,
    div[data-testid="stBlock"] label,
    div[data-testid="stBlock"] p,
    div[data-testid="stBlock"] span {
        color: #1b5e20 !important;
    }

    /* Bouton d'envoi API */
    div.stButton > button {
        background-color: #1b5e20 !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        width: 100% !important;
        padding: 15px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
    }

    div.stButton > button:hover {
        background-color: #2e7d32 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. En-tête : Titre + Slogan
st.markdown(
    """
    <div class="header-container">
        <h1 class="main-title">🥗 Master Shelf</h1>
        <p class="slogan">« Toutes nos recettes dans ton frigo »</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 4. Organisation en 2 colonnes du haut
col_gauche, col_milieu = st.columns(2, gap="large")

# --- COLONNE 1 : TON FRIGO ---
with col_gauche:
    st.header("🧊 Ton frigo")
    st.write("Importe la photo de ton frigo :")

    uploaded_file = st.file_uploader(
        "Sélectionne une image",
        type=["jpg", "jpeg", "png"],
        key="frigo_uploader"
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Photo chargée", use_container_width=True)

# --- COLONNE 2 : TES PRÉFÉRENCES ---
with col_milieu:
    st.header("❤️ Tes préférences")

    # Temps disponible
    st.subheader("Le temps que tu as :")
    temps_options = ["15 minutes", "30 minutes", "60 minutes", "Autres"]
    temps_choisi = st.select_slider(
        "Temps disponible",
        options=temps_options,
        value="30 minutes",
        label_visibility="collapsed",
        key="temps_slider"
    )

    # Type de repas
    st.subheader("Quel repas ?")
    repas_choisi = st.selectbox(
        "Repas",
        ["Petit-déjeuner", "Déjeuner", "Dîner", "Goûter", "Encas"],
        key="repas_select"
    )

    # Régime alimentaire (Sélection multiple)
    st.subheader("Ton régime alimentaire")
    regimes_choisis = st.multiselect(
        "Régimes",
        ["Végétarien", "Pauvre en gras", "Diabétique", "Kasher", "Halal", "Sans gluten", "Végétalien"],
        key="regime_select"
    )

    # Origine / Voyage
    st.subheader("Tu voyages où ?")
    voyage_choisi = st.selectbox(
        "Voyage",
        ["Italie", "Japon", "Chine", "France", "Mexique", "Inde", "Autre"],
        key="voyage_select"
    )

    # Occasion
    st.subheader("Quelle occasion ?")
    occasion_choisie = st.selectbox(
        "Occasion",
        ["Aucune", "Noël", "Halloween", "Pique-nique", "Anniversaire", "Soirée entre amis"],
        key="occasion_select"
    )

# --- BOUTON D'ENVOI API (Sous les deux colonnes) ---
st.write("")
btn_envoyer = st.button("🚀 Obtenir ma recette", key="btn_api")

# Variable d'état pour conserver la recette retournée
if "recette_resultat" not in st.session_state:
    st.session_state.recette_resultat = None

if btn_envoyer:
    if uploaded_file is None:
        st.warning("⚠️ Merci d'importer d'abord une photo de ton frigo !")
    else:
        with st.spinner("Analyse de l'image et génération de la recette par l'API..."):
            try:
                # Préparation du fichier et des paramètres à envoyer à ton API
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {
                    "temps": temps_choisi,
                    "repas": repas_choisi,
                    "regimes": ",".join(regimes_choisis),
                    "voyage": voyage_choisi,
                    "occasion": occasion_choisie
                }
                SERVICE_URL = os.environ.get("SERVICE_URL")
                # REMPLACE L'URL CI-DESSOUS PAR L'URL DE TON API
                print(SERVICE_URL)
                response = requests.post(f"{SERVICE_URL}/ingredients", files=files, data=data)
                response_json = response.json()
                # response_json = {
                # "steps": [
                # "Chop onions and garlic.",
                # "Saute onions and garlic in olive oil until browned .",
                # "Mix everything together in a deep nonstick pot.",
                # "Bring to boil ( use no more than medium heat) stirring often.",
                # "Turn down low and simmer at least 30 minutes -- stirring often -- you can simmer prepared, cooked, meatballs in the sauce too.-- it is easy to make your own meatballs. The sauce with thicken up as you cook and the alcohol will cook off.",
                # "Serve over your favorite pasta."
                # ]
                # }

                # Simulation de la réponse API (à remplacer par le vrai appel)

                st.session_state.recette_resultat = response_json
                st.success("Recette générée avec succès !")

            except Exception as e:
                st.error(f"Erreur lors de la connexion à l'API : {e}")

# --- COLONNE 3 : LA MEILLEURE RECETTE (En bas) ---
st.write("")
col_recette = st.container()

with col_recette:
    st.header("🏆 La meilleure recette")

    if st.session_state.recette_resultat:
        recette = st.session_state.recette_resultat
        length = len(recette)

        number = random.randint(0, length)

        st.markdown(f"## 👨‍🍳 Recette : {recette[number]['name']}")

        st.markdown("### 👨‍🍳 Ingrédients :")
        liste = ""
        for i, ing in enumerate(recette[number]["ingredients"]):
            liste = liste + "- " + str(ing).capitalize() + "\n"
        print(liste)

        st.markdown(f"{liste}")

        st.markdown("### 👨‍🍳 Étapes :")
        for idx, etape in enumerate(recette[number]["steps"], 1):
            st.write(f"{idx}. {etape}")
        st.write(f"{recette}")
    else:
        st.info("Importe une photo, sélectionne tes préférences et clique sur **'Obtenir ma recette'** pour voir la meilleure recette s'afficher ici !")
