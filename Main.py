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
from forms import uploadMenu, adminSettings, confirmOrder, adminLogin, addCredits, newUser, buyDrink, customDrink
from flask import Flask, render_template, url_for, flash, redirect, session, make_response

import os

app = Flask(__name__, template_folder="GUI", static_url_path="/GUI", static_folder="GUI")

app.config['SECRET_KEY'] = '5791628bb0b13ceh98dfjk7lp76dfde280ba245'

#Updates all data from files
def initializeMenu(InitFile="Standard"):
    Update.updateCupType('Init/Cups.ini') #updates the cup volume list
    Update.updateIngredientAlcohol('Init/AlcoholContent.ini') #updates the alcholic content of ingredients list
    Update.updateIngredientPump('Init/' + InitFile + '/Pumps.ini') #updates the ingredient pumps
    Update.updateIngredientList('Init/' + InitFile + '/Ingredients.ini') #updates a list of available ingredients
    Update.updateMenu('Init/' + InitFile + '/Menu.ini') #updates the menu and recipe instructions

users = "Init/Users.csv"
menus = "Init/Menu.csv"

def startSession():
    try:
        if session['RUN'] != True:
            initializeMenu()
            session['OpenBar'] = False
            session['CustomDrinks'] = False
            session['AdminOveride'] = False
    except:
        session['RUN'] = True
        initializeMenu()
        session['OpenBar'] = False
        session['CustomDrinks'] = False
        session['AdminOveride'] = False
    session['RUN'] = True

def closeAuth():
    session.pop('Auth')

def generateAuth(_ID):
    usersIN = open(users, 'r')
    for line in usersIN:
        if len(line) > 5:
            ID, Credit, Name, Access = line.split(', ')
            if _ID == ID:
                if Access.strip('\n') == "Admin":
                    session['Auth'] = True
                else:
                    flash('No Admin Access', 'danger')
    usersIN.close()

def checkAuth():
    return session.get('Auth')

def purchaseDrink(_ID, drink):
    usersIN = open(users, 'r')
    usersOUT = open('Init/out.csv', 'w')
    for line in usersIN:
        if len(line) > 5:
            ID, Credit, Name, Access = line.split(', ')
            if _ID == ID:
                if session['AdminOveride'] == True and Access == 'Admin':
                    submitDrink(drink)
                elif int(Credit) > 0:
                    Credit = int(Credit) - 1
                    line = ID + ', ' + str(Credit) + ', ' + Name + ', ' + Access + '\n'
                    submitDrink(drink)
                else:
                    flash('No Credit', 'danger')
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

def saveFile(file, location, name='NULL'):
    try:
        os.mkdir(location)
        print("Directory " , location,  " Created ")
    except FileExistsError:
        print("Directory " , location,  " already exists")
    if name == 'NULL':
        name = file
    fileIN = open(file, 'r')
    fileOUT = open(location + name, 'w')
    for line in fileIN:
        fileOUT.write(line)
    fileIN.close()
    fileOUT.close()

def saveMenu(_menu, _ingredients, _pumps, name):
    menusIN = open(menus, 'r')
    menuNUM = 0
    for line in menusIN:
        if name in line:
            menuNNUM += 1
    if menuNUM > 0:
        flash((name + ' already exists. creating ' + name + str(menuNUM)), 'danger')
        name = name + str(menuNUM)
    menusIN.close()
    menusOUT = open(menus, 'a')
    menusOUT.write(name)
    menusOUT.close()
    location = 'Init/' + name + '/'
    try:
        os.mkdir(location)
        print("Directory " , location,  " Created ")
    except FileExistsError:
        print("Directory " , location,  " already exists")
    saveFile(_menu, location, 'Menu.ini')
    saveFile(_ingredients, location, 'Ingredients.ini')
    saveFile(_pumps, location, 'Pumps.ini')

initializeMenu()

@app.route("/home")
@app.route("/")
def home():
    startSession()
    return redirect(url_for('setting'))

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

@app.route("/purchase/credits", methods=['GET', 'POST'])
def buyCredit():
    form = addCredits()
    if form.ID.data:
        generateAuth(form.adminID.data)
        if checkAuth:
            closeAuth()
            usersIN = open(users, 'r')
            usersOUT = open('Init/out.csv', 'w')
            for line in usersIN:
                if len(line) > 5:
                    ID, Credit, Name, Access = line.split(', ')
                    if form.ID.data == ID:
                        Credit = int(Credit) + form.credit.data
                    line = ID + ', ' + str(Credit) + ', ' + Name + ', ' + Access
                    usersOUT.write(line)
            usersIN.close()
            usersOUT.close()
            try:
                os.remove(users)
                os.rename('Init/out.csv', users)
            except PermissionError:
                print(users + 'is running in a higher process')
            flash((str(Credit) + "'s purchased"), 'success')
            return redirect(url_for('menu'))
    return render_template('credits.html', form=form)

@app.route("/missing")
def drinkMissing():
    return render_template('missing.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = newUser()
    if form.ID.data:
        generateAuth(form.adminID.data)
        if checkAuth:
            closeAuth()
            usersIN = open(users, 'r')
            exists = False
            for line in usersIN:
                if len(line) > 5:
                    ID, Credit, Name, Access = line.split(', ')
                    if ID == form.ID.data:
                        exists = True
            usersIN.close()
            if exists == False:
                usersIN = open(users, 'a')
                line = form.ID.data + ', ' + str(form.credit.data) + ', ' + form.name.data + ', User\n'
                usersIN.write(line)
                usersIN.close()
                flash((form.ID.data + ' registered successfully'), 'success')
                return redirect(url_for('menu'))
            else:
                flash((form.ID.data + ' has already registered'), 'danger')
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = adminLogin()
    if form.ID.data:
        generateAuth(form.ID.data)
        if checkAuth():
            flash('logged in successfully', 'success')
            return redirect(url_for('setting'))
    return render_template('login.html', form=form, title='login')

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
    return render_template('settings.html', form=form, title='settings')

@app.route("/select/menu", methods=['GET', 'POST'])
def selectMenu():
    menusIN = open(menus, 'r')
    list = []
    for line in menusIN:
        line = line.strip('\n')
        list.append(line)
    return render_template('select-menu.html', list=list, title='settings')

@app.route("/select/menu/<menuName>", methods=['GET', 'POST'])
def initMenu(menuName):
    initializeMenu(menuName)
    return redirect(url_for('menu'))

@app.route("/upload/menu", methods=['GET', 'POST'])
def newMenu():
    form = uploadMenu()
    if form.confirm.data:
        absFilePath = form.location.data
        if absFilePath[-1] != '/':
            absFilePath = absFilePath + '/'
        menu = absFilePath + 'Menu.ini'
        ingredients = absFilePath + 'Ingredients.ini'
        pumps = absFilePath + 'Pumps.ini'
        saveMenu(menu, ingredients, pumps, form.name.data)
        return redirect(url_for('selectMenu'))
    return render_template('upload-menu.html', form=form, title='settings')

if __name__ == '__main__':
    app.run(debug=True)
