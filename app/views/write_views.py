from flask import Blueprint, render_template, request, redirect, url_for, current_app, session, flash
from app.models import Post, Sell, db, StatusEnum  # Sell 모델을 import
import os
import uuid
from werkzeug.utils import secure_filename


bp = Blueprint('write_views', __name__)

from flask import Blueprint, jsonify, request, current_app, session
from app.models import Post, Sell, db, StatusEnum
import os
import uuid
from werkzeug.utils import secure_filename

bp = Blueprint('write_views', __name__)


@bp.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        content = request.form['content']
        user_id = session.get('user_id')
        image_filenames = request.form.getlist('image_filename')  # HTML에서 업로드된 파일명을 받아옵니다.
        print("-----------------------------------------Image Filenames:", image_filenames)
        print(type(image_filenames))
        print("-----------------------------------------title: ", title)
        if not user_id:
            return jsonify({"success": False, "message": "로그인이 필요합니다."}), 401

        try:
            filenames_str = ', '.join(image_filenames) if image_filenames else ''
            new_post = Post(
                title=title,
                price=price,
                content=content,
                filename=filenames_str,
                image_filename=filenames_str,  # 이미지 경로들을 데이터베이스에 저장
                user_id=user_id
            )
            db.session.add(new_post)
            db.session.commit()
            print("-----------------------------------------Image Filenames:", image_filenames)

            new_sell = Sell(
                item_name=title,
                description=content,
                status=StatusEnum.PENDING,
                user_id=user_id,
                post_id=new_post.id
            )
            db.session.add(new_sell)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": f"오류가 발생했습니다: {str(e)}"}), 500

        return jsonify({"success": True, "message": "글 작성 완료"})

    return render_template('front/write.html')


@bp.route('/write/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    upload_folder = current_app.config['UPLOAD_FOLDER']
    filenames = []

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file.save(os.path.join(upload_folder, unique_filename))
            filenames.append(unique_filename)

    if filenames:
        return jsonify({"success": True, "filenames": filenames})
    return jsonify({"success": False, "message": "파일 업로드에 실패했습니다."}), 400


@bp.route('/information/write.html')
def information_write():
    return render_template('front/write.html')  # 필요한 템플릿을 반환합니다.
