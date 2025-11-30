from typing import Dict, List, Any
from datetime import datetime
import json
import time

# 3.2절에서 구현한 구성요소들을 import
# 각 구성요소는 독립적으로 개발되었지만,
# 이제 하나의 시스템으로 통합됩니다
import sys
sys.path.append('../core')      # Planner가 있는 경로
sys.path.append('../memory')     # MemorySystem이 있는 경로
sys.path.append('../tools')      # ToolManager가 있는 경로

from planner import Planner          # 코드 3-1: 계획 수립
from executor import Executor        # 코드 3-2: 계획 실행
from system import MemorySystem      # 코드 3-4: 기억 관리
from base import ToolManager, BaseTool  # 코드 3-3: 도구 관리

# 2장의 통합 LLM 인터페이스
sys.path.append('../chapter2')
from llm_interface import LLM        # 코드 2-6

class Agent:
    """
    모든 구성요소를 통합한 에이전트입니다.
    
    Agent는 사용자 요청을 받아 5단계 프로세스로 처리합니다:
    1. 과거 경험 검색
    2. 계획 수립
    3. 계획 실행
    4. 경험 저장
    5. 응답 생성
    
    각 단계는 특정 구성요소가 담당하며,
    Agent는 이들을 조율하는 역할을 합니다.
    """
    
    def __init__(self):
        """
        네 가지 핵심 구성요소를 초기화하고 연결합니다.
        
        초기화 순서가 중요합니다:
        1. LLM (다른 구성요소가 사용)
        2. Memory (독립적)
        3. ToolManager (LLM 사용)
        4. Planner (LLM 사용)
        5. Executor (ToolManager와 Memory 사용)
        """
        print("에이전트 초기화 시작...")
        print("-" * 50)
        
        # 1. LLM 인터페이스 초기화
        # 이것이 먼저 초기화되어야 다른 구성요소가 사용할 수 있습니다
        print(" 1. LLM 인터페이스 설정...")
        self.llm = LLM()  # Ollama, OpenAI, Mock 중 자동 선택
        
        # 2. 메모리 시스템 초기화
        # 과거 경험을 저장하고 검색하는 역할
        print(" 2. 메모리 시스템 초기화...")
        self.memory = MemorySystem()
        
        # 3. 도구 관리자 초기화
        # 에이전트가 사용할 도구들을 관리
        print(" 3. ToolManager 초기화...")
        self.tool_manager = ToolManager(llm=self.llm)
        
        # 4. 계획 수립기 초기화
        # 사용자 요청을 실행 가능한 계획으로 변환
        print(" 4. Planner 초기화...")
        self.planner = Planner(llm=self.llm)
        
        # 5. 실행 엔진 초기화
        # 계획을 실제로 실행하는 역할
        print(" 5. Executor 초기화...")
        self.executor = Executor(
            tool_manager=self.tool_manager,
            memory=self.memory
        )
        
        # 6. 기본 도구들 등록
        print(" 6. 기본 도구 등록...")
        self._register_default_tools()
        
        print("-" * 50)
        print("에이전트 초기화 완료\n")
    
    def _register_default_tools(self):
        """
        에이전트가 사용할 기본 도구들을 등록합니다.
        
        실제 환경에서는 WebSearchTool, DatabaseTool 등
        구체적인 도구 클래스를 등록하겠지만,
        여기서는 학습을 위해 간단한 시뮬레이션 도구를 사용합니다.
        """
        # 회의 준비에 필요한 도구들
        tools = [
            BaseTool(name="database", description="참석자 정보를 조회합니다"),
            BaseTool(name="calendar", description="일정과 회의실을 관리합니다"),  
            BaseTool(name="email", description="이메일을 발송합니다"),
            BaseTool(name="document", description="문서를 생성하고 편집합니다")
        ]
        
        # 각 도구를 ToolManager에 등록
        for tool in tools:
            self.tool_manager.register_tool(tool)
            
    def process_request(self, user_request: str) -> str:
        """
        사용자 요청을 처리하는 메인 메서드입니다.
        
        이 메서드는 시퀀스 다이어그램의 5단계 프로세스를 
        정확히 구현합니다. 각 단계는 특정 구성요소를 호출하고,
        그 결과를 다음 단계로 전달합니다.
        """
        print(f"\n{'='*60}")
        print(f"사용자: {user_request}")
        print(f"{'='*60}\n")
        
        try:
            # ==========================================
            # 1단계: 요청 수신과 기억 검색
            # 목적: 과거의 유사한 경험을 찾아 현재 작업에 활용
            # ==========================================
            print("[1단계] 요청 수신과 기억 검색")
            print("-" * 40)
            
            # MemorySystem의 retrieve 메서드 호출
            # 모든 메모리 타입(단기, 장기, 작업)에서 검색합니다
            memories = self.memory.retrieve(
                query=user_request,
                memory_type='all',  # 모든 메모리 타입에서 검색
                k=5  # 상위 5개의 관련 기억을 가져옴
            )
            
            # 검색 결과 표시
            if memories:
                print(f" 관련 기억 {len(memories)}개 발견:")
                # 처음 2개만 표시 (너무 많으면 출력이 복잡해짐)
                for i, mem in enumerate(memories[:2], 1):  
                    content = mem.get('content', '')[:50]
                    print(f"    {i}. {content}...")
            else:
                print("  관련 기억 없음 (새로운 작업입니다)")
            
            # ==========================================
            # 2단계: 계획 수립
            # 목적: 요청을 실행 가능한 작은 단계들로 분해
            # ==========================================
            print("\n[2단계] 계획 수립")
            print("-" * 40)
            
            # 계획 수립을 위한 컨텍스트 준비
            # 이 정보들이 더 나은 계획을 만드는 데 도움이 됩니다
            context = {
                'memories': memories,  # 과거 경험
                'timestamp': datetime.now(),  # 현재 시간
                'user_preferences': self._get_user_preferences()  # 사용자 선호
            }
            print(f" 컨텍스트 준비 완료")
            
            # 사용 가능한 도구 목록 가져오기
            available_tools = self.tool_manager.list_tools()
            print(f" 사용 가능한 도구: {available_tools}")
            
            # Planner에게 계획 수립 요청
            plan = self.planner.create_plan(
                user_request=user_request,
                available_tools=available_tools,
                context=context
            )
            
            # 생성된 계획을 보기 좋게 출력
            self._display_plan(plan)
            
            # ==========================================
            # 3단계: 계획 실행
            # 목적: 각 단계를 순서대로(또는 병렬로) 실행
            # ==========================================
            print("\n [3단계] 계획 실행")
            print("-" * 40)
            
            print("  실행 루프 시작...")
            print("  (의존성 확인 → 도구 실행 → 결과 저장)")
            
            # Executor가 계획을 실행
            # 내부적으로 복잡한 처리가 일어나지만,
            # Agent는 결과만 받으면 됩니다
            results = self.executor.execute_plan(plan)
            
            print(f"  실행 완료: {len(results)}개 작업 처리")
            
            # ==========================================
            # 4단계: 경험 저장
            # 목적: 이번 작업을 경험으로 저장하여 학습
            # ==========================================
            print("\n[4단계] 경험 저장")
            print("-" * 40)
            
            # 전체 작업 경험을 하나의 데이터로 구성
            experience = {
                'content': f"요청: {user_request}",  # 간단한 설명
                'request': user_request,  # 원본 요청
                'plan': plan,  # 수립된 계획
                'results': results,  # 실행 결과
                'timestamp': datetime.now(),  # 처리 시간
                'is_important': self._is_important_experience(results)  # 중요도
            }
            
            # Memory에 경험 저장
            self.memory.store(
                information=experience,
                memory_type='short'  # 일단 단기 기억에 저장
            )

            # 중요한 경험은 자동으로 장기 기억으로 승격됩니다
            if experience['is_important']:
                print("  중요 경험으로 표시 → 장기 기억 승격 가능")
            else:
                print("  일반 경험으로 단기 기억에 저장")
            
            # ==========================================
            # 5단계: 응답 생성
            # 목적: 복잡한 내부 처리를 간단한 메시지로 변환
            # ==========================================
            print("\n[5단계] 응답 생성")
            print("-" * 40)
            
            # 결과를 분석하여 사용자 친화적 메시지 생성
            response = self._generate_response(results, user_request)

            print(f"\n{'='*60}")
            print(f"에이전트: {response}")
            print(f"{'='*60}")
            
            return response
            
        except Exception as e:
            # 오류 처리도 중요한 부분입니다
            error_msg = f"오류 발생: {str(e)}"
            print(f"\n{error_msg}")
            
            # 오류도 경험으로 저장합니다 (학습을 위해)
            self.memory.store({
                'content': f"오류: {user_request} - {str(e)}",
                'type': 'error',
                'timestamp': datetime.now()
            }, memory_type='short')
            
            return error_msg
        
    def _display_plan(self, plan: Dict):
        """
        생성된 계획을 사용자가 이해하기 쉽게 출력합니다.
        
        계획의 각 단계와 의존성 관계를 시각적으로 표현하여,
        어떤 작업이 언제 실행될 수 있는지 명확하게 보여줍니다.
        """
        steps = plan.get('steps', [])
        print(f" {len(steps)}단계 계획 생성 완료")
        print("\n 계획 내용:")
        
        for step in steps:
            step_num = step.get('step_number', '?')
            desc = step.get('description', '')
            tool = step.get('tool_required', '')
            deps = step.get('dependencies', [])
            
            # 의존성을 이해하기 쉽게 표시
            # 빈 배열 = 즉시 실행 가능
            # [1, 2] = 1번과 2번이 완료된 후 실행
            if deps:
                deps_str = f"[{', '.join(map(str, deps))}번 완료 후]"
            else:
                deps_str = "[즉시 실행 가능]"
            
            print(f"    단계 {step_num}: {desc}")
            print(f"           도구: {tool} {deps_str}")
    
    def _generate_response(self, results: Dict, request: str) -> str:
        """
        실행 결과를 분석하여 사용자 친화적인 응답을 생성합니다.
        
        이 메서드는 기술적인 실행 결과를 
        일반 사용자가 이해하기 쉬운 메시지로 변환합니다.
        성공률에 따라 다른 톤과 메시지를 사용합니다.
        """
        # 성공한 작업 수 계산
        success_count = 0
        total_count = len(results)
        
        for step_id, result in results.items():
            if isinstance(result, dict):
                # success 필드가 있으면 그 값을 사용
                # 없으면 data 필드의 존재 여부로 판단
                if result.get('success', False) or 'data' in result:
                    success_count += 1
        
        # 작업이 없는 경우
        if total_count == 0:
            return "실행할 작업이 없습니다."
        
        # 성공률 계산
        success_rate = (success_count / total_count) * 100
        
        # 성공률에 따른 메시지 생성
        # 이모지를 사용하여 상태를 직관적으로 전달
        if success_rate == 100:
            return f" 모든 작업이 성공적으로 완료되었습니다! ({success_count}/{total_count} 단계)"
        elif success_rate >= 75:
            return f" 대부분의 작업이 완료되었습니다. ({success_count}/{total_count} 단계 성공)"
        elif success_rate >= 50:
            return f" 일부 작업이 완료되었습니다. ({success_count}/{total_count} 단계 성공)"
        else:
            return f" 대부분의 작업이 실패했습니다. ({success_count}/{total_count} 단계만 성공)"
    
    def _get_user_preferences(self) -> Dict:
        """
        사용자 선호도를 반환합니다.
        
        실제 환경에서는 데이터베이스나 설정 파일에서 
        사용자별 선호도를 로드하겠지만,
        여기서는 예시를 위해 하드코딩된 값을 사용합니다.
        """
        return {
            'preferred_meeting_room': 'Conference Room B',
            'meeting_duration': 60,  # 기본 회의 시간 (분)
            'notification_time': 15,  # 회의 전 알림 시간 (분)
            'preferred_time_slots': ['10:00', '14:00', '16:00'],  # 선호 시간대
            'attendee_limit': 10  # 최대 참석자 수
        }
    
    def _is_important_experience(self, results: Dict) -> bool:
        """
        경험의 중요도를 평가합니다.
        
        중요한 경험은 장기 기억으로 승격될 가능성이 높습니다.
        다음과 같은 경험이 중요하다고 판단됩니다:
        1. 실패한 작업이 있는 경우 (학습 기회)
        2. 복잡한 작업 (많은 단계)
        3. 완전히 성공한 복잡한 작업 (모범 사례)
        """
        # 실패가 있으면 중요 (왜 실패했는지 학습해야 함)
        has_failure = False
        for result in results.values():
            if isinstance(result, dict) and not result.get('success', True):
                has_failure = True
                break
        
        if has_failure:
            return True

        # 복잡한 작업 (5단계 이상)은 중요
        if len(results) > 5:
            return True
        
        # 모든 작업이 성공한 경우 중 복잡한 것은 중요
        # (성공 패턴을 학습하기 위해)
        all_success = all(
            r.get('success', False) or 'data' in r
            for r in results.values()
            if isinstance(r, dict)
        )

        return all_success and len(results) >= 3
    
    def start_task(self, task_name: str):
        """
        새로운 작업을 시작합니다.
        
        작업 기억을 초기화하고 현재 작업 정보를 저장합니다.
        이를 통해 여러 작업을 순차적으로 처리할 때
        각 작업이 독립적인 컨텍스트를 가질 수 있습니다.
        """
        # 이전 작업 기억 정리
        # 새 작업을 시작하기 전에 깨끗한 상태로 만듭니다
        self.memory.clear_working_memory()
        
        # 새 작업 정보를 작업 기억에 저장
        task_info = {
            'key': 'current_task',
            'task': task_name,
            'started_at': datetime.now()
        }
        self.memory.store(
            information=task_info,
            memory_type='working'  # 작업 기억에 저장
        )
        
        print(f"새 작업 시작: {task_name}")
        print(f" 시작 시간: {task_info['started_at'].strftime('%H:%M:%S')}")
    
    def end_task(self):
        """
        현재 작업을 종료합니다.
        
        작업 요약을 단기 기억에 저장하고,
        작업 기억을 정리하여 다음 작업을 위한 준비를 합니다.
        """
        # 현재 작업 정보 가져오기
        working_data = self.memory.working_memory.get('current_task')
        
        if working_data:
            # 작업 소요 시간 계산
            duration = datetime.now() - working_data['started_at']
            
            # 작업 요약을 만들어 단기 기억에 저장
            summary = {
                'content': f"작업 완료: {working_data['task']}",
                'task': working_data['task'],
                'duration': str(duration),  # 문자열로 변환하여 저장
                'completed_at': datetime.now()
            }
            self.memory.store(summary, memory_type='short')
            
            print(f" 작업 종료: {working_data['task']}")
            print(f" 소요 시간: {duration}")
        
        # 작업 기억 초기화
        self.memory.clear_working_memory()
        print(" 작업 기억이 초기화되었습니다")
    
    def get_status(self) -> Dict:
        """
        에이전트의 현재 상태를 반환합니다.
        
        이 메서드는 디버깅과 모니터링에 유용합니다.
        메모리 상태, 등록된 도구, 현재 작업 등
        시스템의 전체적인 상태를 한눈에 볼 수 있습니다.
        """
        # 메모리 상태
        memory_status = {
            'short_term': len(self.memory.short_term_memory),
            'long_term': len(self.memory.long_term_memory),
            'working': len(self.memory.working_memory)
        }
        
        # 현재 작업 정보
        current_task = self.memory.working_memory.get('current_task')
        if current_task:
            task_info = {
                'name': current_task['task'],
                'started_at': current_task['started_at'].strftime('%H:%M:%S')
            }
        else:
            task_info = None
        
        # 전체 상태 정보
        status = {
            'memory': memory_status,
            'tools': self.tool_manager.list_tools(),
            'tool_count': len(self.tool_manager.tools),
            'current_task': task_info,
            'llm_provider': self.llm.__class__.__name__
        }
        
        return status

    def get_memory_summary(self) -> str:
        """
        메모리 상태에 대한 간단한 요약을 반환합니다.
        
        사용자가 에이전트의 기억 상태를 
        빠르게 파악할 수 있도록 돕습니다.
        """
        status = self.get_status()
        mem = status['memory']
        
        summary = f"메모리 상태: "
        summary += f"단기({mem['short_term']}), "
        summary += f"장기({mem['long_term']}), "
        summary += f"작업({mem['working']})"
        
        return summary



