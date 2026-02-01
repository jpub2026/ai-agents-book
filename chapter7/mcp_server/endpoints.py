# /mcp_server/endpoints.py
from fastapi import APIRouter
from typing import Dict, Any, List
from datetime import datetime
import psutil

from registry import TOOLS
from models import MCPRequest, MCPResponse
from metrics import get_statistics

router = APIRouter(prefix="/mcp", tags=["MCP Protocol"])


@router.get("/tools", response_model=Dict[str, Any])  
async def list_tools():
    """
    사용 가능한 모든 도구 목록 반환
    
    Returns:
        tools: 도구 정보 리스트
        count: 도구 개수
    """
    tools_list = []
    
    for name, tool_data in TOOLS.items(): 
        tools_list.append({
            "name": name,
            "description": tool_data["info"].description,
            "parameters": tool_data["info"].parameters
        })
    
    return {
        "tools": tools_list,
        "count": len(tools_list)  
    }

@router.post("/execute", response_model=MCPResponse)  
async def execute_mcp(request: MCPRequest):  
    """
    MCP 요청 처리 - JSON-RPC 2.0 프로토콜
    
    지원 메서드:
    - tools/list: 도구 목록 조회
    - tools/call: 도구 실행
    """
    try:
        method = request.method
        params = request.params or {}
        
        # 1. tools/list 메서드
        if method == "tools/list":  
            tools_list = []
            for name, tool_data in TOOLS.items():
                tools_list.append({
                    "name": name,
                    "description": tool_data["info"].description,
                    "inputSchema": tool_data["info"].parameters  
                })
            
            return MCPResponse(
                id=request.id,
                result={"tools": tools_list}
            )
        # 2. tools/call 메서드
        elif method == "tools/call":  
            tool_name = params.get("name")
            tool_params = params.get("arguments", {})
            
            # 도구 존재 확인
            if tool_name not in TOOLS:  
                return MCPResponse(
                    id=request.id,
                    error={
                        "code": -32601,  # Method not found
                        "message": f"Tool not found: {tool_name}"
                    }
                )
            
            # 도구 실행
            handler = TOOLS[tool_name]["handler"]  
            result = await handler(tool_params)  
            
            return MCPResponse(
                id=request.id,
                result=result
            )
        
        # 3. 알 수 없는 메서드
        else:  
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            )
            
    except Exception as e:  
        return MCPResponse(
            id=request.id,
            error={
                "code": -32603,  # Internal error
                "message": str(e)
            }
        )

@router.get("/health")
async def health_check():
    """서버 상태 확인"""
    
    is_healthy = True
    issues = []
    
    # 1. 도구 등록 확인
    if len(TOOLS) == 0:  
        is_healthy = False
        issues.append("No tools registered")
    
    # 2. 메모리 사용량 확인  
    memory_percent = psutil.virtual_memory().percent  
    if memory_percent > 90:
        is_healthy = False
        issues.append(f"High memory usage: {memory_percent}%")
    
    # 3. CPU 사용량 확인
    cpu_percent = psutil.cpu_percent(interval=0.1)  
    if cpu_percent > 90:
        is_healthy = False
        issues.append(f"High CPU usage: {cpu_percent}%")
    
    return {
        "status": "healthy" if is_healthy else "degraded",  
        "timestamp": datetime.now().isoformat(),
        "tools_count": len(TOOLS),
        "system": {
            "memory_percent": memory_percent,
            "cpu_percent": cpu_percent
        },
        "issues": issues
    }

@router.get("/metrics")
async def get_metrics():
    """성능 메트릭 조회"""
    return get_statistics()  


