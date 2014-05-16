import json

from flask import render_template, flash, redirect, session, url_for, request

from . import app
from .database import db_session
from .forms import LoginForm, RegistrationForm, BookForm, AuthorForm, SearchForm
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


@app.route('/authors')
def authors():
    authors = db_session.query(Author).all()
    return render_template('authors.html', authors=authors)


@app.route('/book/<book_id>', methods=['GET', 'POST'])
def book(book_id):
    book = db_session.query(Book).get(book_id)
    form = BookForm(
        title = book.title,
        abstract = book.abstract,
    )

    if form.validate_on_submit():
        book.title = form.title.data
        book.abstract =form.abstract.data
        db_session.add(book)
        db_session.commit()

    return render_template('book.html', book=book, form=form)


@app.route('/author/<author_id>', methods=['GET', 'POST'])
def author(author_id):
    author = db_session.query(Author).get(author_id)
    form = AuthorForm(
        name = author.name,
        biography = author.biography,
    )

    if form.validate_on_submit():
        author.name = form.name.data
        author.biography =form.biography.data
        db_session.add(author)
        db_session.commit()

    return render_template('author.html', author=author, form=form)


@app.route('/del/book/<book_id>')
def del_book(book_id):
    book = db_session.query(Book).get(book_id)
    db_session.delete(book)
    db_session.commit()
    return redirect(url_for('books'))


@app.route('/del/author/<author_id>')
def del_author(author_id):
    author = db_session.query(Author).get(author_id)
    db_session.delete(author)
    db_session.commit()
    return redirect(url_for('authors'))


@app.route('/new/book/', methods=['GET', 'POST'])
def new_book():
    form = BookForm()
    authors = db_session.query(Author).all()

    if form.validate_on_submit():
        book = Book(
            form.title.data,
            form.abstract.data,
        )

        ids = request.form.getlist('authors')
        book.authors = db_session.query(Author).filter(Author.id.in_(ids)).all()

        db_session.add(book)
        db_session.commit()

        return redirect(url_for('books'))
    return render_template('new_book.html', form=form, authors=authors)


@app.route('/new/author/', methods=['GET', 'POST'])
def new_author():
    form = AuthorForm()
    books = db_session.query(Book).all()

    if form.validate_on_submit():
        author = Author(
            form.name.data,
            form.biography.data,
        )

        ids = request.form.getlist('books')
        author.books = db_session.query(Book).filter(Book.id.in_(ids)).all()

        db_session.add(author)
        db_session.commit()

        return redirect(url_for('authors'))
    return render_template('new_author.html', form=form, books=books)


@app.route('/search', methods=['GET', 'POST'])
def search(exception=None):
    form = SearchForm()
    if form.validate_on_submit():
        response = []

        query = form.query.data
        books = db_session.query(Book).filter(Book.title.like(query)).all()
        authors = db_session.query(Author).filter(Author.name.like(query)).all()

        if (not books) and (not authors):
            return json.dumps({'message': 'Ничего не найдено!', 'success': False})

        result = ''
        for author in authors:
            result += '<tr><td>Писатель: <a href="/author/{}">{}</a></td></tr>'.format(author.id, author.name)
        for book in books:
            result += '<tr><td>Книга: <a href="/book/{}">{}</a></td></tr>'.format(book.id, book.title)

        return json.dumps({'message': result, 'success': True})

    return render_template('search.html', form=form)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()