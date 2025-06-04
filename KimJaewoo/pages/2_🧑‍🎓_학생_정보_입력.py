import streamlit as st
import pandas as pd
import numpy as np

# MODEL_FEATURES_INPUT_ORDER는 모델이 학습될 때 사용된 특성들의 순서입니다.
# 이 순서대로 DataFrame을 만들어 모델에 입력해야 합니다.
MODEL_FEATURES_INPUT_ORDER = [
    'Marital status', 'Course', 'Daytime/evening attendance', 'Previous qualification',
    "Mother's occupation", "Father's occupation", 'Displaced', 'Educational special needs', 'Debtor',
    'Tuition fees up to date', 'Gender', 'Scholarship holder', 'Age',
    'Curricular units 1st sem (approved)', 'Curricular units 1st sem (grade)',
    'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)'
]

FEATURE_DETAILS = {
    'Marital status': {"label": "결혼 상태", "options": {1: "미혼", 2: "기혼", 3: "과부", 4: "이혼", 5: "사실혼", 6: "법적 별거"},
                       "default": 1, "type": "select"},
    'Course': {"label": "수강 과정(코드)", "desc": "데이터셋 코드 참고", "min": 1, "max": 17, "default": 10, "type": "int"},
    'Daytime/evening attendance': {"label": "주/야간 수업", "options": {1: "주간", 0: "야간"}, "default": 1, "type": "select"},
    'Previous qualification': {"label": "이전 학력(코드)", "desc": "데이터셋 코드 참고", "min": 1, "max": 17, "default": 1,
                               "type": "int"},
    "Mother's occupation": {"label": "어머니 직업(코드)", "desc": "데이터셋 코드 참고", "min": 1, "max": 46, "default": 5,
                            "type": "int"},  # 데이터셋 최대값으로 수정
    "Father's occupation": {"label": "아버지 직업(코드)", "desc": "데이터셋 코드 참고", "min": 1, "max": 46, "default": 5,
                            "type": "int"},  # 데이터셋 최대값으로 수정
    'Displaced': {"label": "이재민 여부", "options": {1: "예", 0: "아니오"}, "default": 0, "type": "select"},
    'Educational special needs': {"label": "특수 교육 필요 여부", "options": {1: "예", 0: "아니오"}, "default": 0,
                                  "type": "select"},
    'Debtor': {"label": "학자금 연체 여부", "options": {1: "예", 0: "아니오"}, "default": 0, "type": "select"},
    'Tuition fees up to date': {"label": "등록금 납부 여부", "options": {1: "예", 0: "아니오"}, "default": 1, "type": "select"},
    'Gender': {"label": "성별", "options": {1: "남성", 0: "여성"}, "default": 1, "type": "select"},
    'Scholarship holder': {"label": "장학금 수혜 여부", "options": {1: "예", 0: "아니오"}, "default": 0, "type": "select"},
    'Age': {"label": "입학 시 나이", "min": 17, "max": 70, "default": 20, "type": "int"},
    'Curricular units 1st sem (approved)': {"label": "1학기 합격 과목 수", "min": 0, "max": 26, "default": 0, "type": "int"},
    'Curricular units 1st sem (grade)': {"label": "1학기 평균 성적", "min": 0.0, "max": 20.0, "default": 0.0, "type": "float",
                                         "step": 0.01, "format": "%.2f"},
    'Curricular units 2nd sem (approved)': {"label": "2학기 합격 과목 수", "min": 0, "max": 20, "default": 0, "type": "int"},
    'Curricular units 2nd sem (grade)': {"label": "2학기 평균 성적", "min": 0.0, "max": 20.0, "default": 0.0, "type": "float",
                                         "step": 0.01, "format": "%.2f"}
}

DUMMY_DATA_DROPOUT_RISK = {
    'Marital status': 1, 'Course': 2, 'Daytime/evening attendance': 1, 'Previous qualification': 1,
    "Mother's occupation": 10, "Father's occupation": 10, 'Displaced': 1, 'Educational special needs': 0, 'Debtor': 1,
    'Tuition fees up to date': 0, 'Gender': 1, 'Scholarship holder': 0, 'Age': 19,
    'Curricular units 1st sem (approved)': 0, 'Curricular units 1st sem (grade)': 0.0,
    'Curricular units 2nd sem (approved)': 0, 'Curricular units 2nd sem (grade)': 0.0
}

DUMMY_DATA_GRADUATE_EXPECTED = {
    'Marital status': 1, 'Course': 11, 'Daytime/evening attendance': 1, 'Previous qualification': 1,
    "Mother's occupation": 4, "Father's occupation": 4, 'Displaced': 0, 'Educational special needs': 0, 'Debtor': 0,
    'Tuition fees up to date': 1, 'Gender': 0, 'Scholarship holder': 1, 'Age': 18,
    'Curricular units 1st sem (approved)': 6, 'Curricular units 1st sem (grade)': 15.50,
    'Curricular units 2nd sem (approved)': 6, 'Curricular units 2nd sem (grade)': 16.00
}

st.header("🧑‍🎓 학생 정보 입력")
st.markdown("예측하고자 하는 학생의 정보를 입력해주세요.")

# 모델 로드 확인 (st.session_state.model 사용)
if 'model' not in st.session_state or st.session_state.model is None:
    st.error("모델 로딩에 실패했습니다. 메인 페이지(app.py)를 먼저 실행하거나, 모델 파일을 확인해주세요.")
    if st.button("메인 페이지로 돌아가기"):
        st.switch_page("app.py")
    st.stop()

# 입력 필드 값을 저장할 세션 상태 초기화
for feature_key in MODEL_FEATURES_INPUT_ORDER:
    session_key_form = f"form_{feature_key}"  # 폼 위젯용 세션 키
    if session_key_form not in st.session_state:
        st.session_state[session_key_form] = FEATURE_DETAILS[feature_key]["default"]


# 더미 데이터 로드 콜백 함수
def load_dummy_data(dummy_profile):
    for key, value in dummy_profile.items():
        session_key_form = f"form_{key}"
        if session_key_form in st.session_state:  # 해당 키가 세션 상태에 있는지 확인
            st.session_state[session_key_form] = value
        else:
            # 이 경우는 MODEL_FEATURES_INPUT_ORDER 와 dummy_profile의 키가 불일치할 때 발생 가능
            print(f"Warning: Dummy data key '{key}' not found in session state form keys.")


st.markdown("---")
st.subheader("빠른 입력 (더미 데이터)")
col_dummy1, col_dummy2, col_dummy3 = st.columns(3)

if col_dummy1.button("중퇴 위험군 예시", use_container_width=True, key="dummy_dropout_btn"):
    load_dummy_data(DUMMY_DATA_DROPOUT_RISK)
    # 버튼 클릭 시 바로 반영되도록 rerun() 대신 key를 사용한 위젯 값 업데이트로 처리

if col_dummy2.button("졸업 예상군 예시", use_container_width=True, key="dummy_graduate_btn"):
    load_dummy_data(DUMMY_DATA_GRADUATE_EXPECTED)

if col_dummy3.button("입력 필드 초기화", use_container_width=True, key="dummy_reset_btn"):
    for feature in MODEL_FEATURES_INPUT_ORDER:
        session_key_form = f"form_{feature}"
        st.session_state[session_key_form] = FEATURE_DETAILS[feature]["default"]
st.markdown("---")

with st.form("student_input_form_actual"):  # form key 변경
    input_data_form = {}
    cols = st.columns(2)

    for i, feature_key in enumerate(MODEL_FEATURES_INPUT_ORDER):
        detail = FEATURE_DETAILS[feature_key]
        current_col = cols[i % 2]
        session_key_form = f"form_{feature_key}"

        if detail["type"] == "select":
            options_keys = list(detail["options"].keys())
            # st.session_state에 저장된 값을 value로 사용, 없으면 default
            current_selection = st.session_state.get(session_key_form, detail["default"])
            try:
                default_index = options_keys.index(current_selection)
            except ValueError:
                default_index = options_keys.index(detail["default"])  # current_selection이 유효하지 않으면 default

            input_data_form[feature_key] = current_col.selectbox(
                label=detail["label"],
                options=options_keys,
                format_func=lambda x: detail["options"][x],
                index=default_index,
                help=detail.get("desc", ""),
                key=session_key_form  # key를 사용하여 위젯 상태 관리
            )
        elif detail["type"] == "int":
            input_data_form[feature_key] = current_col.number_input(
                label=detail["label"],
                min_value=detail["min"],
                max_value=detail["max"],
                value=int(st.session_state.get(session_key_form, detail["default"])),
                step=1,
                help=detail.get("desc", ""),
                key=session_key_form
            )
        elif detail["type"] == "float":
            input_data_form[feature_key] = current_col.number_input(
                label=detail["label"],
                min_value=float(detail["min"]),
                max_value=float(detail["max"]),
                value=float(st.session_state.get(session_key_form, detail["default"])),
                step=float(detail.get("step", 0.01)),
                format=detail.get("format", "%.2f"),
                help=detail.get("desc", ""),
                key=session_key_form
            )

    submit_button = st.form_submit_button(label="예측 결과 보기", use_container_width=True, type="primary")

if submit_button:
    # 폼 제출 시에는 각 위젯의 현재 값(st.session_state[session_key_form]에 저장된 값)을 가져와 DataFrame 생성
    final_input_data_from_form = {key: st.session_state[f"form_{key}"] for key in MODEL_FEATURES_INPUT_ORDER}
    input_df = pd.DataFrame([final_input_data_from_form], columns=MODEL_FEATURES_INPUT_ORDER)

    st.session_state.student_info_df = input_df  # DataFrame을 세션 상태에 저장

    st.success("정보가 입력되어 예측 페이지로 이동합니다.")
    st.switch_page("pages/3_📈_예측_결과.py")