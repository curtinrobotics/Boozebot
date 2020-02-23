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

#flask
from PIL import Image
from forms import uploadMenu, settings, confirmOrder, adminLogin, addCredits, register
from flask import Flask, render_template, url_for, flash, redirect, session, make_response
from flask_login import LoginManager

import os

app = Flask(__name__, template_folder="GUI", static_url_path = "/GUI", static_folder = "GUI")
loginManager = LoginManager(app)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#Updates all data from files
InitFile = "Standard"
Update.updateCupType('Init/Cups.ini') #updates the cup volume list
Update.updateIngredientAlcohol('Init/AlcoholContent.ini') #updates the alcholic content of ingredients list
Update.updateIngredientPump('Init/' + InitFile + '/Pumps.ini') #updates the ingredient pumps
Update.updateIngredientList('Init/' + InitFile + '/Ingredients.ini') #updates a list of available ingredients
Update.updateMenu('Init/' + InitFile + '/Menu.ini') #updates the menu and recipe instructions

def submitDrink(drink='NULL'):
    print("bugtest")
    print(drink)
    Data.menu[drink].setRecipeVolume()
    Data.menu[drink].setRecipeInstructions()
    Arduino.sendDrink(Data.menu[drink].recipeInstructions, "/dev/tty.usbmodem142101")

#settings
OpenBar = False
CustomDrinks = False
Authorised = False

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/menu")
def menu():
    return render_template('menu.html', menu = Data.menu, title = 'Menu')

@app.route("/menu/<drinkName>", methods=['GET', 'POST'])
def drink(drinkName):
    drinkExists = False
    form = confirmOrder()
    if form.confirm.data:
        for drink in Data.menu:
            if Data.menu[drink].name == drinkName:
                submitDrink(drink)
                drinkExists = True
                return redirect(url_for('menu'))
    for drink in Data.menu:
        if Data.menu[drink].name == drinkName:
            drinkExists = True
            return render_template('confirm.html', drink = Data.menu[drink], form = form)
    if drinkExists == False:
        return redirect(url_for('drinkMissing'))
    return render_template('menu.html', menu = Data.menu)

@app.route("/missing")
def drinkMissing():
    return render_template('missing.html')

if __name__ == '__main__':
    app.run(debug=True)
