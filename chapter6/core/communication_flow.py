# MCP 통신 흐름을 보여주는 개념적 예제
class MCPCommunicationFlow:
    """
    MCP 시스템에서 메시지가 어떻게 흐르는지 보여주는 예제
    실제 구현이 아닌 개념 설명용 코드입니다
    """
    
    def demonstrate_flow(self):
        """MCP 통신 흐름 단계별 예제"""
        client_to_host = {
            "step": "1. 연결 요청",
            "from": "Client (Claude Desktop)",
            "to": "Host",
            "message": "안녕하세요, 저는 Claude입니다. 시스템에 참여하고 싶습니다."
        }

        
        host_response = {
            "step": "2. 등록 확인",
            "from": "Host",
            "to": "Client",
            "message": "등록되었습니다. 사용 가능한 서비스 목록을 보내드립니다."
        }
        
        
        service_discovery = {
            "step": "3. 서비스 발견",
            "available_services": [
                "database_server: SQL 쿼리 실행 가능",
                "weather_api: 날씨 정보 제공",
                "file_system: 파일 읽기/쓰기"
            ]
        }

        
        client_request = {
            "step": "4. 기능 요청",
            "from": "Client",
            "to": "Host",
            "message": "데이터베이스에서 사용자 정보를 조회하고 싶습니다"
        }
        
        
        host_routing = {
            "step": "5. 라우팅",
            "from": "Host",
            "to": "Database Server",
            "message": "Client의 쿼리 요청을 전달합니다"
        }
        
        
        server_response = {
            "step": "6. 결과 반환",
            "from": "Database Server",
            "to": "Host",
            "result": "쿼리 실행 완료: 3명의 사용자 정보"
        }
        
        
        final_response = {
            "step": "7. 최종 응답",
            "from": "Host",
            "to": "Client",
            "result": "요청하신 사용자 정보입니다: [...]"
        }
