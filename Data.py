#This program holds data sets relevant to boozebot
#Programmers: TRG
#Iteration: 0.1
#Last edited: 07/04/2019
#Created: 10/04/2019

#Constants:
MLperS = 1 #ml per second of the pump
StndDrink = 21 #ml alcohol in a standard drink

#Updateable:
IngredientAlcohol = {'orange juice': 0, 'tequila': 40, 'vodka': 40, 'lemonade': 0, 'milk': 0} #key: ingredient name, value: percentage alchohol
CupType = {'shot glass': 44, 'wine glass': 415, 'UK pint': 568, 'US pint': 473, 'martini glass': 200} #key: Cup type, value: volume in cup(ml)

#Initialized:
IngredientPump = {} #key: ingredient name, value: pump number
Menu = {} #list of drinks
IngredientList = [] #List of Ingredients
