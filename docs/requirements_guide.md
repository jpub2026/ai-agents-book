# 챕터별 설치 가이드

책 저장소는 챕터를 넘나들며 필요한 패키지가 조금씩 다르기 때문에, 학습
순서에 맞춰 필요한 패키지만 설치하는 방식을 권장합니다. 모든 코드를 한
번에 실행해 보고 싶다면 루트의 `requirements.txt`를 사용해 주세요.

> **공통 사전 조건**
> - Python 3.10 이상(3.11 권장)
> - 가상 환경 사용 권장: `python -m venv .venv && source .venv/bin/activate`
> - Windows PowerShell에서는 `.venv\Scripts\Activate.ps1`
> - pip 최신화: `pip install -U pip setuptools wheel`

---

## 1. 전 챕터 공통(가장 먼저)

```bash
pip install python-dotenv pydantic
```

`.env` 파일을 활용한 API 키 관리와 입력 검증에 필요합니다.

---

## 2. 2장 – 프롬프트 · 툴콜

```bash
pip install openai anthropic
```

환경 변수:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="..."
```

---

## 3. 3장 – LangChain 기본

```bash
pip install langchain langchain-openai langchain-community
```

LLM 호출에는 `OPENAI_API_KEY`가 필요합니다.

---

## 4. 4장 – LangGraph 상태 머신

```bash
pip install langchain langchain-openai langgraph
```

상태 정의용 `dataclass`는 표준 라이브러리라 추가 설치가 필요하지 않습니다.

---

## 5. 5장 – CrewAI 멀티에이전트

```bash
pip install crewai crewai-tools langchain-openai python-dotenv
```

> 책 본문에서는 `gpt-4o-mini` 모델을, 저장소 기본값은 `gpt-3.5-turbo`를
> 사용합니다. 가격과 품질에 따라 `CrewAITeam`의 `model` 인자를 바꿔
> 실행하세요. (ERRATA 1-3 참고)

---

## 6. 6장 – MCP 기초와 어댑터

```bash
pip install websockets httpx langchain langchain-core langgraph crewai pydantic
```

- `chapter6/simulation/real_client.py`는 WebSocket 서버(ws://localhost:3000)
  가 필요합니다. 실제 서버 없이 동작만 확인하고 싶다면 `run_*.py`
  보조 스크립트를 사용하세요.
- 개념 예제(`communication_flow.py`, `jsonrpc_structure.py`)는 별도 의존성이
  없습니다. `chapter6/*/run_*.py` 스크립트로 실행 결과를 확인할 수 있습니다.

---

## 7. 7장 – MCP 서버 · 클라이언트 직접 구현

```bash
pip install fastapi uvicorn httpx ollama langgraph pydantic
```

### 서버 실행

```bash
cd chapter7/mcp_server
python main.py
# 주소: http://localhost:8000
# 문서: http://localhost:8000/docs
# 헬스체크: http://localhost:8000/mcp/health  ← ERRATA 1-1 참고
```

### 클라이언트 실행

```bash
# 사전 준비: Ollama 설치 및 모델 pull
ollama pull llama3.2

cd chapter7/mcp_client
python main.py
```

Ollama를 사용하지 않고 OpenAI API로만 테스트하려면 `OllamaAgent`를
`OpenAI` 클라이언트로 교체해야 합니다. 자세한 사항은 `ERRATA.md`를 참고해
주세요.

---

## 8. 부록 A – 프로덕션 배포(구 8장)

```bash
pip install fastapi uvicorn docker python-dotenv
```

Docker Compose·Kubernetes 예제는 각 하위 디렉터리 README를 참고하세요.

---

## 9. 부록 B – 경량 모델 최적화(구 9장)

```bash
pip install llama-cpp-python[server] huggingface_hub sentence-transformers
```

GGUF 파일은 용량이 크기 때문에 Hugging Face CLI(`huggingface-cli`)로 직접
다운로드하는 과정이 필요합니다. 자세한 사용법은 부록 B의 README를
참고하세요.

---

## 10. 한 번에 설치하고 싶다면

```bash
pip install -r requirements.txt
```

위 명령은 본문 + 부록의 모든 예제를 실행할 수 있는 패키지를 한꺼번에
설치합니다. 저장 공간이 부족하거나 운영체제 호환성 문제가 있다면 필요한
챕터만 선택적으로 설치해 주세요.
