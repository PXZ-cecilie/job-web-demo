#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from ..forms import UserDetailForm, RegisterUserForm, ArticleForm, AddTagForm
from ..models import Article,db,Favorites,Vote
from sqlalchemy import or_
import re

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

@user.route('/search',methods=['GET', 'POST'])
def search():
    if not current_user.is_authenticated:
    # search_type = request.args.get('type')
        kw = request.args.get('kw')
        if kw is not None and kw != '':
            pagination = Article.query.filter(or_(Article.details.like("%" + kw + "%")),(Article.tags.like("%" + kw + "%"))).order_by(
                Article.rating.desc()).paginate(
                    per_page=10,
                    error_out=False
                )
        return render_template('article/index.html', pagination = pagination, kw=kw, content = [], res = kw)
    if current_user.is_user():
        kw = request.args.get('kw')
        res = []
        stopwords = ['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now']
        punc = [',','.','?','*','(',')','!','@','=','-','~']
        kw2 = re.sub(r'[^\w\s]','',kw)
        kws = kw2.split(" ")
        for word in kws:
            if word not in stopwords and word not in punc:
                res.append(word)
        kw_final = ' '.join(res)
        print("keyword is",kw_final)
        fav_content = Favorites.query.filter(Favorites.user_id == current_user.id).distinct().all()
        promote_content = Vote.query.filter(Favorites.user_id == current_user.id).all()
        
        fav_list = []
        for obj in fav_content:
            fav_list.append(obj.article_id)
        promote_list = []
        for obj in promote_content:
            promote_list.append(obj.article_id)
        #print("list",fav_list)
        fav_article = Article.query.filter(Article.id.in_(fav_list)).distinct().all()
        #print("length of fav",len(fav_article))
        fav_str_list = []
        for obj in fav_article:
            fav_str_list.extend(obj.title.split(" "))
            fav_str_list.extend(obj.details.split(" "))
        voted_article = Article.query.filter(Article.id.in_(promote_list)).distinct().all()
        vote_str_list = []
        for obj in voted_article:
            vote_str_list.extend(obj.title.split(" "))
            vote_str_list.extend(obj.details.split(" "))
        #print("fav str",fav_str_list)
        #if kw is not None and kw != '':
        related_article = []
        kw_split = kw_final.split(" ")
        for kw in kw_split:
            print("kw here", kw)
            related = Article.query.filter((Article.details.like("%" + kw + "%"))|(Article.tags.like("%" + kw + "%"))|(Article.title.like("%" + kw + "%"))).distinct().all()
            related_article.extend(related)
        count_list = [[art,0] for art in related_article]
        for i,arti in enumerate(related_article):
            content = arti.details.split(" ")
            print(content)
            for word in content:
                if word in fav_str_list:
                    count_list[i][1] += 1
                if word in vote_str_list:
                    count_list[i][1] += 1
            # print("count_list",count_list[0][1])
            count_list = sorted(count_list, key = lambda x: x[1],reverse=True)
            # print("count_list",count_list[0][1])
            item_list = []
            rank_list = []
            for item,count in count_list:
                item_list.append(item)
                rank_list.append(count)
        '''
        if kw is not None and kw != '':
                pagination = Article.query.filter((Article.details.like("%" + kw + "%"))|(Article.tags.like("%" + kw + "%"))).paginate(
                        per_page=10,
                        error_out=False
                    )
        '''
        return render_template('article/index.html', pagination = count_list, kw=kw, content = rank_list, res = kw_final)

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
        return browse()
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
def file_error(error):
    flash('file larger than limit', 'warning')
    return redirect(request.path)

@user.errorhandler(404)
def page_not_found(errot):
    flash('page not found','warning')
    return render_template('404.html')
