from app import flapp, db
from app.models import User, Book, Author, Ownership

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Book': Book, 'Author': Author, 'Ownership': Ownership}