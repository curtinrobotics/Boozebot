#This program defines the Drink class for the booze bot
#Programmers: TRG
#Iteration: 0.4
#Last edited: 10/04/2019
#Created: 10/04/2019

#imports the relevant libraries
import Data #imports the data file
import time #imports the time library

def new(name, cupSize, percentage, ingredients):
    Data.menu[name] = Drink()  # creates a new drink instant with name name

    # converts cupSize to an integer value
    if cupSize in Data.cupTypes:
        cupSize = Data.cupTypes[cupSize]
    else:
        cupSize = int(cupSize)

    Data.menu[name].CupSize = cupSize
    Data.menu[name].MaxFillPercent = percentage

    # creates recipe
    for ingredient in ingredients:
        if ingredient in Data.ingredientList:
            Data.menu[name].setRecipeRatio(ingredient, int(ingredients[ingredient]))
            Data.menu[name].SetDrinkIngredients(ingredient)
        else:  # catches unavailable ingredients
            print('Fatal Error: Missing ingredient. ' + ingredient + ' not available in IngredientList. Exiting program')
            time.sleep(5)  # sleeps for 5 seconds for readability
            return 1
    return 0

#the drink class
class Drink:
    #initializes drink variables
    def __init__(self):
        #class variables
        self.cupSize = 475 #the size of the cup(ml). Default value is 475, it can be changed to match the drink when an instance is created.
        self.maxFillPercent = 90 #how much of the cup to fill. Default value is 90%, it can be changed to match the drink when an instance is created.
        self.drinkIngredients = [] #list of ingredient in drink
        self.recipeRatio = {} #key: ingredient name, value: ratio of ingredient
        self.recipeVolume = {} #key: ingredient name, value: volume of ingredient(ml)
        self.recipeInstructions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #RecipeVolume in an instruction set for the arduino. Default value is 0. key: pump number, value: pump run time

    #appends to the drink ingredient list
    def setDrinkIngredients(self, ingredient):
        self.drinkIngredients.append(ingredient)
        return 0

    #sets the ingredient ratio
    def setRecipeRatio(self, ingredient, ratio):
        self.recipeRatio[ingredient] = ratio
        return 0

    #returns thse volume of 1 part
    def partVolume(self):
        total = 0
        for ingredient in self.drinkIngredients:
            total += self.recipeRatio[ingredient]
        maxFill = (self.maxFillPercent / 100) * self.cupSize
        part = maxFill/total
        return part

    #converts an Ingredient from RecipeRatio to from a ratio to a Volume(ml), currently doesn't work
    def ingredientVolume(self, ingredient):
        volume = self.recipeRatio[ingredient] * self.partVolume()
        return volume

    #converts RecipeRatio to RecipeVolume and assigns it
    def setRecipeVolume(self):
        for ingredient in self.drinkIngredients:
            self.recipeVolume[ingredient] = self.recipeRatio[ingredient] * self.partVolume()
        return 0

    #converts Recipevolume to Recipe RecipeInstructions and assigns it
    def setRecipeInstructions(self):
        for ingredient in self.drinkIngredients:
            pump = Data.ingredientPump[ingredient]
            self.recipeInstructions[pump] = self.recipeVolume[ingredient] / Data.MLperS
        return 0

    #gets the amount of standard drinks
    def getStndDrink(self):
        alcoholContent = 0
        for ingredient in self.drinkIngredients:
            alcoholContent += self.recipeRatio[ingredient] * self.partVolume() * (Data.ingredientAlcohol[ingredient] / 100)
        drinks = alcoholContent / Data.stndDrink
        return drinks
