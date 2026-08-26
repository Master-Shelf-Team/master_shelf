from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "raw_data"
MODEL_PATH = PROJECT_ROOT / "models"

PREP_WORDS = [
    "chopped", "diced", "minced", "sliced",
    "peeled", "crushed", "grated", "shredded",
    "melted", "softened", "divided",
    "finely", "roughly", "thinly",
    "drained", "rinsed", "cooked",
    "uncooked", "boiled", "roasted", "hard",
    "soft"
]

SIZE_WORDS = [
    "small", "medium", "large", "extra-large"
]

QUALITY_WORDS = [
    "fresh", "frozen", "organic",
    "ripe", "optional", "preferred",
    "approximately", "about"
]

UNIT_WORDS = [
    "g", "kg", "gram", "grams",
    "ml", "l", "liter", "liters",
    "cup", "cups",
    "tbsp", "tablespoon", "tablespoons",
    "tsp", "teaspoon", "teaspoons",
    "oz", "ounce", "ounces",
    "lb", "lbs", "pound", "pounds"
]

WORDS_TO_REMOVE = (
        PREP_WORDS
        + SIZE_WORDS
        + QUALITY_WORDS
        + UNIT_WORDS
    )

TIME_TO_MAKE = ['15-minutes-or-less', '30-minutes-or-less', '60-minutes-or-less']

TYPE_DISH = ['cobblers-and-crisps','cakes','cookies-and-brownies','pork-chops','pies-and-tarts','breads','rolls-biscuits','salads','pasta','vegetables','salad-dressings',
             'pancakes-and-waffles','candy','stews','barbecue','puddings-and-mousses','beverages','cocktails','clear-soups','sauces','roast','marinades-and-rubs',
             'bar-cookies','omelets-and-frittatas','savory-pies','quick-breads','sweet','bisques-cream-soups','cheesecake','brownies','sandwiches','pies','savory-sauces',
             'shakes','spaghetti','ravioli-tortellini','jams-and-preserves','pork-loins','chili','garnishes','granola-and-porridge','rolled-cookies','pot-pie','chocolate-chip-cookies',
             'manicotti','lasagna','cupcakes','tarts','burgers','ice-cream','scones','tempeh','penne','chowders','sweet-sauces','coffee-cakes','biscotti','pork-ribs','quiche','roast-beef',
             'meatloaf','mashed-potatoes','meatballs','chutneys','veggie-burgers','macaroni-and-cheese','oatmeal','sugar-cookies','labor-day','dips-lunch-snacks','turkey-burgers',
             'prepared-potatoes','desserts-fruit','desserts-easy','halloween-cupcakes','breakfast-eggs','eggs-breakfast','halloween-cakes','halloween-cocktails','no-bake-cookies']


TYPE_DIET = ['dietary','low-protein','high-protein','low-carb','low-sodium','vegetarian','comfort-food','low-cholesterol','pasta-rice-and-grains','diabetic',
             'kosher','kid-friendly','inexpensive','gluten-free','healthy','low-fat','low-saturated-fat','low-calorie','healthy-2','spicy','very-low-carbs','heirloom-historical',
             'egg-free','high-calcium','toddler-friendly','pet-food','infant-baby-friendly','high-fiber','dairy-free','no-shell-fish','heirloom-historical-recipes']


TYPE_OCCASION = ['brunch','potluck','picnic','to-go','dinner-party','barbecue','camping','fall','summer','christmas','romantic','st-patricks-day','winter','thanksgiving',
                 'independence-day','new-years','wedding','valentines-day','spring','halloween','easter','hanukkah','kwanzaa','mardi-gras-carnival','birthday','chinese-new-year'
                 'rosh-hashana','ramadan','cinco-de-mayo','mothers-day','fathers-day','super-bowl','april-fools-day','memorial-day','rosh-hashanah','fourth-of-july','irish-st-patricks-day']

TYPE_MEAL = ['desserts','main-dish','brunch','potluck','picnic','dinner-party','breakfast','lunch',
             'side-dishes','appetizers','beverages','cocktails','snacks','frozen-desserts','dips-lunch-snacks','one-dish-meal','barbecue','finger-food','non-food-products']

TYPE_ORIGIN = ['north-american','french','european','american','southern-united-states','southwestern-united-states','cajun','creole','canadian','asian','indian','spanish','south-west-pacific',
               'australian','laotian','scottish','middle-eastern','mexican','tex-mex','greek','italian','english','midwestern','african','moroccan','pacific-northwest',
               'beijing','chinese','thai','korean','german','californian','british-columbian','brazilian','south-american','native-american','new-zealand',
               'dutch','nigerian','pakistani','caribbean','central-american','northeastern-united-states','japanese','hungarian','jewish-ashkenazi','austrian',
               'czech','scandinavian','argentine','indonesian','swedish','lebanese','swiss','chilean','irish','quebec','portuguese','amish-mennonite','hawaiian',
               'jewish-sephardi','south-african','turkish','cambodian','vietnamese','cuban','russian','szechuan','danish','ethiopian','polish','norwegian','micro-melanesia',
               'peruvian','hunan','malaysian','angolan','iranian-persian','pennsylvania-dutch','finnish','filipino','sudanese','saudi-arabian','belgian','iraqi',
               'icelandic','nepalese','ecuadorean','venezuelan','costa-rican','palestinian','guatemalan','colombian','libyan','georgian','congolese','honduran','mongolian',
               'somalian','namibian','welsh']
