import math

def calculate_study_strategy():
    # 1. 초기 데이터 설정 (정보시스템적 데이터 구조화)
    # 과목명: [현재 등급, 단위수(가중치)]
    current_grades = {
        "국어": [3, 4],
        "수학": [4, 4],
        "영어": [2, 3],
        "탐구1": [5, 2],
        "탐구2": [4, 2]
    }
    
    target_avg = 2.5  # 목표 평균 등급 (5등급제 기준)
    
    print("="*50)
    print(f"🎯 목표 평균 등급: {target_avg}")
    print("="*50)

    # 2. 현재 상태 분석
    total_units = sum(info[1] for info in current_grades.values())
    current_weighted_sum = sum(info[0] * info[1] for info in current_grades.values())
    current_avg = current_weighted_sum / total_units
    
    # 3. 목표 달성을 위한 필요 점수 계산
    # 목표 가중치 합 = 목표 등급 * 총 단위수
    target_weighted_sum = target_avg * total_units
    needed_improvement = current_weighted_sum - target_weighted_sum
    
    if needed_improvement <= 0:
        print(f"현재 평균 {current_avg:.2f}로 이미 목표를 달성 중입니다! 유지에 힘쓰세요.")
        return

    # 4. 과목별 전략 배분 (알고리즘: 가중치 대비 상승 가능성 우선순위)
    # 정보시스템 효율성 원칙: 단위수가 높고 등급이 낮은 과목에 투자할 때 ROI(투자 대비 효율)가 높음
    print(f"현재 평균: {current_avg:.2f} | 목표까지 필요한 등급 합 개선: {needed_improvement:.1f}")
    print("\n[📊 과목별 목표 및 시간 배분 전략]")
    
    strategy = []
    for subject, (grade, unit) in current_grades.items():
        # 상승 가능한 폭 (1등급이 최상이라고 가정)
        potential_gain = grade - 1
        # 효율성 점수 = 단위수 * 잠재적 이득
        efficiency_score = unit * potential_gain
        strategy.append({
            "과목": subject,
            "현재": grade,
            "단위수": unit,
            "효율성": efficiency_score
        })

    # 효율성(내림차순)으로 정렬
    strategy.sort(key=lambda x: x['효율성'], reverse=True)

    remaining_improvement = needed_improvement
    total_study_time_pct = 100
    time_allocation = {}

    for s in strategy:
        if remaining_improvement > 0:
            # 현실적으로 과목당 최대 2등급까지만 올리는 것으로 시뮬레이션
            possible_jump = min(s['현재'] - 1, math.ceil(remaining_improvement / s['단위수']))
            if possible_jump < 0: possible_jump = 0
            
            target_grade = s['현재'] - possible_jump
            remaining_improvement -= (possible_jump * s['단위수'])
            
            # 시간 배분: 단위수가 높고 목표 점수 차이가 클수록 많이 배정
            time_weight = s['단위수'] * (s['현재'] - target_grade + 0.5)
            time_allocation[s['과목']] = time_weight
        else:
            target_grade = s['현재']
            time_allocation[s['과목']] = s['단위수'] * 0.5

    # 시간 비중 백분율 계산
    total_w = sum(time_allocation.values())
    
    print(f"{'과목':<6} | {'현재':<4} -> {'목표':<4} | {'공부 비중':<10}")
    print("-" * 40)
    for s in strategy:
        subj = s['과목']
        share = (time_allocation[subj] / total_w) * 100
        # 실제 목표 등급 계산 반영 (단순 표시용)
        final_target = s['현재'] - min(s['현재']-1, max(0, math.ceil((time_allocation[subj]/total_w)*needed_improvement/s['단위수'])))
        
        # 만약 계산상 목표가 현재보다 낮아지면 현재 등급 유지로 표시
        if final_target > s['현재']: final_target = s['현재']
            
        print(f"{subj:<7} | {s['현재']:>3}등급 -> {final_target:>3}등급 | {share:>8.1f}%")

    print("\n💡 Tip: 비중이 높은 과목은 단위수가 크거나 현재 등급이 낮아 성적 상승 시 평균 기여도가 큰 과목입니다.")

if __name__ == "__main__":
    calculate_study_strategy()
