from flask import Blueprint, render_template, \
    redirect, url_for, flash, request, current_app, abort
from flask_login import current_user
from ..models import User, Article, Publish, db

submit_content = Blueprint('submit_content', __name__, url_prefix='/submit_content')

@submit_content.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    form = RegisterCompanyForm()
    if form.validate_on_submit():
        form.publish_article()
        flash('submit success', 'success')
        return redirect(url_for('user.publish'))
    #return render_template('submit_content/index.html', pagination=pagination, kw=kw, active='company')
