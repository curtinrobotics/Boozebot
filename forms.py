from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, MultipleFileField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

#TODO: custom drink form, select menu form

class uploadMenu(FlaskForm):
    name = StringField('Menu Name', validators=[DataRequired(), Length(min=2, max=30)])
    menu = MultipleFileField('Menu', validators=[FileAllowed(['ini'])])
    ingredients = MultipleFileField('Ingredients', validators=[FileAllowed(['ini'])])
    pumps = MultipleFileField('Pumps', validators=[FileAllowed(['ini'])])
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
    Credit = IntegerField('Credit', validators=[DataRequired()])
    submit = SubmitField('Add Credits')

class register(FlaskForm):
    ID = StringField('Student ID', validators=[DataRequired(), Length(min=2, max=30)])
    adminID = StringField('Admin ID', validators=[DataRequired(), Length(min=2, max=30)])
    Credit = IntegerField('Credit', validators=[DataRequired()])
    submit = SubmitField('Add Credits')
