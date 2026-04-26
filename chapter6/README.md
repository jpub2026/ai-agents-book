# Chapter 6: MCP 통합

Model Context Protocol(MCP)을 활용한 에이전트 프레임워크 통합 예제입니다.

## 프로젝트 구조

```
chapter6/
├── adapters/                           # MCP 어댑터
│   ├── crewai_mcp_integration.py      # CrewAI + MCP 통합
│   ├── langchain_mcp_adapter.py       # LangChain + MCP 어댑터
│   └── langgraph_mcp_node.py          # LangGraph + MCP 노드
├── core/                               # 핵심 모듈
│   └── communication_flow.py          # MCP 통신 흐름
├── protocol/                           # 프로토콜 구조
│   └── jsonrpc_structure.py           # JSON-RPC 2.0 메시지 구조
├── examples/                           # 예제
│   ├── mcp_unified_approach.py        # MCP 통합 접근법
│   └── traditional_integration.py     # 전통적 통합 방식
├── simulation/                         # 시뮬레이션
│   └── real_client.py                 # 실제 클라이언트 시뮬레이션
└── config/                             # 설정 (있는 경우)
```

## 주요 개념

### MCP (Model Context Protocol)
LLM 기반 애플리케이션과 외부 도구/데이터 소스를 표준화된 방식으로 연결하는 프로토콜

### 주요 특징
- **표준화된 인터페이스**: 다양한 프레임워크 간 일관된 통합
- **플러그인 아키텍처**: 손쉬운 도구 추가/제거
- **양방향 통신**: 클라이언트-서버 간 효율적인 데이터 교환

## 모듈 설명

### 1. Adapters (어댑터)
각 프레임워크를 MCP와 연결하는 어댑터 구현

#### `langchain_mcp_adapter.py`
LangChain 프레임워크를 MCP와 통합
- MCP 도구를 LangChain Tool로 변환
- 체인 내에서 MCP 리소스 활용

#### `langgraph_mcp_node.py`
LangGraph 워크플로우에 MCP 통합
- MCP 호출을 그래프 노드로 구현
- 상태 기반 MCP 리소스 관리

#### `crewai_mcp_integration.py`
CrewAI 에이전트와 MCP 통합
- MCP 도구를 CrewAI Tool로 변환
- 팀 협업에서 MCP 활용

### 2. Core (핵심)

#### `communication_flow.py`
MCP 클라이언트-서버 통신 흐름 구현
- 요청/응답 처리
- 연결 관리
- 에러 핸들링

### 3. Protocol (프로토콜)

#### `jsonrpc_structure.py`
JSON-RPC 2.0 메시지 구조 예제
- 요청 메시지 구조 (method, params, id)
- 성공/에러 응답 구조
- 알림 메시지 구조 (id 없음)
- MCP 통신의 기반이 되는 프로토콜 이해

### 4. Examples (예제)

#### `traditional_integration.py`
전통적인 도구 통합 방식
- 직접적인 API 호출
- 프레임워크별 커스텀 구현

#### `mcp_unified_approach.py`
MCP를 활용한 통합 접근법
- 표준화된 인터페이스 활용
- 프레임워크 독립적 구현

### 5. Simulation (시뮬레이션)

#### `real_client.py`
실제 MCP 클라이언트 동작 시뮬레이션
- MCP 서버 연결
- 도구 호출 테스트
- 참고: WebSocket을 이용한 학습용 예제이며, 실제 실행에는 ws://localhost:3000 으로
  동작하는 MCP 호환 WebSocket 서버가 필요합니다 (stdio/HTTP가 실제 MCP 표준).

### 6. Config (설정 예제)
- `config/claude_desktop_config.json`, `claude_desktop_config.json`: Claude Desktop용 MCP 서버 설정 예시
- `config/cursor_mcp_config.json`: Cursor IDE용 MCP 설정 예시
- `mcp.json`, `mcp_config.json`: 본문에서 언급되는 통합 설정 참고용

> 설정 파일 안의 `/path/to/...`, `ghp_your_token_here`, `your_api_key` 등은 **샘플 자리표시자**이므로
> 실제 환경에 맞게 수정한 뒤 사용해주세요.

## 사용 방법

### 필수 요구사항

```bash
pip install langchain langchain-core langgraph crewai websockets
# 전통적 통합 예제를 실행하려면 추가 설치가 필요합니다
pip install openai anthropic google-generativeai
```

### 예제 실행

> 각 스크립트는 리포지토리 루트에서 실행하는 것을 권장합니다.

#### 1. 전통적 통합 방식 vs MCP 통합 비교
```bash
# 전통적 방식 (OpenAI/Anthropic/Gemini API 키 필요)
python chapter6/examples/traditional_integration.py

# MCP 통합 방식 (실제 실행에는 MCP 호환 서버 필요)
python chapter6/examples/mcp_unified_approach.py
```

#### 2. 프레임워크별 어댑터 테스트
```bash
# LangChain 어댑터 (모의 응답 출력)
python chapter6/adapters/langchain_mcp_adapter.py

# LangGraph 어댑터
python chapter6/adapters/langgraph_mcp_node.py

# CrewAI 어댑터
python chapter6/adapters/crewai_mcp_integration.py
```

#### 3. 클라이언트 시뮬레이션
```bash
python chapter6/simulation/real_client.py
```

#### 4. 프로토콜 구조 / 통신 흐름 확인
```bash
python chapter6/protocol/jsonrpc_structure.py
python chapter6/core/communication_flow.py
```

## 학습 포인트

1. **통합 패턴 비교**
   - 전통적 방식의 한계
   - MCP의 장점 이해

2. **어댑터 패턴**
   - 각 프레임워크의 특성에 맞는 어댑터 구현
   - 표준 인터페이스 활용

3. **실전 적용**
   - MCP 서버 구축 (Chapter 7과 연계)
   - 프로덕션 환경 고려사항

## 관련 챕터

- Chapter 5: 멀티 에이전트 협업 (기반 지식)
- Chapter 7: MCP 서버/클라이언트 구현
- Appendix A: 프로덕션 배포 (옵션)

## 참고자료

- [MCP 공식 문서](https://modelcontextprotocol.io)
- LangChain MCP 통합 가이드
- CrewAI 도구 통합
