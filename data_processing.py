#U.S. Department of Agriculture, Agricultural Research Service. 2020. USDA Food and Nutrient Database for Dietary Studies 2017-2018. Food Surveys Research Group Home Page, http://www.ars.usda.gov/nea/bhnrc/fsrg

# Set up working environment
import pandas as pd

# Import the data
database = pd.read_csv('2017-2018 FNDDS At A Glance - FNDDS Nutrient Values.csv')

# Remove unneeded columns
database = database.drop(['Food code', 'Main food description', 'WWEIA Category number', 'Sugars, total\n(g)', 'Fiber, total dietary (g)',
                          'Fatty acids, total saturated (g)', 'Fatty acids, total monounsaturated (g)', 'Fatty acids, total polyunsaturated (g)', 'Cholesterol (mg)',
                          'Retinol (mcg)', 'Vitamin A, RAE (mcg_RAE)', 'Carotene, alpha (mcg)', 'Carotene, beta (mcg)', 'Cryptoxanthin, beta (mcg)', 'Lycopene (mcg)',
                          'Lutein + zeaxanthin (mcg)', 'Thiamin (mg)', 'Riboflavin (mg)', 'Niacin (mg)', 'Vitamin B-6 (mg)', 'Folic acid (mcg)',
                          'Folate, food (mcg)', 'Folate, DFE (mcg_DFE)', 'Folate, total (mcg)', 'Choline, total (mg)', 'Vitamin B-12 (mcg)',
                          'Vitamin B-12, added\n(mcg)', 'Vitamin C (mg)', 'Vitamin D (D2 + D3) (mcg)', 'Vitamin E (alpha-tocopherol) (mg)',
                          'Vitamin E, added\n(mg)', 'Vitamin K (phylloquinone) (mcg)', 'Calcium (mg)', 'Phosphorus (mg)', 'Magnesium (mg)', 'Iron\n(mg)',
                          'Zinc\n(mg)', 'Copper (mg)', 'Selenium (mcg)', 'Potassium (mg)', 'Sodium (mg)', 'Caffeine (mg)', 'Theobromine (mg)', 'Alcohol (g)',
                          '4:0\n(g)', '6:0\n(g)', '8:0\n(g)', '10:0\n(g)', '12:0\n(g)', '14:0\n(g)', '16:0\n(g)', '18:0\n(g)', '16:1\n(g)', '18:1\n(g)',
                          '20:1\n(g)', '22:1\n(g)', '18:2\n(g)', '18:3\n(g)', '18:4\n(g)','20:4\n(g)', '20:5 n-3\n(g)', '22:5 n-3\n(g)', '22:6 n-3\n(g)',
                          'Water\n(g)'], axis = 1)

# Change the column names
database.columns = ['Name', 'Calories', 'Protein(g)', 'Carbohydrate(g)', 'TotalFat(g)']


# Exclude food items with these words in their names
exclude_list = ['Not included in a food category', 'Baby', 'single code', 'excludes', 'other', 'Other', 'dish', 'Soup',
                'Formula', 'sandwich']
for item in exclude_list:
    for index in database.index:
        name = database.loc[index, 'Name']
        if item in name or item == name:
            database = database.drop(index, axis = 0)

# Ensure all items are properly removed
for item in exclude_list:
    for name in list(database.Name.unique()):
        if item in name:
            print('Error: Found unneeded food item.')
        else:
            break
    break

# Change food names to lowercase in case user types in lowercase
database['Name'] = database['Name'].str.lower()

# Aggregate the data by calculating the mean of each food item
# Divide by 100 to get nutrient content per g of food item
database = database.groupby(by = 'Name').mean()
database = database.div(100)

# Need to insert the names of food items back as a column
name = {'Name': list(database.index)}
name = pd.DataFrame(name)
database.index = list(range(0, len(database)))
database = pd.concat([name, database], axis = 1)

# Replace awkward, unusual names
database = database.replace('ready-to-eat cereal, lower sugar (=<21.2g/100g)', 'cereal, lower sugar')
database = database.replace('ready-to-eat cereal, higher sugar (>21.2g/100g)', 'cereal, higher sugar')
database = database.replace('chicken, whole pieces', 'chicken')


# Replace the '/' in names with 'and'
database = database.replace('fried rice and lo/chow mein', 'fried rice and lo mein and chow mein')
database = database.replace('cottage/ricotta cheese', 'cottage cheese and ricotta cheese')
database = database.replace('pretzels/snack mix', 'pretzels and snack mix')

# Replace certain names for later splitting
database = database.replace('chicken patties, nuggets and tenders', 'chicken patties and chicken nuggets and chicken tenders')
database = database.replace('sport and energy drinks', 'sport drinks and energy drinks')
database = database.replace('diet sport and energy drinks', 'diet sport drinks and energy drinks')
database = database.replace('protein and nutritional powders', 'protein powders and nutritional powders')
database = database.replace('stir-fry and soy-based sauce mixtures', 'stir-fry sauce mixtures and soy-based sauce mixtures')

# Split up the names with multiple food items in them separated by 'and' or ','
and_names = []
for name in list(database.Name.unique()):
    if 'and ' in name:
        and_names.append(name)
and_names.remove('macaroni and cheese')

comma_names = []
for name in list(database.Name.unique()):
    if ',' in name:
        comma_names.append(name)
to_be_removed = ['flavored milk, lowfat', 'flavored milk, nonfat', 'flavored milk, reduced fat', 'flavored milk, whole',
                 'milk, lowfat', 'milk, nonfat', 'milk, reduced fat', 'milk, whole', 'pasta sauces, tomato-based',
                 'cereal, higher sugar', 'cereal, lower sugar', 'white potatoes, baked or boiled', 'yogurt, greek',
                 'yogurt, regular']
for item in to_be_removed:
    comma_names.remove(item)

def splitter(names, marker):
    global database
    for n in names:
        row = database[database['Name'] == n]
        row_name = row.iloc[0, 0]
        if n is row_name:
            database = database.drop(list(row.index)[0], axis = 0)
        split_names_list = []
        split_name = n.split(marker)
        for split in split_name:
            split_names_list.append(split)
        for split in split_names_list:
            split = split.strip()
            row['Name'] = split
            database = pd.concat([database, row], axis = 0)

splitter(and_names, 'and')
splitter(comma_names, ',')

database.index = list(range(0, len(database)))
print(database)