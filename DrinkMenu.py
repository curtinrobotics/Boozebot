#This program is the main program for boozebot and integrates all other programs
#Programmers: TRG
#Iteration: 0.5
#Last edited: 05/04/2019
#Created: 10/04/2019

#imports relevate libraries
import time #imports the time library
import DrinkClass #imports the the drink class
import NewDrink #imports the NewDrink function
import Data #imports the data file
import DataUpdate # imports the Dataupdate function set

#Updates all data from files
DataUpdate.UpdateCuptype('Cups.ini') #updates the cup volume list
DataUpdate.UpdateIngredientAlcohol('AlcoholContent.ini') #updates the alcholic content of ingredients list
DataUpdate.UpdateIngredientPump('Pumps.ini') #updates the ingredient pumps
DataUpdate.UpdateIngredientList('Ingredients.ini') #updates a list of available ingredients
DataUpdate.UpdateMenu('Menu.ini') #updates the menu and recipe instructions

#gets input
Drink = input('Drink: ') #gets drink type

if Drink in Data.Menu:
    #assigns ingredients ratios
    print(Data.Menu[Drink].RecipeRatio)

    #converts ratios to volume and prints
    Data.Menu[Drink].SetRecipeVolume()
    print(Data.Menu[Drink].RecipeVolume)

    #converts volume to instructions for arduino and prints
    Data.Menu[Drink].SetRecipeInstructions()
    print(Data.Menu[Drink].RecipeInstructions)

    #print amount of standard Menu[Drink]s
    print(Data.Menu[Drink].GetStndDrink())
else: # gets data for a new custom drink
    custom = input('Drink not on menu, would you like to create a custom drink? ')
    if (custom == 'Yes'):
        Cup = input('Cup Type(ml): ') #gets the cup type/volume
        Fill = input('how full would you like your drink(%): ') #gets the percentage fill of the cup

        # gets an ingredient list and ratio
        Ingredients = {}
        Ingredient = input('Ingredient: ')
        Amount = input('Amount as a ratio: ')
        Ingredients[Ingredient] = Amount
        while (Ingredient != ''):
            Ingredient = input('Ingredient: ')
            Amount = input('Amount as a ratio: ')
            Ingredients[Ingredient] = Amount

        #creates a new drink using the New function
        NewDrink.New(Drink, Cup, Fill, Ingredients)
    elif (custom == 'No'):
        print('okay, returning to main menu')
    else:
        print('unrecognised command, returning to main menu')

print('end program')
time.sleep(60) #stops program for 60 seconds for readability
