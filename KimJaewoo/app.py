import streamlit as st
from PIL import Image
import os
import joblib
import pandas as pd # pandas import 추가
import base64
from io import BytesIO

# --- 프로젝트 경로 설정 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "img")
MODELS_DIR = os.path.join(BASE_DIR, "models")

LOGO_PATH = os.path.join(IMG_DIR, "logo.png")
IMG1_PATH = os.path.join(IMG_DIR, "img1.png")

st.set_page_config(
    page_title="PLAY DATA 학생 관리", # 페이지 타이틀 변경
    layout="wide",
    initial_sidebar_state="collapsed" # 사이드바 기본적으로 닫힘
)

# --- 공통 변수 및 함수 ---
# 노트북에서 최종 모델 학습에 사용된 특성들 (Target 제외, 드롭된 컬럼 제외)
# 이 순서는 모델 예측 시 DataFrame 컬럼 순서에 매우 중요합니다.
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
    'Daytime/evening attendance', 'Previous qualification', 'Nacionality', # 'Nacionality' 철자 주의
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

# 모델 로드 함수 (st.cache_resource 사용)
@st.cache_resource
def load_model_pipeline():
    model_path = os.path.join(MODELS_DIR, 'best_model_pipeline.pkl')
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
    st.session_state.model = load_model_pipeline()

if 'student_info_df' not in st.session_state: # 예측할 학생의 DataFrame (숫자로 변환된 상태)
    st.session_state.student_info_df = None

if 'form_input_original' not in st.session_state: # 결과 페이지 표시용 원본 입력값 (한글 포함)
    st.session_state.form_input_original = None

# --- CSS 스타일 ---
st.markdown(
    """
    <style>
    /* ... (제공해주신 CSS 스타일 그대로 유지) ... */
    .main .block-container { /* 메인 콘텐츠 영역 상단 패딩 조정 */
        padding-top: 80px !important; /* 헤더 높이 고려 */
    }
    .nav-menu a.active, .nav-menu a:hover { /* 활성/호버 메뉴 스타일 */
        color: #007bff; 
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 헤더 섹션 ---
try:
    logo_image = Image.open(LOGO_PATH)
    buffered = BytesIO()
    logo_image.save(buffered, format="PNG")
    logo_base64 = base64.b64encode(buffered.getvalue()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="PLAY DATA Logo">'
except FileNotFoundError:
    logo_html = '<span style="font-weight:bold; font-size: 20px;">PLAY DATA</span>' # 로고 없을 시 텍스트
    st.error(f"로고 파일 '{LOGO_PATH}'을(를) 찾을 수 없습니다. 텍스트 로고로 대체합니다.")


# 페이지 이동을 위한 JavaScript 함수
def nav_page(page_script_path):
    st.session_state.current_page = page_script_path # 현재 페이지 추적용
    st.switch_page(page_script_path)

# 헤더 HTML 구성
# '학생관리' 메뉴를 pages/2_🧑‍🎓_학생_정보_입력.py 로 연결
# 링크는 실제 파일 경로를 사용합니다.
header_html = f"""
<div class="header-container">
    <div class="logo">
        {logo_html}
    </div>
    <nav class="nav-menu">
        <ul>
            <li><a href="#">백엔드 캠프</a></li>
            <li><a href="#">취업지원</a></li>
            <li><a href="#">스토리</a></li>
            <li><a href="#">캠퍼스투어</a></li>
            <li><a href="#">파트너</a></li>
            <li><a href="#">프리코스</a></li>
            <li><a href="#" onclick="window.location.href='학생_정보_입력'; return false;">학생관리</a></li>
            <li><a href="#">로그인</a></li>
        </ul>
    </nav>
</div>
"""
# st.markdown(header_html, unsafe_allow_html=True) # 헤더는 각 페이지 상단에 표시되므로 주석 처리 또는 제거

# 현재 페이지 확인 및 네비게이션 (쿼리 파라미터 사용 방식 제거)
# Streamlit의 멀티페이지는 사이드바로 기본 제공되므로, 헤더의 링크는
# st.page_link 또는 st.switch_page를 사용하는 버튼/콜백으로 처리하는 것이 더 Streamlit-native 합니다.
# 여기서는 헤더의 "학생관리"를 클릭하면 input_form 페이지로 이동하는 버튼을 아래에 만듭니다.

# --- 히어로 섹션 ---
try:
    img1_image = Image.open(IMG1_PATH)
    buffered_bg = BytesIO()
    img1_image.save(buffered_bg, format="PNG") # 이미지 형식에 맞게
    img1_base64 = base64.b64encode(buffered_bg.getvalue()).decode()
    hero_bg_img_html = f'<img src="data:image/png;base64,{img1_base64}" class="background-img" alt="PLAY DATA Interior">'
except FileNotFoundError:
    hero_bg_img_html = '<div style="background-color:#333; width:100%; height:100%; position:absolute; top:0; left:0; z-index:1;"></div>' # 배경 이미지 없을 시 단색 배경
    st.error(f"배경 이미지 파일 '{IMG1_PATH}'을(를) 찾을 수 없습니다. 단색 배경으로 대체합니다.")

st.markdown(
    f"""
    <div class="header-container">
        <div class="logo">
            {logo_html}
        </div>
        <nav class="nav-menu">
            <ul>
                <li><a href="#">백엔드 캠프</a></li>
                <li><a href="#">취업지원</a></li>
                <li><a href="#">스토리</a></li>
                <li><a href="#">캠퍼스투어</a></li>
                <li><a href="#">파트너</a></li>
                <li><a href="#">프리코스</a></li>
            </ul>
        </nav>
    </div>
    <div class="hero-section">
        {hero_bg_img_html}
        <div class="overlay-text">
            <h1>PLAY DATA에서</h1>
            <h2>개발자 커리어로 출발하는 모든 학생들을</h2>
            <h3>응원합니다.</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# "학생 관리" 버튼을 중앙에 배치하고, 클릭 시 페이지 이동
st.markdown("<br>", unsafe_allow_html=True) # 간격
cols_button = st.columns([2,1,2]) # 버튼을 중앙에 위치시키기 위한 컬럼
with cols_button[1]:
    if st.button("학생 관리 페이지로 이동", type="primary", use_container_width=True):
        st.switch_page("pages/2_🧑‍🎓_학생_정보_입력.py")

st.sidebar.info("이 앱은 학생들의 학업 성취도를 예측합니다.")