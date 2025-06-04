import streamlit as st
import joblib
import numpy as np

# 모델 불러오기
model = joblib.load('best_model_pipeline.pkl')  # 실제 경로에 맞게 수정

# 세션 상태로 페이지 관리
if 'page' not in st.session_state:
    st.session_state.page = 'input'

# ===== 1. 정보 입력 페이지 =====
if 'page' not in st.session_state:
    st.session_state.page = 'input'

if st.session_state.page == 'input':
    st.title("학생 중도이탈 예측 시스템")
    st.subheader("정보 입력")

    # ---- 사진 업로드 ----
    uploaded_file = st.file_uploader("사진 추가", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, width=150)
    else:
        st.image("https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png", width=150)

    # ---- 기본 정보 ----
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 기본 정보")
        age = st.number_input("입학 나이", min_value=15, max_value=40, value=20)
        gender = st.selectbox("성별", ["여성", "남성"])
        marital_status = st.selectbox("결혼 상태", ["미혼", "기혼", "이혼"])

    with col2:
        st.markdown("### 학업 정보")
        course = st.selectbox("수강 전공", ["경영학", "컴퓨터공학", "전자공학", "기타"])
        attendance = st.selectbox("주/야간 수업", ["주간", "야간"])
        prev_qualification = st.selectbox("이전 학력", ["고졸", "전문대졸", "학사", "기타"])

    # ---- 재정 및 환경 정보 ----
    st.markdown("### 재정 및 환경 정보")
    col3, col4 = st.columns(2)
    with col3:
        mother_job = st.selectbox("어머니 직업", ["서비스/보건/판매", "관리직", "기타"])
        father_job = st.selectbox("아버지 직업", ["미숙련 근로자", "관리직", "기타"])
        displaced = st.selectbox("이재민 여부", ["아니오", "예"])
        special_needs = st.selectbox("특수 교육 필요 여부", ["아니오", "예"])
    with col4:
        debtor = st.selectbox("연체 여부", ["아니오", "예"])
        tuition = st.selectbox("등록금 납부 여부", ["예", "아니오"])
        scholarship = st.selectbox("장학금 수혜 여부", ["미수혜", "수혜"])

    # ---- 성적 정보 ----
    st.markdown("### 성적 정보")
    first_sem_approved = st.number_input("1학기 합격 과목 수", min_value=0, max_value=10, value=5)
    first_sem_grade = st.number_input("1학기 성적 평균", min_value=0.0, max_value=20.0, value=12.5)
    second_sem_approved = st.number_input("2학기 합격 과목 수", min_value=0, max_value=10, value=4)
    second_sem_grade = st.number_input("2학기 성적 평균", min_value=0.0, max_value=20.0, value=11.0)

    # ---- 정보 확인하기 버튼 ----
    if st.button("정보 확인하기"):
        st.session_state.form_input = {
            "Gender": gender,
            "Age": age,
            "Marital status": marital_status,
            "Course": course,
            "Daytime/evening attendance": attendance,
            "Previous qualification": prev_qualification,
            "Mother's occupation": mother_job,
            "Father's occupation": father_job,
            "Displaced": displaced,
            "Educational special needs": special_needs,
            "Debtor": debtor,
            "Tuition fees up to date": tuition,
            "Scholarship holder": scholarship,
            "Curricular units 1st sem (approved)": first_sem_approved,
            "Curricular units 1st sem (grade)": first_sem_grade,
            "Curricular units 2nd sem (approved)": second_sem_approved,
            "Curricular units 2nd sem (grade)": second_sem_grade,
        }
        st.session_state.page = 'form_input'
        st.switch_page("pages/3_result.py")

    # 이전으로 돌아가기
    if st.button("이전으로"):
        st.session_state.page = 'input'
        st.rerun()
