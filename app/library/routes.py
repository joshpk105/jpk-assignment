from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_required, current_user
from app import db
from app.library import bp
from app.library.forms import NewBookForm
from app.models import Book, Author, Ownership, Authorship

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_book():
    form = NewBookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data)
        db.session.add(book)
        db.session.flush()
        authors_db = []
        for a in form.authors:
            if len(a.data) != 0:
                authors_db.append(Author(name=a.data))
                db.session.add(authors_db[-1])
        db.session.flush()
        db.session.refresh(book)
        map(db.session.refresh, authors_db)
        for a in authors_db:
            db.session.refresh(a)
            authorship = Authorship(author_id=a.id, book_id=book.id)
            db.session.add(authorship)
        db.session.commit()
        return redirect(url_for("library.view"))
    return render_template("library/add.html", title="Add Book", form=form)

@bp.route("/view", methods=["GET"])
@login_required
def view():
    rows = db.session.query(Book, Authorship, Author).filter(Book.id == Authorship.book_id).filter(Authorship.author_id == Author.id).all()
    library = {}
    for r in rows:
        if r[0].id not in library:
            library[r[0].id] = {"title": r[0].title, "authors": r[2].name}
        else:
            library[r[0].id]["authors"] += (", " + r[2].name)
    #library = Book.query.join(Authorship.book_id).join(Author.id)
    print(library)
    return render_template("library/view.html", books=library)
    


