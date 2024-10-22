import functools
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from flask import current_app  # 추가

from app import db
from app.forms import UserCreateForm, UserLoginForm,VerificationCodeForm
from app.models import User, EmailVerification
from flask_mail import Message
from .. import mail  # flask_mail 설정이 되어 있어야 합니다.
import random
import string

bp = Blueprint('auth', __name__, url_prefix='/auth')


#이메일중복허용되게 함> 내 계정으로 되는지 보려고
@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 이메일이 @duksung.ac.kr 도메인인지 확인
        if not form.email.data.endswith('@duksung.ac.kr'):
            flash('duksung.ac.kr 도메인 이메일만 사용할 수 있습니다.', 'danger')
            return render_template('auth/signup.html', form=form)

        # 사용자 이름 중복 확인
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            # 유저 추가
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)  # 중복 이메일 허용
            db.session.add(user)
            db.session.commit()

            # 이메일 인증 생성 및 전송
            verification = EmailVerification(user_id=user.id, email=user.email)
            verification.generate_code()
            db.session.add(verification)
            db.session.commit()

            # 직접 정의한 send_verification_email 함수 호출
            send_verification_email(user.email, verification.code)

            flash('이메일로 인증 코드가 발송되었습니다. 확인 후 입력해주세요.', 'info')
            return redirect(url_for('auth.verify_email', user_id=user.id))

        else:
            flash('이미 존재하는 사용자입니다.', 'danger')

    return render_template('auth/signup.html', form=form)



@bp.route('/verify_email/<int:user_id>/', methods=('GET', 'POST'))
def verify_email(user_id):
    user = User.query.get_or_404(user_id)
    form = VerificationCodeForm()  # VerificationCodeForm의 인스턴스를 생성
    if request.method == 'POST' and form.validate_on_submit():
        code = form.code.data  # 사용자가 입력한 인증 코드를 가져옴
        verification = EmailVerification.query.filter_by(user_id=user_id, code=code).first()
        if verification and not verification.verified:
            verification.verified = True
            db.session.commit()
            flash('이메일 인증이 완료되었습니다.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('잘못된 인증 코드입니다.', 'danger')

    return render_template('auth/verify_email.html', user=user, form=form)  # 폼을 템플릿에 전달

'''
def send_verification_email(email, code):
    msg = Message('이메일 인증 코드', recipients=[email])
    msg.body = f'인증 코드: {code}'
    mail.send(msg)'''

def send_verification_email(user_email, verification_code):
    msg = Message('이메일 인증', sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[user_email])
    msg.body = f'인증 코드: {verification_code}'
    mail.send(msg)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        femail = form.email.data  # username 대신 email로 변경했다면 email로 사용
        password = form.password.data

        # 데이터베이스에서 유저 조회
        user = User.query.filter_by(email=femail).first()

        # 유저가 존재하고 비밀번호가 일치하는지 확인
        if user is None:
            flash("존재하지 않는 사용자입니다.", 'danger')
        elif not check_password_hash(user.password, password):
            flash("비밀번호가 올바르지 않습니다.", 'danger')
        else:
            # 세션에 유저 정보를 저장하고 홈 화면으로 리디렉션
            session.clear()
            session['user_id'] = user.id
            session['user_name'] = user.username
            print(f"login_user_id____________________________ {session['user_id']}")
            print(f"login_user_id____________________________ {session['user_name']}")
            return redirect(url_for('home_views.home'))

    return render_template('front/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)

    return wrapped_view


def generate_verification_code(length=6):
    """랜덤 인증 코드 생성"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@bp.route('/resend_verification_email/<int:user_id>/', methods=['POST'])
def resend_verification_email(user_id):
    user = User.query.get_or_404(user_id)
    verification = EmailVerification.query.filter_by(user_id=user_id, verified=False).first()

    if verification:
        verification.generate_code()  # 새로운 인증 코드 생성
        db.session.commit()
        send_verification_email(user.email, verification.code)  # 이메일 재전송
        flash('인증 코드가 재전송되었습니다.', 'info')
    else:
        flash('인증 코드 생성에 실패했습니다.', 'danger')

    return redirect(url_for('auth.verify_email', user_id=user_id))


