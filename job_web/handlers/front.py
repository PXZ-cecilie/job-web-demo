#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models import Job, User, Company, Article
from ..forms import LoginForm

front = Blueprint('front', __name__)


@front.route('/')
def index():
    company_all = Company.query.filter(Company.is_enable.is_(True)).order_by(Company.updated_at.desc())
    companies = []
    for c in company_all:
        if c and c.enabled_jobs().count() != 0:
            companies.append(c)
            if len(companies) == 8:
                break
    jobs = Job.query.group_by(Job.company_id).order_by(Job.updated_at.desc()).limit(12)
    return render_template('index.html', active='index', jobs=jobs, companies=companies)


@front.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('front.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_data = User.query.filter_by(email=form.email.data).first()
        if not user_data:
            user_data = Company.query.filter_by(email=form.email.data).first()
            if not user_data:
                flash('wrong information, login again', 'danger')
                return redirect(url_for('front.login'))
        if not user_data.check_password(form.password.data):
            flash('wrong information, login again', 'danger')
            return redirect(url_for('front.login'))
        if not user_data.is_enable:
            flash('wrong information, login again, please contact admin', 'danger')
            return redirect(url_for('front.login'))
        login_user(user_data, form.remember_me.data)
        flash('login successful', 'success')
        next_page = request.args.get('next')
        return redirect(next_page or url_for('front.index'))
    return render_template('login.html', form=form, active='login')


@front.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('you have logged out', 'success')
    return redirect(url_for('front.index'))


@front.route('/search',methods=['GET', 'POST'])
def search():
    
    # search_type = request.args.get('type')
    kw = request.args.get('kw')
    if kw is not None and kw != '':
        pagination = Article.query.filter(Article.details.like("%" + kw + "%")).order_by(
            Article.created_at.desc()).paginate(
                per_page=10,
                error_out=False
            )
    return render_template('article/index.html', pagination=pagination,
                           kw=kw)
    
    '''
    #kw = request.args.get('kw')
    book = request.form['book']

    print("kw is",kw)

    data = Article.query.filter(Article.details.like("%" + kw + "%")).all()
        # all in the search box will return all the tuples
    if len(data) == 0 : 
        flash('no result','warning')
    return render_template('find/find.html')
    '''
