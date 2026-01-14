# /mcp_server/registry.py
"""전역 도구 레지스트리 - 순환 참조 방지를 위해 분리"""
from typing import Dict, Any

# 전역 도구 레지스트리
TOOLS: Dict[str, Dict[str, Any]] = {}
