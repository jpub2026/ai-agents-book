# MCP 통신 흐름을 보여주는 개념적 예제
class MCPCommunicationFlow:
    """
    MCP 시스템에서 메시지가 어떻게 흐르는지 보여주는 예제
    실제 구현이 아닌 개념 설명용 코드입니다
    """
    
    def demonstrate_flow(self):
        
        host_creates_client = {
            "step": "1. Client 생성",
            "from": "Host (Claude Desktop)",
            "action": "설정 파일을 읽고 MCP 서버별로 Client 인스턴스를 생성합니다"
        }
        
        client_to_server = {
            "step": "2. 연결 및 초기화",
            "from": "Client",
            "to": "Server (파일 시스템 MCP 서버)",
            "message": {
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "clientInfo": {"name": "claude-desktop", "version": "1.0"}
                }
            }
        }
        
        server_response = {
            "step": "3. 서버 응답",
            "from": "Server",
            "to": "Client",
            "message": {
                "jsonrpc": "2.0",
                "result": {
                    "serverInfo": {"name": "filesystem-server"},
                    "capabilities": {"tools": {}}
                }
            }
        }
        
        tool_discovery = {
            "step": "4. 도구 발견",
            "from": "Client",
            "to": "Server",
            "message": {
                "jsonrpc": "2.0",
                "method": "tools/list"
            },
            "response": {
                "tools": [
                    "read_file: 파일 읽기",
                    "write_file: 파일 쓰기",
                    "list_directory: 디렉터리 목록 조회"
                ]
            }
        }
        
        tool_execution = {
            "step": "5. 도구 실행 요청",
            "from": "Client",
            "to": "Server",
            "message": {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "read_file",
                    "arguments": {"path": "/Users/user/report.txt"}
                }
            }
        }
        
        tool_result = {
            "step": "6. 결과 반환",
            "from": "Server",
            "to": "Client",
            "result": "파일 내용을 성공적으로 읽었습니다: [파일 데이터]"
        }
        
        result_to_host = {
            "step": "7. Host에 결과 전달",
            "from": "Client",
            "to": "Host",
            "action": "Host가 결과를 받아 사용자 인터페이스에 표시합니다"
        }