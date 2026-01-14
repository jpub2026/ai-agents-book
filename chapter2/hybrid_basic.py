from ollama_client import OllamaClient


class HybridLLM:
    """
    작업에 따라 로컬/클라우드를 선택하는 시스템
    """
    
    def __init__(self):
        self.local_client = OllamaClient()
        # self.cloud_client = OpenAIClient()  # 실제로는 OpenAI 클라이언트
    
    def process(self, task: str, complexity: str = "simple") -> str:
        """
        복잡도에 따라 적절한 모델 선택
        """
        if complexity == "simple":
            # 간단한 작업은 로컬에서  ❶
            print("→ 로컬 모델 사용 (무료)")
            return self.local_client.generate("llama3.2", task)
        else:
            # 복잡한 작업은 클라우드에서  ❷
            print("→ 클라우드 모델 사용 (고성능)")
            # return self.cloud_client.generate(task)
            return "클라우드 응답 시뮬레이션"
    
    def estimate_complexity(self, task: str) -> str:
        """
        작업 복잡도 자동 판단
        """
        # 간단한 규칙으로 복잡도 추정  ❸
        if len(task) < 100 and "간단" in task:
            return "simple"
        elif "코드" in task or "분석" in task:
            return "complex"
        else:
            return "simple"

# 사용 예제
hybrid = HybridLLM()

tasks = [
    ("오늘 날씨 어때?", "simple"),
    ("이 코드의 버그를 찾아줘", "complex")
]

for task, complexity in tasks:
    print(f"\n작업: {task}")
    result = hybrid.process(task, complexity)
    print(f"결과: {result[:100]}...")
