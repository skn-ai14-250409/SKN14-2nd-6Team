import streamlit as st
from utils import mappings

st.title("📘 학생 정보 입력")

# 선택 옵션
gender_options = list(mappings.gender_map.values())
marital_status = list(mappings.marital_status_map.values())
attendance_options = list(mappings.attendance_map.values())
course_options = list(mappings.course_map.values())
qualification_options = list(mappings.previous_qualification_map.values())
occupation_options = list(mappings.occupation_map.values())
yes_no_options = list(mappings.yes_no_map.values())
scholarship_options = list(mappings.scholarship_holder_map.values())

with st.form("student_form"):
    st.subheader("🎓 기본 정보")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("**성별**", gender_options)
        course = st.selectbox("**전공**", course_options)
    with col2:
        marital_status = st.selectbox("**결혼 상태**", marital_status)
        attendance = st.selectbox("**수업 형태**", attendance_options)

    age = st.slider("**입학 나이**", 17, 70, 21)

    st.markdown("---")
    st.subheader("📚 학력 및 가족 정보")
    col4, col5, col6 = st.columns(3)
    with col4:
        prev_qual = st.selectbox("**이전 학력**", qualification_options)
    with col5:
        mother_occ = st.selectbox("**어머니 직업**", occupation_options)
    with col6:
        father_occ = st.selectbox("**아버지 직업**", occupation_options)

    st.markdown("---")
    st.subheader("📈 성적 입력")
    col7, col8 = st.columns(2)
    with col7:
        cu1_approved = st.number_input("**1학기 이수 과목 수**", 0, 20, 5)
        cu1_grade = st.number_input("**1학기 평균 성적**", 0.0, 20.0, 10.0, step=0.1)
    with col8:
        cu2_approved = st.number_input("**2학기 이수 과목 수**", 0, 20, 5)
        cu2_grade = st.number_input("**2학기 평균 성적**", 0.0, 20.0, 10.0, step=0.1)

    st.markdown("---")
    st.subheader("📝 기타 정보")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        displaced = st.radio("**거주지 이탈 여부**", yes_no_options)
    with col2:
        special_needs = st.radio("**특수 교육 필요**", yes_no_options)
    with col3:
        debtor = st.radio("**채무 여부**", yes_no_options)
    with col4:
        tuition_paid = st.radio("**등록금 납부 여부**", yes_no_options)
    with col5:
        scholarship = st.radio("**장학금 수혜 여부**", scholarship_options)

    st.markdown("---")
    submitted = st.form_submit_button("예측하기")

# ----------------------------
# 제출 후 세션 저장 및 페이지 이동
# ----------------------------
if submitted:
    st.session_state['form_input'] = {
        'Course': course,
        'Daytime/evening attendance': attendance,
        'Previous qualification': prev_qual,
        "Mother's occupation": mother_occ,
        "Father's occupation": father_occ,
        'Displaced': displaced,
        'Educational special needs': special_needs,
        'Debtor': debtor,
        'Tuition fees up to date': tuition_paid,
        'Gender': gender,
        'Marital status': marital_status,
        'Scholarship holder': scholarship,
        'Age at enrollment': age,
        'Curricular units 1st sem (approved)': cu1_approved,
        'Curricular units 1st sem (grade)': cu1_grade,
        'Curricular units 2nd sem (approved)': cu2_approved,
        'Curricular units 2nd sem (grade)': cu2_grade
    }

    st.success("✅ 정보가 저장되었습니다. 예측 결과 페이지로 이동합니다.")
    st.switch_page("pages/result.py")
