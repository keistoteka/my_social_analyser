from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('El. pašto adresas', validators=[DataRequired(), Email()])
    password = PasswordField('Slaptažodis', validators=[DataRequired()])
    remember = BooleanField('Prisiminti mane')
    submit = SubmitField('Prisijungti')

class RegistrationForm(FlaskForm):
    username = StringField('Vartotojo vardas', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('El. pašto adresas', validators=[DataRequired(), Email()])
    password = PasswordField('Slaptažodis', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Patvirtinkite slaptažodį', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registruotis')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Dabartinis slaptažodis', validators=[DataRequired()])
    new_password = PasswordField('Naujas slaptažodis', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Patvirtinkite naują slaptažodį', 
        validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Atnaujinti slaptažodį') 