# /mcp_server/models.py
from pydantic import BaseModel, Field, model_validator  # ❶
from typing import Dict, List, Any, Optional, Literal  # ❷
from datetime import datetime

class MCPRequest(BaseModel):
    """MCP 요청 모델 - JSON-RPC 2.0 표준 준수"""

    jsonrpc: Literal["2.0"] = "2.0"  # ❶
    method: str = Field(..., description="호출할 메서드명")  # ❷
    params: Optional[Dict[str, Any]] = Field(
        default={},
        description="메서드에 전달할 매개변수"
    )  # ❸
    id: Optional[str] = Field(
        default=None,
        description="요청 식별자 (None이면 알림)"
    )  # ❹

    class Config:
        json_schema_extra = {
            "example": {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "get_customer",
                    "arguments": {"customer_id": "CUST-12345"}
                },
                "id": "req-001"
            }
        }

class MCPResponse(BaseModel):
    """MCP 응답 모델 - 성공 시 result, 실패 시 error 포함"""

    jsonrpc: Literal["2.0"] = "2.0"
    id: Optional[str] = None
    result: Optional[Any] = None  # ❶
    error: Optional[Dict[str, Any]] = None  # ❷

    @model_validator(mode='after')
    def check_result_or_error(self):  # ❸
        """result와 error는 상호 배타적"""
        if self.result is not None and self.error is not None:
            raise ValueError('result와 error는 동시에 존재할 수 없음')
        if self.result is None and self.error is None:
            raise ValueError('result 또는 error 중 하나는 반드시 존재해야 함')
        return self

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "jsonrpc": "2.0",
                    "id": "req-001",
                    "result": {"success": True, "data": {}}
                },
                {
                    "jsonrpc": "2.0",
                    "id": "req-002",
                    "error": {"code": -32601, "message": "Method not found"}
                }
            ]
        }

class ToolInfo(BaseModel):
    """도구 정보 모델 - 도구 발견(discovery)에 사용"""
    
    name: str = Field(..., description="도구의 고유 식별자")  # ❶
    description: str = Field(
        ..., 
        description="도구의 기능 설명 (LLM이 읽고 이해함)"
    )  # ❷
    parameters: Dict[str, Any] = Field(
        ..., 
        description="JSON Schema 형식의 파라미터 정의"
    )  # ❸
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "get_customer",
                "description": "고객 정보를 조회합니다. 구매 이력, 등급, 신용도 포함",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_id": {
                            "type": "string",
                            "description": "고객 ID"
                        }
                    },
                    "required": ["customer_id"]
                }
            }
        }
