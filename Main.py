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
from functools import partial

#flask
from PIL import Image
from Forms import uploadMenu, adminSettings, confirmOrder, adminLogin, addCredits, register, buyDrink
from flask import Flask, render_template, url_for, flash, redirect, session, make_response

import os

app = Flask(__name__, template_folder="GUI", static_url_path="/GUI", static_folder="GUI")

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#Updates all data from files
InitFile = "Standard"
Update.updateCupType('Init/Cups.ini') #updates the cup volume list
Update.updateIngredientAlcohol('Init/AlcoholContent.ini') #updates the alcholic content of ingredients list
Update.updateIngredientPump('Init/' + InitFile + '/Pumps.ini') #updates the ingredient pumps
Update.updateIngredientList('Init/' + InitFile + '/Ingredients.ini') #updates a list of available ingredients
Update.updateMenu('Init/' + InitFile + '/Menu.ini') #updates the menu and recipe instructions

users = "Init/Users.csv"

def startSession():
    try:
        if session['RUN'] != True:
            session['OpenBar'] = False
            session['CustomDrinks'] = False
            session['AdminOveride'] = False
    except:
        session['RUN'] = True
        session['OpenBar'] = False
        session['CustomDrinks'] = False
        session['AdminOveride'] = False
    session['RUN'] = True

def closeAuth():
    session.pop('Auth')

def generateAuth(_ID):
    usersIN = open(users, 'r')
    usersOUT = open('Init/out.csv', 'w')
    for line in usersIN:
        ID, credit, Name, Access = line.split(', ')
        if _ID == ID:
            if Access.strip('\n') == "Admin":
                session['Auth'] = True
            else:
                flash(f'No Admin Access', 'danger')
        usersOUT.write(line)
    usersIN.close()
    usersOUT.close()
    try:
        os.remove(users)
        os.rename('Init/out.csv', users)
    except PermissionError:
        print(users + 'is running in a higher process')

def checkAuth():
    return session.get('Auth')

def purchaseDrink(_ID, drink):
    usersIN = open(users, 'r')
    usersOUT = open('Init/out.csv', 'w')
    for line in usersIN:
        ID, credit, Name, Access = line.split(', ')
        if _ID == ID:
            if session['AdminOveride'] == True and Access == 'Admin':
                submitDrink(drink)
            elif int(credit) > 0:
                credit = int(credit) - 1
                line = ID + ', ' + str(credit) + ', ' + Name + ', ' + Access + '\n'
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

def submitDrink(drink='NULL'):
    print(drink)
    Data.menu[drink].setRecipeVolume()
    Data.menu[drink].setRecipeInstructions()
    Arduino.sendDrink(Data.menu[drink].recipeInstructions, "/dev/tty.usbmodem142101")

@app.route("/home")
@app.route("/")
def home():
    startSession()
    return render_template('home.html')

@app.route("/menu")
def menu():
    return render_template('menu.html', menu=Data.menu, title='Menu')

@app.route("/menu/<drinkName>", methods=['GET', 'POST'])
def drink(drinkName):
    drinkExists = False
    if session['OpenBar'] == True:
        form = confirmOrder()
    else:
        form = buyDrink()
    if form.confirm.data:
        for drink in Data.menu:
            if Data.menu[drink].name == drinkName:
                drinkExists = True
                if session['OpenBar'] == True:
                    submitDrink(drink)
                else:
                    purchaseDrink(form.ID.data, drink)
                return redirect(url_for('menu'))
    for drink in Data.menu:
        if Data.menu[drink].name == drinkName:
            drinkExists = True
            return render_template('confirm.html', drink=Data.menu[drink], form=form)
    if drinkExists == False:
        return redirect(url_for('drinkMissing'))
    return render_template('menu.html', menu=Data.menu)

@app.route("/missing")
def drinkMissing():
    return render_template('missing.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = adminLogin()
    if form.ID.data:
        generateAuth(form.ID.data)
        if checkAuth():
            return redirect(url_for('setting'))
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    closeAuth()
    return redirect(url_for('menu'))

@app.route("/settings", methods=['GET', 'POST'])
def setting():
    form = adminSettings()
    if checkAuth() == True:
        #SETTINGS
        session['OpenBar'] = False
        session['CustomDrinks'] = False
        session['AdminOveride'] = False
        if form.confirm.data:
            if form.openBar.data:
                session['OpenBar'] = True
            else:
                session['OpenBar'] = False
            if form.custom.data:
                session['CustomDrinks'] = True
            else:
                session['CustomDrinks'] = False
            if form.adminOveride.data:
                session['AdminOveride'] = True
            else:
                session['AdminOveride'] = False
            return redirect(url_for('menu'))
    return render_template('settings.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
