from mastershelf.recipes.preprocessing import load_recipes
from mastershelf.algo_filter.filtering import *
from mastershelf.inventory.inventory import PHOTO_INV

result = get_matching_recipes(PHOTO_INV)
print("On affiche les résultats")
for i in result:
    print(i)
