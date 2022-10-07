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

nutrient_tracker.py (Updated 10/7/22)

The original version of this script asks the user for their food consumption in the console. Now, this updated script creates a
GUI using the tkinter package for the user to interact with the program. The script creates a window that displays a logo for
the nutrient tracker and has fields for the user to type in the name of the food and the amount eaten in grams. The program will
ask the user for an alternative input if the input name is not found in the database, and it can offer other foods items with
characters that match those in the input. The program will also not accept any non-numeric input for the amount. The entries
are all saved as separate rows in an already existing txt file titled 'nutrient_log.txt'. The file uses Date, Food, Amount,
Calories, Carbohydrate, Protein, and Fat as the columns, and there must be an empty line at the bottom of the file in order
for the entries to be saved in a readable and processable format for visualization (see below). Although it's a txt file, the
entries are delimited by commas like a csv file so that it can be converted into a dataframe using the pandas package.
![Screenshot 2022-10-07 193615](https://user-images.githubusercontent.com/114125018/194675539-3ada20d3-a509-4bf4-a524-17ca0f280b32.jpg)

The user has an option to visualize their caloric, fat, carbohydrate, and protein intakes from a certain date to a
certain date. This is done using the 'Visualize' button that takes the start date and end date and calls on functions that
sum the nutrient intakes on each day using the pandas package and graphs the results using the seaborn and matplotlib packages.
The graph has 4 separate plots for calories, carbohydrates, proteins, and fats.
![Screenshot 2022-10-07 194158](https://user-images.githubusercontent.com/114125018/194675847-3531a8fd-db7a-47d0-8f44-9917b4a6f07b.jpg)


## References

1. I was able to build this program by learning tkinter from a course on Udemy.

   Yu, Angela. (Dec 2021). "100 Days of Code: The Complete Python Pro Bootcamp for 2022". Available at
   https://www.udemy.com/course/100-days-of-code/

2. The logo image is a cropped and slightly modified version of an image from Pixabay.

   Lisionka. (2022). Food vector image (not actual title of image). Available at
   https://pixabay.com/vectors/icon-flat-vector-pizza-1447860/

3. I also used a StackOverflow post to use PIL to process the logo image png file.

   bastelflp. (Nov 17, 2017). "Tkinter error: Couldn't recognize data in image file". Available at
   https://stackoverflow.com/questions/47357090/tkinter-error-couldnt-recognize-data-in-image-file

4. I read a code example from one of Seaborn's Gallery pages to learn how to create subplots.

   Waskom, Michael. (2022). "Color palette choices". Available at
   https://seaborn.pydata.org/examples/palette_choices.html

5. I looked up multiple resources to create and use the combobox class to create the dropdown menus.

   Tkinter 8.6.12 documentation. (2012). Available at 
   https://www.tcl.tk/man/tcl8.6/TkCmd/ttk_combobox.html
   
   Roseman, Mark. (2022) "Basic Widgets". Avalable at
   https://tkdocs.com/tutorial/widgets.html#combobox
   
   Panigrahi, Kiran. (Oct 26, 2021). "How to use a StringVar object in an Entry widget in Tkinter?" Available at
   https://www.tutorialspoint.com/how-to-use-a-stringvar-object-in-an-entry-widget-in-tkinter

6. I used the following website to find codes for different colors to improve my GUI aesthetics.
   
   Color Hunt. Available at https://colorhunt.co/
