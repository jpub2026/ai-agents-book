import openai
import anthropic
import google.generativeai as genai
from typing import Optional, Dict, Any
import os

class TraditionalIntegration:
    """
    현재 AI 서비스 통합의 복잡성을 보여주는 실제 동작 코드
    각 서비스마다 완전히 다른 방식으로 통신해야 합니다
    """
    
    def __init__(self):
        self.openai_client = None
        self.claude_client = None
        self.gemini_model = None
        
    def connect_openai(self, api_key: str) -> None:
        """OpenAI API 연결 및 메시지 전송"""
        #  OpenAI는 클라이언트 객체를 통한 인증 
        self.openai_client = openai.OpenAI(api_key=api_key)
        
    def connect_claude(self, api_key: str) -> None:
        """Claude API 연결"""
        #  Claude는 앤트로픽 클라이언트를 사용
        self.claude_client = anthropic.Anthropic(api_key=api_key)
        
    def connect_gemini(self, api_key: str) -> None:
        """Gemini API 연결"""
        # Gemini는 configure 메서드로 API 키 설정
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    def query_openai(self, prompt: str) -> str:
        """OpenAI에 질의"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        # GPT의 메시지 형식
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    def query_claude(self, prompt: str) -> str:
        """Claude에 질의"""
        if not self.claude_client:
            raise ValueError("Claude client not initialized")
        # Claude의 메시지 형식
        response = self.claude_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def query_gemini(self, prompt: str) -> str:
        """Gemini에 질의"""
        if not self.gemini_model:
            raise ValueError("Gemini model not initialized")

        response = self.gemini_model.generate_content(prompt)
        return response.text
    
    def query_all(self, prompt: str) -> Dict[str, str]:
        """모든 AI 서비스에 동일한 질문"""
        results = {}
        
        # 각 서비스마다 다른 에러 처리 필요
        try:
            results['openai'] = self.query_openai(prompt)
        except Exception as e:
            results['openai'] = f"Error: {str(e)}"
            
        try:
            results['claude'] = self.query_claude(prompt)
        except Exception as e:
            results['claude'] = f"Error: {str(e)}"
            
        try:
            results['gemini'] = self.query_gemini(prompt)
        except Exception as e:
            results['gemini'] = f"Error: {str(e)}"
            
        return results

# 사용 예제
if __name__ == "__main__":
    integration = TraditionalIntegration()
    
    # 각 서비스별로 다른 초기화 방식
    integration.connect_openai(os.getenv("OPENAI_API_KEY"))
    integration.connect_claude(os.getenv("ANTHROPIC_API_KEY"))
    integration.connect_gemini(os.getenv("GEMINI_API_KEY"))
    
    # 동일한 질문을 서로 다른 방식으로 전송
    results = integration.query_all("What is MCP protocol?")
    
    for service, response in results.items():
        print(f"\n{service.upper()} Response:")
        print(response[:200] + "..." if len(response) > 200 else response)
