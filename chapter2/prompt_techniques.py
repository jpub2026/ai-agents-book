class PromptTechniques:
    """
    다양한 프롬프트 기법을 보여주는 예제 클래스
    """
    
    def zero_shot_example(self):
        """Zero-shot: 예시 없이 직접 질문"""
        prompt = "파이썬의 장점을 설명해주세요."
        return prompt

    def few_shot_example(self):
        """Few-shot: 예시를 통한 패턴 학습"""
        prompt = """
        다음 패턴을 따라주세요:
        
        입력: 사과
        출력: 빨간색 과일
        
        입력: 바나나  
        출력: 노란색 과일
        
        입력: 포도
        출력:
        """
        return prompt

    def chain_of_thought_example(self):
        """Chain of Thought: 단계별 사고"""
        prompt = """
        다음 문제를 단계별로 풀어주세요:
        
        문제: 가게에 사과가 10개 있었습니다. 
        오전에 3개를 팔고, 오후에 5개를 더 받았습니다.
        지금 사과는 몇 개입니까?
        
        1단계: 처음 개수 확인
        2단계: 판매한 개수 빼기
        3단계: 새로 받은 개수 더하기
        4단계: 최종 답 계산
        """
        return prompt

    def role_playing_example(self):
        """Role Playing: 역할 부여"""
        prompt = """
        당신은 초등학교 선생님입니다.
        아이들이 이해하기 쉽게 설명해주세요.
        
        질문: 컴퓨터는 어떻게 작동하나요?
        """
        return prompt

# 각 기법의 프롬프트 확인
techniques = PromptTechniques()
print("Zero-shot:", techniques.zero_shot_example())
print("\nFew-shot:", techniques.few_shot_example())
