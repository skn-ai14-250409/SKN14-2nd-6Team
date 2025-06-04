import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# 프로젝트 루트 경로를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

import mappings

MODEL_FEATURES_INPUT_ORDER = [
    'Marital status', 'Course', 'Daytime/evening attendance', 'Previous qualification',
    "Mother's occupation", "Father's occupation", 'Displaced', 'Educational special needs', 'Debtor',
    'Tuition fees up to date', 'Gender', 'Scholarship holder', 'Age',
    'Curricular units 1st sem (approved)', 'Curricular units 1st sem (grade)',
    'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)'
]

FEATURE_DETAILS = {
    'Marital status': {"label": "결혼 상태", "options_map": mappings.marital_status_map, "default_key": 1,
                       "type": "select"},
    'Course': {"label": "수강 과정", "options_map": mappings.course_map, "default_key": 10, "type": "select"},
    'Daytime/evening attendance': {"label": "주/야간 수업", "options_map": mappings.attendance_map, "default_key": 1,
                                   "type": "select"},
    'Previous qualification': {"label": "이전 학력", "options_map": mappings.previous_qualification_map, "default_key": 1,
                               "type": "select"},
    "Mother's occupation": {"label": "어머니 직업", "options_map": mappings.occupation_map, "default_key": 5,
                            "type": "select"},
    "Father's occupation": {"label": "아버지 직업", "options_map": mappings.occupation_map, "default_key": 5,
                            "type": "select"},
    'Displaced': {"label": "거주지 이탈 여부", "options_map": mappings.yes_no_map, "default_key": 0, "type": "select"},
    'Educational special needs': {"label": "특수 교육 필요 여부", "options_map": mappings.yes_no_map, "default_key": 0,
                                  "type": "select"},
    'Debtor': {"label": "학자금 연체 여부", "options_map": mappings.yes_no_map, "default_key": 0, "type": "select"},
    'Tuition fees up to date': {"label": "등록금 납부 여부", "options_map": mappings.yes_no_map, "default_key": 1,
                                "type": "select"},
    'Gender': {"label": "성별", "options_map": mappings.gender_map, "default_key": 1, "type": "select"},
    'Scholarship holder': {"label": "장학금 수혜 여부", "options_map": mappings.scholarship_holder_map, "default_key": 0,
                           "type": "select"},
    'Age': {"label": "입학 시 나이", "min": 17, "max": 70, "default": 21, "type": "int_slider"},
    'Curricular units 1st sem (approved)': {"label": "1학기 이수 과목 수", "min": 0, "max": 26, "default": 0,
                                            "type": "int_input"},
    'Curricular units 1st sem (grade)': {"label": "1학기 평균 성적", "min": 0.0, "max": 20.0, "default": 0.0,
                                         "type": "float_input", "step": 0.01, "format": "%.2f"},
    'Curricular units 2nd sem (approved)': {"label": "2학기 이수 과목 수", "min": 0, "max": 20, "default": 0,
                                            "type": "int_input"},
    'Curricular units 2nd sem (grade)': {"label": "2학기 평균 성적", "min": 0.0, "max": 20.0, "default": 0.0,
                                         "type": "float_input", "step": 0.01, "format": "%.2f"}
}

DUMMY_DATA_DROPOUT_RISK_KEYS = {
    'Marital status': 1, 'Course': 2, 'Daytime/evening attendance': 1, 'Previous qualification': 1,
    "Mother's occupation": 10, "Father's occupation": 10, 'Displaced': 1, 'Educational special needs': 0, 'Debtor': 1,
    'Tuition fees up to date': 0, 'Gender': 1, 'Scholarship holder': 0, 'Age': 19,
    'Curricular units 1st sem (approved)': 0, 'Curricular units 1st sem (grade)': 0.0,
    'Curricular units 2nd sem (approved)': 0, 'Curricular units 2nd sem (grade)': 0.0
}

DUMMY_DATA_GRADUATE_EXPECTED_KEYS = {
    'Marital status': 1, 'Course': 11, 'Daytime/evening attendance': 1, 'Previous qualification': 1,
    "Mother's occupation": 4, "Father's occupation": 4, 'Displaced': 0, 'Educational special needs': 0, 'Debtor': 0,
    'Tuition fees up to date': 1, 'Gender': 0, 'Scholarship holder': 1, 'Age': 18,
    'Curricular units 1st sem (approved)': 6, 'Curricular units 1st sem (grade)': 15.50,
    'Curricular units 2nd sem (approved)': 6, 'Curricular units 2nd sem (grade)': 16.00
}

st.title("🧑‍🎓 학생 정보 입력")
st.markdown("예측하고자 하는 학생의 정보를 입력해주세요.")

if 'model' not in st.session_state or st.session_state.model is None:
    st.error("모델 로딩에 실패했습니다. 메인 페이지(app.py)를 먼저 실행하거나, 모델 파일을 확인해주세요.")
    if st.button("메인 페이지로 돌아가기"):
        st.switch_page("app.py")
    st.stop()

# 입력 필드 값을 저장할 세션 상태 초기화 (수정된 부분)
for feature_key in MODEL_FEATURES_INPUT_ORDER:
    session_key_form = f"form_{feature_key}"
    if session_key_form not in st.session_state:
        detail = FEATURE_DETAILS[feature_key]
        if "default_key" in detail:
            st.session_state[session_key_form] = detail["default_key"]
        elif "default" in detail:
            st.session_state[session_key_form] = detail["default"]
        else:
            st.error(f"FEATURE_DETAILS의 '{feature_key}' 항목에 'default' 또는 'default_key'가 정의되지 않았습니다.")
            # 이 경우, 해당 feature_key에 대한 기본값을 설정하거나, FEATURE_DETAILS 정의를 수정해야 합니다.
            # 예시로 None 또는 적절한 기본값(e.g., 0 또는 첫번째 옵션 키)을 넣어줍니다.
            if detail.get("type") == "select" and "options_map" in detail and detail["options_map"]:
                st.session_state[session_key_form] = list(detail["options_map"].keys())[0]  # 첫 번째 옵션의 키를 기본값으로
            elif detail.get("type") in ["int_slider", "int_input"]:
                st.session_state[session_key_form] = detail.get("min", 0)  # 최소값을 기본값으로
            elif detail.get("type") == "float_input":
                st.session_state[session_key_form] = detail.get("min", 0.0)  # 최소값을 기본값으로
            else:
                st.session_state[session_key_form] = None

if 'form_student_name' not in st.session_state:
    st.session_state.form_student_name = ""


def load_dummy_data(dummy_profile_keys):
    for key, value in dummy_profile_keys.items():
        session_key_form = f"form_{key}"
        if session_key_form in st.session_state:
            st.session_state[session_key_form] = value
        else:
            print(f"Warning: Dummy data key '{key}' not found for session state form keys.")
    st.session_state.form_student_name = "더미 학생"


st.markdown("---")
st.subheader("빠른 입력 (더미 데이터)")
col_dummy1, col_dummy2, col_dummy3 = st.columns(3)

if col_dummy1.button("중퇴 위험군 예시", use_container_width=True, key="dummy_dropout_btn_input"):
    load_dummy_data(DUMMY_DATA_DROPOUT_RISK_KEYS)

if col_dummy2.button("졸업 예상군 예시", use_container_width=True, key="dummy_graduate_btn_input"):
    load_dummy_data(DUMMY_DATA_GRADUATE_EXPECTED_KEYS)

if col_dummy3.button("입력 필드 초기화", use_container_width=True, key="dummy_reset_btn_input"):
    for feature_key in MODEL_FEATURES_INPUT_ORDER:
        session_key_form = f"form_{feature_key}"
        detail = FEATURE_DETAILS[feature_key]
        if "default_key" in detail:
            st.session_state[session_key_form] = detail["default_key"]
        elif "default" in detail:
            st.session_state[session_key_form] = detail["default"]
        else:  # 위의 초기화 로직과 동일하게 처리
            if detail.get("type") == "select" and "options_map" in detail and detail["options_map"]:
                st.session_state[session_key_form] = list(detail["options_map"].keys())[0]
            elif detail.get("type") in ["int_slider", "int_input"]:
                st.session_state[session_key_form] = detail.get("min", 0)
            elif detail.get("type") == "float_input":
                st.session_state[session_key_form] = detail.get("min", 0.0)
            else:
                st.session_state[session_key_form] = None
    st.session_state.form_student_name = ""
st.markdown("---")

with st.form("student_input_form_actual"):
    input_data_form_values = {}
    input_data_form_labels = {}

    st.subheader("🎓 기본 정보")
    student_name_input = st.text_input("**학생 이름**", value=st.session_state.form_student_name,
                                       key="form_student_name_widget")

    # 기본 정보 섹션 (기존 UI 유지)
    col_basic1, col_basic2 = st.columns(2)
    with col_basic1:
        # Gender
        detail_gender = FEATURE_DETAILS['Gender']
        key_gender = f"widget_Gender"
        session_key_gender = f"form_Gender"
        options_keys_gender = list(detail_gender["options_map"].keys())
        options_labels_gender = list(detail_gender["options_map"].values())
        current_val_gender = st.session_state.get(session_key_gender, detail_gender["default_key"])
        try:
            idx_gender = options_keys_gender.index(current_val_gender)
        except ValueError:
            idx_gender = options_keys_gender.index(detail_gender["default_key"])

        selected_label_gender = st.selectbox(
            label=f'**{detail_gender["label"]}**',
            options=options_labels_gender,
            index=idx_gender,
            key=key_gender
        )
        input_data_form_values['Gender'] = mappings.reverse_map(selected_label_gender, detail_gender["options_map"])
        input_data_form_labels['Gender'] = selected_label_gender

        # Course
        detail_course = FEATURE_DETAILS['Course']
        key_course = f"widget_Course"
        session_key_course = f"form_Course"
        options_keys_course = list(detail_course["options_map"].keys())
        options_labels_course = list(detail_course["options_map"].values())
        current_val_course = st.session_state.get(session_key_course, detail_course["default_key"])
        try:
            idx_course = options_keys_course.index(current_val_course)
        except ValueError:
            idx_course = options_keys_course.index(detail_course["default_key"])

        selected_label_course = st.selectbox(
            label=f'**{detail_course["label"]}**',
            options=options_labels_course,
            index=idx_course,
            key=key_course
        )
        input_data_form_values['Course'] = mappings.reverse_map(selected_label_course, detail_course["options_map"])
        input_data_form_labels['Course'] = selected_label_course

    with col_basic2:
        # Marital status
        detail_marital = FEATURE_DETAILS['Marital status']
        key_marital = f"widget_Marital status"
        session_key_marital = f"form_Marital status"
        options_keys_marital = list(detail_marital["options_map"].keys())
        options_labels_marital = list(detail_marital["options_map"].values())
        current_val_marital = st.session_state.get(session_key_marital, detail_marital["default_key"])
        try:
            idx_marital = options_keys_marital.index(current_val_marital)
        except ValueError:
            idx_marital = options_keys_marital.index(detail_marital["default_key"])

        selected_label_marital = st.selectbox(
            label=f'**{detail_marital["label"]}**',
            options=options_labels_marital,
            index=idx_marital,
            key=key_marital
        )
        input_data_form_values['Marital status'] = mappings.reverse_map(selected_label_marital,
                                                                        detail_marital["options_map"])
        input_data_form_labels['Marital status'] = selected_label_marital

        # Daytime/evening attendance
        detail_attendance = FEATURE_DETAILS['Daytime/evening attendance']
        key_attendance = f"widget_Daytime/evening attendance"
        session_key_attendance = f"form_Daytime/evening attendance"
        options_keys_attendance = list(detail_attendance["options_map"].keys())
        options_labels_attendance = list(detail_attendance["options_map"].values())
        current_val_attendance = st.session_state.get(session_key_attendance, detail_attendance["default_key"])
        try:
            idx_attendance = options_keys_attendance.index(current_val_attendance)
        except ValueError:
            idx_attendance = options_keys_attendance.index(detail_attendance["default_key"])

        selected_label_attendance = st.selectbox(
            label=f'**{detail_attendance["label"]}**',
            options=options_labels_attendance,
            index=idx_attendance,
            key=key_attendance
        )
        input_data_form_values['Daytime/evening attendance'] = mappings.reverse_map(selected_label_attendance,
                                                                                    detail_attendance["options_map"])
        input_data_form_labels['Daytime/evening attendance'] = selected_label_attendance

    # Age
    detail_age = FEATURE_DETAILS['Age']
    key_age = f"widget_Age"
    session_key_age = f"form_Age"
    input_data_form_values['Age'] = st.slider(
        label=f'**{detail_age["label"]}**',
        min_value=detail_age["min"],
        max_value=detail_age["max"],
        value=int(st.session_state.get(session_key_age, detail_age["default"])),
        key=key_age
    )
    input_data_form_labels['Age'] = input_data_form_values['Age']

    st.markdown("---")
    st.subheader("📚 학력 및 가족 정보")
    col_edu1, col_edu2, col_edu3 = st.columns(3)
    with col_edu1:
        # Previous qualification
        detail_prev_qual = FEATURE_DETAILS['Previous qualification']
        key_prev_qual = f"widget_Previous qualification"
        session_key_prev_qual = f"form_Previous qualification"
        options_keys_prev_qual = list(detail_prev_qual["options_map"].keys())
        options_labels_prev_qual = list(detail_prev_qual["options_map"].values())
        current_val_prev_qual = st.session_state.get(session_key_prev_qual, detail_prev_qual["default_key"])
        try:
            idx_prev_qual = options_keys_prev_qual.index(current_val_prev_qual)
        except ValueError:
            idx_prev_qual = options_keys_prev_qual.index(detail_prev_qual["default_key"])

        selected_label_prev_qual = st.selectbox(
            label=f'**{detail_prev_qual["label"]}**',
            options=options_labels_prev_qual,
            index=idx_prev_qual,
            key=key_prev_qual
        )
        input_data_form_values['Previous qualification'] = mappings.reverse_map(selected_label_prev_qual,
                                                                                detail_prev_qual["options_map"])
        input_data_form_labels['Previous qualification'] = selected_label_prev_qual

    with col_edu2:
        # Mother's occupation
        detail_mother_occ = FEATURE_DETAILS["Mother's occupation"]
        key_mother_occ = f"widget_Mother's occupation"
        session_key_mother_occ = f"form_Mother's occupation"
        options_keys_mother_occ = list(detail_mother_occ["options_map"].keys())
        options_labels_mother_occ = list(detail_mother_occ["options_map"].values())
        current_val_mother_occ = st.session_state.get(session_key_mother_occ, detail_mother_occ["default_key"])
        try:
            idx_mother_occ = options_keys_mother_occ.index(current_val_mother_occ)
        except ValueError:
            idx_mother_occ = options_keys_mother_occ.index(detail_mother_occ["default_key"])

        selected_label_mother_occ = st.selectbox(
            label=f'**{detail_mother_occ["label"]}**',
            options=options_labels_mother_occ,
            index=idx_mother_occ,
            key=key_mother_occ
        )
        input_data_form_values["Mother's occupation"] = mappings.reverse_map(selected_label_mother_occ,
                                                                             detail_mother_occ["options_map"])
        input_data_form_labels["Mother's occupation"] = selected_label_mother_occ

    with col_edu3:
        # Father's occupation
        detail_father_occ = FEATURE_DETAILS["Father's occupation"]
        key_father_occ = f"widget_Father's occupation"
        session_key_father_occ = f"form_Father's occupation"
        options_keys_father_occ = list(detail_father_occ["options_map"].keys())
        options_labels_father_occ = list(detail_father_occ["options_map"].values())
        current_val_father_occ = st.session_state.get(session_key_father_occ, detail_father_occ["default_key"])
        try:
            idx_father_occ = options_keys_father_occ.index(current_val_father_occ)
        except ValueError:
            idx_father_occ = options_keys_father_occ.index(detail_father_occ["default_key"])

        selected_label_father_occ = st.selectbox(
            label=f'**{detail_father_occ["label"]}**',
            options=options_labels_father_occ,
            index=idx_father_occ,
            key=key_father_occ
        )
        input_data_form_values["Father's occupation"] = mappings.reverse_map(selected_label_father_occ,
                                                                             detail_father_occ["options_map"])
        input_data_form_labels["Father's occupation"] = selected_label_father_occ

    st.markdown("---")
    st.subheader("📈 성적 입력")
    col_grade1, col_grade2 = st.columns(2)
    with col_grade1:
        # Curricular units 1st sem (approved)
        detail_cu1_app = FEATURE_DETAILS['Curricular units 1st sem (approved)']
        key_cu1_app = f"widget_Curricular units 1st sem (approved)"
        session_key_cu1_app = f"form_Curricular units 1st sem (approved)"
        input_data_form_values['Curricular units 1st sem (approved)'] = st.number_input(
            label=f'**{detail_cu1_app["label"]}**',
            min_value=detail_cu1_app["min"], max_value=detail_cu1_app["max"],
            value=int(st.session_state.get(session_key_cu1_app, detail_cu1_app["default"])),
            step=1, key=key_cu1_app
        )
        input_data_form_labels['Curricular units 1st sem (approved)'] = input_data_form_values[
            'Curricular units 1st sem (approved)']

        # Curricular units 1st sem (grade)
        detail_cu1_grd = FEATURE_DETAILS['Curricular units 1st sem (grade)']
        key_cu1_grd = f"widget_Curricular units 1st sem (grade)"
        session_key_cu1_grd = f"form_Curricular units 1st sem (grade)"
        input_data_form_values['Curricular units 1st sem (grade)'] = st.number_input(
            label=f'**{detail_cu1_grd["label"]}**',
            min_value=float(detail_cu1_grd["min"]), max_value=float(detail_cu1_grd["max"]),
            value=float(st.session_state.get(session_key_cu1_grd, detail_cu1_grd["default"])),
            step=float(detail_cu1_grd["step"]), format=detail_cu1_grd["format"], key=key_cu1_grd
        )
        input_data_form_labels['Curricular units 1st sem (grade)'] = input_data_form_values[
            'Curricular units 1st sem (grade)']

    with col_grade2:
        # Curricular units 2nd sem (approved)
        detail_cu2_app = FEATURE_DETAILS['Curricular units 2nd sem (approved)']
        key_cu2_app = f"widget_Curricular units 2nd sem (approved)"
        session_key_cu2_app = f"form_Curricular units 2nd sem (approved)"
        input_data_form_values['Curricular units 2nd sem (approved)'] = st.number_input(
            label=f'**{detail_cu2_app["label"]}**',
            min_value=detail_cu2_app["min"], max_value=detail_cu2_app["max"],
            value=int(st.session_state.get(session_key_cu2_app, detail_cu2_app["default"])),
            step=1, key=key_cu2_app
        )
        input_data_form_labels['Curricular units 2nd sem (approved)'] = input_data_form_values[
            'Curricular units 2nd sem (approved)']

        # Curricular units 2nd sem (grade)
        detail_cu2_grd = FEATURE_DETAILS['Curricular units 2nd sem (grade)']
        key_cu2_grd = f"widget_Curricular units 2nd sem (grade)"
        session_key_cu2_grd = f"form_Curricular units 2nd sem (grade)"
        input_data_form_values['Curricular units 2nd sem (grade)'] = st.number_input(
            label=f'**{detail_cu2_grd["label"]}**',
            min_value=float(detail_cu2_grd["min"]), max_value=float(detail_cu2_grd["max"]),
            value=float(st.session_state.get(session_key_cu2_grd, detail_cu2_grd["default"])),
            step=float(detail_cu2_grd["step"]), format=detail_cu2_grd["format"], key=key_cu2_grd
        )
        input_data_form_labels['Curricular units 2nd sem (grade)'] = input_data_form_values[
            'Curricular units 2nd sem (grade)']

    st.markdown("---")
    st.subheader("📝 기타 정보")
    # 기타 정보 항목들 (radio 버튼 사용 유지)
    # Displaced
    detail_disp = FEATURE_DETAILS['Displaced']
    key_disp = f"widget_Displaced"
    session_key_disp = f"form_Displaced"
    options_labels_disp = list(detail_disp["options_map"].values())
    current_val_disp_key = st.session_state.get(session_key_disp, detail_disp["default_key"])
    default_idx_disp = list(detail_disp["options_map"].keys()).index(current_val_disp_key)
    selected_label_disp = st.radio(f'**{detail_disp["label"]}**', options_labels_disp, index=default_idx_disp,
                                   horizontal=True, key=key_disp)
    input_data_form_values['Displaced'] = mappings.reverse_map(selected_label_disp, detail_disp["options_map"])
    input_data_form_labels['Displaced'] = selected_label_disp

    # Educational special needs
    detail_needs = FEATURE_DETAILS['Educational special needs']
    key_needs = f"widget_Educational special needs"
    session_key_needs = f"form_Educational special needs"
    options_labels_needs = list(detail_needs["options_map"].values())
    current_val_needs_key = st.session_state.get(session_key_needs, detail_needs["default_key"])
    default_idx_needs = list(detail_needs["options_map"].keys()).index(current_val_needs_key)
    selected_label_needs = st.radio(f'**{detail_needs["label"]}**', options_labels_needs, index=default_idx_needs,
                                    horizontal=True, key=key_needs)
    input_data_form_values['Educational special needs'] = mappings.reverse_map(selected_label_needs,
                                                                               detail_needs["options_map"])
    input_data_form_labels['Educational special needs'] = selected_label_needs

    # Debtor
    detail_debtor = FEATURE_DETAILS['Debtor']
    key_debtor = f"widget_Debtor"
    session_key_debtor = f"form_Debtor"
    options_labels_debtor = list(detail_debtor["options_map"].values())
    current_val_debtor_key = st.session_state.get(session_key_debtor, detail_debtor["default_key"])
    default_idx_debtor = list(detail_debtor["options_map"].keys()).index(current_val_debtor_key)
    selected_label_debtor = st.radio(f'**{detail_debtor["label"]}**', options_labels_debtor, index=default_idx_debtor,
                                     horizontal=True, key=key_debtor)
    input_data_form_values['Debtor'] = mappings.reverse_map(selected_label_debtor, detail_debtor["options_map"])
    input_data_form_labels['Debtor'] = selected_label_debtor

    # Tuition fees up to date
    detail_tuition = FEATURE_DETAILS['Tuition fees up to date']
    key_tuition = f"widget_Tuition fees up to date"
    session_key_tuition = f"form_Tuition fees up to date"
    options_labels_tuition = list(detail_tuition["options_map"].values())
    current_val_tuition_key = st.session_state.get(session_key_tuition, detail_tuition["default_key"])
    default_idx_tuition = list(detail_tuition["options_map"].keys()).index(current_val_tuition_key)
    selected_label_tuition = st.radio(f'**{detail_tuition["label"]}**', options_labels_tuition,
                                      index=default_idx_tuition, horizontal=True, key=key_tuition)
    input_data_form_values['Tuition fees up to date'] = mappings.reverse_map(selected_label_tuition,
                                                                             detail_tuition["options_map"])
    input_data_form_labels['Tuition fees up to date'] = selected_label_tuition

    # Scholarship holder
    detail_scholar = FEATURE_DETAILS['Scholarship holder']
    key_scholar = f"widget_Scholarship holder"
    session_key_scholar = f"form_Scholarship holder"
    options_labels_scholar = list(detail_scholar["options_map"].values())
    current_val_scholar_key = st.session_state.get(session_key_scholar, detail_scholar["default_key"])
    default_idx_scholar = list(detail_scholar["options_map"].keys()).index(current_val_scholar_key)
    selected_label_scholar = st.radio(f'**{detail_scholar["label"]}**', options_labels_scholar,
                                      index=default_idx_scholar, horizontal=True, key=key_scholar)
    input_data_form_values['Scholarship holder'] = mappings.reverse_map(selected_label_scholar,
                                                                        detail_scholar["options_map"])
    input_data_form_labels['Scholarship holder'] = selected_label_scholar

    st.markdown("---")
    submitted = st.form_submit_button("예측하기", use_container_width=True)

if submitted:
    if not student_name_input:
        st.error("❗ 학생 이름을 입력해주세요.")
    else:
        # MODEL_FEATURES_INPUT_ORDER 순서대로 숫자 값으로 DataFrame 생성
        final_numeric_input_data = {}
        for feat in MODEL_FEATURES_INPUT_ORDER:
            # 위젯에서 직접 값을 가져오지 않고, input_data_form_values에 이미 변환된 숫자 값을 사용
            if feat in input_data_form_values:
                final_numeric_input_data[feat] = input_data_form_values[feat]
            else:
                # 이 경우는 MODEL_FEATURES_INPUT_ORDER에 있는데, 위에서 처리가 안된 경우 (로직 오류)
                st.error(f"입력 값 처리 중 오류: {feat} 값을 찾을 수 없습니다.")
                st.stop()

        input_df_for_model = pd.DataFrame([final_numeric_input_data], columns=MODEL_FEATURES_INPUT_ORDER)

        st.session_state.student_info_df = input_df_for_model

        # 결과 페이지에서 사용할 원본 레이블 값 저장
        st.session_state.form_input_original = {'Student Name': student_name_input}
        # MODEL_FEATURES_INPUT_ORDER에 있는 feature들의 레이블 값만 저장
        for feat_key in MODEL_FEATURES_INPUT_ORDER:
            if feat_key in input_data_form_labels:
                st.session_state.form_input_original[feat_key] = input_data_form_labels[feat_key]
            elif feat_key in input_data_form_values:  # 레이블이 따로 없는 숫자형 데이터
                st.session_state.form_input_original[feat_key] = input_data_form_values[feat_key]

        st.success("✅ 정보가 저장되었습니다. 예측 결과 페이지로 이동합니다.")
        st.switch_page("pages/3_📈_예측_결과.py")