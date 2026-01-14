import re
from korean import LanguageProcessor

class EnglishProcessor(LanguageProcessor):
    """영어 텍스트의 전처리와 후처리를 담당합니다."""
    
    def preprocess(self, text: str) -> str:
        """영어 입력을 정규화합니다."""
        text = text.replace("don't", "do not")
        text = text.replace("won't", "will not")
        return text.strip()
    
    def postprocess(self, text: str) -> str:
        """영어 응답의 형식을 보정합니다."""
        sentences = text.split('. ')
        sentences = [s[0].upper() + s[1:] if s else s for s in sentences]
        text = '. '.join(sentences)
        
        text = re.sub(r'^[-*]\s*', '• ', text, flags=re.MULTILINE)
        
        return text
