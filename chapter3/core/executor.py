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

    def check_dependencies(self, step: Dict, results: Dict) -> bool:
        """
        단계의 의존성이 충족되었는지 확인합니다.
        모든 선행 단계가 완료되어야 현재 단계를 실행할 수 있습니다.
        """
        dependencies = step.get('dependencies', [])

        # 의존성이 없으면 바로 실행 가능
        if not dependencies:
            return True

        # 모든 의존성 단계가 결과에 있는지 확인
        for dep in dependencies:
            if dep not in results:
                return False
            # 의존 단계가 실패했는지도 확인
            dep_result = results[dep]
            if isinstance(dep_result, dict) and not dep_result.get('success', True):
                return False

        return True

    def prepare_tool_input(self, step: Dict, previous_results: Dict) -> Dict:
        """
        도구 실행을 위한 입력을 준비합니다.
        이전 단계의 결과를 참조하여 필요한 데이터를 구성합니다.
        """
        tool_input = {
            'description': step.get('description', ''),
            'expected_output': step.get('expected_output', ''),
            'step_number': step.get('step_number', 0)
        }

        # 의존성 단계의 결과를 입력에 포함
        dependencies = step.get('dependencies', [])
        if dependencies:
            tool_input['dependency_results'] = {
                dep: previous_results.get(dep, {})
                for dep in dependencies
            }

        return tool_input

    def validate_result(self, result: Any, expected_output: str) -> bool:
        """
        실행 결과가 예상과 일치하는지 검증합니다.
        """
        # 결과가 None이면 실패
        if result is None:
            return False

        # 결과가 딕셔너리이고 success 필드가 있으면 그 값 사용
        if isinstance(result, dict):
            if 'success' in result:
                return result['success']
            # data 필드가 있으면 성공으로 간주
            if 'data' in result:
                return True

        # 그 외의 경우 결과가 존재하면 성공으로 간주
        return True

    def handle_failure(self, step: Dict, error: Exception) -> Dict:
        """
        단계 실행 실패를 처리합니다.
        """
        return {
            'success': False,
            'step_number': step.get('step_number', 0),
            'description': step.get('description', ''),
            'error': str(error),
            'timestamp': datetime.now()
        }

    def compile_results(self, results: Dict) -> Dict:
        """
        모든 단계의 결과를 최종 결과로 컴파일합니다.
        """
        # 성공/실패 통계 계산
        success_count = 0
        failure_count = 0

        for step_id, result in results.items():
            if isinstance(result, dict):
                if result.get('success', False) or 'data' in result:
                    success_count += 1
                else:
                    failure_count += 1
            else:
                success_count += 1  # 결과가 있으면 성공으로 간주

        # 실행 이력에 추가
        self.execution_history.append({
            'timestamp': datetime.now(),
            'total_steps': len(results),
            'success_count': success_count,
            'failure_count': failure_count
        })

        return results
