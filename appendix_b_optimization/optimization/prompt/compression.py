def _compress_keeping_context(self, text: str) -> str:
    """컨텍스트를 우선적으로 보존하며 압축합니다."""
    parts = text.split('\n\n')
    
    if len(parts) > 2:
        context_len = int(self.max_length * 0.7)
        context = parts[0][:context_len]
        
        remaining_len = self.max_length - len(context)
        instruction = ' '.join(parts[1:])[:remaining_len]

        return f"{context}\n\n{instruction}"
        
    return text[:self.max_length]

def _compress_keeping_instruction(self, text: str) -> str:
    """지시사항을 우선적으로 보존하며 압축합니다."""
    parts = text.split('\n\n')
    
    if len(parts) > 1:
        instruction = parts[-1]
        instruction_len = min(
            len(instruction), 
            int(self.max_length * 0.4)
        )
        
        context_len = self.max_length - instruction_len
        context = ' '.join(parts[:-1])[:context_len]

        return f"{context}\n\n{instruction}"
        
    return text[:self.max_length]

def _balanced_compression(self, text: str) -> str:
    """균형있게 압축합니다."""
    if len(text) <= self.max_length:
        return text
        
    sentences = text.split('.')
    target_len = int(self.max_length * self.compression_ratio)
    
    compressed = []
    current_len = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if current_len + len(sentence) < target_len:
            compressed.append(sentence)
            current_len += len(sentence)
        else:
            break
            
    return '. '.join(compressed)

def _restructure(self, text: str) -> str:
    """프롬프트를 명확한 구조로 재구성합니다."""
    sections = []
    
    if "질문:" in text or "Question:" in text:
        sections.append("[지시사항]")

    if "컨텍스트:" in text or "Context:" in text:
        sections.append("[참고자료]")

    structured = text
    for section in sections:
        structured = structured.replace(
            section.strip("[]"), 
            f"\n{section}\n"
        )
        
    return structured.strip()
