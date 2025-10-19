# /mcp_server/tools/order.py
from typing import Dict
from datetime import datetime, timedelta
import uuid
import random

async def process_order_tool(params: Dict) -> Dict:
    """
    주문 처리 도구
    
    복잡한 비즈니스 프로세스:
    1. 입력 검증
    2. 재고 확인  
    3. 가격 계산
    4. 결제 처리
    5. 배송 준비
    """
    # 입력 검증
    customer_id = params.get("customer_id", "")  # ❶
    items = params.get("items", [])
    payment_method = params.get("payment_method", "credit_card")
    shipping_address = params.get("shipping_address", {})
    
    if not customer_id:  # ❷
        return {
            "success": False,
            "error": "customer_id is required",
            "error_code": "MISSING_CUSTOMER_ID"
        }
    
    if not items:  # ❸
        return {
            "success": False,
            "error": "items list cannot be empty",
            "error_code": "EMPTY_CART"
        }
        
    # 주문 ID 생성
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"  # ❶
    
    # 가격 계산 로직
    total_amount = sum(
        item.get("price", 0) * item.get("quantity", 1) 
        for item in items
    )  # ❷
    
    # 조건부 배송비
    shipping_fee = 0 if total_amount >= 50000 else 3000  # ❸
    
    # 고객 등급별 할인
    discount = 0
    if customer_id.startswith("VIP"):  # ❹
        discount = int(total_amount * 0.1)  # VIP 10% 할인
    
    final_amount = total_amount + shipping_fee - discount
    
    # 재고 확인 시뮬레이션
    inventory_check = random.choice([True, True, True, False])  # 75% 성공률  # ❺
    
    if not inventory_check:
        return {
            "success": False,
            "error": "Some items are out of stock",
            "error_code": "OUT_OF_STOCK",
            "unavailable_items": [items[0].get("product_id")] if items else []
        }
        
    # 결제 처리 시뮬레이션
    payment_result = {  # ❶
        "transaction_id": f"TXN-{uuid.uuid4().hex[:12].upper()}",
        "payment_method": payment_method,
        "amount": final_amount,
        "status": "approved",
        "approval_code": f"APR{random.randint(100000, 999999)}"
    }
    
    # 배송일 계산
    estimated_delivery = (datetime.now() + timedelta(days=3)).date().isoformat()  # ❷
    
    return {
        "success": True,
        "order_id": order_id,
        "customer_id": customer_id,
        "items": items,
        "pricing": {
            "subtotal": total_amount,
            "shipping_fee": shipping_fee,
            "discount": discount,
            "total": final_amount
        },
        "payment": payment_result,
        "shipping": {
            "address": shipping_address,
            "estimated_delivery": estimated_delivery,
            "tracking_number": f"TRK{order_id[-8:]}"
        },
        "status": "confirmed",
        "created_at": datetime.now().isoformat()
    }


