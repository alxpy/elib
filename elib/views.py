import json

from flask import render_template, flash, redirect, session, url_for, jsonify

from . import app
from .database import db_session
from .forms import LoginForm, RegistrationForm, SearchForm
from .models import Book, Author, User


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    form_s = SearchForm()
    return render_template('index.html', form=form, form_s=form_s)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_session.query(User).filter_by(username=form.username.data).first()
        if not user:
            return json.dumps({'message': 'Неверный логин или пароль!'})
        elif not user.check_password(form.password.data):
            return json.dumps({'message': 'Неверный логин или пароль!'})
        else:
            session['logged_in'] = True
            return json.dumps({'message': 'Вы удачно вошли!', 'success': True})

        return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password_one.data)
        db_session.add(user)
        try:
            db_session.commit()
            return 'Удачная регистрация'
        except:
            return 'Не смогли зарегистрировать пользователя. Скорее всего, уже есть пользователь с таким именем!'
    return render_template('registration.html', form=form)


@app.route('/books')
def books():
    books = db_session.query(Book).all()
    return render_template('books.html', books=books)


@app.route('/book/<book_id>')
def book(book_id):
    book = db_session.query(Book).get(book_id)
    return render_template('book.html', book=book)


@app.route('/authors')
def authors():
    #authors = db_session.query(Author).all()
    #authors = db_session.query(Author).filter(Author.book.any(title="Книга 1"))

    #book = db_session.query(Book).filter()

    #authors = db_session.query(Author).filter(Author.book.any(title=book[1].title))
    authors = db_session.query(Author).all()

    return render_template('authors.html', authors=authors)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()