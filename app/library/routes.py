from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_required, current_user
from app import db
from app.library import bp
from app.library.forms import NewBookForm
from app.models import Book, Author, Ownership

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_book():
    form = NewBookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("library.view"))
    return render_template("library/add.html", title="Add Book", form=form)

@bp.route("/view", methods=["GET"])
@login_required
def view():
    books = Book.query.all()
    return render_template("library/view.html", books=books)
    


