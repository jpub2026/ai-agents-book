# /mcp_server/middleware.py
from fastapi import Request
from time import time
from metrics import (
    increment_request_count,
    increment_error_count,
    record_response_time
)


def add_metrics_middleware(app):
    """메트릭 미들웨어를 앱에 추가하는 함수"""

    @app.middleware("http")  # ❶
    async def metrics_middleware(request: Request, call_next):  # ❷
        """모든 HTTP 요청에 대해 메트릭 수집"""

        # 시작 시간 기록
        start_time = time()  # ❸

        # 요청 카운트 증가
        increment_request_count()

        try:
            # 실제 엔드포인트 실행
            response = await call_next(request)  # ❹

            # 응답 시간 계산
            response_time = (time() - start_time) * 1000  # ms 단위  # ❺
            record_response_time(response_time)

            # 응답 헤더에 메트릭 추가
            response.headers["X-Response-Time"] = f"{response_time:.2f}ms"  # ❻

            return response

        except Exception as e:  # ❼
            # 에러 카운트 증가
            increment_error_count()

            # 에러 재발생 (정상적인 에러 처리가 이루어지도록)
            raise
