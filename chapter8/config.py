import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 읽어옵니다
load_dotenv()

# 환경 변수 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # 기본값 설정 가능

# 필수 값이 없으면 에러 발생
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다!")
