from flask import render_template, request, session, flash, redirect, url_for
from app.models import Buy, Sell, db
from flask import Blueprint

bp = Blueprint('mydeal', __name__, url_prefix='/mydeal_views')
# 구매 목록 라우트
@bp.route('/mydealbuy')
def mydealbuy():
    # 데이터베이스에서 구매 데이터 가져오기
    user_id = session.get('user_id')
    if not user_id:
        flash("로그인 후 이용해 주세요.")
        return redirect(url_for('auth_views.login'))

    # 현재 사용자에 대한 구매 목록 조회

    purchase_list = Buy.query.filter_by(user_id=user_id).all()
    return render_template('front/mydealbuy.html', purchases=purchase_list)

# 판매 목록 라우트
@bp.route('/mydealsell')
def mydealsell():
    # 데이터베이스에서 판매 데이터 가져오기
    user_id = session.get('user_id')
    if not user_id:
        flash("로그인 후 이용해 주세요.")
        return redirect(url_for('auth_views.login'))
    sale_list = Sell.query.filter_by(user_id=user_id).all()

    # 판매 항목의 상태가 잘못된 경우 PENDING으로 초기화
    for sale in sale_list:
        if sale.status not in ['PENDING', 'PAYMENT_COMPLETED', 'SIZE_SELECTED', 'LOCKER_ASSIGNED', 'TRANSACTION_COMPLETED']:
            sale.status = 'PENDING'
    db.session.commit()

    return render_template('front/mydealsell.html', sales=sale_list)


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

    # 구매 상태 업데이트
    purchase.status = new_status
    db.session.commit()

    # 판매 상태도 업데이트
    sell_item = Sell.query.filter_by(post_id=purchase.post_id).first()
    if sell_item:
        sell_item.status = new_status
        db.session.commit()

    return jsonify({"success": True, "message": "상태가 업데이트되었습니다."})


