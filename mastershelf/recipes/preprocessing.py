import os
import pandas as pd
import ast
from mastershelf.recipes.params import *
import re
import spacy
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle


def load_recipes():
    """
    On charge le dataset clean si il existe , sinon on clean le dataset de base
    """

    file_path = RAW_DATA_PATH / "recipes_clean.csv"
    if os.path.exists(file_path):
        print("The file exists. Loading ...")
        df_recipes_clean = pd.read_csv(file_path)
        print("recipes loaded")
        df_recipes_clean = transform_str_to_list_clean(df_recipes_clean)
        print("preprocess done")
    else:
        print("The file does not exist. Let's create it ...")
        df_recipes = pd.read_csv(RAW_DATA_PATH / "recipes_ingredients.csv")
        df_recipes_clean = clean_recipes(df_recipes)
        df_recipes_clean = df_recipes_clean.sample(100000)
        df_recipes_clean["ingredients"] = df_recipes_clean["ingredients"].apply(
    lambda x: [str(i).strip() for i in x]
)
        df_recipes_clean.to_csv(file_path, index=False)
    return df_recipes_clean


def clean_recipes(data):
    """
    Cleaning et preprocessing du dataset de base
    """
    data = data.copy()
    data = data.drop(columns=["description","id"])
    data = data.dropna(
    subset=[
        "ingredients",
        "ingredients_raw",
        "steps",
        "tags"
    ]
)
    #Change les strings en listes
    data = transform_str_to_list(data)
    #Divise la colonne serving size en 2 colonnes distinctes
    print("deleting useless colomns, and spliting")
    data[["persons", "portion_size"]] = data["serving_size"].str.extract(r"(\d+)\s*\(([^)]+)\)")
    data = data.drop(columns="serving_size", axis=1)
    data["persons"] = pd.to_numeric(data["persons"],errors="coerce")
    #Retire les trop grosses valeur
    print("deleting useless recipes")
    data = data[data["servings"] <= 50]
    print("Creating new columns...")
    data = data[data["tags"].apply(lambda tags: any(tag in tags for tag in TIME_TO_MAKE))]
    data['type_dish'] = data['tags'].apply(lambda x: type_column(x, TYPE_DISH))
    data['type_diet'] = data['tags'].apply(lambda x: type_column(x, TYPE_DIET))
    data['type_meal'] = data['tags'].apply(lambda x: type_column(x, TYPE_MEAL))
    data['type_occasion'] = data['tags'].apply(lambda x: type_column(x, TYPE_OCCASION))
    data['type_origin'] = data['tags'].apply(lambda x: type_column(x, TYPE_ORIGIN))
    data = data[data["tags"].apply(len) > 0]
    print("cleaning ingredients...")
    data["ingredients_clean"] = data["ingredients"].apply(lambda ingredients: [clean_ingredient(x) for x in ingredients])
    unique_clean = (data["ingredients_clean"].explode().dropna().unique())
    #lemmatization des ingredients
    print("lemmatization ...")
    nlp = spacy.load("en_core_web_sm")

    lemmatized = []

    for doc in nlp.pipe(unique_clean, batch_size=1000):
        lemma = " ".join(token.lemma_ for token in doc)
        lemmatized.append(lemma)
    lemma_mapping = dict(zip(unique_clean, lemmatized))
    data["ingredients_lemmatized"] = data["ingredients_clean"].apply(lambda ingredients: [lemma_mapping[ingredient]for ingredient in ingredients])
    ingredient_counts = (data["ingredients_lemmatized"].explode().value_counts())

    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    most_common = ingredient_counts.head(4800).index.tolist()

    most_common_embeddings = embedder.encode(
        most_common,
        batch_size=256,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    print("normalization ...")
    normalization_mapping = build_normalization_mapping(
        ingredient_counts=ingredient_counts,
        embedder=embedder,
        most_common=most_common,
        most_common_embeddings=most_common_embeddings,
        threshold=0.93)

    data["ingredients_normalized"] = (data["ingredients_lemmatized"].apply(lambda ingredients: [normalization_mapping[ingredient]for ingredient in ingredients]))
    with open(MODEL_PATH / "ingredient_mapping.pkl", "wb") as f:
        pickle.dump(normalization_mapping, f)
    print("deleting extra columns")
    data = data.drop(columns= ["ingredients_lemmatized","tags","ingredients_clean","ingredients"], axis=1)
    data["ingredients"] = data["ingredients_normalized"]
    data = data.drop("ingredients_normalized", axis=1)

    return data



def safe_literal_eval(value):
    """
    Transforme les strings en liste de string
    """

    try:
        result = ast.literal_eval(value)

        if isinstance(result, list):
            return result

        return []

    except (ValueError, SyntaxError, TypeError):
        return []


def clean_ingredient(text):
    """
    Removing words from ingredients
    """

    text = text.lower().strip()


    text = re.sub(r"\b\d+([./]\d+)?\b", " ", text)

    for word in WORDS_TO_REMOVE:
        text = re.sub(rf"\b{re.escape(word)}\b", " ", text)


    text = re.sub(r"[,()]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def build_normalization_mapping(
    ingredient_counts,
    embedder,
    most_common,
    most_common_embeddings,
    threshold=0.93,
    encode_batch_size=128,
    similarity_batch_size=2000
):
    most_common_set = set(most_common)

    normalization_mapping = {
        ingredient: ingredient
        for ingredient in most_common
    }

    rare_ingredients = [
        ingredient
        for ingredient in ingredient_counts.index
        if ingredient not in most_common_set
    ]

    rare_embeddings = embedder.encode(
        rare_ingredients,
        batch_size=encode_batch_size,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    for start in range(0, len(rare_ingredients), similarity_batch_size):

        end = start + similarity_batch_size

        batch_ingredients = rare_ingredients[start:end]
        batch_embeddings = rare_embeddings[start:end]

        scores = batch_embeddings @ most_common_embeddings.T

        best_indices = np.argmax(scores, axis=1)
        best_scores = np.max(scores, axis=1)

        for ingredient, idx, score in zip(
            batch_ingredients,
            best_indices,
            best_scores
        ):
            if score >= threshold:
                normalization_mapping[ingredient] = most_common[idx]
            else:
                normalization_mapping[ingredient] = ingredient

    return normalization_mapping


def transform_str_to_list(data):
    """
    transforme le contenu des colonnes en liste pour le data_clean
    """

    data["ingredients"] = data["ingredients"].apply(safe_literal_eval)
    data["ingredients_raw"] = data["ingredients_raw"].apply(safe_literal_eval)
    data["steps"] = data["steps"].apply(safe_literal_eval)
    data["tags"] = data["tags"].apply(safe_literal_eval)
    #Vire les listes vides
    data = data[data["ingredients"].apply(len) > 0]
    data = data[data["ingredients_raw"].apply(len) > 0]
    data = data[data["steps"].apply(len) > 0]
    data = data[data["tags"].apply(len) > 0]
    return data


def transform_str_to_list_clean(data):
    """
    transforme le contenu des colonnes en liste pour le data de base
    """

    data["ingredients"] = data["ingredients"].apply(safe_literal_eval)
    data["ingredients_raw"] = data["ingredients_raw"].apply(safe_literal_eval)
    data["steps"] = data["steps"].apply(safe_literal_eval)
    data["type_dish"] = data["type_dish"].apply(safe_literal_eval)
    data["type_diet"] = data["type_diet"].apply(safe_literal_eval)
    data["type_origin"] = data["type_origin"].apply(safe_literal_eval)
    data["type_occasion"] = data["type_occasion"].apply(safe_literal_eval)
    data["type_meal"] = data["type_meal"].apply(safe_literal_eval)
    #Vire les listes vides
    data = data[data["ingredients"].apply(len) > 0]
    data = data[data["ingredients_raw"].apply(len) > 0]
    data = data[data["steps"].apply(len) > 0]
    return data


def type_column(liste, type_liste):
    matched_elements = []
    for element in type_liste:
        if element in liste:
            matched_elements.append(element)
    return matched_elements
