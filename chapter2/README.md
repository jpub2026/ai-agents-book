# Chapter 2: LLM 기본 원리와 API 활용

AI 에이전트의 핵심인 LLM(Large Language Model)의 기본 원리를 이해하고, 다양한 API를 활용하는 방법을 배웁니다.

## 학습 내용

### 1. LLM 기본 원리
- LLM의 작동 방식 이해
- 토큰화와 예측 메커니즘
- Temperature와 창의성 제어

### 2. 통합 LLM 인터페이스
- 자동 제공자 감지 (Ollama/OpenAI)
- 통일된 API 사용법
- Mock 모드를 통한 테스트

### 3. 다양한 LLM API
- Ollama 로컬 LLM 활용
- OpenAI API 연동
- 프롬프트 엔지니어링 기법

## 예제 파일

### 기본 예제
- `llm_basics.py` - LLM 시뮬레이터로 기본 원리 이해
- `tokenization.py` - 토큰화 과정 실습
- `prompt_techniques.py` - 효과적인 프롬프트 작성법

### API 활용
- `llm_interface.py` - **통합 LLM 인터페이스** (이 책의 모든 예제에서 사용)
- `ollama_client.py` - Ollama API 사용법
- `openai_api_client.py` - OpenAI API 사용법

### 하이브리드 접근
- `hybrid_basic.py` - Mock과 실제 LLM 자동 전환

## 실행하기

### 1. 기본 원리 학습
```bash
# LLM 시뮬레이터 실행
python llm_basics.py

# 토큰화 실습
python tokenization.py

# 프롬프트 기법 테스트
python prompt_techniques.py
```

### 2. 통합 인터페이스 사용 (권장)
```bash
# 자동으로 사용 가능한 LLM 감지
python llm_interface.py
```

이 인터페이스는:
- Ollama가 실행 중이면 자동으로 Ollama 사용
- OpenAI API 키가 있으면 OpenAI 사용
- 둘 다 없으면 Mock 모드로 테스트 가능

### 3. 개별 API 테스트
```bash
# Ollama (로컬 LLM)
python ollama_client.py

# OpenAI API
python openai_api_client.py
```

## 요구사항

### 필수 패키지
```bash
pip install requests
```

### 선택사항

#### Ollama (로컬 LLM - 권장)
```bash
# Ollama 설치: https://ollama.ai
# 모델 다운로드
ollama pull llama3.2
ollama pull qwen2.5:3b
```

#### OpenAI API
```bash
pip install openai

# API 키 설정
export OPENAI_API_KEY='your-api-key-here'
```

**참고**: Ollama나 OpenAI가 없어도 Mock 모드로 모든 예제를 테스트할 수 있습니다.

## 핵심 개념

### LLM 통합 인터페이스
이 책의 모든 예제에서 사용하는 표준 인터페이스:

```python
from llm_interface import LLM

# 자동 감지 모드
llm = LLM()

# 텍스트 생성
response = llm.generate("파이썬의 장점을 설명해주세요")
print(response)
```

### Temperature 이해
- `0.0` - 가장 확실한 답변 (일관성 높음)
- `0.7` - 균형잡힌 창의성 (기본값)
- `1.0+` - 매우 창의적 (다양성 높음)

### 프롬프트 엔지니어링
효과적인 프롬프트 작성 기법:
- 명확한 지시사항
- 역할 부여 (Role Playing)
- Few-shot 학습 (예시 제공)
- 단계별 사고 (Chain-of-Thought)

## 다음 단계

Chapter 3에서는 이 LLM 인터페이스를 활용하여 본격적인 AI 에이전트를 구축합니다:
- 메모리 시스템
- 도구(Tool) 통합
- 에이전트 프레임워크
