from collections import deque
from datetime import datetime
from typing import Dict, List, Any
import uuid

class MemorySystem:
    """
    에이전트의 기억 시스템
    단기, 장기, 작업 기억을 통합 관리합니다
    """
    
    def __init__(self, vector_store=None):
        # 단기 기억: 최근 100개 상호작용만 유지
        self.short_term_memory = deque(maxlen=100)

        # 장기 기억: 중요한 정보를 영구 저장
        self.long_term_memory = []  # 실제로는 벡터 DB 사용

        # 작업 기억: 현재 작업 컨텍스트
        self.working_memory = {}
        
        self.importance_threshold = 0.7
    
    def store(self, information: Dict, memory_type: str = 'short'):
        """
        정보를 메모리에 저장합니다
        """
        information['timestamp'] = datetime.now()
        information['id'] = str(uuid.uuid4())
        
        if memory_type == 'short':
            self.short_term_memory.append(information)
            
            # 중요도 평가하여 장기 기억으로 승격  ❹
            if self._evaluate_importance(information) > self.importance_threshold:
                self.long_term_memory.append(information)
                print(f" 중요 정보를 장기 기억으로 승격")
                
        elif memory_type == 'working':
            # 작업 기억에 저장
            key = information.get('key', information['id'])
            self.working_memory[key] = information
    
    def retrieve(self, query: str, memory_type: str = 'all', k: int = 5) -> List:
        """
        관련 기억을 검색합니다
        """
        results = []
        
        # 작업 기억에서 먼저 검색 (가장 빠름)
        if memory_type in ['all', 'working']:
            for value in self.working_memory.values():
                if query.lower() in str(value).lower():
                    results.append(value)
        
        # 단기 기억에서 검색
        if memory_type in ['all', 'short']:
            for memory in self.short_term_memory:
                if query.lower() in str(memory).lower():
                    results.append(memory)
        
        # 장기 기억에서 검색
        if memory_type in ['all', 'long']:
            for memory in self.long_term_memory:
                if query.lower() in str(memory).lower():
                    results.append(memory)
        
        # 최근 것부터 반환
        return sorted(results, 
                     key=lambda x: x.get('timestamp', datetime.min), 
                     reverse=True)[:k]
    
    def _evaluate_importance(self, information: Dict) -> float:
        """정보의 중요도를 평가합니다"""
        score = 0.5  # 기본 점수
        
        # 특정 키워드가 있으면 중요도 상승
        important_keywords = ['중요', '기억', '반드시', 'important', 'remember']
        content = str(information.get('content', '')).lower()
        
        for keyword in important_keywords:
            if keyword in content:
                score += 0.3
                break
        
        # 사용자가 명시적으로 중요하다고 표시한 경우
        if information.get('is_important', False):
            score = 1.0
        
        return min(score, 1.0)
    
    def clear_working_memory(self):
        """작업 기억을 비웁니다 (작업 완료 시)"""
        self.working_memory.clear()
        print("작업 기억이 초기화되었습니다")
