# Chapter 4: 실전 AI 에이전트 구축 - 단계별 접근

간단한 FAQ 봇부터 시작하여 프로덕션 수준의 AI 에이전트까지 단계별로 구축하는 방법을 학습합니다.

## 학습 내용

이 챕터는 실무에서 AI 에이전트를 구축할 때 거치게 되는 **5단계 진화 과정**을 다룹니다:

1. **Step 1**: 간단한 LLM 브리지 (Mock 응답)
2. **Step 2**: 실제 LLM 통합 및 캐싱
3. **Step 3**: 도구(Tool) 시스템 추가
4. **Step 4**: ReAct 패턴과 메모리 시스템
5. **Step 5**: 프로덕션 환경 (메트릭, 세션, 분석)

## 디렉토리 구조

```
chapter4/
├── requirements.txt           # 필요한 패키지 목록
├── step1_basic/              # 단계 1: 기본 브리지
│   └── simple_llm_bridge.py     # LangChain 브리지 구현
├── step2_real_llm/           # 단계 2: 실제 LLM
│   ├── real_llm_bridge.py       # LLM 통합
│   └── cached_llm_bridge.py     # 캐싱 추가
├── step3_tools/              # 단계 3: 도구 시스템
│   ├── simple_faq_tool.py       # 기본 FAQ 도구
│   └── hybrid_faq_tool.py       # 하이브리드 검색
├── step4_agent/              # 단계 4: 에이전트 패턴
│   ├── simple_react_agent.py    # ReAct 패턴
│   └── memory_agent.py          # 메모리 통합
└── step5_production/         # 단계 5: 프로덕션
    ├── metrics.py               # 성능 메트릭
    ├── session.py               # 세션 관리
    ├── statistics.py            # 통계 수집
    ├── analyzer.py              # 로그 분석
    └── extended_system.py       # 전체 시스템 통합
```

## 실행하기

### 단계 1: 기본 브리지
가장 간단한 LLM 브리지 구현

```bash
cd step1_basic
python simple_llm_bridge.py
```

**핵심 개념:**
- LangChain의 `BaseLLM` 상속
- `_call()` 메서드 구현
- Mock 응답으로 테스트

### 단계 2: 실제 LLM 통합
Chapter 2의 LLM 인터페이스 활용

```bash
cd step2_real_llm
python real_llm_bridge.py
python cached_llm_bridge.py
```

**핵심 개념:**
- 실제 LLM (Ollama/OpenAI) 연동
- 응답 캐싱으로 성능 개선
- 비용 절감

### 단계 3: 도구 시스템
외부 기능 통합

```bash
cd step3_tools
python simple_faq_tool.py
python hybrid_faq_tool.py
```

**핵심 개념:**
- `BaseTool` 상속
- FAQ 데이터베이스 검색
- 하이브리드 검색 (키워드 + 시맨틱)

### 단계 4: 에이전트 패턴
추론-행동 사이클

```bash
cd step4_agent
python simple_react_agent.py
python memory_agent.py
```

**핵심 개념:**
- ReAct 패턴 (Reasoning + Acting)
- 대화 메모리 유지
- 컨텍스트 기반 응답

### 단계 5: 프로덕션 시스템
실전 배포 준비

```bash
cd step5_production
python extended_system.py
```

**핵심 개념:**
- 성능 메트릭 수집
- 세션 관리
- 로그 분석
- A/B 테스트 준비

## 요구사항

### 패키지 설치
```bash
pip install -r requirements.txt
```

주요 패키지:
- `langchain` - LangChain 프레임워크
- `langchain-core` - 핵심 인터페이스
- `langchain-community` - 커뮤니티 도구
- `pydantic` - 데이터 검증
- `sentence-transformers` - 시맨틱 검색
- `rank-bm25` - 키워드 검색

### LLM 설정
Chapter 2의 `llm_interface.py` 필요:
```bash
# chapter2 디렉토리가 있는지 확인
ls ../chapter2/llm_interface.py
```

## 핵심 개념

### 1. LangChain 브리지 패턴
기존 LLM을 LangChain과 연결:

```python
from langchain_core.language_models import BaseLLM

class MyLLMBridge(BaseLLM):
    @property
    def _llm_type(self) -> str:
        return "my-llm"

    def _call(self, prompt: str, stop=None, **kwargs) -> str:
        # 실제 LLM 호출
        return self.llm.generate(prompt)
```

### 2. 도구(Tool) 시스템
에이전트가 사용할 수 있는 기능 정의:

```python
from langchain.tools import BaseTool

class FAQTool(BaseTool):
    name = "faq_search"
    description = "FAQ 데이터베이스에서 답변을 검색합니다"

    def _run(self, query: str) -> str:
        # 검색 로직
        return self.search_faq(query)
```

### 3. ReAct 패턴
추론(Reasoning)과 행동(Acting)을 반복:

```
1. Thought: 무엇을 해야 할까?
2. Action: FAQ를 검색하자
3. Observation: 환불 정책을 찾음
4. Thought: 이제 답변할 수 있다
5. Answer: 환불은 14일 이내 가능합니다
```

### 4. 프로덕션 메트릭
시스템 모니터링:

```python
metrics = {
    'response_time': 0.5,      # 응답 시간
    'cache_hit_rate': 0.8,     # 캐시 적중률
    'tool_usage': {...},       # 도구 사용 통계
    'error_rate': 0.01         # 에러 발생률
}
```

## 각 단계별 학습 목표

### Step 1: 기본 이해
- LangChain 아키텍처 이해
- 브리지 패턴 구현
- 최소 기능 구현

### Step 2: 실용성 추가
- 실제 LLM 통합
- 성능 최적화 (캐싱)
- 비용 관리

### Step 3: 기능 확장
- 외부 데이터 연동
- 검색 품질 개선
- 하이브리드 접근

### Step 4: 지능화
- 추론 능력 추가
- 메모리 관리
- 대화 흐름 제어

### Step 5: 실전 배포
- 모니터링 체계
- 성능 분석
- 지속적 개선

## 실전 팁

### 개발 순서
1. Step 1로 구조 이해
2. Step 2로 실제 LLM 연동
3. Step 3부터 프로젝트 요구사항에 맞게 선택
4. Step 5는 배포 전 필수

### 디버깅
- 각 단계마다 독립적으로 테스트
- 로그를 활용한 문제 추적
- Step 5의 분석 도구 활용

### 성능 최적화
- 캐싱 적극 활용
- 불필요한 LLM 호출 최소화
- 메트릭 기반 병목 지점 파악

## 다음 단계

Chapter 5에서는 이러한 에이전트들이 서로 협업하는 멀티 에이전트 시스템을 구축합니다.
