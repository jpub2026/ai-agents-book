# 《처음 만나는 AI 에이전트 with 랭체인 & MCP》 ERRATA

본 문서는 책에 인쇄된 예제 코드와 깃허브 저장소의 차이, 그리고 책 본문에서
수정이 필요한 부분을 정리한 정오표입니다. 깃허브 저장소의 코드는 **책과
동일하게 인쇄된 형태**를 유지하되, 실행 시 주의해야 할 사항을 이 문서와 각
챕터의 `run_*.py` 보조 스크립트로 안내합니다.

최종 업데이트: 2026-04-20

---

## 1. 책 본문의 오탈자 · 오류

### 1-1. 7장 코드 7-32 — 헬스체크 엔드포인트 경로

**책 출력** (`chapter7/mcp_server/main.py`의 실행 스크립트):

```python
print(f" - 헬스체크: http://localhost:8000/health")
```

**올바른 경로**:

```python
print(f" - 헬스체크: http://localhost:8000/mcp/health")
```

> `chapter7/mcp_server/endpoints.py`에서 `router = APIRouter(prefix="/mcp")`
> 로 선언했기 때문에 실제 헬스체크 엔드포인트는 `/mcp/health`입니다.
> 저장소는 책과 동일한 `"/health"`로 인쇄되어 있습니다. 서버를 띄운 뒤에는
> 주소창에 `http://localhost:8000/mcp/health`를 입력해 상태를 확인해 주세요.

### 1-2. 7장 코드 7-32 — 시작 시 등록 도구 목록

**책 출력**:

```python
print(f" - 등록 도구: {', '.join(TOOLS.keys())}")
```

위 `print` 문은 `uvicorn.run()` 이전, 즉 FastAPI의 `startup` 이벤트가
실행되기 **전**에 호출됩니다. 이 시점에는 `TOOLS` 딕셔너리가 비어 있으므로
"등록 도구: "만 출력됩니다. 실제로는 서버 기동 직후 `register_all_tools()`
에서 각 도구가 등록되며, `chapter7/mcp_server/endpoints.py`의 `GET /mcp/tools`
엔드포인트 또는 콘솔의 "도구 등록: ..." 로그로 확인할 수 있습니다.

### 1-3. 5장 코드 5-10 — LLM 모델 지정

**책 본문 설명**: 비용이 저렴한 `gpt-4o-mini` 모델 사용을 권장합니다.

**저장소 현재 값** (`chapter5/crewai_agents.py`):

```python
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.3
)
```

책 본문대로 `gpt-4o-mini`로 실행하려면 해당 줄을 직접 바꾸거나, 보조 스크립트
`chapter5/run_crewai.py`에 안내된 대로 `team.llm.model_name = "gpt-4o-mini"`
를 지정해 주세요. 두 모델 모두 CrewAI 공식 예제에서 제공되며 가격·속도 조건
이 다를 뿐 기능상 차이는 없습니다.

---

## 2. 책과 저장소 코드의 구성 차이

### 2-1. 7장 `chapter7/mcp_server/main.py`의 누락 임포트

책 본문에는 **가독성**을 이유로 `...생략...` 처리된 부분이 있습니다.

- `from endpoints import router`
- `from middleware import add_metrics_middleware`
- `from tools.customer import get_customer_tool`
- `from tools.order import process_order_tool`
- `from tools.report import generate_report_tool`
- `sys.path.insert(...)` (다른 디렉터리에서 실행할 때 import 경로를 맞추기 위한 보조)

저장소에는 위 항목이 실제로 모두 포함되어 있어 `python main.py` 만으로 바로
실행됩니다.

### 2-2. 개념 설명용 코드의 보조 실행 스크립트

책 6장·7장에는 **흐름을 설명하기 위한 개념 예제**(JSON-RPC 메시지 구조,
MCP 통신 흐름 등)가 포함되어 있습니다. 이 파일들은 그 자체로 `main` 블록이
없기 때문에 저장소에는 각 챕터 하위에 `run_*.py` 보조 스크립트를 두어
실제로 실행해 볼 수 있도록 구성했습니다.

| 책 코드 번호 | 원본 파일 | 실행 방법 |
| --- | --- | --- |
| 5-10 ~ 5-12 | `chapter5/crewai_agents.py` | `python chapter5/run_crewai.py` |
| 6-1 ~ 6-2 | `chapter6/examples/traditional_integration.py` | `python chapter6/examples/run_traditional_integration.py` |
| 6-3 ~ 6-4 | `chapter6/examples/mcp_unified_approach.py` | `python chapter6/examples/run_mcp_unified.py` |
| 6-5 | `chapter6/core/communication_flow.py` | `python chapter6/core/run_communication_flow.py` |
| 6-6 | `chapter6/protocol/jsonrpc_structure.py` | `python chapter6/protocol/run_jsonrpc_structure.py` |
| 6-16 | `chapter6/adapters/langchain_mcp_adapter.py` | `python chapter6/adapters/run_langchain_mcp.py` |
| 6-17 | `chapter6/adapters/langgraph_mcp_node.py` | `python chapter6/adapters/run_langgraph_mcp.py` |
| 6-18 | `chapter6/adapters/crewai_mcp_integration.py` | `python chapter6/adapters/run_crewai_mcp.py` |

### 2-3. 부록 A · 부록 B

책 본문에서 빠진 8장·9장의 프로덕션 배포·최적화 관련 예제는 저장소에서
`appendix_a_production/`, `appendix_b_optimization/` 디렉터리로 이동해
보존했습니다. 본문의 흐름상 필수는 아니지만, 실전 배포나 성능 튜닝에 관심이
있는 독자에게 참고 자료로 제공됩니다.

---

## 3. 실행 시 유의 사항

- 책 예제는 **Python 3.10 이상**을 가정합니다. 3.9 이하에서는 `X | None`
  식의 타입 어노테이션이 동작하지 않습니다.
- 대부분의 예제가 OpenAI·Anthropic·Google AI Studio API 키를 요구합니다.
  `.env` 파일 혹은 쉘 환경 변수로 사전에 등록해 주세요.
- `chapter6/simulation/real_client.py`는 `ws://localhost:3000`에서 동작하는
  MCP 호환 WebSocket 서버가 필요합니다. 테스트 서버가 없다면 오프라인
  모드를 제공하는 `chapter6/examples/run_mcp_unified.py`로 대신 실행할 수
  있습니다.
- `chapter7`의 MCP 서버·클라이언트를 함께 띄우려면 두 개의 터미널에서
  각각 `python main.py`와 `python client_main.py`(또는 `python main.py` 등
  챕터별 README의 안내)를 실행합니다.

---

## 4. 정정 요청

본 정오표에 포함되지 않은 오류를 발견하시면
[깃허브 이슈 페이지](https://github.com/)에 제보해 주세요. 2쇄 이후 반영
하겠습니다.
