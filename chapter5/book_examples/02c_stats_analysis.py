"""
조건부 협업 3단계: 실행 및 성능 분석
목표: 시스템 효율성 측정
"""

class SmartCoordinator:
    # ... (이전 코드 계속)
    
    def print_stats(self):
        """처리 통계 출력"""
        total = self.stats["total"]
        if total == 0:
            print("아직 처리된 문의가 없습니다.")
            return
        
        print(f"\n{'='*60}")
        print("처리 통계")
        print(f"{'='*60}")
        print(f"총 문의: {total}건")
        print(f"기술 문의만: {self.stats['tech_only']}건 "
              f"({self.stats['tech_only']/total*100:.1f}%)")
        print(f"정책 문의만: {self.stats['policy_only']}건 "
              f"({self.stats['policy_only']/total*100:.1f}%)")
        print(f"복합 문의: {self.stats['both']}건 "
              f"({self.stats['both']/total*100:.1f}%)")

# 테스트
if __name__ == "__main__":
    coordinator = SmartCoordinator()
    
    test_cases = [
        "제품이 자꾸 멈춰요",
        "환불 받고 싶어요",
        "고장났는데 교환 가능한가요?",
        "영업시간이 언제인가요?"
    ]
    
    for inquiry in test_cases:
        result = coordinator.process(inquiry)
        print(result)
        print()
    
    coordinator.print_stats()