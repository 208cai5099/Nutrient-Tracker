from data_processing import database
from datetime import date
import tkinter
from PIL import ImageTk, Image
from tkinter import messagebox

def calculate():
    food = food_entry.get()
    amount = amount_entry.get()

    if food == '' or amount == '':
        messagebox.showerror(title = 'Error', message = 'Please fill out all entries.')
    else:
        if food not in list(database.Name):
            possible_foods = []
            for possible in list(database.Name):
                if food in possible:
                    possible_foods.append(possible)
                    if len(possible_foods) == 3:
                        break
            if len(possible_foods) == 0:
                messagebox.showerror(title = 'Error', message = f'{food} is not found in database. Please check spelling or '
                                                                f'enter a different food item.')
            elif len(possible_foods) >= 1:
                messagebox.showerror(title = 'Error', message = f'{food} is not found in database. Here are some similar '
                                                                f'items: \n {str(possible_foods).strip("[]")}.')
        try:
            amount = float(amount)
            calories = round(amount * float(database[database['Name'] == food]['Calories']), 0)
            carbohydrate = round(amount * float(database[database['Name'] == food]['Carbohydrate(g)']), 0)
            protein = round(amount * float(database[database['Name'] == food]['Protein(g)']), 0)
            fat = round(amount * float(database[database['Name'] == food]['TotalFat(g)']), 0)
            today_date = str(date.today())

            amount_label.config(text = 'How much did you eat (g)?')

            return [today_date, food, amount, calories, carbohydrate, protein, fat]
        except:
            amount_label.config(text = 'How much did you eat (g)?\n'
                                       'Please enter numeric value')

def save():
    entry = calculate()
    if entry is None:
        pass
    else:
        entry = str(entry).strip('[]')
        with open('nutrient_log.txt', 'a') as file:
            file.write(f'{entry} \n')

# Create a window
window = tkinter.Tk()
window.minsize()
window.title('Nutrient Tracker')
window.config(bg = '#F8EDE3', padx = 20, pady = 20)

# Add logo
canvas = tkinter.Canvas(width= 500, height= 300, bg = '#F8EDE3', highlightthickness=0)
food = Image.open('food.png')
food = ImageTk.PhotoImage(food)
canvas.create_image(275, 150, image = food)
canvas.create_text(275, 30, text = 'Welcome to the Nutrient Tracker!', font = ('Arial', 18, 'bold'))
canvas.grid(row = 0, column = 0, columnspan=2)

# Add food and amount labels and entries
food_label = tkinter.Label(text = 'What did you eat?', bg = '#F8EDE3', font = ('Arial', 10, 'bold'))
food_label.grid(row = 2, column = 0)

food_entry = tkinter.Entry()
food_entry.grid(row = 2, column = 1)

amount_label = tkinter.Label(text = 'How much did you eat (g)?', bg = '#F8EDE3', font = ('Arial', 10, 'bold'))
amount_label.grid(row = 3, column = 0)

amount_entry = tkinter.Entry()
amount_entry.grid(row = 3, column = 1)

# Add save button
save_button = tkinter.Button(text = 'Save', bg = 'white', font = ('Arial', 10, 'bold'), command = save)
save_button.grid(row = 3, column = 2)

window.mainloop()
