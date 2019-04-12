#This program defines a series of functions for initializing and updating boozebots data
#Programmers: TRG
#Iteration: 0.2
#Last edited: 09/04/2019
#Created: 10/04/2019

#imports the relevant libraries
import time #imports the time library
import DrinkClass #imports the the drink class
import NewDrink #imports the new drink function
import Data #imports the data file

#updates the cup list
def UpdateCuptype(file_name):
    File = open(file_name, 'r')
    for line in File:
        Cup = line.split(': ')
        Data.CupType[Cup[0]] = int(Cup[1])
    File.close()
    return 0

#updates the percentage alcohol of ingredients list
def UpdateIngredientAlcohol(file_name):
    File = open(file_name, 'r')
    for line in File:
        Ingredient = line.split(': ')
        Data.IngredientAlcohol[Ingredient[0]] = int(Ingredient[1])
    File.close()
    return 0

#updates the ingredient pumps
def UpdateIngredientPump(file_name):
    File = open(file_name, 'r')
    for line in File:
        Ingredient = line.split(': ')
        Data.IngredientPump[Ingredient[0]] = int(Ingredient[1])
    File.close()
    return 0

#updates the list of available ingredients
def UpdateIngredientList(file_name):
    File = open(file_name, 'r')
    for line in File:
        if line not in Data.IngredientList:
            Data.IngredientList.append(line.strip('\n'))
        elif line in Data.IngredientList:
            print('Error: Ingredient double up. ' + line + ' is already in IngredientList')
            time.sleep(5)
    File.close()
    return 0

#updates the menu and recipe instructions
def UpdateMenu(file_name):
    File = open(file_name, 'r')
    for line in File:
        #splits the recipe info apart
        Recipe = line.split(', ')
        Name = Recipe[0]
        Cup = Recipe[1]

        #converts Cup to integervalue
        if Cup in Data.CupType:
            Cup = Data.CupType[Cup]
        else:
            Cup = int(Cup)


        Fill = int(Recipe[2])
        Data.Menu[Name] = DrinkClass.Drink() #creates a new drink instant with name name
        Data.Menu[Name].CupSize = Cup
        Data.Menu[Name].MaxFillPercent = Fill

        #creates recipe
        for ingredient in Recipe:
            if ((ingredient != Recipe[0]) & (ingredient != Recipe[1]) & (ingredient != Recipe[2])):
                Amount = ingredient.split(': ')
                if Amount[0] in Data.IngredientList:
                    Data.Menu[Name].SetRecipeRatio(Amount[0], int(Amount[1]))
                    Data.Menu[Name].SetDrinkIngredients(Amount[0])
                else: #catches unavailable ingredients
                    print('Fatal Error: Missing ingredient. ' + Amount[0] + ' not available in IngredientList. Exiting program')
                    time.sleep(5) #sleeps for 5 seconds for readability
                    File.close()
                    return 1

    #ends the function
    File.close()
    return 0
