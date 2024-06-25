from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email
from app.constants import PROBLEM_TYPES, DAMAGE_TYPES

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirmation = PasswordField('Confirme a Senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class ReportForm(FlaskForm):
    description = SelectField('Descrição', choices=[(p, p) for p in PROBLEM_TYPES], validators=[DataRequired()])
    latitude = HiddenField('Latitude', validators=[DataRequired()])
    longitude = HiddenField('Longitude', validators=[DataRequired()])
    damage_type = SelectField('Tipo de Dano', choices=[(d, d) for d in DAMAGE_TYPES], validators=[DataRequired()])
    submit = SubmitField('Enviar')

class CSRFForm(FlaskForm):
    pass




    
