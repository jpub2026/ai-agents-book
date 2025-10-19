# AI Agents Book - 예제 코드

"AI 에이전트" 책의 예제 코드 리포지토리입니다.

## 📚 챕터별 구성

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

## 🚀 시작하기

각 챕터 폴더의 README.md에서 상세한 설명과 실행 방법을 확인하세요.

```bash
# 예제 실행
cd chapter5/book_examples
python 01_basic_collaboration.py
```

## 📋 공통 요구사항

```bash
pip install python-docx langgraph crewai langchain
```

챕터별 추가 요구사항은 각 폴더의 README를 참조하세요.

## 📖 출처

jpub2026/ai-agents-book 리포지토리 기반
