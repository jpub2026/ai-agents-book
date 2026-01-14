# Chapter 5: 협업형 멀티 에이전트

멀티 에이전트 시스템의 협업 패턴과 주요 프레임워크를 활용한 구현 예제입니다.

## 프로젝트 구조

```
chapter5/
├── basic_collaboration.py    # 기본 멀티 에이전트: 두 전문가의 순차적 협업
├── smart_coordinator.py      # 조건부 협업: 문의 유형 분석 및 스마트 처리
├── langgraph_workflow.py     # LangGraph를 사용한 조건부 워크플로우
├── crewai_agents.py          # CrewAI를 사용한 고객 서비스 팀
├── complexity_analyzer.py    # 하이브리드 시스템: 복잡도 분석기
└── hybrid_router.py          # 하이브리드 시스템: 적응형 라우터
```

## 예제 분류

### 1. 기본 협업 시스템
두 개 이상의 에이전트가 순차적으로 협업하는 기본 패턴

**파일:**
- `basic_collaboration.py`: 기술 전문가와 정책 전문가의 협업

**주요 개념:**
- 순차적 에이전트 실행
- 컨텍스트 전달
- 결과 통합

### 2. 조건부 협업
문의 유형에 따라 필요한 에이전트만 선택적으로 실행

**파일:**
- `smart_coordinator.py`: 문의 유형 분석 및 조건부 에이전트 실행

**주요 개념:**
- 동적 에이전트 선택
- 조건부 라우팅
- 효율성 측정

### 3. LangGraph 프레임워크
상태 기반 워크플로우 관리 프레임워크

**파일:**
- `langgraph_workflow.py`: 상태 정의, 노드 구현, 워크플로우 실행

**주요 개념:**
- 상태 그래프
- 노드 기반 워크플로우
- 조건부 분기

### 4. CrewAI 프레임워크
역할 기반 팀 협업 프레임워크

**파일:**
- `crewai_agents.py`: 전문가 에이전트 정의, 작업 정의, 팀 협업 실행

**주요 개념:**
- 역할 기반 에이전트
- Task 의존성 관리
- 팀 협업 조율

### 5. 하이브리드 시스템
복잡도에 따라 적응적으로 실행 방식을 선택

**파일:**
- `complexity_analyzer.py`: 복잡도 분석기
- `hybrid_router.py`: 적응형 라우터 및 성능 분석

**주요 개념:**
- 적응형 라우팅
- 복잡도 평가
- 성능 최적화

## 사용 방법

### 필수 요구사항

```bash
pip install langgraph crewai langchain-openai python-dotenv
```

### 예제 실행

각 예제는 독립적으로 실행 가능합니다:

```bash
cd chapter5

# 기본 협업
python basic_collaboration.py

# 조건부 협업
python smart_coordinator.py

# LangGraph 워크플로우
python langgraph_workflow.py

# CrewAI 팀 협업 (OpenAI API 키 필요)
python crewai_agents.py

# 하이브리드 시스템
python hybrid_router.py
```

## 참고사항

- 이 코드들은 4장에서 개발한 `CachedLLMBridge` 클래스를 사용합니다
- 실제 LLM 호출을 위해서는 해당 클래스를 import해야 합니다
- CrewAI 예제는 OpenAI API 키가 필요합니다

## 관련 챕터

- Chapter 4: 기본 LLM 브리지 구현
- Chapter 6: MCP 통합
