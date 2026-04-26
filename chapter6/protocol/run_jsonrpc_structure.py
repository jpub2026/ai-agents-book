"""
코드 6-6(`jsonrpc_structure.py`)의 클래스를 실행해 JSON-RPC 2.0
메시지 구조를 콘솔로 확인할 수 있는 데모 스크립트.

책 본문에는 포함되지 않은 보조 실행 스크립트이며, 예제 코드 자체는 변경하지 않음.

실행:
    cd chapter6/protocol
    python run_jsonrpc_structure.py
"""
import json

from jsonrpc_structure import JSONRPCStructure


def main() -> None:
    s = JSONRPCStructure()

    examples = {
        "① 요청(Request)": s.request_structure(),
        "② 성공 응답(Success Response)": s.success_response_structure(),
        "③ 에러 응답(Error Response)": s.error_response_structure(),
        "④ 알림(Notification)": s.notification_structure(),
    }

    for title, message in examples.items():
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50)
        print(json.dumps(message, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
