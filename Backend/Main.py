# This program is the main program for boozebot and integrates all other programs
# Programmers: TRG, LMB, AT
# Iteration: 0.5
# Last edited: 05/04/2019
# Created: 10/04/2019

# imports relevate libraries
import Data  # imports the data file
import Update  # imports the Dataupdate function set
import Arduino  # imports Arduino communication library
import Database

# threading
import threading
from queue import Queue
import VirtualQueue

# flask
from PIL import Image
from forms import uploadMenu, adminSettings, confirmOrder, adminLogin, addCredits, \
     newUser, buyDrink, customDrink
from flask import Flask, render_template, url_for, flash, redirect, session, make_response

# Blueprints
from views import menu

import os

is_scanning = None

app = Flask(__name__, template_folder="templates", static_url_path="/templates", \
            static_folder="templates")
app.register_blueprint(menu.bp)

app.config['SECRET_KEY'] = '5791628bb0b13ceh98dfjk7lp76dfde280ba245'

users = "Init/Users.csv"
menus = "Init/Menu.csv"
drinkQueue = Queue()


# Updates all data from files
def initializeMenu(InitFile="Standard"):
    """
    Initialises the menu
    """
    # updates the cup volume list
    Update.updateCupType('Init/Cups.ini')
    # updates the alcholic content of ingredients list
    Update.updateIngredientAlcohol('Init/AlcoholContent.ini')
    # updates the ingredient pumps
    Update.updateIngredientPump('Init/' + InitFile + '/Pumps.ini')
    # updates a list of available ingredients
    Update.updateIngredientList('Init/' + InitFile + '/Ingredients.ini')
    # updates the menu and recipe instructions
    Update.updateMenu('Init/' + InitFile + '/Menu.ini')


def startSession():
    """
    Sets up run once functions for the python/flask backend
    Currently sets up cookies and initialises menu
    """
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
    """
    Delete Auth cookie to logout user
    """
    session.pop('Auth')


def generateAuth(_ID):
    """
    Check for valid ID and generates login cookie
    """
    print("genAuth", _ID)
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
    """
    Check for login cookie
    """
    return session.get('Auth')


def purchaseDrink(_ID, drink):
    """
    Lets the user purchase a drink
    Look up the user ID on the database to check for credit
    """
    usersIN = open(users, 'r')
    usersOUT = open('Init/out.csv', 'w')
    for line in usersIN:
        if len(line) > 5:
            ID, Credit, Name, Access = line.split(', ')
            if _ID == ID:
                if session['AdminOveride'] == True and Access == 'Admin':
                    submitDrink(_ID, drink)
                elif int(Credit) > 0:
                    Credit = int(Credit) - 1
                    line = ID + ', ' + str(Credit) + ', ' + Name + ', ' + Access + '\n'
                    submitDrink(_ID, drink)
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


def submitDrink(id, drink='NULL'):
    """
    Sends the drink instructions to the Booze Bot to serve
    """
    print(drink)
    Data.menu[drink].setRecipeVolume()
    # Fixme — Recipe needs implementation
    # Data.menu[drink].setRecipeInstructions()
    print(Data.menu[drink].getStndDrink())
    ArduinoQueue.queue.put(Data.menu[drink].recipeInstructions)

    if id != -1:
        Database.log_drink(id, Data.menu[drink].getStndDrink())


def saveFile(file, location, name='NULL'):
    """
    Copies file to a location
    """
    try:
        os.mkdir(location)
        print("Directory ", location, " Created ")
    except FileExistsError:
        print("Directory ", location, " already exists")
    if name == 'NULL':
        name = file
    fileIN = open(file, 'r')
    fileOUT = open(location + name, 'w')
    for line in fileIN:
        fileOUT.write(line)
    fileIN.close()
    fileOUT.close()


def saveMenu(_menu, _ingredients, _pumps, name):
    """
    Saves current menu to file
    """
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
        print("Directory ", location, " Created ")
    except FileExistsError:
        print("Directory ", location, " already exists")
    saveFile(_menu, location, 'Menu.ini')
    saveFile(_ingredients, location, 'Ingredients.ini')
    saveFile(_pumps, location, 'Pumps.ini')


@app.route("/home")
@app.route("/")
def home():
    """
    Homepage
    """
    startSession()
    return redirect(url_for('setting'))


@app.route("/card_order_drink/<drinkName>")
def card_order_drink(drinkName):
    """
    Page to order drinks
    """
    print(drinkName)
    # Get the scanned ID from the Arduino
    thread = threading.Thread(target=card_scan_background)
    # scanned_id = Arduino.getID()
    thread.start()
    return redirect(url_for('timeout'))

    # If the ID is empty, an invalid ID was scanned or the read timed out
    # if scanned_id == "":
    #     # Redirect to timeout page
    #     return redirect(url_for('timeout'))
    #
    # print(f"Scanned ID: {scanned_id}")
    #
    # drinkExists = False
    #
    # is_drunk = Database.is_drunk(scanned_id)
    #
    # for drink in Data.menu:
    #     if Data.menu[drink].name == drinkName:
    #
    #         if is_drunk and Data.menu[drink].getStndDrink() != 0.0:
    #             return redirect(url_for('drunk'))
    #
    #         drinkExists = True
    #         if session['OpenBar'] == True:
    #             submitDrink(-1, drink)
    #         else:
    #             purchaseDrink(scanned_id, drink)
    #         return redirect(url_for('menu'))
    # if drinkExists == False:
    #     return redirect(url_for('drinkMissing'))


def card_scan_background():
    scanned_id = Arduino.getID()
    print("Scanned card:", scanned_id)
    print(scanned_id, file=open('scanned_card.txt', 'w'))


@app.route("/card_status")
def card_status():
    with open('scanned_card.txt', 'r') as file:
        return file.read()


@app.route("/drunk")
def drunk():
    """
    Inform user they had too many standard drinks
    """
    return render_template('drunk.html')


@app.route("/purchase/credits", methods=['GET', 'POST'])
def buyCredit():
    """
    Add credit to their account
    """
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
    """
    Missing drink error page
    """
    return render_template('missing.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register new users
    """
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
                line = form.ID.data + ', ' + str(form.credit.data) + ', ' + \
                       form.name.data + ', User\n'
                usersIN.write(line)
                usersIN.close()
                flash((form.ID.data + ' registered successfully'), 'success')
                return redirect(url_for('menu'))
            else:
                flash((form.ID.data + ' has already registered'), 'danger')
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Standard login
    """
    form = adminLogin()

    return render_template('login.html', form=form, title='login')


@app.route("/card_login")
def card_login():
    """
    Card scanning page
    """
    # Get the scanned ID from the Arduino
    scanned_id = Arduino.getID()

    # If the ID is empty, an invalid ID was scanned or the read timed out
    if scanned_id == "":
        # Redirect to timeout page
        return redirect(url_for('timeout'))

    # Generate credentials for scanned ID and redirect to settings page
    generateAuth(scanned_id)
    return redirect(url_for('setting'))


@app.route("/timeout", methods=['GET', 'POST'])
def timeout():
    """
    Manual login page, shown when card scanner is disconnected or has timed out
    """
    form = adminLogin()

    if form.ID:
        print("Got form ID")
        print("ID", form.ID.data)
        generateAuth(form.ID.data)
        if checkAuth():
            flash('logged in successfully', 'success')
            return redirect(url_for('setting'))

    return render_template('timeout.html', form=form, title='login')


@app.route("/logout")
def logout():
    """
    Logout endpoint
    """
    closeAuth()
    return redirect(url_for('menu'))


@app.route("/settings", methods=['GET', 'POST'])
def setting():
    """
    Settings form
    """
    form = adminSettings()
    if checkAuth() == True:
        # SETTINGS
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
    """
    Shows the the list of available menus to select
    """
    menusIN = open(menus, 'r')
    list = []
    for line in menusIN:
        line = line.strip('\n')
        list.append(line)
    return render_template('select-menu.html', list=list, title='settings')


@app.route("/select/menu/<menuName>", methods=['GET', 'POST'])
def initMenu(menuName):
    """
    Selects a menu as the current menu
    """
    initializeMenu(menuName)
    return redirect(url_for('menu'))


@app.route("/upload/menu", methods=['GET', 'POST'])
def newMenu():
    """
    Form for creating a new menu
    """
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
    initializeMenu()
    ArduinoQueue = VirtualQueue.ArduinoThread(drinkQueue)
    ArduinoQueue.start()
    app.run(debug=True, threaded=True)
