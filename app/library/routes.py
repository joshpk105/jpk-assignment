from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.library import bp
from app.library.forms import NewBookForm, SendLibraryForm, EditBookForm
from app.models import Book, Author, Ownership, Authorship
from app.email import send_email
from urllib.parse import urlparse, urlunparse, urlencode, unquote

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

# Query to collect a users library
# return - All library rows
def library_query():
    # Replace with a view
    rows = db.session.query(Ownership, Book, Authorship, Author)\
        .where(Ownership.user_id==current_user.id)\
        .filter(Ownership.book_id==Book.id)\
        .filter(Book.id == Authorship.book_id)\
        .filter(Authorship.author_id == Author.id).all()
    return rows

# Build the edit link with the ownership id
def build_edit_link(base, owner):
    q = {"own": owner}
    edit = base._replace(query=urlencode(q))
    return '<a href="{}">Edit</a>'.format(urlunparse(edit))

@bp.route("/view", methods=["GET","POST"])
@login_required
def view():
    form = SendLibraryForm()
    library = {}
    edit_url = urlparse(request.base_url)
    edit_url = edit_url._replace(path=url_for("library.edit"))
    for r in library_query():
        if r[0].id not in library:
            library[r[0].book_id] = {"title": r[1].title, 
                "authors": r[3].name, "note": r[0].note, 
                "purchase": r[0].purchase_date,
                "edit": build_edit_link(edit_url, r[0].id)}
        else:
            library[r[0].book_id]["authors"] += (", " + r[3].name)
    if form.validate_on_submit():
        send_email("Shared Library", form.recipient.data, str(library), "")
        form.recipient.data = ""
        flash("Email sent")
    return render_template("library/view.html", books=library, form=form)
    
# Query to edit an entry, must be in author id order to
# reflect user changes.
# own_id - The Ownership.id used to find edit materials
# return - All found rows related to own_id
def edit_query(own_id):
    return db.session.query(Ownership, Book, Authorship, Author)\
        .where(Ownership.id==own_id)\
        .where(Ownership.user_id==current_user.id)\
        .filter(Ownership.book_id==Book.id)\
        .filter(Book.id == Authorship.book_id)\
        .filter(Authorship.author_id == Author.id)\
        .order_by(Author.id).all()

# Ideally this would be simply handled by the database
# but I couldn't quickly determine the necessary syntax for
# SQLAlchemy.
def delete_book_tree(form, rows):
    for row in rows:
        for t in row:
            db.session.delete(t)
    db.session.commit()

# Update authors based on form contents
# form - the form object providing new data
# rows - the current database objects to update
def db_update_authors(form, rows):
    book = rows[0][1]
    new_authors = []
    for i, author in enumerate(form.authors):
        # Add new author
        if i > len(rows) and author.data != "":
            new_authors.append(Author(name = author.data))
            db.session.add(new_authors[-1])
        # Delete author
        elif i < len(rows) and author.data == "":
            db.session.delete(rows[i][2])
            # Annoying hack since deletes not setup nicely
            db.session.flush()
            db.session.delete(rows[i][3])
        # Update author
        elif i < len(rows) and rows[i][3].name != author.data:
            rows[i][3].name = author.data
    # Add Authorship for new authors
    for author in new_authors:
        db.session.refresh(author)
        a = Authorship(book_id=book.id, author_id=author.id)
        db.session.add(a)


# Update the DB based on user changes
# form - the EditBookForm with changes
# rows - the current row data to change
def merge_db_changes(form, rows):
    ownership = rows[0][0]
    book = rows[0][1]
    # Delete all entries, this may be overkill
    if len(form.title.data) == 0:
        delete_book_tree(form, rows)
        return
    # Update title, purcahse, and note
    if form.title.data != book.title:
        book.title = form.title.data
    if form.purchase.data != ownership.purchase_date:
        ownership.purchase_date = form.purchase.data
    if form.note.data != ownership.note:
        ownership.note = form.note.data

    # Update authors
    db_update_authors(form, rows)
    db.session.commit()

@bp.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditBookForm()
    own_id = unquote(request.args['own'])
    rows = edit_query(own_id)
    if len(rows) == 0:
        print("Ownership not found: ", own_id)
        return redirect(url_for("library.view"))
    
    if form.validate_on_submit():
        merge_db_changes(form, rows)
        return redirect(url_for("library.view"))
    form.title.data = rows[0][1].title
    form.purchase.data = rows[0][0].purchase_date
    form.note.data = rows[0][0].note
    for i, row in enumerate(rows):
        form.authors[i].data = row[3].name
    return render_template("library/add.html", title="Edit Book", form=form)
