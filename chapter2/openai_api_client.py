import os
from openai import OpenAI
from dotenv import load_dotenv

class OpenAIClient:
    """
    OpenAI API를 사용하는 클라이언트
    """
    
    def __init__(self):
        # 환경변수에서 API 키 로드
        load_dotenv()
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def generate(self, prompt, model="gpt-3.5-turbo"):
        """
        OpenAI 모델로 텍스트 생성
        """
        try:
            # API 호출
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # 응답 추출
            return response.choices[0].message.content
            
        except Exception as e:
            return f"API 호출 오류: {str(e)}"

# 사용 예제
openai_client = OpenAIClient()

# 텍스트 생성
response = openai_client.generate(
    "파이썬의 장점을 간단히 설명해주세요."
)
print("응답:", response)
