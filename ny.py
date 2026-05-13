import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. 데이터 로드 (기획자의 데이터베이스) ---
@st.cache_data
def load_data():
    try:
        # 실제로는 대학 입시 결과가 담긴 CSV 파일을 읽어옵니다.
        return pd.read_csv("univ_data.csv")
    except:
        # 파일이 없을 경우를 대비한 가상의 샘플 데이터
        data = {
            "대학": ["서울대", "서울대", "연세대", "한양대"],
            "학과": ["정보시스템", "컴퓨학", "산업공학", "정보시스템"],
            "전형": ["교과", "학종", "교과", "학종"],
            "컷": [1.2, 1.5, 1.4, 2.1]
        }
        return pd.DataFrame(data)

db = load_data()

# --- 2. UI 구성 ---
st.set_page_config(page_title="Academic Strategy Planner", layout="wide")
st.title("🏛️ 전략적 기획자를 위한 입시 타겟 시뮬레이터")

# 사이드바: 타겟 설정
st.sidebar.header("🎯 Target Setting")
selected_univ = st.sidebar.selectbox("타겟 대학", db["대학"].unique())
filtered_dept = db[db["대학"] == selected_univ]["학과"].unique()
selected_dept = st.sidebar.selectbox("타겟 학과", filtered_dept)
selected_type = st.sidebar.selectbox("지원 전형", db[(db["대학"] == selected_univ) & (db["학과"] == selected_dept)]["전형"])

target_cut = db[(db["대학"] == selected_univ) & (db["학과"] == selected_dept) & (db["전형"] == selected_type)]["컷"].values[0]

# --- 3. 성적 관리 시스템 (세션 관리) ---
if 'grade_table' not in st.session_state:
    st.session_state.grade_table = pd.DataFrame(columns=["학기", "단위수", "등급"])

st.header(f"📍 {selected_univ} {selected_dept} [{selected_type}] 분석 리포트")
st.write(f"해당 학과의 평균 합격 컷: **{target_cut} 등급**")

# 입력창
with st.expander("📝 성적 데이터 업데이트", expanded=True):
    c1, c2, c3 = st.columns(3)
    in_term = c1.selectbox("해당 학기", ["1-1", "1-2", "2-1", "2-2", "3-1"])
    in_unit = c2.number_input("이수 단위 합계", 1, 50, 20)
    in_grade = c3.number_input("해당 학기 평균 등급", 1.0, 5.0, 2.0)
    
    if st.button("데이터 동기화"):
        new_row = pd.DataFrame({"학기": [in_term], "단위수": [in_unit], "등급": [in_grade]})
        st.session_state.grade_table = pd.concat([st.session_state.grade_table, new_row], ignore_index=True)
        st.rerun()

# --- 4. 분석 엔진 (핵심) ---
if not st.session_state.grade_table.empty:
    df = st.session_state.grade_table
    
    # 가중 평균 계산
    total_weighted_grade = (df["단위수"] * df["등급"]).sum()
    total_units = df["단위수"].sum()
    my_avg = total_weighted_grade / total_units
    
    # 갭 분석 (Gap Analysis)
    gap = my_avg - target_cut
    
    col1, col2, col3 = st.columns(3)
    col1.metric("나의 현재 평균", f"{my_avg:.2f}")
    col2.metric("목표 합격 컷", f"{target_cut}")
    col3.metric("전략적 격차", f"{-gap:.2f}", delta_color="inverse")
    
    # 시각화: 성적 추이 (학종용 전략)
    st.subheader("📉 학기별 성적 변동 추이")
    fig = px.line(df, x="학기", y="등급", markers=True)
    fig.update_yaxes(autorange="reversed") # 등급은 낮을수록 높음
    st.plotly_chart(fig, use_container_width=True)
    
    # 전략 제언
    st.divider()
    st.subheader("💡 기획자 전략 제언")
    if gap <= 0:
        st.success("✅ **안정권:** 현재 데이터를 유지하며 비교과(학종 시)를 보완하는 '방어적 전략'을 추천합니다.")
    else:
        # 남은 학기 목표 계산 (전체 170단위 가정)
        rem_units = 170 - total_units
        req_grade = (target_cut * 170 - total_weighted_grade) / rem_units
        st.warning(f"⚠️ **상향권:** 목표 달성을 위해 남은 학기 평균 **{req_grade:.2f} 등급**이 필요합니다. 리소스 재배치가 필요합니다.")

else:
    st.info("성적 데이터를 입력하면 전략 리포트가 생성됩니다.")
