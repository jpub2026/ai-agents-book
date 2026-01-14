# Chapter 3: AI 에이전트 핵심 구성요소

AI 에이전트를 구성하는 핵심 요소들(메모리, 도구, 계획, 실행)을 학습하고, 주요 프레임워크를 활용하는 방법을 배웁니다.

## 학습 내용

### 1. 에이전트 핵심 구성요소
- **메모리 시스템**: 단기/장기/작업 기억 관리
- **도구(Tool) 관리**: 에이전트가 사용할 수 있는 도구 등록 및 실행
- **계획(Planning)**: 사용자 요청을 실행 가능한 단계로 분해
- **실행(Execution)**: 계획된 작업을 순차적/병렬적으로 실행

### 2. 주요 에이전트 프레임워크
- **LangChain**: 체인 기반 에이전트 구축
- **LangGraph**: 그래프 기반 워크플로우
- **CrewAI**: 팀 협업 에이전트 시스템

## 디렉토리 구조

```
chapter3/
├── core/              # 핵심 구성요소
│   ├── planner.py        # 계획 수립
│   └── executor.py       # 계획 실행
├── memory/            # 메모리 시스템
│   └── system.py         # 통합 메모리 관리
├── tools/             # 도구 관리
│   └── base.py           # 도구 기본 클래스
├── agent/             # 통합 에이전트
│   ├── core.py           # 전체 시스템 통합
│   └── example.py        # 실행 예제
├── langchain/         # LangChain 프레임워크
│   └── agent.py
├── langgraph/         # LangGraph 프레임워크
│   └── workflow.py
└── crewai/            # CrewAI 프레임워크
    └── team.py
```

## 실행하기

### 1. 핵심 구성요소 개별 테스트

```bash
# 메모리 시스템
cd memory
python system.py

# 도구 관리자
cd tools
python base.py

# 계획 수립기
cd core
python planner.py

# 실행 엔진
cd core
python executor.py
```

### 2. 통합 에이전트 실행 (권장)

```bash
cd agent
python example.py
```

이 예제는 모든 구성요소를 통합하여 실제 에이전트가 어떻게 작동하는지 보여줍니다:
1. 요청 수신 및 기억 검색
2. 계획 수립
3. 계획 실행
4. 경험 저장
5. 응답 생성

### 3. 프레임워크별 에이전트

```bash
# LangChain 에이전트
cd langchain
python agent.py

# LangGraph 워크플로우
cd langgraph
python workflow.py

# CrewAI 팀 에이전트
cd crewai
python team.py
```

## 요구사항

### 핵심 구성요소 (필수)
```bash
pip install requests
```

### 프레임워크 (선택)
```bash
# LangChain & LangGraph
pip install langchain langgraph langchain-openai

# CrewAI
pip install crewai crewai-tools

# 모두 설치
pip install langchain langgraph crewai crewai-tools
```

### LLM 설정
Chapter 2의 `llm_interface.py`를 사용하므로:
- Ollama 또는 OpenAI 설정 필요
- Mock 모드로도 테스트 가능

## 핵심 개념

### 1. 메모리 시스템
에이전트의 3가지 기억 타입:

```python
from memory.system import MemorySystem

memory = MemorySystem()

# 단기 기억: 최근 100개 상호작용
memory.store(info, memory_type='short')

# 장기 기억: 중요한 정보 영구 저장
# (중요도가 높으면 자동 승격)

# 작업 기억: 현재 작업 컨텍스트
memory.store(task_info, memory_type='working')
```

### 2. 도구 시스템
에이전트가 외부 기능을 사용하는 방법:

```python
from tools.base import BaseTool, ToolManager

# 도구 정의
search_tool = BaseTool(
    name="search",
    description="웹에서 정보를 검색합니다"
)

# 도구 관리자에 등록
tool_manager = ToolManager()
tool_manager.register_tool(search_tool)

# 도구 실행
result = tool_manager.execute_tool("search", {"query": "AI agents"})
```

### 3. 계획과 실행
사용자 요청을 실행 가능한 단계로 분해:

```python
from core.planner import Planner
from core.executor import Executor

# 계획 수립
planner = Planner(llm=llm)
plan = planner.create_plan(
    user_request="회의 준비",
    available_tools=["calendar", "email", "document"]
)

# 계획 실행
executor = Executor(tool_manager, memory)
results = executor.execute_plan(plan)
```

### 4. 통합 에이전트
모든 구성요소를 하나로:

```python
from agent.core import Agent

# 에이전트 초기화
agent = Agent()

# 요청 처리 (5단계 프로세스)
response = agent.process_request("내일 팀 회의를 준비해줘")
```

## 프레임워크 선택 가이드

### LangChain
- 체인 기반 간단한 워크플로우
- 다양한 도구 통합
- 빠른 프로토타이핑

### LangGraph
- 복잡한 상태 관리
- 조건부 분기 워크플로우
- 그래프 기반 설계

### CrewAI
- 다중 에이전트 협업
- 역할 기반 팀 구성
- 자율적인 작업 분담

## 다음 단계

Chapter 4에서는 이러한 에이전트 구성요소들을 활용하여 실전 프로젝트를 단계별로 구축합니다.
