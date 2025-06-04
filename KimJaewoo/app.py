import streamlit as st
import pandas as pd
import joblib
import os

# 페이지 설정 (앱 전체에 적용)
st.set_page_config(
    page_title="학생 학업 성취도 예측",
    page_icon="🎓",
    layout="wide"
)


# 모델 로드 함수
@st.cache_resource  # 모델은 한 번만 로드하도록 캐싱
def load_model():
    model_path = os.path.join('models', 'best_model_pipeline.pkl')
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return model
    else:
        st.error(f"'{model_path}' 에서 모델 파일을 찾을 수 없습니다. 노트북을 실행하여 모델을 먼저 저장해주세요.")
        return None


model = load_model()

# 원본 데이터셋의 컬럼 순서 및 정보를 유지 (재학습 및 입력폼 생성에 중요)
# 노트북에서 사용된 최종 컬럼 순서와 이름을 정의합니다.
# 원본 데이터셋의 모든 컬럼 (dataset.csv 기준)
ORIGINAL_COLUMNS = [
    'Marital status', 'Application mode', 'Application order', 'Course',
    'Daytime/evening attendance', 'Previous qualification', 'Nacionality',
    "Mother's qualification", "Father's qualification", "Mother's occupation",
    "Father's occupation", 'Displaced', 'Educational special needs', 'Debtor',
    'Tuition fees up to date', 'Gender', 'Scholarship holder', 'Age', 'International',
    'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
    'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)',
    'Curricular units 1st sem (grade)', 'Curricular units 1st sem (without evaluations)',
    'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)',
    'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)',
    'Curricular units 2nd sem (grade)', 'Curricular units 2nd sem (without evaluations)',
    'Unemployment rate', 'Inflation rate', 'GDP', 'Target'
]

# 노트북에서 drop된 컬럼들
DROPPED_COLUMNS = [
    'Application mode', 'Application order', 'Nacionality',
    "Mother's qualification", "Father's qualification", 'International',
    'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
    'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (without evaluations)',
    'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)',
    'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (without evaluations)',
    'Unemployment rate', 'Inflation rate', 'GDP'
]

# 최종 모델 학습에 사용된 특성들 (Target 제외, 드롭된 컬럼 제외)
# 노트북에서 실제로 X = df.drop('Target', axis=1) 하기 전의 df.columns와 일치해야 함
# (즉, DROPPED_COLUMNS가 빠진 상태)
MODEL_FEATURES = [col for col in ORIGINAL_COLUMNS if col not in DROPPED_COLUMNS + ['Target']]

# 세션 상태 초기화
if 'student_info' not in st.session_state:
    st.session_state['student_info'] = None
if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None
if 'probability' not in st.session_state:
    st.session_state['probability'] = None
if 'model' not in st.session_state:
    st.session_state['model'] = model


# --- 1. 환영 페이지 ---
def welcome_page():
    st.title("🎓 학생 학업 성취도 예측 서비스")
    st.subheader("학생들의 학업 지속 여부를 예측하고, 맞춤형 지원을 제공하세요.")
    st.markdown("""
    이 웹 애플리케이션은 학생들의 다양한 정보를 바탕으로 해당 학생이 학업을 중도에 포기할지, 
    아니면 성공적으로 졸업할지를 예측합니다. 

    선생님들께서는 이 예측 결과를 바탕으로 학생들에게 필요한 지원과 상담을 제공하여 
    학업 성취도를 높이는 데 도움을 받을 수 있습니다.

    **주요 기능:**
    -   **학생 정보 입력:** 예측을 원하는 학생의 정보를 입력합니다.
    -   **예측 결과 확인:** 입력된 정보를 바탕으로 학생의 중퇴/졸업 확률을 시각화하여 보여줍니다.
    -   **모델 재학습:** 새로운 데이터를 활용하여 예측 모델의 성능을 지속적으로 개선할 수 있습니다.

    👈 사이드바에서 원하는 페이지를 선택하거나, 아래 버튼을 눌러 시작하세요.
    """)
    if st.button("학생 정보 입력 및 예측 시작하기", type="primary", use_container_width=True):
        st.switch_page("pages/2_🧑‍🎓_학생_정보_입력.py")


welcome_page()