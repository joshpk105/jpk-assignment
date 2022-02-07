from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_required, current_user
from app import db
from app.library import bp
from app.library.forms import NewBookForm, SendLibraryForm
from app.models import Book, Author, Ownership, Authorship
from app.email import send_email

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
        for a in authors_db:
            db.session.refresh(a)
            authorship = Authorship(author_id=a.id, book_id=book.id)
            db.session.add(authorship)
        owner = Ownership(user_id=current_user.id, 
            book_id=book.id, 
            note=form.note.data)
        if not form.purchase.data is None:
            owner.purchase_date = form.purchase.data
        db.session.add(owner)
        db.session.commit()
        return redirect(url_for("library.view"))
    return render_template("library/add.html", title="Add Book", form=form)

@bp.route("/view", methods=["GET","POST"])
@login_required
def view():
    form = SendLibraryForm()
    rows = db.session.query(Ownership, Book, Authorship, Author)\
        .filter(Ownership.book_id==Book.id)\
        .filter(Book.id == Authorship.book_id)\
        .filter(Authorship.author_id == Author.id)\
        .where(Ownership.user_id==current_user.id).all()
    library = {}
    for r in rows:
        if r[0].id not in library:
            library[r[0].book_id] = {"title": r[1].title, 
                "authors": r[3].name, "note": r[0].note, 
                "purchase": r[0].purchase_date}
        else:
            library[r[0].book_id]["authors"] += (", " + r[3].name)
    if form.validate_on_submit():
        send_email("Shared Library", form.recipient.data, str(library), "")
    return render_template("library/view.html", books=library, form=form)
    


