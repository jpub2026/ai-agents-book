from abc import ABC, abstractmethod
from typing import Any, Dict, List
from datetime import datetime

# 코드 2-6의 통합 LLM 인터페이스를 import
import sys
sys.path.append('../chapter2')
from llm_interface import LLM

class BaseTool(ABC):
    """
    모든 도구의 기본 클래스
    """
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.usage_count = 0
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Any:
        """도구를 실행하는 추상 메서드"""
        pass
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """입력 데이터의 유효성을 검증"""
        return True  # 각 도구가 오버라이드하여 구현

class WebSearchTool(BaseTool):
    """
    웹 검색을 수행하는 도구
    """
    def __init__(self, api_key: str):
        super().__init__(
            name="web_search",
            description="인터넷에서 정보를 검색합니다"
        )
        self.api_key = api_key
    
    def execute(self, input_data: Dict[str, Any]) -> Any:
        query = input_data.get('query')
        if not query:
            raise ValueError("검색어가 필요합니다")
        
        # 실제 검색 수행
        results = self._perform_search(query)
        
        # 결과 포맷팅 및 관련성 점수 계산
        formatted = [{
            'title': r['title'],
            'url': r['url'],
            'relevance': self._calculate_relevance(query, r)
        } for r in results]
        
        return formatted
    
    def _perform_search(self, query: str) -> List:
        # 실제 API 호출 (여기서는 간단한 시뮬레이션)
        return [{'title': f"Result for {query}", 'url': "http://..."}]
    
    def _calculate_relevance(self, query: str, result: dict) -> float:
        # 검색어와 결과의 관련성 점수 계산
        return 0.8  # 실제로는 복잡한 로직

class ToolManager:
    """
    모든 도구를 관리하는 클래스
    """
    def __init__(self, llm=None):
        self.tools = {}  # ❻
        self.llm = llm or LLM()  # 통합 LLM 인터페이스 사용
    
    def register_tool(self, tool: BaseTool):
        """도구를 등록합니다"""
        self.tools[tool.name] = tool
        print(f" 도구 등록됨: {tool.name}")
    
    def get_tool(self, name: str) -> BaseTool:
        """이름으로 도구를 가져옵니다"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """등록된 모든 도구의 이름을 반환합니다"""
        return list(self.tools.keys())
    
    def select_best_tool(self, task_description: str) -> BaseTool:
        """작업에 가장 적합한 도구를 자동 선택합니다"""
        
        # 도구 정보를 프롬프트에 포함
        tools_info = "\n".join([
            f"- {name}: {tool.description}"
            for name, tool in self.tools.items()
        ])
        
        prompt = f"""
        작업: {task_description}
        
        사용 가능한 도구:
        {tools_info}
        
        가장 적합한 도구 이름만 반환하세요.
        """
        
        # LLM을 사용하여 도구 선택
        selected = self.llm.generate(prompt, temperature=0.3, max_tokens=50)
        
        return self.tools.get(selected.strip()) or list(self.tools.values())[0]
