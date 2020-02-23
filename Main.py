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
from forms import uploadMenu, settings, confirmOrder, adminLogin, addCredits, register, buyDrink
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

users = "Init/users.csv"

def submitDrink(drink='NULL'):
    print("bugtest")
    print(drink)
    Data.menu[drink].setRecipeVolume()
    Data.menu[drink].setRecipeInstructions()
    Arduino.sendDrink(Data.menu[drink].recipeInstructions, "/dev/tty.usbmodem142101")

#SETTINGS
SETTINGS = {'OpenBar': False, 'CustomDrinks': False, 'AdminOveride': False}
Auth = False

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html', auth=Auth)

@app.route("/menu")
def menu():
    return render_template('menu.html', menu = Data.menu, title = 'Menu', auth=Auth)

@app.route("/login")
def login():
    print('hi')

@app.route("/menu/<drinkName>", methods=['GET', 'POST'])
def drink(drinkName):
    drinkExists = False
    if SETTINGS['OpenBar'] == True:
        form = confirmOrder()
    else:
        form = buyDrink()
    if form.confirm.data:
        for drink in Data.menu:
            if Data.menu[drink].name == drinkName:
                drinkExists = True
                if SETTINGS['OpenBar'] == True:
                    submitDrink(drink)

                else:
                    usersIN = open(users, 'r')
                    usersOUT = open('Init/out.csv', 'w')
                    for line in usersIN:
                        ID, credit, Name, Access = line.split(', ')
                        if str(form.ID.data) == ID:
                            if int(credit) > 0:
                                credit = int(credit) - 1
                                line = ID + ', ' + str(credit) + ', ' + Name + ', ' + Access
                                submitDrink(drink)
                            else:
                                flash(f'No Credit', 'danger')
                        usersOUT.write(line)
                    usersIN.close()
                    usersOUT.close()
                    try:
                        os.remove(users)
                        os.rename('Init/out.csv', users)
                    except PermissionError:
                        print(users + 'is running in a higher process')

                return redirect(url_for('menu'))
    for drink in Data.menu:
        if Data.menu[drink].name == drinkName:
            drinkExists = True
            return render_template('confirm.html', drink = Data.menu[drink], form = form, auth = Auth, openBar = SETTINGS['OpenBar'])
    if drinkExists == False:
        return redirect(url_for('drinkMissing'))
    return render_template('menu.html', menu = Data.menu, auth = Auth, customDrinks = SETTINGS['CustomDrinks'])

@app.route("/missing")
def drinkMissing():
    return render_template('missing.html', auth=Auth)

if __name__ == '__main__':
    app.run(debug=True)
