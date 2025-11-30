# Chapter 5: 협업형 멀티 에이전트

멀티 에이전트 시스템의 협업 패턴과 주요 프레임워크를 활용한 구현 예제입니다.

## 프로젝트 구조

```
book_examples/
├── 01_basic_collaboration.py          # 기본 멀티 에이전트: 두 전문가의 순차적 협업
├── 02a_inquiry_analyzer.py            # 조건부 협업 1단계: 문의 유형 분석
├── 02b_conditional_execution.py       # 조건부 협업 2단계: 필요한 에이전트만 실행
├── 02c_stats_analysis.py              # 조건부 협업 3단계: 실행 및 성능 분석
├── 03a_langgraph_state.py             # LangGraph 1단계: 상태 정의와 워크플로우 구조
├── 03b_langgraph_nodes.py             # LangGraph 2단계: 노드(작업) 구현
├── 03c_langgraph_run.py               # LangGraph 3단계: 워크플로우 실행
├── 04a_crewai_agents.py               # CrewAI 1단계: 전문가 에이전트 정의
├── 04b_crewai_tasks.py                # CrewAI 2단계: 작업(Task) 정의
├── 04c_crewai_run.py                  # CrewAI 3단계: 팀 협업 실행
├── 05a_complexity_analyzer.py         # 하이브리드 시스템 1단계: 복잡도 분석기
├── 05b_hybrid_router.py               # 하이브리드 시스템 2단계: 적응형 라우터
└── 05c_performance_analysis.py        # 하이브리드 시스템 3단계: 실행 및 분석
```

## 예제 분류

### 1. 기본 협업 시스템
두 개 이상의 에이전트가 순차적으로 협업하는 기본 패턴

**파일:**
- `01_basic_collaboration.py`: 기술 전문가와 비즈니스 전문가의 협업

**주요 개념:**
- 순차적 에이전트 실행
- 컨텍스트 전달
- 결과 통합

### 2. 조건부 협업
문의 유형에 따라 필요한 에이전트만 선택적으로 실행

**파일:**
- `02a_inquiry_analyzer.py`: 문의 유형 분석기
- `02b_conditional_execution.py`: 조건부 에이전트 실행
- `02c_stats_analysis.py`: 실행 통계 분석

**주요 개념:**
- 동적 에이전트 선택
- 조건부 라우팅
- 효율성 측정

### 3. LangGraph 프레임워크
상태 기반 워크플로우 관리 프레임워크

**파일:**
- `03a_langgraph_state.py`: 상태 정의
- `03b_langgraph_nodes.py`: 노드(작업) 구현
- `03c_langgraph_run.py`: 워크플로우 실행

**주요 개념:**
- 상태 그래프
- 노드 기반 워크플로우
- 조건부 분기

### 4. CrewAI 프레임워크
역할 기반 팀 협업 프레임워크

**파일:**
- `04a_crewai_agents.py`: 전문가 에이전트 정의
- `04b_crewai_tasks.py`: 작업(Task) 정의
- `04c_crewai_run.py`: 팀 협업 실행

**주요 개념:**
- 역할 기반 에이전트
- Task 의존성 관리
- 팀 협업 조율

### 5. 하이브리드 시스템
복잡도에 따라 적응적으로 실행 방식을 선택

**파일:**
- `05a_complexity_analyzer.py`: 복잡도 분석기
- `05b_hybrid_router.py`: 적응형 라우터
- `05c_performance_analysis.py`: 성능 분석

**주요 개념:**
- 적응형 라우팅
- 복잡도 평가
- 성능 최적화

## 사용 방법

### 필수 요구사항

```bash
pip install python-docx langgraph crewai langchain
```

### 예제 실행

각 예제는 독립적으로 실행 가능합니다:

```bash
cd book_examples

# 기본 협업
python 01_basic_collaboration.py

# 조건부 협업 (순서대로 실행)
python 02a_inquiry_analyzer.py
python 02b_conditional_execution.py
python 02c_stats_analysis.py

# LangGraph (순서대로 실행)
python 03a_langgraph_state.py
python 03b_langgraph_nodes.py
python 03c_langgraph_run.py

# CrewAI (순서대로 실행)
python 04a_crewai_agents.py
python 04b_crewai_tasks.py
python 04c_crewai_run.py

# 하이브리드 시스템 (순서대로 실행)
python 05a_complexity_analyzer.py
python 05b_hybrid_router.py
python 05c_performance_analysis.py
```

## 참고사항

- 이 코드들은 4장에서 개발한 `CachedLLMBridge` 클래스를 사용합니다
- 실제 LLM 호출을 위해서는 해당 클래스를 import해야 합니다
- 일부 예제는 순서대로 실행해야 이전 단계의 결과를 활용할 수 있습니다

## 관련 챕터

- Chapter 4: 기본 LLM 브리지 구현
- Chapter 6: MCP 통합
