from datetime import datetime

def format_datetime(value=None, fmt='%Y년 %m월 %d일 %p %I:%M'):
    if value is None:
        value = datetime.now()  # 현재 시간을 기본값으로 설정
    return value.strftime(fmt)
