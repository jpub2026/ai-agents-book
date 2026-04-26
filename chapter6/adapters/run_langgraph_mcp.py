"""
코드 6-17(`langgraph_mcp_node.py`)의 `create_mcp_workflow()` 함수를 실행해
MCPNode 기반 LangGraph 워크플로가 생성되는지 확인하는 데모 스크립트.

책 본문에는 포함되지 않은 보조 실행 스크립트이며, 예제 코드 자체는 변경하지 않음.

필수 패키지:
    pip install langgraph
"""
from langgraph_mcp_node import create_mcp_workflow


def main() -> None:
    workflow = create_mcp_workflow()
    print("[LangGraph 워크플로 생성 성공]")
    print(f"  workflow 타입: {type(workflow).__name__}")


if __name__ == "__main__":
    main()
