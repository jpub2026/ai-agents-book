import re
from korean import LanguageProcessor

class JapaneseProcessor(LanguageProcessor):
    """일본어 텍스트의 전처리와 후처리를 담당합니다."""
    
    def preprocess(self, text: str) -> str:
        """일본어 입력을 정규화합니다."""
        text = text.replace('！', '!')
        text = text.replace('？', '?')
        return text.strip()
    
    def postprocess(self, text: str) -> str:
        """일본어 응답의 정중체와 형식을 보정합니다."""
        if not re.search(r'(です|ます|ません|でした)。?$', text):
            text += 'です。'
        
        text = re.sub(r'^[-*]\s*', '・', text, flags=re.MULTILINE)
        
        return text
