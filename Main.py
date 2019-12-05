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

def submitDrink(drink='NULL'):
    print(drink)
    Data.menu[drink].setRecipeVolume()
    Data.menu[drink].setRecipeInstructions()
    Arduino.sendDrink(Data.menu[drink].recipeInstructions, "/dev/tty.usbmodem142101")
    minusDrinkButtons()
    back = tkinter.Button(top, text = 'back', command = lambda:[plusDrinkButtons(),back.pack_forget()])
    back.pack()

def minusDrinkButtons():
    for button in drinkButtons:
        button.pack_forget()

def plusDrinkButtons():
    for button in drinkButtons:
        button.pack()

def initDrinkButtons():
    i = 0
    for drink in Data.menu:
        drinkButtons.append(tkinter.Button(top, text = Data.menu[drink].name, command = partial(submitDrink, Data.menu[drink].name)))
        drinkButtons[i].pack()
        i += 1

#gets input
top = tkinter.Tk()

drinkButtons = []
initDrinkButtons()

top.mainloop()
