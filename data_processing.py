# Set up working environment
import pandas as pd

# Import the data
food_df = pd.read_csv('2017-2018 FNDDS At A Glance - FNDDS Nutrient Values.csv')

# Remove unneeded columns
food_df = food_df.drop(['Food code', 'Main food description', 'WWEIA Category number', 'Sugars, total\n(g)', 'Fiber, total dietary (g)',
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
food_df.columns = ['Name', 'Calories', 'Protein(g)', 'Carbohydrate(g)', 'TotalFat(g)']


# Exclude food items with these words in their names
exclude_list = ['Not included in a food category', 'Baby', 'single code', 'excludes', 'other', 'Other', 'dish', 'Soup',
                'Formula', 'sandwich']
for item in exclude_list:
    for index in food_df.index:
        name = food_df.loc[index, 'Name']
        if item in name or item == name:
            food_df = food_df.drop(index, axis = 0)

# Ensure all items are properly removed
for item in exclude_list:
    for name in list(food_df.Name.unique()):
        if item in name:
            print('Error: Found unneeded food item.')
        else:
            break
    break

# Change food names to lowercase in case user types in lowercase
food_df['Name'] = food_df['Name'].str.lower()

# Aggregate the data by calculating the mean of each food item
# Divide by 100 to get nutrient content per g of food item
food_df = food_df.groupby(by = 'Name').mean()
food_df = food_df.div(100)

# Need to insert the names of food items back as a column
name = {'Name': list(food_df.index)}
name = pd.DataFrame(name)
food_df.index = list(range(0, len(food_df)))
food_df = pd.concat([name, food_df], axis = 1)

# Replace awkward, unusual names
food_df = food_df.replace('ready-to-eat cereal, lower sugar (=<21.2g/100g)', 'cereal, lower sugar')
food_df = food_df.replace('ready-to-eat cereal, higher sugar (>21.2g/100g)', 'cereal, higher sugar')
food_df = food_df.replace('chicken, whole pieces', 'chicken')


# Replace the '/' in names with 'and'
food_df = food_df.replace('fried rice and lo/chow mein', 'fried rice and lo mein and chow mein')
food_df = food_df.replace('cottage/ricotta cheese', 'cottage cheese and ricotta cheese')
food_df = food_df.replace('pretzels/snack mix', 'pretzels and snack mix')

# Replace certain names for later splitting
food_df = food_df.replace('chicken patties, nuggets and tenders', 'chicken patties and chicken nuggets and chicken tenders')
food_df = food_df.replace('sport and energy drinks', 'sport drinks and energy drinks')
food_df = food_df.replace('diet sport and energy drinks', 'diet sport drinks and energy drinks')
food_df = food_df.replace('protein and nutritional powders', 'protein powders and nutritional powders')
food_df = food_df.replace('stir-fry and soy-based sauce mixtures', 'stir-fry sauce mixtures and soy-based sauce mixtures')

# Split up the names with multiple food items in them separated by 'and' or ','
and_names = []
for name in list(food_df.Name.unique()):
    if 'and ' in name:
        and_names.append(name)
and_names.remove('macaroni and cheese')

comma_names = []
for name in list(food_df.Name.unique()):
    if ',' in name:
        comma_names.append(name)
to_be_removed = ['flavored milk, lowfat', 'flavored milk, nonfat', 'flavored milk, reduced fat', 'flavored milk, whole',
                 'milk, lowfat', 'milk, nonfat', 'milk, reduced fat', 'milk, whole', 'pasta sauces, tomato-based',
                 'cereal, higher sugar', 'cereal, lower sugar', 'white potatoes, baked or boiled', 'yogurt, greek',
                 'yogurt, regular']
for item in to_be_removed:
    comma_names.remove(item)

def splitter(names, marker):
    global food_df

    for n in names:
        row = food_df[food_df['Name'] == n]
        row_name = row.iloc[0, 0]
        if n is row_name:
            food_df = food_df.drop(list(row.index)[0], axis = 0)
        split_names_list = []
        split_name = n.split(marker)
        for split in split_name:
            split_names_list.append(split)
        for split in split_names_list:
            split = split.strip()
            row['Name'] = split
            food_df = pd.concat([food_df, row], axis = 0)

splitter(and_names, 'and')
splitter(comma_names, ',')

food_df.index = list(range(0, len(food_df)))
