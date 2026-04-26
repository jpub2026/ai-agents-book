"""
코드 6-5(`communication_flow.py`)의 MCPCommunicationFlow 클래스에 정의된
각 단계를 콘솔로 출력해 주는 데모 스크립트.

책 본문에는 포함되지 않은 보조 실행 스크립트이며, 예제 코드 자체는 변경하지 않음.

실행:
    cd chapter6/core
    python run_communication_flow.py
"""
from communication_flow import MCPCommunicationFlow


def main() -> None:
    flow = MCPCommunicationFlow()

    # demonstrate_flow() 내부에는 단계별 딕셔너리만 정의되어 있고
    # 반환값이 없으므로 지역 변수를 그대로 출력하기 위해 다시 구성한다.
    steps = {
        "1. Client 생성": {
            "from": "Host (Claude Desktop)",
            "action": "설정 파일을 읽고 MCP 서버별로 Client 인스턴스를 생성합니다",
        },
        "2. 연결 및 초기화": {
            "from": "Client",
            "to": "Server (파일 시스템 MCP 서버)",
            "method": "initialize",
        },
        "3. 서버 응답": {
            "from": "Server",
            "to": "Client",
            "description": "serverInfo + capabilities 응답",
        },
        "4. 도구 발견": {
            "from": "Client",
            "to": "Server",
            "method": "tools/list",
        },
        "5. 도구 실행 요청": {
            "from": "Client",
            "to": "Server",
            "method": "tools/call",
        },
        "6. 결과 반환": {
            "from": "Server",
            "to": "Client",
            "description": "파일 내용을 성공적으로 읽었습니다",
        },
        "7. Host에 결과 전달": {
            "from": "Client",
            "to": "Host",
            "action": "Host가 결과를 받아 사용자 인터페이스에 표시합니다",
        },
    }

    # 메서드 호출 자체는 사이드이펙트 없이도 클래스가 정상 임포트되는지
    # 확인할 수 있도록 남겨 둔다.
    flow.demonstrate_flow()

    print("\n=== MCP 메시지 흐름 ===")
    for step, detail in steps.items():
        print(f"[{step}] {detail}")


if __name__ == "__main__":
    main()
