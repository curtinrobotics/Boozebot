#This program defines a series of functions for initializing and updating boozebots data
#Programmers: TRG
#Iteration: 0.2
#Last edited: 09/04/2019
#Created: 10/04/2019

#imports the relevant libraries
import time #imports the time library
import Drink #imports the the drink class
import Data #imports the data file

#updates the cup list
def updateCupType(file_name):
    file = open(file_name, 'r')
    for line in file:
        cup = line.split(': ')
        Data.cupTypes[cup[0]] = int(cup[1])
    file.close()
    return 0

#updates the percentage alcohol of ingredients list
def updateIngredientAlcohol(file_name):
    file = open(file_name, 'r')
    for line in file:
        ingredient = line.split(': ')
        Data.ingredientAlcohol[ingredient[0]] = int(ingredient[1])
    file.close()
    return 0

#updates the ingredient pumps
def updateIngredientPump(file_name):
    file = open(file_name, 'r')
    for line in file:
        ingredient = line.split(': ')
        Data.ingredientPump[ingredient[0]] = int(ingredient[1])
    file.close()
    return 0

#updates the list of available ingredients
def updateIngredientList(file_name):
    file = open(file_name, 'r')
    for line in file:
        if line not in Data.ingredientList:
            Data.ingredientList.append(line.strip('\n'))
        elif line in Data.ingredientList:
            print('Error: Ingredient double up. ' + line + ' is already in IngredientList')
            time.sleep(5)
    file.close()
    return 0

#updates the menu and recipe instructions
def updateMenu(file_name):
    Data.menu.clear()
    file = open(file_name, 'r')
    for line in file:
        #splits the recipe info apart
        recipe = line.split(', ')
        name = recipe[0].lower()
        cup = recipe[1]

        #converts Cup to integer value
        if cup in Data.cupTypes:
            cup = Data.cupTypes[cup]
        else:
            cup = int(cup)


        fill = int(recipe[2])
        Data.menu[name] = Drink.Drink(name) #creates a new drink instant with name name
        Data.menu[name].CupSize = cup
        Data.menu[name].MaxFillPercent = fill

        #creates recipe
        for ingredient in recipe:
            if ((ingredient != recipe[0]) & (ingredient != recipe[1]) & (ingredient != recipe[2])):
                amount = ingredient.split(': ')
                if amount[0] in Data.ingredientList:
                    Data.menu[name].setRecipeRatio(amount[0], int(amount[1]))
                    Data.menu[name].setDrinkIngredients(amount[0])
                else: #catches unavailable ingredients
                    print('Fatal Error: Missing ingredient. ' + amount[0] + ' not available in IngredientList. Exiting program')
                    time.sleep(5) #sleeps for 5 seconds for readability
                    file.close()
                    return 1

    #ends the function
    file.close()
    return 0
