
class JSONRPCStructure:
    """
    JSON-RPC 2.0의 메시지 구조를 설명하는 예제
    MCP의 모든 통신은 이 형식을 따릅니다
    """

    def request_structure(self):
        """요청 메시지의 구조"""
        request = {
            "jsonrpc": "2.0",  # ❶
            "method": "query",  # ❷
            "params": {  # ❸
                "sql": "SELECT * FROM users"
            },
            "id": "req_123"  # ❹
        }
        return request

    def success_response_structure(self):
        """성공 응답의 구조"""
        response = {
            "jsonrpc": "2.0",
            "result": {  # ❺
                "users": [
                    {"id": 1, "name": "Alice"},
                    {"id": 2, "name": "Bob"}
                ]
            },
            "id": "req_123"  # ❻
        }
        return response

    def error_response_structure(self):
        """에러 응답의 구조"""
        error_response = {
            "jsonrpc": "2.0",
            "error": {  # ❼
                "code": -32601,  # ❽
                "message": "Method not found",  # 에러 메시지
                "data": {  # 추가 정보(선택적)
                    "method": "unknown_method"
                }
            },
            "id": "req_123"
        }
        return error_response

    def notification_structure(self):
        """알림 메시지의 구조(응답이 필요 없는 경우)"""
        notification = {
            "jsonrpc": "2.0",
            "method": "log",
            "params": {
                "message": "작업이 완료되었습니다"
            }
            # 아이디가 없다.  # ❾
        }
        return notification
