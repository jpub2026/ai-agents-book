# Python 3.11을 기본으로 사용합니다
FROM python:3.11-slim

# 작업할 폴더를 만듭니다
WORKDIR /app

# requirements.txt를 먼저 복사합니다
COPY requirements.txt .

# 필요한 패키지들을 설치합니다
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 코드를 모두 복사합니다
COPY . .

# 8000번 포트를 사용한다고 알립니다
EXPOSE 8000

# 프로그램을 실행합니다
CMD ["python", "main.py"]
