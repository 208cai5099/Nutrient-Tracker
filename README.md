# Nutrient-Tracker
The nutrient tracker program asks the user what food they've eaten and how much they've eaten in grams. The tracker will
reference a database of foods and their nutrient profiles to record the calories, carbohydrates, proteins, and fats consumed
per input. The database is based on a file from the U.S. Department of Agriculture's Agricultural Research Service.

Reference:
U.S. Department of Agriculture, Agricultural Research Service. 2020. USDA Food and Nutrient Database for Dietary Studies
2017-2018. Food Surveys Research Group Home Page, http://www.ars.usda.gov/nea/bhnrc/fsrg

data_processing.py
This script processes the dataset into a working database that can be referenced by the nutrient tracker. Before processing
the data in Python, I first used Excel to format the dataset to be readable into a dataframe using pandas. Once it's imported,
the dataset's unneeded columns are dropped. Only the name, calorie, protein, carbohydrate and total fat columns are kept. The
dataset contains two columns that describe the food in each row, but for simplicity, only one of them is kept to be the name
column. Next, certain food items are removed, because their names were way too vague. The means of each unique food item's
calories, carbohydrate, protein, and fat are calculated. The dataset has rows in which multiple different foods were listed
as one entire name, so those names were split into separate rows with identical nutrient profiles.

nutrient_tracker.py
This script creates a Tracker class that is used to ask the user for what foods they've eaten and how much they've eaten.
The food's name, along with the associated amount, calories, carbohydrates, proteins, and fats, are appended to running lists,
which are saved as the Tracker object's attributes. The datetime module is used to record the date of the entry. The Tracker
object uses a while loop to keep asking the user for another food item, if the food item is not listed in the database. Another
while loop is used to ask the user for how much they've eaten in grams until the user gives a valid, numeric value. Once the
user inputs that they would no longer like to record another entry, the script will ask the user whether they want the entries
to be saved. The script can save the file as a csv file with the date as the title.
