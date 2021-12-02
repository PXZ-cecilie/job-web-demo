from flask import Blueprint, render_template, \
    redirect, url_for, flash, request, current_app, abort
from flask_login import current_user
from ..models import User, Article, Publish, db

read_content = Blueprint('read_content', __name__, url_prefix='/read_content')

@read_content.route('/')
def index():
    pagination = Article.query.all(order_by(
            Article.created_at.desc()).paginate(
                page=page,
                per_page=10,
                error_out=False
            )
    return render_template('read_content/index.html', pagination=pagination)
