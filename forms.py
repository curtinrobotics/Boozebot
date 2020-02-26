from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

#TODO: custom drink form, select menu form

class uploadMenu(FlaskForm):
    name = StringField('Menu Name', validators=[DataRequired(), Length(min=2, max=30)])
    menu = FileField('Menu', validators=[FileAllowed(['ini', 'txt'])])
    ingredients = FileField('Ingredients', validators=[FileAllowed(['ini', 'txt'])])
    pumps = FileField('Pumps', validators=[FileAllowed(['ini', 'txt'])])
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
    Credit = IntegerField('Credit', validators=[DataRequired()])
    submit = SubmitField('Add Credits')

class register(FlaskForm):
    ID = StringField('Student ID', validators=[DataRequired(), Length(min=2, max=30)])
    adminID = StringField('Admin ID', validators=[DataRequired(), Length(min=2, max=30)])
    Credit = IntegerField('Credit', validators=[DataRequired()])
    submit = SubmitField('Add Credits')
