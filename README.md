# AI Agents Book - Chapter 5 Examples

이 리포지토리는 "AI 에이전트" 책의 5장(협업형 멀티 에이전트) 예제 코드를 포함하고 있습니다.

## 📁 프로젝트 구조

```
chapter5/
└── book_examples/
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

## 📚 예제 분류

### 1. 기본 협업 시스템
- **01_basic_collaboration.py**: 기본 멀티 에이전트 구현

### 2. 조건부 협업
- **02a_inquiry_analyzer.py**: 문의 유형 분석
- **02b_conditional_execution.py**: 조건부 실행
- **02c_stats_analysis.py**: 성능 통계

### 3. LangGraph 프레임워크
- **03a_langgraph_state.py**: 상태 정의
- **03b_langgraph_nodes.py**: 노드 구현
- **03c_langgraph_run.py**: 워크플로우 실행

### 4. CrewAI 프레임워크
- **04a_crewai_agents.py**: 에이전트 정의
- **04b_crewai_tasks.py**: 작업 정의
- **04c_crewai_run.py**: 팀 협업 실행

### 5. 하이브리드 시스템
- **05a_complexity_analyzer.py**: 복잡도 분석
- **05b_hybrid_router.py**: 적응형 라우팅
- **05c_performance_analysis.py**: 성능 분석

## 🚀 사용 방법

### 필수 요구사항

```bash
pip install python-docx
```

### 예제 실행

각 예제 파일은 독립적으로 실행 가능합니다:

```bash
cd chapter5/book_examples
python 01_basic_collaboration.py
```

## 📝 참고사항

- 이 코드들은 4장에서 개발한 `CachedLLMBridge` 클래스를 사용합니다
- 실제 LLM 호출을 위해서는 해당 클래스를 import해야 합니다
- 일부 예제는 LangGraph, CrewAI 등의 프레임워크가 필요할 수 있습니다

## 📖 출처

jpub2026/ai-agents-book 리포지토리에서 추출된 예제 코드입니다.
