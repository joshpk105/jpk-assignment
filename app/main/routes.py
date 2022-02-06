from app import db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.main import bp

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')
