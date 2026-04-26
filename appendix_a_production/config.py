"""환경 변수 로더
설치 필요: pip install python-dotenv
"""
import os

try:
    from dotenv import load_dotenv
    # .env 파일에서 환경 변수를 읽어옵니다
    load_dotenv()
except ImportError:
    # python-dotenv 가 없어도 OS 환경변수만 사용하여 동작
    pass

# 환경 변수 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # 기본값 설정 가능


def require_api_key() -> str:
    """API_KEY가 필요할 때 호출. 없으면 예외를 발생시킴."""
    if not API_KEY:
        raise ValueError("API_KEY 환경변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    return API_KEY


if __name__ == "__main__":
    print(f"ENVIRONMENT = {ENVIRONMENT}")
    print(f"DATABASE_URL 설정됨: {bool(DATABASE_URL)}")
    print(f"API_KEY 설정됨: {bool(API_KEY)}")
