"""
코드 6-16(`langchain_mcp_adapter.py`)에서 정의한
`demonstrate_langchain_mcp_integration()`을 실행하는 데모 스크립트.

책 본문에는 포함되지 않은 보조 실행 스크립트이며, 예제 코드 자체는 변경하지 않음.

필수 패키지:
    pip install langchain langchain-core
"""
from langchain_mcp_adapter import demonstrate_langchain_mcp_integration


def main() -> None:
    file_tool = demonstrate_langchain_mcp_integration()
    print(f"[생성된 Tool] name={file_tool.name}")
    print(f"[설명] {file_tool.description}")


if __name__ == "__main__":
    main()
