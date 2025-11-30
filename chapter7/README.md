# Chapter 7: MCP 서버/클라이언트

Model Context Protocol 기반 에이전트 서버와 클라이언트를 구현한 실전 예제입니다.

## 프로젝트 구조

```
chapter7/
├── mcp_server/                         # MCP 서버
│   ├── main.py                        # 서버 메인
│   ├── endpoints.py                   # API 엔드포인트
│   ├── models.py                      # 데이터 모델
│   ├── middleware.py                  # 미들웨어
│   └── metrics.py                     # 메트릭 수집
├── mcp_client/                         # MCP 클라이언트
│   ├── main.py                        # 클라이언트 메인
│   ├── client.py                      # MCP 클라이언트 구현
│   └── workflow.py                    # 워크플로우
└── tools/                              # 비즈니스 도메인 도구
    ├── customer.py                    # 고객 관리 도구
    ├── order.py                       # 주문 관리 도구
    └── report.py                      # 리포트 생성 도구
```

## 주요 개념

### MCP 서버
MCP 프로토콜을 구현한 서버로, 다양한 도구와 리소스를 제공

### MCP 클라이언트
MCP 서버에 연결하여 도구를 호출하고 워크플로우를 실행

### 비즈니스 도메인 도구
실제 비즈니스 로직을 수행하는 도구 집합

## 모듈 설명

### 1. MCP Server (서버)

#### `main.py`
MCP 서버의 진입점
- FastAPI 기반 서버 구동
- MCP 프로토콜 핸들러 등록
- CORS 및 미들웨어 설정

#### `endpoints.py`
MCP API 엔드포인트 정의
- `/tools/list`: 사용 가능한 도구 목록
- `/tools/call`: 도구 호출 실행
- `/resources/list`: 리소스 목록
- `/resources/read`: 리소스 읽기

#### `models.py`
요청/응답 데이터 모델
- Pydantic 모델 정의
- 타입 안전성 보장
- 검증 로직

#### `middleware.py`
요청 처리 미들웨어
- 인증/인가
- 로깅
- 에러 처리

#### `metrics.py`
성능 메트릭 수집
- 응답 시간 측정
- 호출 통계
- 에러 추적

### 2. MCP Client (클라이언트)

#### `main.py`
클라이언트 메인 실행 파일
- 서버 연결 초기화
- 워크플로우 실행

#### `client.py`
MCP 클라이언트 구현
- 서버 연결 관리
- 도구 호출 인터페이스
- 응답 처리

#### `workflow.py`
비즈니스 워크플로우
- 여러 도구 조합
- 순차/병렬 실행
- 결과 통합

### 3. Tools (도구)

#### `customer.py`
고객 관리 도구
- 고객 조회
- 고객 생성
- 고객 정보 업데이트

#### `order.py`
주문 관리 도구
- 주문 조회
- 주문 생성
- 주문 상태 업데이트

#### `report.py`
리포트 생성 도구
- 판매 리포트
- 고객 분석 리포트
- 통계 리포트

## 사용 방법

### 필수 요구사항

```bash
pip install fastapi uvicorn mcp pydantic httpx
```

### 1. MCP 서버 실행

```bash
cd mcp_server
python main.py

# 또는 uvicorn 직접 실행
uvicorn main:app --reload --port 8000
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 2. MCP 클라이언트 실행

별도 터미널에서:

```bash
cd mcp_client
python main.py
```

### 3. 개별 도구 테스트

```bash
cd tools

# 고객 도구 테스트
python customer.py

# 주문 도구 테스트
python order.py

# 리포트 도구 테스트
python report.py
```

### 4. API 문서 확인

서버 실행 후 브라우저에서:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 실습 시나리오

### 시나리오 1: 고객 주문 조회
1. 고객 ID로 고객 정보 조회
2. 해당 고객의 주문 목록 조회
3. 주문 상세 정보 확인

### 시나리오 2: 판매 리포트 생성
1. 기간별 주문 데이터 수집
2. 고객별 구매 분석
3. 종합 리포트 생성

### 시나리오 3: 멀티 에이전트 협업
1. 여러 도구를 조합한 복잡한 워크플로우
2. 조건부 실행 및 에러 처리
3. 결과 통합 및 보고

## 커스터마이징

### 새 도구 추가하기

1. `tools/` 디렉토리에 새 파일 생성
2. 도구 클래스 정의
3. `mcp_server/endpoints.py`에 등록

```python
# tools/my_tool.py
class MyTool:
    def execute(self, params):
        # 도구 로직
        return result
```

### 워크플로우 확장

`mcp_client/workflow.py`에서 새로운 워크플로우 정의:

```python
async def my_workflow(client):
    # 도구 호출 조합
    result1 = await client.call_tool("tool1", params1)
    result2 = await client.call_tool("tool2", params2)
    return combine_results(result1, result2)
```

## 모니터링

### 메트릭 확인
```bash
# 서버 메트릭 엔드포인트
curl http://localhost:8000/metrics
```

### 로그 확인
서버 실행 시 콘솔에서 실시간 로그 확인 가능

## 관련 챕터

- Chapter 6: MCP 통합 (이론 및 어댑터)
- Chapter 8: 프로덕션 배포 (Docker, 모니터링)
- Chapter 9: 최적화 (성능 향상)

## 참고사항

- MCP 서버는 비동기(async) 방식으로 구현
- 클라이언트는 HTTP 또는 WebSocket 연결 지원
- 프로덕션 환경에서는 인증/보안 강화 필요
- 도구는 독립적으로 테스트 가능하도록 설계

## 트러블슈팅

### 서버 연결 실패
- 포트 충돌 확인 (`netstat -ano | findstr :8000`)
- 방화벽 설정 확인

### 도구 호출 에러
- 파라미터 형식 확인
- 서버 로그 확인
- API 문서 참조

## 다음 단계

Chapter 8에서 이 서버를 Docker 컨테이너로 배포하고 프로덕션 환경에서 운영하는 방법을 학습합니다.
