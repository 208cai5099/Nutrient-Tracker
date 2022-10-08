from data_processing import food_df
from datetime import date
import tkinter
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#------------------------ SAVE ENTRY -----------------------------#

# Checks if inputted food is in the food_df
def check_food():

    food = food_entry.get()
    amount = amount_entry.get()

    if food == '' or amount == '':
        messagebox.showerror(title = 'Error', message = 'Please fill out all entries.')
    else:
        if food in list(food_df.Name):
            return food
        elif food not in list(food_df.Name):
            possible_foods = []
            for possible in list(food_df.Name):
                if food in possible:
                    possible_foods.append(possible)
                    if len(possible_foods) == 3:
                        break
            if len(possible_foods) == 0:
                messagebox.showerror(title = 'Error', message = f'{food} is not recognized in our records. Please check spelling or '
                                                                f'enter a different food item.')
            elif len(possible_foods) >= 1:
                messagebox.showerror(title = 'Error', message = f'{food} is not recognized in our records. Here are other options '
                                                                f'items: \n {str(possible_foods).strip("[]")}.')

# Converts the amount to float type
def convert_amount():

    try:
        amount = float(amount_entry.get())
        return amount
    except:
        amount_label.config(text='How much did you eat (g)?\n'
                                 'Please enter numeric value')

# Calculates the fat, caloric, protein, and carb intakes based on amount and food
def calculate():

    food = check_food()
    amount = convert_amount()

    if food is None or amount is None:
        pass
    else:
        calories = round(amount * float(food_df[food_df['Name'] == food]['Calories']), 0)
        carbohydrate = round(amount * float(food_df[food_df['Name'] == food]['Carbohydrate(g)']), 0)
        protein = round(amount * float(food_df[food_df['Name'] == food]['Protein(g)']), 0)
        fat = round(amount * float(food_df[food_df['Name'] == food]['TotalFat(g)']), 0)
        today_date = str(date.today())

        amount_label.config(text = 'How much did you eat (g)?')

        return f'{today_date}, {food}, {amount}, {calories}, {carbohydrate}, {protein}, {fat}'

# Saves the entry as a single row in txt file
def save():

    entry = calculate()
    if entry is None:
        pass
    else:
        with open('nutrient_log.txt', 'a') as file:
            file.write(entry)
            file.write('\n')

        # Updates the dates dropdown menus after entering today's first entry
        global dates_list
        if str(date.today()) not in dates_list:
            updated_df = pd.read_csv('nutrient_log.txt')
            updated_dates = list(updated_df.Date.unique())
            start_dates.config(values = updated_dates)
            end_dates.config(values = updated_dates)

# Create a window
window = tkinter.Tk()
window.minsize()
window.title('Nutrient Tracker')
window.config(bg = '#F8EDE3', padx = 20, pady = 20)

# Add logo
canvas = tkinter.Canvas(width = 500, height = 275, bg = '#F8EDE3', highlightthickness = 0)
food = Image.open('food.png')
food = ImageTk.PhotoImage(food)
canvas.create_image(275, 150, image = food)
canvas.create_text(275, 30, text = 'Welcome to the Nutrient Tracker!', font = ('Arial', 18, 'bold'))
canvas.grid(row = 0, column = 0, columnspan=2)

# Add food and amount labels and entries
food_label = tkinter.Label(text = 'What did you eat?', bg = '#F8EDE3', font = ('Arial', 10, 'bold'))
food_label.grid(row = 1, column = 0)

food_entry = tkinter.Entry()
food_entry.grid(row = 1, column = 1)

amount_label = tkinter.Label(text = 'How much did you eat (g)?', bg = '#F8EDE3', font = ('Arial', 10, 'bold'))
amount_label.grid(row = 2, column = 0)

amount_entry = tkinter.Entry()
amount_entry.grid(row = 2, column = 1)

# Add save button
save_button = tkinter.Button(text = 'Save Entry', bg = 'white', font = ('Arial', 10, 'bold'), command = save)
save_button.grid(row = 2, column = 2)

#------------------------ VISUALIZE THE DATA -----------------------------#

# Import the list of dates in the log records before any new entries
df = pd.read_csv('nutrient_log.txt')
dates_list = list(df.Date.unique())

# Create a start date label
start_label = tkinter.Label(text='Start Date', bg='#F8EDE3', font=('Arial', 10, 'bold'))
start_label.grid(row = 3, column = 0)

# Create a dropdown menu for start dates
start_dates = ttk.Combobox(values=dates_list)
start_dates.grid(row = 4, column = 0)

# Create an end date label
end_label = tkinter.Label(text='End Date', bg='#F8EDE3', font=('Arial', 10, 'bold'))
end_label.grid(row = 3, column = 1)

# Create a dropdown menu for end dates
end_dates = ttk.Combobox(values=dates_list)
end_dates.grid(row = 4, column = 1)

# Sums up the calories, fats, proteins, and carbohydrates of each day from start date to end date
def aggregate_data(start, end):

    df = pd.read_csv('nutrient_log.txt')
    dates_list = list(df.Date.unique())

    start_index = dates_list.index(start)
    end_index = dates_list.index(end)

    if start_index > end_index:
        messagebox.showerror(title = 'Error', message = 'Please make sure the Start Date is before the End Date.')
        return None

    elif start_index <= end_index:
        if start_index == end_index:
            dates = []
            dates.append(dates_list[start_index])
        else:
            dates = dates_list[start_index : end_index + 1]
        subset = df[df['Date'].isin(dates)]
        graph_data = subset.groupby(by = 'Date').sum()
        return graph_data

# Takes the aggregated data and created 4 subplots for carb, fat, protein, and calories
def graphing(start, end):

    graph_data = aggregate_data(start, end)
    if graph_data is not None:
        sns.set_style(style = 'darkgrid')
        f, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize = (8, 8))

        nutrients_list = list(graph_data.columns)[1:]

        # Loop through each axis to plot the specific nutrient info and give appropriate y-axis label
        for num in range(len((ax1, ax2, ax3, ax4))):
            if len(graph_data.index) == 1:
                sns.barplot(data=graph_data, x=graph_data.index, y=nutrients_list[num],
                            ax = (ax1, ax2, ax3, ax4)[num])
            else:
                sns.lineplot(data = graph_data, x = graph_data.index, y = nutrients_list[num],
                             ax = (ax1, ax2, ax3, ax4)[num])
            if nutrients_list[num] == 'Calories':
                (ax1, ax2, ax3, ax4)[num].set_ylabel(nutrients_list[num])
            else:
                (ax1, ax2, ax3, ax4)[num].set_ylabel(f'{nutrients_list[num]} (g)')

        plt.show()

# Calls on function to graph the data
def visualize():
    start = start_dates.get()
    end = end_dates.get()

    # Error if there is no start date or end date given
    if start == '' or end == '':
        messagebox.showerror(title='Error', message='Please enter Start Date and End Date.')

    else:
        graphing(start, end)

# Add visualize button
visualize_button = tkinter.Button(text = 'Visualize', bg = 'white', font = ('Arial', 10, 'bold'), command = visualize)
visualize_button.grid(row = 4, column = 2)

window.mainloop()