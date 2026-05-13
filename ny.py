import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. 입시 데이터베이스 (전략적 기획자의 핵심 자산) ---
# 주요 대학 및 학과별 샘플 데이터 (가장 대중적인 학과 위주로 구성)
raw_data = [
    ["서울대", "컴퓨터공학", "학종", 1.1], ["서울대", "정보시스템", "학종", 1.3],
    ["연세대", "IT융합", "교과", 1.2], ["연세대", "인공지능", "학종", 1.5],
    ["고려대", "데이터과학", "교과", 1.4], ["고려대", "컴퓨터학", "학종", 1.6],
    ["한양대", "정보시스템", "교과", 1.5], ["한양대", "소프트웨어", "학종", 1.8],
    ["성균관대", "글로벌바이오메디컬", "교과", 1.3], ["성균관대", "소프트웨어", "학종", 1.9],
    ["서강대", "컴퓨터공학", "교과", 1.6], ["서강대", "시스템반도체", "학종", 1.7],
    ["중앙대", "AI학과", "교과", 1.7], ["중앙대", "산업보안", "학종", 2.0],
    ["경희대", "컴퓨터공학", "교과", 1.8], ["경희대", "소프트웨어융합", "학종", 2.2],
    ["건국대", "컴퓨터공학", "교과", 1.9], ["건국대", "전기전자", "학종", 2.3],
    ["시립대", "컴퓨터과학", "교과", 1.8], ["시립대", "도시공학", "학종", 2.1],
    ["외대", "AI데이터", "교과", 2.1], ["외대", "언어공학", "학종", 2.5],
    ["과기대", "IT융합", "교과", 2.2], ["과기대", "MSDE", "학종", 2.4],
    ["가천대", "클라우드공학", "교과", 2.3], ["가천대", "AI소프트웨어", "학종", 2.8],
    ["인하대", "정보통신", "교과", 2.2], ["인하대", "컴퓨터공학", "학종", 2.6],
    ["인천대", "컴퓨터공학", "교과", 2.6], ["인천대", "정보통신", "학종", 3.0],
    ["경북대", "IT융합", "교과", 2.4], ["경북대", "컴퓨터학", "학종", 2.8],
    ["부산대", "정보컴퓨터", "교과", 2.3], ["부산대", "의생명융합", "학종", 2.7],
    ["전남대", "소프트웨어", "교과", 2.8], ["전남대", "인공지능", "학종", 3.2],
    ["전북대", "컴퓨터공학", "교과", 3.0], ["전북대", "IT융합", "학종", 3.5],
    ["경북대", "전기공학", "교과", 2.5], ["조선대", "컴퓨터공학", "교과", 3.5]
]
db = pd.DataFrame(raw_data, columns=["대학", "학과", "전형", "컷"])

# --- 2. 앱 레이아웃 설정 ---
st.set_page_config(page_title="Total Univ Strategy", layout="wide")
st.title("🎯 전방위 대학 타겟팅 시스템")
st.markdown("전국 주요 대학 데이터 기반 **전략적 입시 로드맵**")

# --- 3. 사이드바: 목표 설정 ---
with st.sidebar:
    st.header("📍 Target Info")
    sel_u = st.selectbox("대학 선택", sorted(db["대학"].unique()))
    sel_d = st.selectbox("학과 선택", db[db["대학"] == sel_u]["학과"].unique())
    sel_t = st.selectbox("전형 선택", db[(db["대학"] == sel_u) & (db["학과"] == sel_d)]["전형"].unique())
    
    target_cut = db[(db["대학"] == sel_u) & (db["학과"] == sel_d) & (db["전형"] == sel_t)]["컷"].values[0]
    st.metric("목표 합격 컷(70%)", f"{target_cut} 등급")

# --- 4. 메인 분석 영역 ---
if 'my_grades' not in st.session_state:
    st.session_state.my_grades = pd.DataFrame(columns=["학기", "단위수", "등급"])

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📝 나의 성적 데이터")
    with st.form("input_form", clear_on_submit=True):
        term = st.selectbox("기록 학기", ["1-1", "1-2", "2-1", "2-2", "3-1"])
        unit = st.number_input("이수 단위 합계", 1, 50, 20)
        grade = st.number_input("평균 등급", 1.0, 5.0, 2.0, step=0.1)
        if st.form_submit_button("데이터 저장"):
            new_row = pd.DataFrame({"학기": [term], "단위수": [unit], "등급": [grade]})
            st.session_state.my_grades = pd.concat([st.session_state.my_grades, new_row], ignore_index=True)
            st.rerun()
    
    st.dataframe(st.session_state.my_grades, use_container_width=True)

with col2:
    st.subheader("📊 전략적 갭 분석")
    if not st.session_state.my_grades.empty:
        df = st.session_state.my_grades
        my_avg = (df["단위수"] * df["등급"]).sum() / df["단위수"].sum()
        gap = my_avg - target_cut
        
        c1, c2 = st.columns(2)
        c1.metric("내 현재 평균", f"{my_avg:.2f}")
        c2.metric("목표 대비 격차", f"{-gap:.2f}", delta_color="inverse")
        
        # 추이 그래프
        fig = px.line(df, x="학기", y="등급", markers=True, title="성적 변화 추이")
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
        
        # 리소스 할당 제언
        st.divider()
        st.subheader("💡 전략적 기획자 코멘트")
        if gap <= 0:
            st.success(f"현재 **{sel_u} {sel_d}** 합격권 내에 있습니다. 학생부 내용의 전문성을 높이는 '심화 전략'을 권장합니다.")
        else:
            total_u = 180 # 졸업 총 단위 가정
            done_u = df["단위수"].sum()
            rem_u = total_u - done_u
            req_g = (target_cut * total_u - (df["단위수"] * df["등급"]).sum()) / rem_u
            st.warning(f"목표 달성을 위해 남은 학기 동안 평균 **{req_g:.2f} 등급**이 필요합니다. 취약 과목에 대한 '리소스 재배치'가 시급합니다.")
    else:
        st.info("성적을 입력하면 분석 결과가 나타납니다.")


