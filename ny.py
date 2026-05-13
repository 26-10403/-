import streamlit as st
import pandas as pd

st.set_page_config(page_title="전략적 내신 기획자", layout="wide")

st.title("🎯 Academic Resource Optimizer")
st.subheader("정보시스템 기반의 전략적 성적 관리 시스템")

# --- 데이터 입력 ---
with st.sidebar:
    st.header("📊 분석 설정")
    target_avg = st.number_input("최종 목표 평균 등급", 1.0, 5.0, 1.5)
    total_hours = st.slider("주간 총 가용 공부 시간 (시간)", 10, 100, 40)

# 세션 데이터 관리
if 'subjects' not in st.session_state:
    st.session_state.subjects = []

with st.expander("➕ 과목 데이터 입력", expanded=True):
    c1, c2, c3 = st.columns(3)
    sub_name = c1.text_input("과목명")
    sub_unit = c2.number_input("단위수", 1, 10, 4)
    sub_difficulty = c3.select_slider("본인 체감 난이도", options=["하", "중", "상"])
    
    if st.button("과목 추가"):
        st.session_state.subjects.append({
            "과목명": sub_name,
            "단위수": sub_unit,
            "난이도": sub_difficulty
        })

# --- 전략 분석 로직 ---
if st.session_state.subjects:
    df = pd.DataFrame(st.session_state.subjects)
    
    st.divider()
    st.header("📋 전략적 리소스 배분 제안")
    
    # 전략 지수 계산 (단위수가 높고 난이도가 높을수록 더 많은 시간 배정)
    diff_map = {"하": 1, "중": 1.5, "상": 2}
    df['priority_score'] = df['단위수'] * df['난이도'].map(diff_map)
    total_score = df['priority_score'].sum()
    df['권장 공부 시간(h)'] = (df['priority_score'] / total_score * total_hours).round(1)
    
    # 결과 출력
    cols = st.columns(len(df))
    for i, row in df.iterrows():
        cols[i].metric(row['과목명'], f"{row['권장 공부 시간(h)']}시간", f"{row['단위수']}단위")

    st.write("### 💡 기획자의 분석 의견")
    top_subject = df.loc[df['priority_score'].idxmax(), '과목명']
    st.info(f"현재 데이터 분석 결과, **{top_subject}** 과목이 전체 등급에 미치는 영향력이 가장 큽니다. 이번 시험 기간에는 해당 과목에 리소스를 집중하는 '집중형 전략'을 추천합니다.")

    # 데이터 시각화
    st.bar_chart(df.set_index("과목명")['권장 공부 시간(h)'])
