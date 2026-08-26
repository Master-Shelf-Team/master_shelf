from mastershelf.recipes.preprocessing import load_recipes

data = load_recipes()

print(data.head())
print(data.shape)
