from logging_setup import setup_logging
from slack_notifier import SlackNotifier

# 로거 초기화
logger = setup_logging("my-agent")

# SlackNotifier는 SLACK_BOT_TOKEN 환경 변수가 필요합니다
# 환경 변수가 없으면 None으로 설정
try:
    slack = SlackNotifier()
except ValueError:
    slack = None
    logger.warning("SLACK_BOT_TOKEN이 설정되지 않아 Slack 알림이 비활성화됩니다.")


def call_api(data):
    """API 호출 시뮬레이션 함수"""
    # 실제 구현에서는 requests나 httpx를 사용
    class MockResponse:
        status_code = 200
        def json(self):
            return {"result": "success", "data": data}
    return MockResponse()

def process_task(task_id, data):
    """작업을 처리하는 함수"""
    
    # 작업 시작 기록
    logger.info(f"작업 시작: {task_id}")
    
    try:
        # 실제 작업 수행
        result = do_something(data)
        
        # 성공 기록
        logger.info(f"작업 완료: {task_id}, 결과: {result}")
        return result
    except Exception as e:
        # 에러 발생 시 상세 정보 기록
        logger.error(f"작업 실패: {task_id}", exc_info=True)
        raise

def do_something(data):
    """실제 작업을 수행"""
    logger.debug(f"데이터 처리 중: {data}")  # 디버그 정보
    
    # 중요한 단계마다 로그 남기기
    logger.info("API 호출 시작")
    response = call_api(data)
    logger.info(f"API 응답 받음: {response.status_code}")
    
    return response.json()

def process_task_with_notification(task_id, data):
    """작업 처리 후 Slack으로 알림"""
    
    try:
        logger.info(f"작업 시작: {task_id}")
        result = do_something(data)
        
        # 성공 알림
        slack.send_task_complete(
            task_id=task_id,
            status="success",
            result=result
        )
        logger.info(f"작업 완료 및 알림 전송: {task_id}")
        return result
        
    except Exception as e:
        # 실패 알림
        slack.send_task_complete(
            task_id=task_id,
            status="failed",
            result=str(e)
        )
        
        logger.error(f"작업 실패: {task_id}", exc_info=True)
        raise

    

