# /mcp_server/main.py
import asyncio
import sys
import os

# 상위 디렉토리(chapter7)를 모듈 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from typing import Dict, Any
from models import ToolInfo
from tools.customer import get_customer_tool
from tools.order import process_order_tool
from tools.report import generate_report_tool
from registry import TOOLS
from endpoints import router
from middleware import add_metrics_middleware

# FastAPI 앱 생성
app = FastAPI(
    title="MCP Server",  # ❷
    description="Model Context Protocol Server - 비즈니스 도구 통합",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# 라우터 등록
app.include_router(router)

# 메트릭 미들웨어 추가
add_metrics_middleware(app)

def register_tool(
    name: str, 
    handler: Any, 
    description: str, 
    parameters: Dict[str, Any]
) -> None:
    """
    도구를 전역 레지스트리에 등록
    
    Args:
        name: 도구 고유 식별자
        handler: 실제 실행할 비동기 함수
        description: 도구 설명
        parameters: JSON Schema 파라미터 정의
    """
    TOOLS[name] = {
        "handler": handler,  # ❶
        "info": ToolInfo(
            name=name,
            description=description,
            parameters=parameters
        )  # ❷
    }
    
    print(f" 도구 등록: {name}")  # ❸
    
# 서버 시작 시 도구 등록
@app.on_event("startup")  # ❶
async def register_all_tools():
    """서버 시작 시 모든 도구를 등록"""
    
    # 1. 고객 조회 도구
    register_tool(
        name="get_customer",
        handler=get_customer_tool,
        description="고객 정보를 조회합니다. 구매 이력, 등급, 신용도 포함",
        parameters={
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "고객 ID (예: CUST-12345, VIP-00001)",
                    "pattern": "^(CUST|VIP)-[0-9]{5}$"  # ❷
                },
                "include_orders": {
                    "type": "boolean",
                    "description": "최근 주문 내역 포함 여부",
                    "default": False
                }
            },
            "required": ["customer_id"]  # ❸
        }
    )
    
    # 2. 주문 처리 도구
    register_tool(
        name="process_order",
        handler=process_order_tool,
        description="새로운 주문을 처리합니다. 재고 확인, 결제, 배송 준비 포함",
        parameters={
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "items": {  # ❹
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "product_id": {"type": "string"},
                            "quantity": {"type": "integer", "minimum": 1},
                            "price": {"type": "number", "minimum": 0}
                        },
                        "required": ["product_id", "quantity", "price"]
                    }
                },
                "payment_method": {  # ❺
                    "type": "string",
                    "enum": ["credit_card", "bank_transfer", "mobile_payment"]
                },
                "shipping_address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                        "postal_code": {"type": "string"},
                        "country": {"type": "string", "default": "KR"}
                    },
                    "required": ["street", "city", "postal_code"]
                }
            },
            "required": ["customer_id", "items"]
        }
    )
    
    # 3. 보고서 생성 도구
    register_tool(
        name="generate_report",
        handler=generate_report_tool,
        description="판매 보고서를 생성합니다. 매출, 주문량, 인기 상품 분석 포함",
        parameters={
            "type": "object",
            "properties": {
                "report_type": {
                    "type": "string",
                    "enum": ["daily", "weekly", "monthly", "quarterly", "custom"],
                    "default": "daily"
                },
                "date_range": {
                    "type": "object",
                    "properties": {
                        "start": {"type": "string", "format": "date"},
                        "end": {"type": "string", "format": "date"}
                    }
                },
                "format": {
                    "type": "string",
                    "enum": ["json", "pdf", "excel"],
                    "default": "json"
                },
                "include_charts": {
                    "type": "boolean",
                    "default": False
                }
            },
            "required": []  # ❶
        }
    )
    
    print(f" 총 {len(TOOLS)}개 도구 등록 완료")

if __name__ == "__main__":
    import uvicorn
        
    print(" MCP 서버 시작")
    print(f" - 주소: http://localhost:8000")
    print(f" - 문서: http://localhost:8000/docs")
    print(f" - 헬스체크: http://localhost:8000/health")
    print(f" - 등록 도구: {', '.join(TOOLS.keys())}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
