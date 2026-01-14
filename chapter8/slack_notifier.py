from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

class SlackNotifier:
    """간단한 Slack 알림 클래스"""
    
    def __init__(self):
        # 환경 변수에서 토큰 가져오기
        token = os.getenv("SLACK_BOT_TOKEN")
        if not token:
            raise ValueError("SLACK_BOT_TOKEN이 설정되지 않았습니다")
        
        self.client = WebClient(token=token)
        self.channel = os.getenv("SLACK_CHANNEL", "#general")

    def send_message(self, message):
            """간단한 텍스트 메시지 보내기"""
            try:
                response = self.client.chat_postMessage(
                    channel=self.channel,
                    text=message
                )
                return True
            except SlackApiError as e:
                print(f"Slack 전송 실패: {e.response['error']}")
                return False
            
    def send_task_complete(self, task_id, status, result):
        """작업 완료 알림"""
        
        # 상태에 따라 이모지 선택
        emoji = "Success" if status == "success" else "Fail"
        
        # 메시지 구성
        message = f"""
                    {emoji} 작업 완료 알림

                    - 작업 ID: {task_id}
                    - 상태: {status}
                    - 결과: {result}
                            """
        
        return self.send_message(message.strip())
    
    def send_task_complete_fancy(self, task_id, status, result, execution_time):
        """더 예쁜 작업 완료 알림"""
    
        emoji = "Success" if status == "success" else "Fail"
        color = "good" if status == "success" else "danger"
        
        # Block Kit 사용 (Slack의 리치 메시지 포맷)
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} 작업 완료"
                }
            },
            {
            "type": "section", 
            "fields": [
                {"type": "mrkdwn", "text": f"*작업 ID:*\n{task_id}"},
                {"type": "mrkdwn", "text": f"*상태:*\n{status}"},
                {"type": "mrkdwn", "text": f"*실행 시간:*\n{execution_time:.2f}초"},
                {"type": "mrkdwn", "text": f"*결과:*\n{result}"}
            ]
            }
        ]
        
        try:
            response = self.client.chat_postMessage(
                channel=self.channel,
                blocks=blocks,
                text=f"작업 {task_id} 완료"  # 알림용 텍스트
            )
            return True
        except SlackApiError as e:
            print(f"Slack 전송 실패: {e}")
            return False



