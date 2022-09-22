from data_processing import database
import pandas as pd
from datetime import date

class Tracker:
    def __init__(self):
        self.food = []
        self.amount = []
        self.calories = []
        self.protein = []
        self.fat = []
        self.carbohydrate = []
        self.date = []

    def entry(self):
        food = input('What food did you eat? ').lower()
        if food not in list(database.Name):
            while True:
                possible_foods = []
                for possible in list(database.Name):
                    if food in possible:
                        possible_foods.append(possible)
                if len(possible_foods) == 0:
                    food = input('Sorry, that food is not recognized in our database. Please re-enter: ').lower()
                else:
                    food = input(f'Sorry, that food is not recognized in our database. Did you perhaps mean one of the choices: \n'
                                 f'{str(possible_foods).strip("[]")}? \n'
                                 'Please re-enter: ').lower()
                if food in list(database.Name):
                    break

        first_time = True
        while True:
            try:
                if first_time:
                    amount = float(input('How much did you eat (in grams)? '))
                else:
                    amount = float(input('How much did you eat (in grams)? Please enter numeric value. '))
                break
            except:
                first_time = False
                continue

        self.food.append(food)
        self.amount.append(amount)
        self.calories.append(round(amount * float(database[database['Name'] == food]['Calories']), 0))
        self.carbohydrate.append(round(amount * float(database[database['Name'] == food]['Carbohydrate(g)']), 0))
        self.protein.append(round(amount * float(database[database['Name'] == food]['Protein(g)']), 0))
        self.fat.append(round(amount * float(database[database['Name'] == food]['TotalFat(g)']), 0))
        self.date.append(date.today())

    def recorder(self):
        self.entry()
        records = pd.DataFrame({'Date': self.date, 'Name': self.food, 'Amount (g)': self.amount, 'Calories': self.calories,
                                'Carbohydrate(g)': self.carbohydrate, 'Protein(g)': self.protein, 'Fat(g)': self.fat})
        total = pd.DataFrame({'Date': f'{date.today()}', 'Name': 'Total', 'Amount (g)': [records['Amount (g)'].sum()],
                              'Calories': [records['Calories'].sum()], 'Carbohydrate(g)': [records['Carbohydrate(g)'].sum()],
                              'Protein(g)': [records['Protein(g)'].sum()], 'Fat(g)': [records['Fat(g)'].sum()]})
        records = pd.concat([records, total], axis = 0)
        print(records)
        print()
        return records

print('Welcome to Nutrient Tracker!')
print(f'Here is a list of food items in our database: \n'
      f'{str(list(database.Name.unique())).strip("[]")}')

tracker = Tracker()
report = tracker.recorder()
while True:
    again = input("Would you like to add another food? Enter 'Y' or 'N': ")
    if again is 'Y' or again is 'y':
        report = tracker.recorder()
        continue
    elif again is 'N' or again is 'n':
        break
    else:
        print("Sorry, we don't recognize that response.")
        continue

response = input("Would you like to save your data? Enter 'Y' or 'N': ")
if response is 'Y' or response is 'y':
    report.to_csv(f'{date.today()}_report.csv')
    print('Data saved as csv file.')
    print('Thank you for using the Nutrient Tracker!')
elif response is 'N' or response is 'n':
    print('Thank you for using the Nutrient Tracker!')
