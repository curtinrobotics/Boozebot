import functools
import Data

from flask import Blueprint, render_template, session

bp = Blueprint('menu', __name__, url_prefix='/menu')


@bp.route('/')
def menu():
    return render_template('menu.html', menu=Data.menu, title='Menu')


@bp.route("/<drinkName>", methods=['GET', 'POST'])
def drink(drinkName):
    drinkExists = False
    if session['OpenBar'] == True:
        form = confirmOrder()
    else:
        drink_dict = {
            "drink_name": drinkName
        }
        return render_template('card-order.html', drink_dict=drink_dict)

    #
    # if form.confirm.data:
    #     is_drunk = Database.is_drunk(form.ID.data)
    #
    #     for drink in Data.menu:
    #         if Data.menu[drink].name == drinkName:
    #
    #             if is_drunk and Data.menu[drink].getStndDrink() != 0.0:
    #                 return redirect(url_for('drunk'))
    #
    #             drinkExists = True
    #             if session['OpenBar'] == True:
    #                 submitDrink(-1, drink)
    #             else:
    #                 purchaseDrink(form.ID.data, drink)
    #             return redirect(url_for('menu'))
    # for drink in Data.menu:
    #     if Data.menu[drink].name == drinkName:
    #         drinkExists = True
    #         return render_template('confirm.html', drink=Data.menu[drink], form=form)
    # if drinkExists == False:
    #     return redirect(url_for('drinkMissing'))
    # return render_template('menu.html', menu=Data.menu)
