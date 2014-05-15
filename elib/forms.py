from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = TextField('Логин', validators=[DataRequired()])
    password = TextField('Пароль', validators=[DataRequired()])


class RegistrationForm(Form):
    username = TextField('Логин', validators=[DataRequired()])
    password_one = TextField('Пароль', validators=[DataRequired()])
    password_two = TextField('Пароль еще раз', validators=[DataRequired()])
        

class SearchForm(Form):
    query = TextField('Поиск', validators=[DataRequired()])

    #def __init__(self):
    #   self.query = 'arg'