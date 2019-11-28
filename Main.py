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
import tkinter
from functools import partial

#Updates all data from files
Update.updateCupType('Cups.ini') #updates the cup volume list
Update.updateIngredientAlcohol('AlcoholContent.ini') #updates the alcholic content of ingredients list
Update.updateIngredientPump('Pumps.ini') #updates the ingredient pumps
Update.updateIngredientList('Ingredients.ini') #updates a list of available ingredients
Update.updateMenu('Menu.ini') #updates the menu and recipe instructions

#gets input
top = tkinter.Tk()

def orderDrink(drink):
    print(drink)
    Data.menu[drink].setRecipeVolume()
    Data.menu[drink].setRecipeInstructions()
    Arduino.sendDrink(Data.menu[drink].recipeInstructions, "/dev/tty.usbmodem142101")

i = 0
for drink in Data.menu:
    B = tkinter.Button(top, text = Data.menu[drink].name, command = partial(orderDrink, Data.menu[drink].name))
    B.pack()
    i += 1

top.mainloop()
