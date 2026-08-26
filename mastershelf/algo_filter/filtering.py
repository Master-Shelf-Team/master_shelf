from mastershelf.recipes.preprocessing import *
from mastershelf.inventory.inventory import *
import mastershelf.api.fast
import re

def final_match():
    data = load_recipes()
    user_inventory = get_user_inv()
    photo_ingredient = get_photo_inv()
    available_names = list(set(set(user_inventory.keys()) | set(photo_ingredient["ingredients_list"])))
    top_recipes = data.copy()
    top_recipes["coverage"] = top_recipes["ingredients"].apply(lambda x: recipe_coverage(x, available_names))
    top_recipes["n_ingredients"] = top_recipes["ingredients"].apply(len)

    possible_recipes = (
        top_recipes[top_recipes["coverage"] == 1.0]
        .sort_values(
            by=["coverage", "n_ingredients"],
            ascending=[False, False]
        )
    )

    possible_recipes[["name","steps","coverage", "n_ingredients"]].head(10)
    return possible_recipes.iloc[3].steps


def get_photo_inv():
    path1 = IMAGE_PATH_1
    path2 = IMAGE_PATH_2
    response = None
    try:
        response = set(mastershelf.api.fast.app.ingredients(path2))
        return response
    except:
        return PHOTO_INV

def get_user_inv():
    inventory = None
    # streamlit case à cocher
    if inventory:
        return inventory
    return  USER_INV

def recipe_coverage(recipe_ingredients, user_ingredients):
    if len(recipe_ingredients) == 0:
        return 0

    matches = 0

    for recipe_ing in recipe_ingredients:
        found = any(
            ingredient_match(user_ing, recipe_ing)
            for user_ing in user_ingredients
        )

        if found:
            matches += 1

    return matches / len(recipe_ingredients)

def ingredient_match(user_ing, recipe_ing):
    user_ing = user_ing.lower().strip()
    recipe_ing = recipe_ing.lower().strip()

    return (
        re.search(rf"\b{re.escape(user_ing)}\b", recipe_ing)
        is not None
    )
