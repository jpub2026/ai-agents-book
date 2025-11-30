# AI Agents Book - 예제 코드

"AI 에이전트" 책의 예제 코드 리포지토리입니다.

##  챕터별 구성

### [Chapter 2: LLM 기본 원리와 API 활용](./chapter2)
AI 에이전트의 핵심인 LLM(Large Language Model) 이해
- LLM 작동 원리와 시뮬레이터
- 통합 LLM 인터페이스 (Ollama/OpenAI 자동 감지)
- 토큰화와 프롬프트 엔지니어링
- Mock 모드를 통한 테스트

### [Chapter 3: AI 에이전트 핵심 구성요소](./chapter3)
에이전트의 필수 구성요소와 프레임워크 활용
- 메모리 시스템 (단기/장기/작업 기억)
- 도구(Tool) 관리 및 실행
- 계획(Planning) 수립과 실행(Execution)
- LangChain, LangGraph, CrewAI 프레임워크

### [Chapter 4: 실전 AI 에이전트 구축](./chapter4)
단계별로 배우는 실전 에이전트 개발
- LangChain 브리지 패턴
- 실제 LLM 통합 및 캐싱
- 도구 시스템과 하이브리드 검색
- ReAct 패턴과 메모리 통합
- 프로덕션 메트릭 및 모니터링

### [Chapter 5: 협업형 멀티 에이전트](./chapter5)
멀티 에이전트 협업 패턴과 주요 프레임워크 활용
- 기본 협업 시스템
- 조건부 협업
- LangGraph 프레임워크
- CrewAI 프레임워크
- 하이브리드 시스템

### [Chapter 6: MCP 통합](./chapter6)
Model Context Protocol을 활용한 에이전트 통합
- MCP 어댑터 구현
- LangChain/LangGraph/CrewAI 통합
- 통합 워크플로우

### [Chapter 7: MCP 서버/클라이언트](./chapter7)
MCP 기반 에이전트 서버와 클라이언트 구현
- MCP 서버 엔드포인트
- MCP 클라이언트
- 비즈니스 도메인 도구 (고객, 주문, 리포트)

### [Chapter 8: 프로덕션 배포](./chapter8)
Docker 기반 에이전트 배포와 운영
- Docker 컨테이너화
- 로깅 및 모니터링
- 배포/롤백 자동화
- Slack 알림 통합

### [Chapter 9: 고급 최적화](./chapter9)
에이전트 성능 최적화 및 엣지 배포
- 엣지 환경 배포 (Ollama, GGUF)
- 오프라인 RAG 시스템
- 다국어 지원
- 다단계 캐싱 및 체인 최적화

## 시작하기

각 챕터 폴더의 README.md에서 상세한 설명과 실행 방법을 확인하세요.

### 빠른 시작
```bash
# Chapter 2: LLM 기본 원리
cd chapter2
python llm_interface.py

# Chapter 3: 통합 에이전트
cd chapter3/agent
python example.py

# Chapter 4: 단계별 구축
cd chapter4/step1_basic
python simple_llm_bridge.py

# Chapter 5: 멀티 에이전트
cd chapter5/book_examples
python 01_basic_collaboration.py
```

## 공통 요구사항

### 기본 패키지
```bash
# 필수 패키지
pip install requests

# Chapter 3-4: LangChain 기반
pip install langchain langchain-core langchain-community

# Chapter 5-9: 고급 프레임워크
pip install langgraph crewai crewai-tools

# 전체 설치
pip install requests langchain langgraph crewai
```

### LLM 설정 (선택)
```bash
# Ollama (로컬 LLM - 권장)
# 설치: https://ollama.ai
ollama pull llama3.2

# 또는 OpenAI API
export OPENAI_API_KEY='your-api-key'
```

**참고**: Ollama나 OpenAI 없이도 Mock 모드로 모든 예제를 테스트할 수 있습니다.

챕터별 추가 요구사항은 각 폴더의 README를 참조하세요.

