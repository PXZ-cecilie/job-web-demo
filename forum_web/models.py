from datetime import datetime
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from sqlalchemy import event, DDL

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.now,
                           onupdate=datetime.now)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)


class UserBase(Base, UserMixin):
    __abstract__ = True

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    email = db.Column(db.String(64), unique=True, nullable=False)
    # phone = db.Column(db.Integer, unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(128), nullable=False)
    is_enable = db.Column(db.Boolean, default=True, index=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def is_user(self):
        return self.role == self.ROLE_USER

    def is_company(self):
        return self.role == self.ROLE_COMPANY

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def check_password(self, password):
        return check_password_hash(self._password, password)


class User(UserBase):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(8), nullable=False)
    # resume = db.Column(db.String(128))
    #photo = db.Column(db.String(128))
    role = db.Column(db.SmallInteger, default=UserBase.ROLE_USER)
    #fav = db.Column(db.Integer)
    #publish = dd.Column(db.Integer)
    #promote = db.Column(db.Integer)

event.listen(User.__table__, "after_create", DDL("ALTER TABLE user AUTO_INCREMENT = 100000000"))

class Article(Base):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    details = db.Column(db.Text)
    fav_count = db.Column(db.Integer,default=0)
    vote_count = db.Column(db.Integer,default=0)
    author = db.Column(db.BigInteger)
    rating = db.Column(db.BigInteger,default=0)
    tags = db.Column(db.String(128),default='')
    def tag_list(self):
        if self.tags and ',' in self.tags:
            return self.tags.split(',')
        return self.tags.split(',')


class Favorites(Base):
    __tablename__ = 'favorites'

    id = db.Column(db.BigInteger, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='SET NULL'))
    # article = db.relationship('Article', uselist=False, backref=db.backref('user_article', lazy='dynamic'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete='SET NULL'))
    # user = db.relationship('User', uselist=False, backref=db.backref('user_article', lazy='dynamic'))

class Publish(Base):
    __tablename__ = 'pubArticle'
    id = db.Column(db.BigInteger, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='SET NULL'))
    # article = db.relationship('Article', uselist=False, backref=db.backref('user_article', lazy='dynamic'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete='SET NULL'))
    # user = db.relationship('User', uselist=False, backref=db.backref('user_article', lazy='dynamic'))
   

class Vote(Base):
    __tablename__ = 'voting'
    id = db.Column(db.BigInteger, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='SET NULL'))
    # article = db.relationship('Article', uselist=False, backref=db.backref('user_article', lazy='dynamic'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete='SET NULL'))
    # user = db.relationship('User', uselist=False, backref=db.backref('user_article', lazy='dynamic'))
