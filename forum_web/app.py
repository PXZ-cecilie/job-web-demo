from flask import Flask
from forum_web.config import configs
from forum_web.models import db, User
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
from flask_share import Share
from flask_uploads import UploadSet, configure_uploads, patch_request_class, IMAGES

uploaded_resume = UploadSet('resume', IMAGES)
uploaded_logo = UploadSet('logo', IMAGES)
#uploaded_photo = UploadSet('photo',IMAGES)


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    CKEditor(app)
    Moment(app)
    share = Share()
    share.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    configure_uploads(app, uploaded_resume)
    configure_uploads(app, uploaded_logo)
    # configure_uploads(app, uploaded_photo)
    patch_request_class(app, app.config['UPLOADED_SIZE'])
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        if User.query.get(id):
            return User.query.get(id)
        elif Company.query.get(id):
            return Company.query.get(id)
    login_manager.login_view = 'front.login'


def register_blueprints(app):
    from .handlers import front, user, search_content
    app.register_blueprint(front)
    app.register_blueprint(user)
    #app.register_blueprint(search_content)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_extensions(app)
    register_blueprints(app)
    db.init_app(app)
    return app
