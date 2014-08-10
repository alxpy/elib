from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = TextField('Логин', validators=[DataRequired()])
    password = TextField('Пароль', validators=[DataRequired()])


class RegistrationForm(Form):
    username = TextField('Логин', validators=[DataRequired()])
    password_one = TextField('Пароль', validators=[DataRequired()])
    password_two = TextField('Пароль еще раз', validators=[DataRequired()])


class BookForm(Form):
    title = TextField('Название', validators=[DataRequired()])
    abstract = TextAreaField('Аннотация', validators=[DataRequired()])


class AuthorForm(Form):
    name = TextField('Имя', validators=[DataRequired()])
    biography = TextAreaField('Биография', validators=[DataRequired()])


class SearchForm(Form):
    query = TextField('Поиск', validators=[DataRequired()])
