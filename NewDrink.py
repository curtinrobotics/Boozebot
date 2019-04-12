#This program creates new drinks on demand for boozebot
#Programmers: TRG
#Iteration: 0.2
#Last edited: 09/04/2019
#Created: 10/04/2019

#imports the relevant libraries
import time #imports the time library
import DrinkClass #imports the the drink class
import Data #imports the data file

#creates a new drink
def New(name, cupSize, percentage, ingredients):
    Data.Menu[name] = DrinkClass.Drink() #creates a new drink instant with name name

    #converts cupSize to an integer value
    if cupSize in Data.CupType:
        cupSize = Data.CupType[cupSize]
    else:
        cupSize = int(cupSize)

    Data.Menu[name].CupSize = cupSize
    Data.Menu[name].MaxFillPercent = percentage

    #creates recipe
    for ingredient in ingredients:
        if ingredient in Data.IngredientList:
            Data.Menu[name].SetRecipeRatio(ingredient, int(ingredients[ingredient]))
            Data.Menu[name].SetDrinkIngredients(ingredient)
        else: #catches unavailable ingredients
            print('Fatal Error: Missing ingredient. ' + ingredient + ' not available in IngredientList. Exiting program')
            time.sleep(5) #sleeps for 5 seconds for readability
            return 1
    return 0
