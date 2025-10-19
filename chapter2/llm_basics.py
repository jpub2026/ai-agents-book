import random
from typing import Dict, List

class SimpleLLMSimulator:
    """
    LLM의 기본 원리를 보여주는 간단한 시뮬레이터
    패턴 학습과 예측 과정을 단순화하여 구현합니다
    """
    
    def __init__(self):
        # 학습된 패턴들(실제로는 수조 개)
        self.patterns = {
            "오늘 날씨가": ["좋네요", "맑아요", "흐려요"],
            "파이썬은": ["프로그래밍 언어입니다", "쉽게 배울 수 있습니다"],
            "AI는": ["미래 기술입니다", "우리 생활을 바꿉니다"]
        }
        
        # 각 패턴의 확률(실제로는 학습으로 결정)
        self.probabilities = {
            "오늘 날씨가": [0.5, 0.3, 0.2],
            "파이썬은": [0.6, 0.4],
            "AI는": [0.5, 0.5]
        }
    
    def predict_next(self, text: str) -> str:
        """주어진 텍스트 다음에 올 단어를 예측합니다"""
        # 패턴 찾기 
        for pattern in self.patterns:
            if pattern in text:
                options = self.patterns[pattern]
                probs = self.probabilities[pattern]

                # 확률에 따라 선택
                choice = random.choices(options, weights=probs)[0]
                return f"{text} {choice}"
        
        return f"{text} ..."
    
    def adjust_creativity(self, probs: List[float], temperature: float) -> List[float]:
        """Temperature로 창의성 조절"""
        # 온도가 낮으면 가장 확률 높은 것 선택 
        # 온도가 높으면 다양한 선택 가능
        if temperature < 0.5:
            # 가장 높은 확률 강화
            max_idx = probs.index(max(probs))
            adjusted = [0.1] * len(probs)
            adjusted[max_idx] = 0.9
            return adjusted
        else:
            # 확률 평준화
            return [1/len(probs)] * len(probs)

# 시뮬레이터 테스트
simulator = SimpleLLMSimulator()
print(simulator.predict_next("오늘 날씨가"))
print(simulator.predict_next("파이썬은"))
