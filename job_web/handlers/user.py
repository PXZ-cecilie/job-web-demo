#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from ..forms import UserDetailForm, RegisterUserForm, ArticleForm, AddTagForm
from ..models import Delivery,Article,db,Favorites,Vote

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('front.index'))
    form = RegisterUserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('sign up successful, please login', 'success')
        return redirect(url_for('front.login'))
    return render_template('user/register.html', form=form, active='user_register')


@user.route('/account', methods=['GET', 'POST'])
@login_required
def edit():
    if not current_user.is_user():
        return redirect(url_for("front.index"))
    form = UserDetailForm(obj=current_user)
    if form.validate_on_submit():
        form.update_detail(current_user)
        flash('personal information has been updated', 'success')
        return redirect(url_for('user.edit'))
    return render_template('user/edit.html', form=form, active='manage', panel='edit')

'''
@user.route('/resume', methods=['GET', 'POST'])
@login_required
def resume():
    if not current_user.is_user():
        return redirect(url_for("front.index"))
    form = UserProfileForm()
    resume_url = current_user.resume
    if form.validate_on_submit():
        resume_url = form.upload_resume(current_user)
    return render_template('user/resume.html', form=form, file_url=resume_url, active='manage', panel='resume')
'''

@user.route('/delivery')
@login_required
def delivery():
    if not current_user.is_user():
        return redirect(url_for("front.index"))
    status = request.args.get('status', None)
    page = request.args.get('page', default=1, type=int)
    if status:
        pagination = current_user.delivery.filter_by(status=status).order_by(Delivery.updated_at.desc()).paginate(
            page=page, per_page=current_app.config['LIST_PER_PAGE'], error_out=False)
    else:
        pagination = current_user.delivery.order_by(Delivery.updated_at.desc()).paginate(
            page=page, per_page=current_app.config['LIST_PER_PAGE'], error_out=False)
    return render_template('user/delivery.html', pagination=pagination,
                           active='manage', panel='delivery', status=status)

@user.route('/publish',methods=['GET', 'POST'])
@login_required
def publish():
    if not current_user.is_user():
        return redirect(url_for("front.index"))
    form = ArticleForm()
    if form.validate_on_submit():
        form.publish_article()
        flash('content has been submitted', 'success')
        return redirect(url_for('front.index'))
    return render_template('user/publish.html',form=form,panel='edit')

@user.route('/browse',methods=['GET', 'POST'])
@login_required
def browse():
    page = 1
    if not current_user.is_user():
        return redirect(url_for("front.index"))
    pagination = Article.query.order_by(
            Article.created_at.desc()).paginate(
        page=page, per_page=100, error_out=False)
    #print(("pagination",len(pagination)))
    return render_template('user/read_content.html',pagination=pagination)

@user.route('<int:article_id>/favorite',methods=['GET', 'POST'])
@login_required
def favorite(article_id):
    if not current_user.is_user():
        return redirect(url_for("front.index"))
    article_cur = Article.query.get(article_id)
    is_faved = Favorites.query.filter(Favorites.user_id == current_user.id,Favorites.article_id == article_id).all()
    # print(is_faved)
    if len(is_faved) > 0:
        flash('you have favorited this content before','warning')
    else:
        article_cur.fav_count += 1
        article_cur.rating += 10
        db.session.commit()
        fav1 = Favorites(article_id = article_id,user_id=current_user.id)
        db.session.add(fav1)
        db.session.commit()
    return browse()

@user.route('<int:article_id>/promote',methods=['GET', 'POST'])
@login_required
def promote(article_id):
    if not current_user.is_user():
        return redirect(url_for("front.index"))
    article_cur = Article.query.get(article_id)
    is_promoted = Vote.query.filter(Vote.user_id == current_user.id,Vote.article_id == article_id).all()
    # print(is_faved)
    if len(is_promoted) > 0:
        flash('you have promoted this content before','warning')
    else:
        article_cur.vote_count += 1
        article_cur.rating += 5
        db.session.commit()
        vote1 = Vote(article_id = article_id,user_id=current_user.id)
        db.session.add(vote1)
        db.session.commit()
    return browse()

@user.route('<int:article_id>/add_tag',methods=['GET', 'POST'])
@login_required
def add_tag(article_id):
    if not current_user.is_user():
        return redirect(url_for("front.index"))
    article_cur = Article.query.get(article_id)
    if current_user.id == article_cur.author:
        flash('you cannot tag your own content','warning')
        return browse()
    else:
        form = AddTagForm()
        if form.validate_on_submit():
            form.update_tag(article_id)
            flash('content has been submitted', 'success')
        dic = {}
        dic['id'] = article_id
    return render_template('user/add_tag.html',form=form,panel='edit',id=article_id)


@user.errorhandler(413)
def page_not_found(error):
    flash('文件大小超过限制', 'warning')
    return redirect(request.path)
