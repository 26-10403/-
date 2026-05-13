class StudyPlanner:
    def __init__(self, target_avg):
        self.target_avg = target_avg
        # 과목명: [현재등급, 단위수]
        self.subjects = {
            "국어": [3, 4],
            "수학": [4, 4],
            "영어": [2, 3],
            "탐구1": [5, 2],
            "탐구2": [4, 2]
        }

    def analyze(self):
        total_units = sum(s[1] for s in self.subjects.values())
        current_sum = sum(s[0] * s[1] for s in self.subjects.values())
        current_avg = current_sum / total_units
        
        # 목표를 위해 도달해야 하는 가중치 합의 총량
        goal_sum = self.target_avg * total_units
        # 줄여야 하는 등급 포인트 (낮을수록 좋은 등급이므로)
        points_to_reduce = current_sum - goal_sum

        print(f"📊 현재 평균: {current_avg:.2f} / 목표 평균: {self.target_avg:.2f}")
        print(f"📉 목표 달성을 위해 총 {points_to_reduce:.1f} 등급 포인트를 낮춰야 합니다.\n")

        # 효율성 계산 (단위수/현재등급 비율 - 낮을수록 개선 여지가 큼)
        # 정보시스템의 '자원 최적화' 논리: 단위수가 크고 등급이 높은(못하는) 과목부터 공략
        sorted_subs = sorted(self.subjects.items(), key=lambda x: (x[1][0] * x[1][1]), reverse=True)

        print(f"{' 과목':<6} | {' 현재':<5} | {' 목표':<5} | {' 권장 비중'}")
        print("-" * 45)

        remaining = points_to_reduce
        for name, info in sorted_subs:
            curr_grade, unit = info
            
            # 이 과목에서 최대로 줄일 수 있는 등급 (1등급이 한계)
            max_reduction = curr_grade - 1
            # 실제 줄일 등급 (필요량과 최대치 중 작은 값)
            actual_reduction = max(0, min(max_reduction, math.ceil(remaining / unit) if unit > 0 else 0))
            
            target_grade = curr_grade - actual_reduction
            remaining -= (actual_reduction * unit)

            # 시간 배분 로직: (단위수 * 개선 필요도) 기반
            study_weight = unit * (curr_grade - target_grade + 0.5) 
            # 단순 표시용 비중 계산 (임시)
            weight_pct = (study_weight / (total_units * 2)) * 100 

            print(f" {name:<6} |  {curr_grade:>2}등급  |  {target_grade:>2}등급  |  {weight_pct:>5.1f}%")

import math
# 실행부
planner = StudyPlanner(target_avg=2.5) # 여기에 목표 등급 입력
planner.analyze()
