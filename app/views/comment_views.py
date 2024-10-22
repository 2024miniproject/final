from flask import Blueprint, request, jsonify
from app import db
from app.models import Comment, User # 필요한 모델 임포트
from datetime import datetime
from flask import session
from app.models import Post  # Post 모델 임포트
from flask import render_template  # render_template 임포트


bp = Blueprint('comment', __name__, url_prefix='/')


@bp.route('/detail/<int:post_id>')  # 게시글 상세 보기
def detail(post_id):
    post = Post.query.get_or_404(post_id)  # 주어진 post_id에 해당하는 게시글 가져오기
    comments = Comment.query.filter_by(post_id=post_id).all()  # 댓글 가져오기
    current_time = datetime.now()  # 현재 시간 가져오기
    #가장 최근 댓글 시간 계산
    recent_comment_time = None
    if comments:
        recent_comment_time = max(comment.created_at for comment in comments)

    return render_template('front/detail.html', post=post, comments=comments,recent_comment_time=recent_comment_time,current_time=current_time)  # 게시글 데이터와 댓글을 템플릿에 전달

@bp.route('/add_comment', methods=['POST'])  # 댓글 추가 엔드포인트
def add_comment():
    user_id = session.get('user_id')  # 세션에서 user_id 가져오기
    if user_id is None:
        return jsonify({'error': '사용자가 로그인하지 않았습니다.'}), 400

    content = request.json.get('content')  # 댓글 내용 가져오기
    post_id = request.json.get('post_id')  # 게시물 ID 가져오기

    user = User.query.get(user_id)  # user_id로 사용자 정보 가져오기
    if user is None:
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404

    # post_id 유효성 검증
    post = Post.query.get(post_id)
    if post is None:
        return jsonify({'error': '게시물이 존재하지 않습니다.'}), 404

    try:
        new_comment = Comment(content=content, user_id=user_id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'message': '댓글이 추가되었습니다!'}), 201
    except Exception as e:
        db.session.rollback()  # 트랜잭션 롤백
        return jsonify({'error': str(e)}), 500  # 에러 메시지 반환



@bp.route('/get_comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()  # 해당 게시글의 댓글만 필터링
    comment_list = []
    for comment in comments:
        comment_list.append({
            'username': comment.user.username,  # user 관계를 통해 username 가져오기
            'content': comment.content,
            'created_at': comment.created_at.isoformat()
        })
    return jsonify(comment_list)




