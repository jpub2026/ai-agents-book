# /mcp_server/tools/customer.py
from typing import Dict
from datetime import datetime

async def get_customer_tool(params: Dict) -> Dict:
    """
    고객 정보 조회 도구
    
    실제 환경에서는 데이터베이스 쿼리를 수행하지만
    여기서는 CRM 시스템을 시뮬레이션합니다.
    """
    customer_id = params.get("customer_id", "")  # ❶
    include_orders = params.get("include_orders", False)  # ❷
    
    # 고객 ID 패턴 분석
    customer_data = {
        "customer_id": customer_id,
        "name": f"고객_{customer_id[-3:]}",  # ❸
        "email": f"customer_{customer_id}@example.com",
        "created_at": "2024-01-15T10:30:00Z",
        "tier": "gold" if customer_id.startswith("VIP") else "silver",  # ❹
        "total_spent": 1250000 if customer_id.startswith("VIP") else 450000,
        "last_login": datetime.now().isoformat()
    }
    
    # 선택적 주문 내역 포함
    if include_orders:  # ❶
        customer_data["recent_orders"] = [
            {
                "order_id": f"ORD-{customer_id}-001",
                "date": "2024-12-01",
                "amount": 89000,
                "status": "delivered"
            },
            {
                "order_id": f"ORD-{customer_id}-002", 
                "date": "2024-12-15",
                "amount": 125000,
                "status": "processing"
            }
        ]
    
    # 비즈니스 로직: 신용도 점수 계산
    credit_score = 700  # ❷
    if customer_data["tier"] == "gold":
        credit_score += 50
    if customer_data["total_spent"] > 1000000:
        credit_score += 30
    customer_data["credit_score"] = credit_score
    
    return {
        "success": True,
        "data": customer_data,
        "query_time_ms": 42,  # ❸
        "cached": False,
        "timestamp": datetime.now().isoformat()
    }

