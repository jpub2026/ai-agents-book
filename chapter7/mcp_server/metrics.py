# /mcp_server/metrics.py
from typing import Dict, List
from datetime import datetime

# 전역 메트릭 저장소
METRICS: Dict[str, any] = {
    "requests": 0,  
    "errors": 0,  
    "tool_calls": {},  
    "response_times": [],  
    "last_request_time": None  
}

def increment_request_count():
    """요청 카운터 증가"""
    METRICS["requests"] += 1
    METRICS["last_request_time"] = datetime.now().isoformat()

def increment_error_count():
    """에러 카운터 증가"""
    METRICS["errors"] += 1

def record_tool_call(tool_name: str):
    """도구 호출 기록"""
    if tool_name not in METRICS["tool_calls"]:
        METRICS["tool_calls"][tool_name] = 0
    METRICS["tool_calls"][tool_name] += 1

def record_response_time(time_ms: float):
    """응답 시간 기록 (메모리 관리 포함)"""
    METRICS["response_times"].append(time_ms)
    
    # 최근 1,000개만 유지 (메모리 누수 방지)
    if len(METRICS["response_times"]) > 1000:  
        METRICS["response_times"] = METRICS["response_times"][-1000:]

def get_statistics() -> Dict:
    """통계 계산"""
    response_times = METRICS["response_times"]
    
    stats = {
        "total_requests": METRICS["requests"],
        "total_errors": METRICS["errors"],
        "error_rate": 0,
        "avg_response_time": 0,
        "p95_response_time": 0,  
        "tool_usage": METRICS["tool_calls"],
        "last_request": METRICS["last_request_time"]
    }
    
    # 에러율 계산
    if METRICS["requests"] > 0:
        stats["error_rate"] = (METRICS["errors"] / METRICS["requests"]) * 100
    
    # 응답 시간 통계
    if response_times:
        stats["avg_response_time"] = sum(response_times) / len(response_times)
        
        # P95 계산 (상위 5%를 제외한 최대값)
        sorted_times = sorted(response_times)
        p95_index = int(len(sorted_times) * 0.95)
        stats["p95_response_time"] = sorted_times[p95_index]  
    
    return stats
