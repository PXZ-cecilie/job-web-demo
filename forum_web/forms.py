from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import IntegerField, PasswordField, SelectField, \
    StringField, SubmitField, TextAreaField, ValidationError, BooleanField
from wtforms.validators import Email, EqualTo, Regexp, Length, URL, DataRequired
from .models import User, db, Article
from .app import uploaded_resume, uploaded_logo
import time
import random
import hmac


class RegisterUserForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(message='please input your email'),
                                          Email(message='please input valid email')])
    password = PasswordField('Password', validators=[DataRequired(message='please input your password'),
                                               Length(6, 24, message='password length: 6-24 characters')])
                                               #Regexp(r'^[a-zA-Z]+\w+', message='仅限使用英文、数字、下划线，并以英文开头')])
    repeat_password = PasswordField('Repeat password', validators=[DataRequired(message='repeat passwords'),
                                                        EqualTo('password', message='passwords are not matching')])
    name = StringField('User Name', validators=[DataRequired(message='please input your user name'),
                                         Length(2, 8, message='user name length: 2-8 characters')])
    submit = SubmitField('submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() or \
                Company.query.filter_by(email=field.data).first():
            raise ValidationError('this email has been used by other users')

    def create_user(self):
        user = User()
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        user.id = int(time.time() * 100000000)
        db.session.add(user)
        db.session.commit()
        return user


class ArticleForm(FlaskForm):
    title = StringField('title')
    details = StringField('content', validators=[DataRequired(message='please input your content')])
    submit = SubmitField('submit')
    def publish_article(self):
        article = Article()
        article.title = self.title.data
        article.details = self.details.data
        article.author = current_user.id
        db.session.add(article)
        db.session.commit()
        return article


class AddTagForm(FlaskForm):
    tag = StringField('tag')
    submit = SubmitField('submit')
    def update_tag(self,article_id):
        article_cur = Article.query.get(article_id)
        article_cur.tags += ',' + self.tag.data
        print(article_cur.tags)
        db.session.commit()
        return article_cur


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(message='please input your email'),
                                          Email(message='please input valid email')])
    password = PasswordField('Password', validators=[DataRequired(message='please input your password'),
                                               Length(6, 24, message='password length: 6-24 character')])
    remember_me = BooleanField('remember login')
    submit = SubmitField('Login')


class UserDetailForm(RegisterUserForm):

    def validate_email(self, field):
        if current_user.email != self.email.data and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('this email has been used by other user')

    def update_detail(self, user):
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

def random_name():
    key = ''.join([chr(random.randint(48, 122)) for _ in range(20)])
    h = hmac.new(key.encode('utf-8'), digestmod='MD5')
    return h.hexdigest() + '.'
