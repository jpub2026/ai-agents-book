"""
FAQ 검색 도구 - 간단한 버전
목표: 미리 준비된 FAQ에서 답변 찾기
"""

from langchain_core.tools import BaseTool
from typing import Optional, Type, Any
from pydantic import BaseModel, Field

# Pydantic 모델로 입력 스키마 정의  # ❶
class FAQSearchInput(BaseModel):
    """FAQ 검색 도구의 입력 스키마"""
    query: str = Field(description="검색할 질문 또는 키워드")

class SimpleFAQTool(BaseTool):
    """간단한 FAQ 검색 도구"""

    name: str = "faq_search"
    description: str = "FAQ 데이터베이스에서 정보를 검색합니다. 환불, 배송, 교환 등의 정책 정보를 찾을 때 사용하세요."  # ❷
    args_schema: Type[BaseModel] = FAQSearchInput  # ❸

    # 간단한 FAQ 데이터를 미리 준비합니다
    faq_data: dict = Field(default_factory=lambda: {
        "환불": {
            "answer": "환불은 구매일로부터 14일 이내에 가능합니다.",
            "details": "제품은 미개봉 상태여야 하며, 영수증이 필요합니다."
        },
        "배송": {
            "answer": "표준 배송은 3-5 영업일이 소요됩니다.",
            "details": "특급 배송(1-2일)도 가능하며, 추가 요금이 발생합니다."
        },
        "교환": {
            "answer": "제품 교환은 수령 후 7일 이내 가능합니다.",
            "details": "사이즈나 색상 교환이 가능하며, 재고가 있어야 합니다."
        }
    })
    
    def _run(
        self,
        query: str,
        run_manager: Optional[Any] = None
    ) -> str:
        """도구를 실행하는 메서드"""
        
        query_lower = query.lower()
        
        for keyword, info in self.faq_data.items():
            if keyword in query_lower:
                return f"{info['answer']}\n추가 정보: {info['details']}"
        
        return ("해당 정보를 찾을 수 없습니다.\n"
                "검색 가능한 주제: 환불, 배송, 교환\n"
                "고객센터: 1234-5678")
    
    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        """비동기 버전"""
        return self._run(query)
