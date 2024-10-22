from app import db  # db 인스턴스를 가져옵니다.
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)  # unique=True를 제거합니다.
    # 관계 설정 (게시글, 구매/판매 기록)
    posts = db.relationship('Post', backref='user', lazy=True)
    buys = db.relationship('Buy', backref='buyer', lazy=True)
    sells = db.relationship('Sell', backref='seller', lazy=True)



class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Float)
    content = db.Column(db.Text)
    filename = db.Column(db.String(200))
    image_filename = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, title, price, content, filename, image_filename=None, user_id=None):
        self.title = title
        self.price = price
        self.content = content
        self.filename = filename
        self.image_filename = image_filename
        self.user_id = user_id

    def __repr__(self):
        return f'<Post {self.title}>'


class StatusEnum(Enum):
    PENDING = '대기중'
    PAYMENT_COMPLETED = '입금완료'
    SIZE_SELECTED = '사물함크기선택완료'
    LOCKER_ASSIGNED = '사물함배치완료'
    TRANSACTION_COMPLETED = '거래완료'

class Buy(db.Model):
    __tablename__ = 'buy'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.PENDING)  # 상태를 Enum으로 정의
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

class Sell(db.Model):
    __tablename__ = 'sell'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.PENDING)  # 상태를 Enum으로 정의
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    # 관계 설정
    user = db.relationship('User', backref='user_comments')
    post = db.relationship('Post', backref='post_comments')

    def __init__(self, content, user_id, post_id):
        self.content = content
        self.user_id = user_id
        self.post_id = post_id

    def __repr__(self):
        return f'<Comment {self.content}>'

    def username(self):
        return self.user.username if self.user else None


import random
import string

import random
import string


class EmailVerification(db.Model):
    __tablename__ = 'email_verification'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    email = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(10), nullable=False)  # 인증 코드를 저장하는 필드
    verified = db.Column(db.Boolean, default=False)  # 인증 여부
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # 생성 시각
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())  # 업데이트 시각

    def generate_code(self, length=6):
        """랜덤 인증 코드 생성"""
        self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
