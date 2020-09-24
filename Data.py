#This program holds data sets relevant to boozebot
#Programmers: TRG
#Iteration: 0.1
#Last edited: 07/04/2019
#Created: 10/04/2019

#Constants:
ParastalticNum = 4
SolenoidNum = 4
ParastalticMLperS = 1 #ml per second of the pump
SolenoidMLperS = 10 #ml per second of the pump
stndDrink = 21 #ml alcohol in a standard drink

#Updateable:
ingredientAlcohol = {'orange juice': 0, 'tequila': 40, 'vodka': 40, 'lemonade': 0, 'milk': 0} #key: ingredient name, value: percentage alchohol
cupTypes = {'shot glass': 44, 'wine glass': 415, 'UK pint': 568, 'US pint': 473, 'martini glass': 200} #key: Cup type, value: volume in cup(ml)

#Initialized:
ingredientPump = {} #key: ingredient name, value: pump number
menu = {} #list of drinks
ingredientList = [] #List of Ingredients
