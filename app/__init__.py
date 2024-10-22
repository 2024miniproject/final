from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_login import LoginManager  # LoginManager 임포트
import os
import config
from flask_mail import Mail

# naming convention 정의
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))  # db 초기화
migrate = Migrate()  # Migrate 초기화
login_manager = LoginManager()  # LoginManager 초기화
mail = Mail()  # Mail 초기화


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # 이미지 업로드 폴더 설정
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

    # Flask-Mail 초기화
    mail.init_app(app)  # Flask-Mail 초기화
    #app.mail = mail

    # ORM 초기화
    db.init_app(app)  # db를 app에 연결
    migrate.init_app(app, db, render_as_batch=True)  # migrate를 app에 연결

    # LoginManager 초기화 및 로그인 뷰 설정
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # 로그인 페이지 경로 설정

    # 데이터베이스 URI에 따른 Migrate 초기화
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)  # SQLite의 경우
    else:
        migrate.init_app(app, db)  # 다른 데이터베이스의 경우

    from . import models  # models를 여기서 import하여 초기화합니다.

    # 사용자 로드 함수 정의
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))  # User 모델에서 사용자 로드

    # 블루프린트 등록
    from .views import main_views, auth_views, information_views, home_views, detail_views, write_views, mydeal_views, comment_views, purchasewant_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(information_views.bp)
    app.register_blueprint(home_views.bp)
    app.register_blueprint(detail_views.bp)
    app.register_blueprint(write_views.bp)
    app.register_blueprint(mydeal_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(purchasewant_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
