import streamlit as st
import pandas as pd
import joblib
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="학생 학업 성취도 예측",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 공통 변수 및 함수 ---
# 노트북에서 최종 모델 학습에 사용된 특성들 (Target 제외, 드롭된 컬럼 제외)
# 이 순서는 모델 예측 시 DataFrame 컬럼 순서에 매우 중요합니다.
# 노트북의 X_train.columns 또는 X.columns (drop 후)와 일치해야 함
MODEL_FEATURES = [
    'Marital status', 'Course', 'Daytime/evening attendance', 'Previous qualification',
    "Mother's occupation", "Father's occupation", 'Displaced', 'Educational special needs', 'Debtor',
    'Tuition fees up to date', 'Gender', 'Scholarship holder', 'Age',
    'Curricular units 1st sem (approved)', 'Curricular units 1st sem (grade)',
    'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)'
]

# 원본 데이터셋의 모든 컬럼명 (Target 포함, 재학습 시 컬럼 검증용)
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

# 노트북에서 drop된 컬럼들 (재학습 시 동일하게 적용)
DROPPED_COLUMNS_FOR_RETRAIN = [
    'Application mode', 'Application order', 'Nacionality',
    "Mother's qualification", "Father's qualification", 'International',
    'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
    'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (without evaluations)',
    'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)',
    'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (without evaluations)',
    'Unemployment rate', 'Inflation rate', 'GDP'
]


# 모델 로드 함수
@st.cache_resource
def load_model():
    model_path = os.path.join('models', 'best_model_pipeline.pkl')
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            return model
        except Exception as e:
            st.error(f"모델 로딩 중 오류 발생: {e}")
            return None
    else:
        st.error(f"경로 '{model_path}'에서 모델 파일을 찾을 수 없습니다. `project.ipynb`를 실행하여 모델을 먼저 저장해주세요.")
        return None

# 세션 상태 초기화
if 'model' not in st.session_state:
    st.session_state.model = load_model()

if 'student_info_df' not in st.session_state:
    st.session_state.student_info_df = None

if 'prediction_proba' not in st.session_state:
    st.session_state.prediction_proba = None


# --- 1. 환영 페이지 ---
st.title("🎓 학생 학업 성취도 예측 서비스")
st.subheader("선생님을 위한 학생 학업 여정 지원 도구")

st.markdown("""
안녕하세요! 이 서비스는 학생들의 정보를 바탕으로 학업 지속 여부(졸업 또는 중퇴)를 예측합니다.
예측 결과를 활용하여 학생들에게 필요한 관심과 지원을 제공함으로써, 모든 학생이 성공적인 학업 여정을 마칠 수 있도록 돕고자 합니다.

**주요 기능:**
- **학생 정보 입력:** 개별 학생의 정보를 손쉽게 입력하여 예측을 수행합니다.
- **예측 결과 확인:** 졸업 및 중퇴 확률을 시각적으로 확인하고, 학생 상태에 따른 조언을 얻을 수 있습니다.
- **모델 재학습:** 새로운 데이터를 통해 예측 모델을 지속적으로 업데이트하여 정확도를 향상시킬 수 있습니다.

아래 버튼을 클릭하거나 사이드바에서 **'🧑‍🎓 학생 정보 입력'** 페이지로 이동하여 시작하세요.
""")

if st.button("예측 시작하기", type="primary", use_container_width=True):
    st.switch_page("pages/2_🧑‍🎓_학생_정보_입력.py")

st.sidebar.success("탐색할 페이지를 선택하세요.")