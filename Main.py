#This program is the main program for boozebot and integrates all other programs
#Programmers: TRG
#Iteration: 0.5
#Last edited: 05/04/2019
#Created: 10/04/2019

#imports relevate libraries
import time #imports the time library
import Drink #imports the the drink class
import Data #imports the data file
import Update #imports the Dataupdate function set
import Arduino #imports Arduino communication library

#Updates all data from files
Update.updateCupType('Cups.ini') #updates the cup volume list
Update.updateIngredientAlcohol('AlcoholContent.ini') #updates the alcholic content of ingredients list
Update.updateIngredientPump('Pumps.ini') #updates the ingredient pumps
Update.updateIngredientList('Ingredients.ini') #updates a list of available ingredients
Update.updateMenu('Menu.ini') #updates the menu and recipe instructions

#gets input
drink = input('Drink: ').lower() #gets drink type

if drink in Data.menu:
    #assigns ingredients ratios
    print(Data.menu[drink].drinkIngredients)
    print(Data.menu[drink].recipeRatio)

    #converts ratios to volume and prints
    Data.menu[drink].setRecipeVolume()
    print(Data.menu[drink].recipeVolume)

    #converts volume to instructions for arduino and prints
    Data.menu[drink].setRecipeInstructions()
    print(Data.menu[drink].recipeInstructions)

    #print amount of standard Menu[Drink]s
    print(Data.menu[drink].getStndDrink())

    #sends Recipe instructions to the arduino
    Arduino.sendDrink(Data.menu[drink].recipeInstructions, "/dev/tty.usbmodem142101")
else: # gets data for a new custom drink
    custom = input('Drink not on menu, would you like to create a custom drink (y/n? ').lower()
    if (custom == 'y'):
        cup = input('Cup Type(ml): ').lower() #gets the cup type/volume
        fill = input('how full would you like your drink(%): ').lower() #gets the percentage fill of the cup

        # gets an ingredient list and ratio
        ingredients = {}
        ingredient = input('Ingredient: ').lower()
        amount = input('Amount as a ratio: ').lower()
        ingredients[ingredient] = amount
        while (ingredient != ''):
            ingredient = input('Ingredient: ').lower()
            amount = input('Amount as a ratio: ').lower()
            ingredients[ingredient] = amount

        #creates a new drink using the New function
        Drink.new(drink, cup, fill, ingredients)
    elif (custom == 'n'):
        print('okay, returning to main menu')
    else:
        print('unrecognised command, returning to main menu')

print('end program')
