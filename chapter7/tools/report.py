# /mcp_server/tools/report.py
from typing import Dict
from datetime import datetime, timedelta
import uuid

async def generate_report_tool(params: Dict) -> Dict:
    """
    판매 보고서 생성 도구
    
    데이터 집계 및 분석:
    - 매출 현황
    - 주문 통계
    - 인기 상품
    """
    import json as json_module
    import ast

    report_type = params.get("report_type", "daily")  # ❶
    date_range = params.get("date_range", {})
    output_format = params.get("format", "json")
    include_charts = params.get("include_charts", False)

    # include_charts가 문자열로 전달된 경우 처리
    if isinstance(include_charts, str):
        include_charts = include_charts.lower() in ("true", "1", "yes")

    # date_range가 문자열로 전달된 경우 처리
    if isinstance(date_range, str):
        try:
            # JSON 형식 시도
            date_range = json_module.loads(date_range.replace("'", '"'))
        except:
            try:
                # Python dict 리터럴 형식 시도
                date_range = ast.literal_eval(date_range)
            except:
                date_range = {}

    # 날짜 범위 설정
    if date_range and isinstance(date_range, dict):  # ❷
        # start 또는 start_date 키 지원
        start_date = date_range.get("start", date_range.get("start_date", ""))
        end_date = date_range.get("end", date_range.get("end_date", ""))
    else:
        start_date = ""
        end_date = ""

    # 날짜가 비어있으면 기본값 사용: 최근 7일
    if not start_date or not end_date:
        end_date = datetime.now().date().isoformat()
        start_date = (datetime.now() - timedelta(days=7)).date().isoformat()
    
    # 보고서 데이터 생성 (실제로는 DB 집계)
    report_data = {  # ❸
        "report_id": f"RPT-{uuid.uuid4().hex[:8].upper()}",
        "type": report_type,
        "period": {
            "start": start_date,
            "end": end_date
        },
        "summary": {
            "total_revenue": 15750000,
            "total_orders": 342,
            "average_order_value": 46052,
            "new_customers": 67
        },
        "top_products": [  # ❹
            {
                "product_id": "PRD-001",
                "name": "프리미엄 노트북",
                "sales_count": 45,
                "revenue": 6750000
            },
            {
                "product_id": "PRD-002", 
                "name": "무선 이어폰",
                "sales_count": 123,
                "revenue": 3690000
            }
        ]
    }
    
    # 차트 데이터 포함
    if include_charts:  # ❶
        report_data["charts"] = {
            "daily_revenue": [
                {"date": "2024-12-01", "amount": 2100000},
                {"date": "2024-12-02", "amount": 1950000},
                {"date": "2024-12-03", "amount": 2300000}
            ],
            "category_distribution": [
                {"category": "전자제품", "percentage": 45},
                {"category": "의류", "percentage": 30},
                {"category": "도서", "percentage": 25}
            ]
        }
    
    # 파일 정보
    file_info = {  # ❷
        "filename": f"sales_report_{report_type}_{datetime.now().strftime('%Y%m%d')}.{output_format}",
        "size_kb": 247,
        "download_url": f"/reports/{report_data['report_id']}.{output_format}"
    }
    
    return {
        "success": True,
        "report": report_data,
        "file": file_info,
        "generated_at": datetime.now().isoformat()
    }

