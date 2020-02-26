from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, FileField, FormField, FieldList
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

#TODO: custom drink form, registration form implement, buy credits form implement

#filefield doesn't work
#class uploadMenu(Form):
#    name = StringField('Menu Name', validators=[DataRequired(), Length(min=2, max=30)])
#    menu = FileField('Menu', validators=[DataRequired(), FileAllowed(['ini'])])
#    ingredients = FileField('Ingredients', validators=[DataRequired(), FileAllowed(['ini'])])
#    pumps = FileField('Pumps', validators=[DataRequired(), FileAllowed(['ini'])])
#    confirm = BooleanField('Confirm Settings')
#    submit = SubmitField('Upload')

#custom drink
class ingredientSelect(FlaskForm):
    name = IntegerField()

class customDrink(FlaskForm):
    #A form for one or more addresses
    ingredients = FieldList(FormField(IngredientSelect), min_entries=1)
#custom drink

class uploadMenu(Form):
    name = StringField('Menu Name', validators=[DataRequired(), Length(min=2, max=30)])
    browse = FileField('Browse File system')
    location = StringField('Menu directory location', validators=[DataRequired(), Length(min=2)])
    confirm = BooleanField('Confirm Settings')
    submit = SubmitField('Upload')

class adminSettings(FlaskForm):
    openBar = BooleanField('Open Bar')
    custom = BooleanField('Custom Drinks')
    adminOveride = BooleanField('Free Drinks for Admin')
    confirm = BooleanField('Confirm Settings')
    submit = SubmitField('Continue')

class buyDrink(FlaskForm):
    ID = StringField('Student ID', validators=[DataRequired(), Length(min=2, max=30)])
    confirm = BooleanField('Confirm Order')
    submit = SubmitField('Continue')

class confirmOrder(FlaskForm):
    confirm = BooleanField('Confirm Order')
    submit = SubmitField('Continue')

class adminLogin(FlaskForm):
    ID = StringField('Student ID', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Login')

class addCredits(FlaskForm):
    ID = StringField('Student ID', validators=[DataRequired(), Length(min=2, max=30)])
    adminID = StringField('Admin ID', validators=[DataRequired(), Length(min=2, max=30)])
    credit = IntegerField('Credit', validators=[DataRequired()])
    submit = SubmitField('Add Credits')

class newUser(FlaskForm):
    ID = StringField('Student ID', validators=[DataRequired(), Length(min=2, max=30)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    adminID = StringField('Admin ID', validators=[DataRequired(), Length(min=2, max=30)])
    credit = IntegerField('Credit', validators=[DataRequired()])
    submit = SubmitField('Add Credits')
