def _remove_duplicates(self, text: str) -> str:
    """중복 문장을 제거합니다."""
    sentences = text.split('.')
    seen = set()
    unique_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and sentence not in seen:
            seen.add(sentence)  
            unique_sentences.append(sentence)
            
    return '. '.join(unique_sentences)

def _clean_whitespace(self, text: str) -> str:
    """불필요한 공백을 정리합니다."""
    import re
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
