"""
하이브리드 시스템 3단계: 실행 및 분석
목표: 시스템 성능 측정 및 인사이트 도출
"""

class HybridSystem:
    # ... (이전 코드 계속)
    
    def print_stats(self):
        """처리 통계 출력"""  # ❶
        total = self.stats["total"]
        if total == 0:
            print("아직 처리된 문의가 없습니다.")
            return
        
        print(f"\n{'='*60}")
        print("시스템 성능 통계")
        print(f"{'='*60}")
        print(f"총 처리 문의: {total}건")
        print(f"총 처리 시간: {self.stats['total_time']:.2f}초")
        print(f"평균 처리 시간: {self.stats['total_time']/total:.2f}초\n")
        
        print("복잡도별 분포:")
        for complexity in ["simple", "moderate", "complex"]:  # ❷
            count = self.stats[complexity]
            percentage = (count / total * 100) if total > 0 else 0
            avg_time = self.stats["avg_time_by_complexity"].get(complexity, 0)
            system = {
                "simple": "직접 구현",
                "moderate": "LangGraph",
                "complex": "CrewAI"
            }[complexity]
            
            print(f"  {complexity:10s}: {count:3d}건 ({percentage:5.1f}%) | "
                  f"평균 {avg_time:.2f}초 | 시스템: {system}")
        
        # 효율성 계산
        print(f"\n{'='*60}")
        simple_time = self.stats["avg_time_by_complexity"].get("simple", 0)
        moderate_time = self.stats["avg_time_by_complexity"].get("moderate", 0)
        if simple_time > 0 and moderate_time > 0:  # ❸
            efficiency = ((moderate_time - simple_time) / moderate_time * 100)
            print(f"효율성 개선: Simple vs Moderate = {efficiency:.1f}% 단축")
        print(f"{'='*60}\n")

# 테스트
if __name__ == "__main__":
    system = HybridSystem()
    
    # 다양한 복잡도의 문의
    test_cases = [
        "영업시간이 언제인가요?",  # Simple
        "제품이 작동하지 않는데 교환 가능한가요?",  # Moderate
        "제품이 계속 고장나는데 환불이나 교환, 아니면 업그레이드 중 뭐가 좋을까요?",  # Complex
    ]
    
    for inquiry in test_cases:
        result = system.route(inquiry)
        print(f"처리 시간: {result['processing_time']:.2f}초\n")
    
    system.print_stats()