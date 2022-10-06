# Nutrient-Tracker
The nutrient tracker program asks the user what food they've eaten and how much they've eaten in grams. The tracker will
reference a database of foods and their nutrient profiles to record the calories, carbohydrates, proteins, and fats consumed.
The database is based on a dataset from the U.S. Department of Agriculture's Agricultural Research Service. I tried to find
other comprehensive datasets online, but this is the best one I've found.

Reference to dataset:

U.S. Department of Agriculture, Agricultural Research Service. 2020. USDA Food and Nutrient Database for Dietary Studies
2017-2018. Food Surveys Research Group Home Page, http://www.ars.usda.gov/nea/bhnrc/fsrg

## Data Processing
data_processing.py

This script processes the dataset into a working database that can be referenced by the nutrient tracker. Before importing
the data into Python, I first used Excel to format the dataset so that processing is easier. Once it's imported, the dataset's
unneeded columns are dropped. Only the name, calorie, protein, carbohydrate and total fat columns are kept. The dataset contains
two columns that describe the food in each row, but for simplicity, only one of them is kept to be the food's identifying name.
Next, certain food items are removed, because their names were way too vague. The means of each unique food's calories,
carbohydrate, protein, and fat are calculated. The dataset has rows in which multiple different foods were listed as one entire
name, so those names were split into separate names each with identical nutrient profiles. This, however, probably reduces the
accuracy of the nutrient profiles of those items.

## GUI Interface via tkinter
![Screenshot 2022-10-05 194819](https://user-images.githubusercontent.com/114125018/194183958-f9f5250c-fa99-48c9-8f0c-0d9255b9baf9.jpg)

nutrient_tracker.py (Updated 10/5/22)

The original version of this script asks the user for their diet in the console. Now, this updated script creates a GUI
using the tkinter package for the user to interact with the program. The script creates a window that displays a logo for
the nutrient tracker and has fields for the user to type in the name of the food and the amount eaten in grams. The program will
ask the user for alternative food names if the input name is not found in the database, and it can offer similarly named
foods in the database as possible inputs. The program will also not accept any non-numeric input for the amount. The entries
are all saved as separate rows in an already existing txt file titled 'nutrient_log.txt'. Although it's a txt file, it's
formatted like a csv file that can be converted into a dataframe using pandas. This will allow the user to visualize their 
nutrient intake using other Python packages in a future update.

References:

I was able to build this program by learning tkinter from a course on Udemy.

Yu, Angela. (Dec 2021). "100 Days of Code: The Complete Python Pro Bootcamp for 2022". Available at
https://www.udemy.com/course/100-days-of-code/

I also used a StackOverflow post to help process an image for the logo.

bastelflp. (Nov 17, 2017). "Tkinter error: Couldn't recognize data in image file". Available at
https://stackoverflow.com/questions/47357090/tkinter-error-couldnt-recognize-data-in-image-file

The logo image is a cropped and slightly modified version of an image from Pixabay.

Lisionka. (2022). Food vector image (not actual title of image). Available at 
https://pixabay.com/vectors/icon-flat-vector-pizza-1447860/
