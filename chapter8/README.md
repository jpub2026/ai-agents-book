# Chapter 8: 프로덕션 배포

에이전트 시스템의 로깅, 모니터링, Docker 배포 자동화 예제입니다.

## 프로젝트 구조

```
chapter8/
├── main.py                             # 메인 애플리케이션 (로깅 + 알림 통합)
├── config.py                           # 환경 변수 설정
├── logging_setup.py                    # 로깅 시스템 구성
├── slack_notifier.py                   # Slack 알림 통합
├── docker/                             # Docker 관련
│   ├── Dockerfile                     # 컨테이너 이미지 정의
│   ├── install_docker.sh              # Docker 설치 스크립트
│   └── verify_installation.sh         # 설치 검증 스크립트
├── docker-compose.yml                  # 컨테이너 오케스트레이션
├── deploy.sh                           # 배포 자동화 스크립트
└── rollback.sh                         # 롤백 스크립트
```

## 주요 개념

### 1. 구조화된 로깅
실전 환경에서 필수적인 로깅 시스템 구축
- 다단계 로깅 (DEBUG, INFO, ERROR)
- 파일 로테이션
- 콘솔 + 파일 이중 출력

### 2. Slack 알림 통합
작업 상태를 실시간으로 팀에 공유
- 작업 완료/실패 알림
- 간단한 텍스트 알림
- Block Kit을 활용한 리치 메시지

### 3. Docker 컨테이너화
일관된 실행 환경 보장
- Dockerfile 기반 이미지 빌드
- 환경 독립성
- 배포 자동화

### 4. 배포 자동화
스크립트를 통한 안전한 배포/롤백
- 버전 백업
- 헬스체크
- 자동 롤백

## 모듈 설명

### 1. 애플리케이션 파일

#### `main.py`
로깅과 Slack 알림이 통합된 메인 애플리케이션
- `process_task()`: 기본 작업 처리 + 로깅
- `do_something()`: 실제 작업 로직
- `process_task_with_notification()`: 작업 처리 + Slack 알림

**주요 기능:**
```python
# 로깅으로 작업 추적
logger.info(f"작업 시작: {task_id}")

# 에러 발생 시 상세 정보 기록
logger.error(f"작업 실패", exc_info=True)

# Slack으로 결과 알림
slack.send_task_complete(task_id, "success", result)
```

#### `config.py`
환경 변수 관리
- `.env` 파일 로딩
- 필수 환경 변수 검증
- 기본값 설정

**사용 예:**
```python
DATABASE_URL = os.getenv("DATABASE_URL")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
```

#### `logging_setup.py`
로깅 시스템 설정
- 콘솔 출력 (INFO 레벨)
- 파일 출력 (DEBUG 레벨)
- 로그 로테이션 (10MB마다 새 파일)
- 최대 5개 백업 파일 유지

**특징:**
- UTF-8 인코딩 지원
- 타임스탬프 포함
- 서비스별 로거 생성

#### `slack_notifier.py`
Slack 알림 클래스
- `send_message()`: 간단한 텍스트 메시지
- `send_task_complete()`: 작업 완료 알림
- `send_task_complete_fancy()`: Block Kit 리치 메시지

**두 가지 메시지 포맷:**
1. 기본 텍스트: 빠르고 간단
2. Block Kit: 구조화되고 시각적

### 2. Docker 파일

#### `docker/Dockerfile`
Python 3.11 기반 이미지
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

**최적화:**
- slim 이미지 사용 (용량 절감)
- requirements.txt 먼저 복사 (캐싱 활용)
- --no-cache-dir로 캐시 제거

#### `docker/install_docker.sh`
Docker 설치 자동화 스크립트
- Docker Engine 설치
- Docker Compose 설치
- 사용자 권한 설정

#### `docker/verify_installation.sh`
설치 검증 스크립트
- Docker 버전 확인
- Docker Compose 버전 확인
- 테스트 컨테이너 실행

#### `docker-compose.yml`
서비스 오케스트레이션 정의
- 컨테이너 설정
- 환경 변수 매핑
- 포트 바인딩
- 볼륨 마운트

### 3. 배포 스크립트

#### `deploy.sh`
자동화된 배포 프로세스
1. 최신 코드 pull
2. `.env` 파일 확인
3. 현재 버전 백업 (타임스탬프 + previous 태그)
4. Docker 이미지 빌드
5. 기존 컨테이너 중지
6. 새 컨테이너 시작
7. 헬스체크 (5초 대기 후 상태 확인)
8. 실패 시 자동 롤백

**백업 전략:**
- 타임스탬프 태그: `backup_20241019_123045`
- previous 태그: 항상 이전 버전 유지

#### `rollback.sh`
이전 버전으로 안전하게 복구
- previous 태그로 롤백
- 컨테이너 재시작
- 상태 확인

## 사용 방법

### 1. 환경 설정

`.env` 파일 생성:
```bash
# .env
DATABASE_URL=postgresql://localhost/mydb
API_KEY=your_api_key_here
ENVIRONMENT=production
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_CHANNEL=#alerts
```

`requirements.txt` 생성:
```
slack-sdk
python-dotenv
```

### 2. Docker 설치 (처음 1회)

```bash
cd docker
bash install_docker.sh
bash verify_installation.sh
```

### 3. 로컬 테스트

```bash
# 로깅 테스트
python logging_setup.py

# Slack 알림 테스트
python slack_notifier.py

# 메인 앱 실행
python main.py
```

### 4. Docker로 실행

```bash
# 이미지 빌드
docker build -t my-agent -f docker/Dockerfile .

# 컨테이너 실행
docker run -d --name my-agent \
  --env-file .env \
  -p 8000:8000 \
  my-agent

# 로그 확인
docker logs -f my-agent
```

### 5. Docker Compose로 실행

```bash
# 서비스 시작
docker-compose up -d

# 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
```

### 6. 자동 배포

```bash
# 배포 실행
bash deploy.sh

# 문제 발생 시 롤백
bash rollback.sh
```

## 실습 시나리오

### 시나리오 1: 로깅 시스템 테스트
1. `logging_setup.py`로 로거 생성
2. 다양한 레벨 로그 출력
3. `logs/` 폴더에서 파일 확인
4. 로그 로테이션 테스트

### 시나리오 2: Slack 알림 테스트
1. Slack Bot 생성 및 토큰 발급
2. `.env`에 토큰 설정
3. 간단한 메시지 전송
4. Block Kit 리치 메시지 전송

### 시나리오 3: 배포 자동화
1. `deploy.sh`로 첫 배포
2. 코드 수정
3. 재배포
4. 의도적 에러 발생시켜 롤백 테스트

## 커스터마이징

### 로그 레벨 변경
```python
# logging_setup.py
logger.setLevel(logging.DEBUG)  # 더 자세한 로그
logger.setLevel(logging.WARNING)  # 경고 이상만
```

### Slack 채널 변경
```python
# .env
SLACK_CHANNEL=#production-alerts
```

### Dockerfile 최적화
```dockerfile
# 멀티스테이지 빌드
FROM python:3.11-slim as builder
# ... 빌드 단계

FROM python:3.11-slim
COPY --from=builder /app /app
```

## 모니터링

### 로그 확인
```bash
# 실시간 로그
tail -f logs/agent-service.log

# 에러만 필터링
grep ERROR logs/agent-service.log

# 특정 시간대
grep "2024-10-19 12:" logs/agent-service.log
```

### Docker 리소스 모니터링
```bash
# 컨테이너 리소스 사용량
docker stats

# 특정 컨테이너
docker stats my-agent
```

### Slack 알림 예시

**간단한 알림:**
```
✅ 작업 완료 알림

- 작업 ID: task_001
- 상태: success
- 결과: 처리 완료
```

**리치 메시지 (Block Kit):**
```
┌─────────────────────────┐
│ ✅ 작업 완료            │
├─────────────────────────┤
│ 작업 ID: task_001       │
│ 상태: success           │
│ 실행 시간: 2.34초       │
│ 결과: 처리 완료         │
└─────────────────────────┘
```

## 트러블슈팅

### Docker 빌드 실패
```bash
# 캐시 없이 다시 빌드
docker build --no-cache -t my-agent .

# 빌드 로그 확인
docker build -t my-agent . --progress=plain
```

### 컨테이너 시작 실패
```bash
# 로그 확인
docker logs my-agent

# 대화형 모드로 디버깅
docker run -it --entrypoint bash my-agent
```

### Slack 알림 실패
- 토큰 확인: `echo $SLACK_BOT_TOKEN`
- 채널 권한 확인
- Bot 스코프 확인 (`chat:write`)

### 로그 파일 없음
```bash
# logs 디렉토리 생성
mkdir -p logs

# 권한 확인
chmod 755 logs
```

## 관련 챕터

- Chapter 7: MCP 서버/클라이언트 (배포할 애플리케이션)
- Chapter 9: 최적화 및 고급 기법

## 배포 체크리스트

### 배포 전
- [ ] `.env` 파일 설정
- [ ] `requirements.txt` 업데이트
- [ ] Slack 토큰 발급 및 설정
- [ ] Docker 설치 및 검증
- [ ] 로컬 테스트 완료

### 배포 후
- [ ] 컨테이너 상태 확인
- [ ] 로그 정상 출력 확인
- [ ] Slack 알림 수신 확인
- [ ] 헬스체크 통과
- [ ] 리소스 사용량 모니터링

## 다음 단계

- CI/CD 파이프라인 구축
- Kubernetes 오케스트레이션
- 프로메테우스/그라파나 메트릭
- ELK 스택 로그 수집

Chapter 9에서는 RAG, 프롬프트 최적화, 엣지 배포 등 고급 기법을 학습합니다.
