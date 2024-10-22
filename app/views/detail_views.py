from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.models import Post, Comment, Sell, Buy
from app import db
from flask import Blueprint, render_template, redirect, url_for, session, flash, jsonify  # jsonify 추가


bp = Blueprint('detail', __name__, url_prefix='/')


@bp.route('/detail/<int:post_id>')
def detail(post_id):
    post = Post.query.get_or_404(post_id)

    # 사용자의 구매 신청 확인
    user_id = session.get('user_id')
    existing_purchase = Buy.query.filter_by(user_id=user_id, post_id=post_id).first()

    # 구매자 ID를 확인하여 구매자가 존재하는지 확인
    buyer = Buy.query.filter_by(post_id=post_id).first()  # 게시글에 대한 첫 번째 구매자 정보 조회
    buyer_exists = True if buyer else False  # 구매자가 있는지 여부 확인

    return render_template('front/detail.html', post=post, existing_purchase=existing_purchase, buyer_exists=buyer_exists)



@bp.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # 로그인한 사용자와 게시글 작성자가 같은지 확인
    if post.user_id != session.get('user_id'):
        return '', 403  # 삭제 권한이 없을 경우 403 Forbidden 응답

    try:
        # 1. Buy 테이블에서 해당 post_id와 관련된 레코드 삭제
        Buy.query.filter(Buy.post_id == post_id).delete()

        # 2. Comment 테이블에서 해당 post_id와 관련된 레코드 삭제
        Comment.query.filter(Comment.post_id == post_id).delete()

        # 3. Sell 테이블에서 해당 post_id와 관련된 레코드 삭제 (필요 시)
        Sell.query.filter(Sell.post_id == post_id).delete()

        # 게시글 삭제
        db.session.delete(post)
        db.session.commit()
        return '', 204  # 성공적으로 삭제되었음을 알리는 204 No Content 응답
    except Exception as e:
        db.session.rollback()
        return '', 500  # 서버 오류가 발생했음을 알리는 500 Internal Server Error 응답


