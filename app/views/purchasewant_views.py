from flask import Blueprint, jsonify, request, session, redirect, url_for, flash
from app.models import Sell, Buy, Post, db, StatusEnum
from datetime import datetime
bp = Blueprint('purchasewant', __name__, url_prefix='/purchasewant')


@bp.route('/submit_purchase', methods=['POST'])
def submit_purchase():
    user_id = session.get('user_id')
    if not user_id:
        flash("로그인 후 이용해 주세요.")
        return redirect(url_for('auth_views.login'))

    data = request.get_json()
    post_id = data.get('post_id')
    print("Received post_id:--------------------------------------------", post_id)

    # 구매하려는 포스트 가져오기
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'success': False, 'message': "존재하지 않는 상품입니다."}), 404

    # 구매 정보 생성
    new_purchase = Buy(
        item_name=post.title,
        description=post.content,
        status="PENDING",
        created_at=datetime.utcnow(),
        user_id=user_id,
        post_id = post_id
    )

    try:
        db.session.add(new_purchase)
        db.session.commit()
        return jsonify({'success': True, 'data': {'title': post.title, 'content': post.content, 'price': post.price}})
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': '구매 신청 중 오류가 발생했습니다.'})


from flask import Blueprint, jsonify, request, session, redirect, url_for, flash
from app.models import Sell, Buy, Post, db, StatusEnum
from datetime import datetime

bp = Blueprint('purchasewant', __name__, url_prefix='/purchasewant')


@bp.route('/submit_purchase', methods=['POST'])
def submit_purchase():
    user_id = session.get('user_id')
    if not user_id:
        flash("로그인 후 이용해 주세요.")
        return redirect(url_for('auth_views.login'))

    data = request.get_json()
    post_id = data.get('post_id')
    print("Received post_id:--------------------------------------------", post_id)

    # 구매하려는 포스트 가져오기
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'success': False, 'message': "존재하지 않는 상품입니다."}), 404

    # 구매 정보 생성
    new_purchase = Buy(
        item_name=post.title,
        description=post.content,
        status="PENDING",  # 초기 상태: 대기 중
        created_at=datetime.utcnow(),
        user_id=user_id,
        post_id=post_id
    )

    try:
        db.session.add(new_purchase)

        # 판매 상태도 PENDING으로 설정
        sell_item = Sell.query.filter_by(post_id=post_id).first()
        if sell_item:
            sell_item.status = "PENDING"

        db.session.commit()
        return jsonify({'success': True, 'data': {'title': post.title, 'content': post.content, 'price': post.price}})
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': '구매 신청 중 오류가 발생했습니다.'})



@bp.route('/cancel_purchase/<int:purchase_id>', methods=['POST'])
def cancel_purchase(purchase_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "로그인이 필요합니다."}), 401

    # 구매 기록을 가져오고 사용자 확인
    purchase = Buy.query.get(purchase_id)
    if not purchase:
        return jsonify({"success": False, "message": "구매 기록을 찾을 수 없습니다."}), 404

    # 구매자가 본인 소유인지 확인
    if purchase.user_id != user_id:
        return jsonify({"success": False, "message": "취소 권한이 없습니다."}), 403

    try:
        db.session.delete(purchase)
        db.session.commit()
        return jsonify({"success": True, "message": "구매 신청이 취소되었습니다."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "취소 중 오류가 발생했습니다."}), 500







@bp.route('/update_purchase_status/<int:purchase_id>', methods=['POST'])
def update_purchase_status(purchase_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "로그인이 필요합니다."}), 401

    data = request.get_json()
    new_status = data.get('status')
    purchase = Buy.query.get(purchase_id)

    if not purchase:
        return jsonify({"success": False, "message": "구매 기록을 찾을 수 없습니다."}), 404

    sell_item = Sell.query.filter_by(post_id=purchase.post_id).first()
    if not sell_item:
        return jsonify({"success": False, "message": "판매 기록을 찾을 수 없습니다."}), 404

    # 단계에 따라 상태를 업데이트
    if new_status == "PAYMENT_COMPLETED":
        purchase.status = "PAYMENT_COMPLETED"
        sell_item.status = "PAYMENT_COMPLETED"
    elif new_status == "SIZE_SELECTED":
        purchase.status = "SIZE_SELECTED"
        sell_item.status = "SIZE_SELECTED"
    elif new_status == "LOCKER_ASSIGNED":
        purchase.status = "LOCKER_ASSIGNED"
        sell_item.status = "LOCKER_ASSIGNED"
    elif new_status == "TRANSACTION_COMPLETED":
        purchase.status = "TRANSACTION_COMPLETED"
        sell_item.status = "TRANSACTION_COMPLETED"
    else:
        return jsonify({"success": False, "message": "유효하지 않은 상태 변경 요청입니다."}), 400

    try:
        db.session.commit()
        return jsonify({"success": True, "message": "상태가 업데이트되었습니다."})
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "상태 업데이트 중 오류가 발생했습니다."})



