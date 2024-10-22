import os

# 현재 파일 경로를 기준으로 BASE_DIR 설정
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 데이터베이스 설정
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'app.db'))+ '?check_same_thread=False'
SQLALCHEMY_TRACK_MODIFICATIONS = False


# 개발용 SECRET_KEY
SECRET_KEY = "dev"

# 이미지 업로드를 위한 폴더 경로 설정

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')  # 'static/uploads' 폴더 경로


import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# 'uploads' 폴더가 없을 경우 자동으로 생성되도록 처리
#if not os.path.exists(UPLOAD_FOLDER):
 #   os.makedirs(UPLOAD_FOLDER)

MAIL_SERVER = 'smtp.gmail.com'  # 네이버 SMTP 서버
MAIL_PORT = 587  # 네이버는 587번 포트를 사용합니다.
MAIL_USE_TLS = True  # TLS 보안 연결을 사용
#MAIL_USE_SSL = False  # SSL은 사용하지 않음
MAIL_USERNAME = 'cji010222@gmail.com'  # 네이버 이메일 계정
MAIL_PASSWORD = 'tskk qbhg xjll rafv'  # 네이버 이메일 계정 비밀번호 (또는 앱 비밀번호)
#MAIL_DEFAULT_SENDER = ('gptprogrammers', 'gptprogrammers@naver.com')  # 이메일 발송 시 기본 발송자 정보
MAIL_DEFAULT_SENDER = 'cji010222@gmail.com'
