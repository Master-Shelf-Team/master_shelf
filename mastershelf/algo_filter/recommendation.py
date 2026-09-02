from sklearn.preprocessing import MultiLabelBinarizer
from numpy import hstack
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import ParameterGrid


def predict_closer(user , df_clean):
    #On créé les mlb pour chaque colonnes à encoder (permettra de faire des 'groupes de colonnes avec le même poids, tout en choisissant les poids')
    mlb_dish = MultiLabelBinarizer()
    mlb_diet = MultiLabelBinarizer()
    mlb_meal = MultiLabelBinarizer()
    mlb_occasion = MultiLabelBinarizer()
    mlb_origin = MultiLabelBinarizer()
    mlb_time_to_make = MultiLabelBinarizer()

    print("1")
    param_grid = {'dish':[3], 'diet':[5], 'meal':[1], 'occasion':[1],
              'origin':[1], 'time_to_make':[3]}

    grid = list(ParameterGrid(param_grid))


    # On applique les mlb aux colonnes
    X_dish = mlb_dish.fit_transform(df_clean['type_dish'])
    X_diet = mlb_diet.fit_transform(df_clean['type_diet'])
    X_meal = mlb_meal.fit_transform(df_clean['type_meal'])
    X_occasion = mlb_occasion.fit_transform(df_clean['type_occasion'])
    X_origin = mlb_origin.fit_transform(df_clean['type_origin'])
    X_time_to_make = mlb_time_to_make.fit_transform(df_clean['time_to_make'])

    print("2")
    # history = get_history()

    # if user["dish"] == "" and user["origin"] == "" and user["time_max"] == "0" and user["diet"] == "" and user["meal"] == "" and user["occasion"] == "":
    #     print("if")
    #     X_test_dish = mlb_dish.transform([[max(set(history["dish"]), key=history["dish"].count)]])
    #     X_test_diet = mlb_diet.transform([[max(set(history["diet"]), key=history["diet"].count)]])
    #     X_test_meal = mlb_meal.transform([[max(set(history["meal"]), key=history["meal"].count)]])
    #     X_test_occasion = mlb_occasion.transform([[max(set(history["occasion"]), key=history["occasion"].count)]])
    #     X_test_origin = mlb_origin.transform([[max(set(history["origin"]), key=history["origin"].count)]])
    #     X_test_time_to_make = mlb_time_to_make.transform([[max(set(history["time_max"]), key=history["time_max"].count)]])
    # else:
    print("else")
    X_test_dish = mlb_dish.transform([list(user["dish"])])
    X_test_diet = mlb_diet.transform([list(user['diet'])])
    X_test_meal = mlb_meal.transform([list(user["meal"])])
    X_test_occasion = mlb_occasion.transform([list(user['occasion'])])
    X_test_origin = mlb_origin.transform([list(user['origin'])])
    X_test_time_to_make = mlb_time_to_make.transform([user['time_max']])

    print("3")
    result = []
    for param in grid:
        X = hstack([X_dish * param['dish'],X_diet * param['diet'],X_meal*param['meal'],
                X_occasion * param['occasion'],X_origin * param['origin'],
                X_time_to_make * param['time_to_make']])


        X_test = hstack([X_test_dish * param['dish'], X_test_diet * param['diet'],X_test_meal*param['meal'],
                        X_test_occasion * param['occasion'],X_test_origin * param['origin'],
                        X_test_time_to_make * param['time_to_make']])

        model = NearestNeighbors(
            n_neighbors=5,
            metric="cosine")

        model.fit(X)
        distances, indices = model.kneighbors(X_test)
        result.append({
        **param,
        "score": distances,
        "recipe_index": indices
    })

    print("4")
    response = []
    for i in list(result[0]["recipe_index"][0]):
        dict = {}
        dict["name"] = str(df_clean.iloc[i]["name"])
        dict["ingredients_raw"] = list(df_clean.iloc[i]["ingredients_raw"])
        dict["steps"] = list(df_clean.iloc[i]["steps"])
        dict["servings"] = int(df_clean.iloc[i]["servings"])
        dict["persons"] = int(df_clean.iloc[i]["persons"])
        dict["portion_size"] = df_clean.iloc[i]["portion_size"]
        dict["ingredients_clean"] = list(df_clean.iloc[i]["ingredients_clean"])
        dict["type_dish"] = list(df_clean.iloc[i]["type_dish"])
        dict["type_diet"] = list(df_clean.iloc[i]["type_diet"])
        dict["type_meal"] = list(df_clean.iloc[i]["type_meal"])
        dict["type_occasion"] = list(df_clean.iloc[i]["type_occasion"])
        dict["type_origin"] = list(df_clean.iloc[i]["type_origin"])
        dict["time_to_make"] = df_clean.iloc[i]["time_to_make"]
        response.append(dict)

    print("5")
    return response


def get_history():
    history = {'time_max': ['15',"30", "15", "15"],
    'occasion': ['summer', "spring", "brunch", "spring"],
    'dish': ["vegetables","pasta" , "vegetables" , "vegetables"],
    'meal': ['main-dish', 'main-dish', 'main-dish', 'main-dish', 'dessert'],
    'diet': ['gluten-free', 'dietary', 'dietary', 'dietary' , 'dietary', 'gluten-free'],
    'origin': ['american', "european", "european", "european" , "american"]}
    return history
