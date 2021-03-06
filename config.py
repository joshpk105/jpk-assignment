import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER="smtp.googlemail.com"
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME="developer.joshpk@gmail.com"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_FROM="no-reply@bookshare.com"