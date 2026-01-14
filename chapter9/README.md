# Chapter 9: 고급 최적화 기법

RAG, 다국어 처리, 프롬프트 최적화, 엣지 배포 등 에이전트 시스템의 고급 기법을 다루는 예제입니다.

## 프로젝트 구조

```
chapter9/
├── rag/                                # RAG (검색 증강 생성)
│   ├── agent.py                       # RAG 에이전트
│   ├── answer.py                      # 답변 생성
│   ├── decision.py                    # 검색 필요 여부 판단
│   ├── indexing.py                    # 문서 인덱싱
│   ├── models.py                      # 데이터 모델
│   ├── pipeline.py                    # RAG 파이프라인
│   └── retrieval.py                   # 문서 검색
├── multilingual/                       # 다국어 처리
│   ├── config.py                      # 언어별 설정
│   ├── pipeline.py                    # 다국어 파이프라인
│   └── router.py                      # 언어 감지 및 라우팅
├── processors/                         # 언어별 프로세서
│   ├── base.py                        # 기본 프로세서
│   ├── korean.py                      # 한국어 처리
│   ├── english.py                     # 영어 처리
│   └── japanese.py                    # 일본어 처리
├── optimization/                       # 성능 최적화
│   ├── chain.py                       # 최적화된 체인
│   ├── metrics.py                     # 성능 메트릭
│   ├── analysis.py                    # 성능 분석
│   ├── chache/                        # 캐싱
│   │   ├── multilevel.py             # 다단계 캐시
│   │   ├── retrieval.py              # 검색 캐시
│   │   └── storage.py                # 캐시 스토리지
│   └── prompt/                        # 프롬프트 최적화
│       ├── optimizer.py              # 프롬프트 최적화
│       ├── compression.py            # 프롬프트 압축
│       └── cleaning.py               # 프롬프트 정제
└── edge/                               # 엣지 환경 배포
    ├── ollama/                        # Ollama 통합
    │   └── generation.py
    ├── gguf/                          # GGUF 모델 지원
    │   ├── loader.py
    │   └── client.py
    ├── offline/                       # 오프라인 시스템
    │   ├── cache.py
    │   ├── database.py
    │   ├── documents.py
    │   ├── statistics.py
    │   └── system.py
    └── adaptive/                      # 적응형 시스템
        ├── config.py
        ├── selection.py
        └── system.py
```

## 주요 개념

### 1. RAG (Retrieval-Augmented Generation)
검색을 통해 관련 문서를 찾아 더 정확한 답변 생성

### 2. 다국어 처리
언어 감지, 전처리, 후처리를 통한 글로벌 서비스

### 3. 성능 최적화
캐싱, 프롬프트 압축으로 응답 속도 및 비용 개선

### 4. 엣지 배포
네트워크 제약이 있는 환경에서 로컬 모델 실행

## 모듈별 상세 설명

## 1. RAG (검색 증강 생성)

문서 검색과 생성 AI를 결합하여 더 정확하고 근거 있는 답변 제공

### `pipeline.py` - RAG 파이프라인
TF-IDF 기반 문서 검색 시스템
```python
class RAGPipeline:
    def __init__(self, chunk_size=500, overlap=50)
    # 문서를 청크로 분할하고 벡터화
```

**주요 기능:**
- 문서 청킹 (chunk_size, overlap 설정)
- TF-IDF 벡터화
- 코사인 유사도 검색

### `agent.py` - RAG 에이전트
문서 검색을 활용하는 증강 에이전트
```python
class RAGAgent:
    def __init__(self, rag_pipeline, mcp_client, use_citations=True)
```

**주요 기능:**
- MCP 클라이언트와 통합
- 인용(citation) 지원
- 검색 결과 기반 답변 생성

### `decision.py` - 검색 필요 여부 판단
쿼리 분석을 통해 RAG 검색 필요성 결정

### `retrieval.py` - 문서 검색
벡터 검색 및 순위 결정

### `indexing.py` - 문서 인덱싱
문서를 검색 가능한 형태로 색인

### `answer.py` - 답변 생성
검색된 문서를 기반으로 최종 답변 생성

### `models.py` - 데이터 모델
RAG 관련 데이터 구조 정의

## 2. 다국어 처리

한국어, 영어, 일본어 등 다양한 언어 지원

### `router.py` - 언어 라우터
언어 감지 및 적절한 프로세서 선택

### `pipeline.py` - 다국어 파이프라인
```python
class MultilingualPipeline:
    async def process(self, query: str) -> Dict[str, Any]:
        lang = self.router.detect_language(query)
        processor = self.processors.get(lang)
        preprocessed = processor.preprocess(query)
        # ... MCP 호출
        postprocessed = processor.postprocess(result)
```

**처리 흐름:**
1. 언어 감지
2. 언어별 전처리
3. 언어별 프롬프트 생성
4. MCP 도구 호출
5. 언어별 후처리

### `config.py` - 언어별 설정
언어별 스타일, 템플릿, 제약사항 정의

### Processors (언어별 프로세서)

#### `base.py` - 기본 프로세서
모든 언어 프로세서의 베이스 클래스

#### `korean.py` - 한국어 프로세서
- 한국어 특화 전처리
- 존댓말/반말 처리
- 맞춤법 정리

#### `english.py` - 영어 프로세서
- 영어 전처리
- 대소문자 처리
- 문법 교정

#### `japanese.py` - 일본어 프로세서
- 일본어 전처리
- 경어 처리
- 문자 변환

## 3. 성능 최적화

### `chain.py` - 최적화된 체인
```python
class OptimizedChain:
    async def plan(self, query: str) -> Dict[str, Any]:
        # 캐시 확인
        if cache_key in self.cache:
            return self.cache[cache_key]

        # 쿼리 분석
        plan = {
            "needs_search": self._analyze_search_need(query),
            "complexity": self._assess_complexity(query)
        }
```

**최적화 기법:**
- 쿼리 분석 캐싱
- 복잡도 평가
- 동적 전략 수립

### `metrics.py` - 성능 메트릭
실행 시간, 캐시 히트율 등 측정

### `analysis.py` - 성능 분석
병목 구간 분석 및 개선점 도출

### Cache (캐싱 시스템)

#### `multilevel.py` - 다단계 캐시
L1 (메모리) → L2 (Redis) → L3 (디스크) 캐시 구조

#### `retrieval.py` - 검색 캐시
문서 검색 결과 캐싱

#### `storage.py` - 캐시 스토리지
영구 저장소 관리

### Prompt (프롬프트 최적화)

#### `optimizer.py` - 프롬프트 최적화
```python
class PromptOptimizer:
    def optimize(self, prompt: str, priority: str = "balanced") -> str:
        prompt = self._remove_duplicates(prompt)
        prompt = self._clean_whitespace(prompt)

        if len(prompt) > self.max_length:
            prompt = self._compress(prompt)
```

**최적화 전략:**
- 중복 제거
- 공백 정리
- 우선순위 기반 압축
- 구조 재조정

#### `compression.py` - 프롬프트 압축
토큰 수 절감을 위한 압축

#### `cleaning.py` - 프롬프트 정제
불필요한 요소 제거

## 4. 엣지 환경 배포

### Ollama 통합

#### `ollama/generation.py`
Ollama를 활용한 로컬 모델 실행
- 로컬 LLM 추론
- 네트워크 독립 실행

### GGUF 모델 지원

#### `gguf/loader.py`
GGUF 포맷 모델 로딩
- 양자화 모델 지원
- 메모리 효율적 로딩

#### `gguf/client.py`
GGUF 모델 클라이언트

### Offline (오프라인 시스템)

#### `offline/system.py`
완전 오프라인 RAG 시스템
- 로컬 문서 데이터베이스
- 오프라인 검색
- 캐시 기반 응답

#### `offline/database.py`
오프라인 문서 DB

#### `offline/documents.py`
문서 관리

#### `offline/cache.py`
오프라인 캐시

#### `offline/statistics.py`
통계 수집 및 분석

### Adaptive (적응형 시스템)

#### `adaptive/system.py`
```python
class EdgeAdaptiveSystem:
    def _detect_device_profile(self) -> Dict[str, Any]:
        return {
            "cpu_count": psutil.cpu_count(),
            "memory_gb": psutil.virtual_memory().total / (1024**3),
            "gpu_available": self._check_gpu()
        }
```

**적응형 기능:**
- 디바이스 프로파일 자동 감지
- 하드웨어 기반 모델 선택
- 최적화 레벨 자동 결정

#### `adaptive/config.py`
적응형 설정 관리

#### `adaptive/selection.py`
모델 선택 로직

## 사용 방법

### 1. RAG 시스템

```bash
cd rag

# 문서 인덱싱
python indexing.py

# RAG 파이프라인 실행
python pipeline.py

# RAG 에이전트 실행
python agent.py
```

**실습:**
1. 문서 준비
2. 인덱싱 실행
3. 쿼리 테스트
4. 검색 결과 확인

### 2. 다국어 처리

```bash
cd multilingual

# 다국어 파이프라인 테스트
python pipeline.py

# 언어 라우터 테스트
python router.py
```

**테스트 쿼리:**
- 한국어: "안녕하세요, 도움이 필요합니다"
- 영어: "Hello, I need help"
- 일본어: "こんにちは、助けが必要です"

### 3. 성능 최적화

```bash
cd optimization

# 최적화된 체인 실행
python chain.py

# 성능 메트릭 수집
python metrics.py

# 성능 분석
python analysis.py

# 프롬프트 최적화
python prompt/optimizer.py
```

### 4. 엣지 배포

#### Ollama 사용
```bash
cd edge/ollama

# Ollama 설치 필요
curl -fsSL https://ollama.ai/install.sh | sh

# 모델 다운로드
ollama pull llama2

# 실행
python generation.py
```

#### GGUF 모델 사용
```bash
cd edge/gguf

# GGUF 모델 다운로드 (예: llama.cpp 호환 모델)
# 모델 로드 및 실행
python client.py
```

#### 오프라인 시스템
```bash
cd edge/offline

# 문서 준비 및 DB 구축
python documents.py

# 오프라인 시스템 실행
python system.py
```

#### 적응형 시스템
```bash
cd edge/adaptive

# 디바이스 자동 감지 및 실행
python system.py
```

## 실습 시나리오

### 시나리오 1: RAG 시스템 구축
1. 기술 문서 수집
2. 문서 인덱싱
3. 질문-답변 테스트
4. 인용 출처 확인

### 시나리오 2: 다국어 챗봇
1. 3개 언어 지원 설정
2. 언어 감지 테스트
3. 언어별 응답 스타일 확인
4. 혼합 언어 처리

### 시나리오 3: 성능 튜닝
1. 기본 응답 시간 측정
2. 캐싱 활성화
3. 프롬프트 압축 적용
4. 개선 효과 비교

### 시나리오 4: 엣지 배포
1. Ollama 설치 및 설정
2. 로컬 모델로 전환
3. 오프라인 모드 테스트
4. 적응형 최적화 확인

## 커스터마이징

### RAG 검색 개선
```python
# pipeline.py
self.vectorizer = TfidfVectorizer(
    max_features=2000,  # 더 많은 특징 사용
    ngram_range=(1, 3)  # trigram까지 확장
)
```

### 언어 추가
```python
# processors/chinese.py
class ChineseProcessor(BaseProcessor):
    def preprocess(self, text: str) -> str:
        # 중국어 전처리 로직
```

### 캐시 레벨 설정
```python
# optimization/cache/multilevel.py
cache = MultilevelCache(
    l1_size=1000,      # 메모리 캐시
    l2_enabled=True,   # Redis
    l3_enabled=True    # 디스크
)
```

## 성능 비교

### 캐싱 효과
- 캐시 없음: ~2000ms
- L1 캐시: ~50ms (40배 개선)
- L2 캐시: ~200ms (10배 개선)

### 프롬프트 압축 효과
- 원본: 3000 토큰
- 압축 후: 2100 토큰 (30% 절감)
- 비용 절감: 30%
- 응답 시간: 20% 개선

### 엣지 vs 클라우드
- 클라우드 API: 200-500ms (네트워크 포함)
- Ollama 로컬: 100-300ms
- GGUF 양자화: 50-150ms

## 트러블슈팅

### RAG 검색 정확도 낮음
- 청크 크기 조정 (`chunk_size`, `overlap`)
- 벡터화 파라미터 튜닝
- 문서 품질 개선

### 다국어 감지 실패
- 언어 라이브러리 업데이트
- 감지 임계값 조정
- 혼합 언어 처리 로직 추가

### 캐시 메모리 부족
- L1 캐시 크기 축소
- TTL 설정으로 자동 만료
- L2/L3 우선 사용

### Ollama 연결 실패
```bash
# Ollama 서비스 확인
ollama list

# 서비스 재시작
systemctl restart ollama
```

## 관련 챕터

- Chapter 5: 멀티 에이전트 협업
- Chapter 6: MCP 통합
- Chapter 7: MCP 서버/클라이언트
- Chapter 8: 프로덕션 배포

## 체크리스트

### RAG 구축
- [ ] 문서 수집 완료
- [ ] 인덱싱 성공
- [ ] 검색 테스트
- [ ] 답변 품질 확인

### 다국어 지원
- [ ] 언어 감지 정확도 90% 이상
- [ ] 언어별 프로세서 동작 확인
- [ ] 응답 스타일 적절성 검증

### 성능 최적화
- [ ] 캐시 히트율 측정
- [ ] 응답 시간 개선 확인
- [ ] 비용 절감 효과 분석

### 엣지 배포
- [ ] Ollama 설치 및 모델 다운로드
- [ ] 오프라인 모드 테스트
- [ ] 디바이스 적응형 동작 확인

## 심화 학습 주제

이 챕터의 개념을 더 깊이 탐구하고 싶다면:

### RAG 고도화
- 벡터 DB 통합 (Pinecone, Weaviate, Qdrant)
- 하이브리드 검색 (키워드 + 의미 검색 결합)
- 리랭킹 모델 적용
- 멀티모달 RAG (이미지 + 텍스트)

### 다국어 확장
- 더 많은 언어 지원 (중국어, 스페인어, 프랑스어 등)
- 언어별 파인튜닝 모델
- 번역 품질 개선
- 문화적 맥락 고려

### 성능 극대화
- GPU 가속 활용
- 배치 처리 최적화
- 모델 양자화 (4-bit, 8-bit)
- 토큰 스트리밍

### 프로덕션 안정화
- A/B 테스트 프레임워크
- 품질 모니터링 대시보드
- 자동 롤백 시스템
- 비용 최적화 전략

이 챕터의 기법들을 Chapter 5-8의 내용과 결합하면 프로덕션급 AI 에이전트 시스템을 완성할 수 있습니다!
