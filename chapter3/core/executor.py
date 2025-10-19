import time
from datetime import datetime
from typing import Dict, Any

class Executor:
    """
    계획을 실제로 실행하는 클래스
    오류 처리, 재시도, 진행 상황 추적을 담당합니다
    """
    
    def __init__(self, tool_manager, memory):
        self.tool_manager = tool_manager
        self.memory = memory
        self.execution_history = []
        self.max_retries = 3
    
    def execute_plan(self, plan: Dict) -> Dict:
        """
        전체 계획을 실행합니다
        """
        results = {}
        total_steps = len(plan['steps'])
        
        for step in plan['steps']:
            step_num = step['step_number']
            
            # 의존성 확인
            if not self.check_dependencies(step, results):
                print(f"단계 {step_num}: 의존성 미충족")
                continue
            
            print(f"\n단계 {step_num}/{total_steps}: {step['description']}")

            # 재시도 로직이 포함된 실행
            for attempt in range(self.max_retries):
                try:
                    result = self.execute_single_step(step, results)
                    results[step_num] = result
                    
                    # 성공 시 메모리에 저장
                    self.memory.store({
                        'step': step_num,
                        'action': step['description'],
                        'result': result,
                        'timestamp': datetime.now()
                    })
                    
                    print(f" 단계 {step_num} 완료")
                    break
                    
                except Exception as e:
                    print(f"시도 {attempt + 1} 실패: {e}")
                    if attempt == self.max_retries - 1:
                        results[step_num] = self.handle_failure(step, e)
                    else:
                        time.sleep(2 ** attempt)  # 지수 백오프
        
        return self.compile_results(results)
    
    def execute_single_step(self, step: Dict, previous_results: Dict) -> Any:
        """
        단일 단계를 실행합니다
        """
        tool_name = step['tool_required']
        tool = self.tool_manager.get_tool(tool_name)
        
        if not tool:
            raise ValueError(f"도구를 찾을 수 없음: {tool_name}")
        
        # 이전 결과를 참조하여 입력 준비
        tool_input = self.prepare_tool_input(step, previous_results)
        
        # 도구 실행
        result = tool.execute(tool_input)
        
        # 결과 검증
        if not self.validate_result(result, step['expected_output']):
            raise ValueError(f"예상과 다른 결과: {result}")
        
        return result
