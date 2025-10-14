"""
조건부 협업 2단계: 필요한 에이전트만 실행
목표: 효율적인 리소스 활용
"""

class SmartCoordinator:
    # ... (이전 코드 계속)
    
    def process(self, inquiry):
        """스마트 처리"""  # ❶
        self.stats["total"] += 1
        
        routing = self.analyze_inquiry_type(inquiry)
        
        print(f"\n{'='*60}")
        print(f"문의: {inquiry}")
        print(f"라우팅 결정: {routing}")
        print(f"{'='*60}\n")
        
        results = {}
        
        # 필요한 에이전트만 실행
        if routing["technical_needed"]:  # ❷
            print(" 기술 에이전트 활성화...")
            results["tech"] = self.tech_agent.analyze(inquiry)
            if not routing["policy_needed"]:
                self.stats["tech_only"] += 1
        
        if routing["policy_needed"]:
            print(" 정책 에이전트 활성화...")
            context = results.get("tech", {})
            results["policy"] = self.policy_agent.check(context)
            if not routing["technical_needed"]:
                self.stats["policy_only"] += 1
        
        if routing["technical_needed"] and routing["policy_needed"]:
            self.stats["both"] += 1
        
        # 결과가 없으면 기본 응답
        if not results:  # ❸
            return self._handle_unknown(inquiry)
        
        # 결과 통합
        return self._integrate_results(results)
    
    def _handle_unknown(self, inquiry):
        """알 수 없는 문의 처리"""
        return """죄송합니다. 문의 내용을 정확히 파악하지 못했습니다.

다음과 같이 구체적으로 설명해주시면 더 정확한 답변을 드릴 수 있습니다:
- 제품명과 모델명
- 발생한 문제의 구체적인 증상
- 원하시는 해결 방안 (수리/교환/환불 등)

또는 고객센터(1234-5678)로 직접 문의해주세요."""
    
    def _integrate_results(self, results):
        """결과 통합"""  # ❹
        response = "고객님께 답변드립니다.\n\n"
        
        if "tech" in results:
            response += f"【기술 진단】\n{results['tech']['analysis']}\n\n"
        
        if "policy" in results:
            response += f"【정책 안내】\n{results['policy']['guidance']}\n\n"
        
        response += "추가 문의사항이 있으시면 언제든 연락 주세요."
        return response