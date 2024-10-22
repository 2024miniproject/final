from flask import Blueprint, render_template, redirect, url_for
from app.models import Post  # Post 모델을 import합니다.
from app import db

bp = Blueprint('home_views', __name__, url_prefix='/')

@bp.route('/home')  # 원하는 URL 경로에 따라 수정 가능
def home():
    posts = Post.query.all()  # 데이터베이스에서 모든 게시글 조회
    return render_template('front/home.html', posts=posts)  # 템플릿 파일 경로

# 게시글 삭제 기능 추가
'''
@bp.route('/delete_post/<int:post_id>', methods=['POST'])  # POST 메서드 추가
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # 게시글이 존재하지 않으면 404 에러
    db.session.delete(post)  # 게시글 삭제
    db.session.commit()  # 변경 사항 저장
    return redirect(url_for('home_views.home'))  # 삭제 후 홈으로 리디렉션
'''
# 오류 발생으로 게시글 삭제 보류