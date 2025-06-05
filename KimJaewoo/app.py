import streamlit as st
from PIL import Image
import os
import joblib
import base64
from io import BytesIO

# --- 페이지 설정 (스크립트 최상단) ---
st.set_page_config(
    page_title="PLAY DATA",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------------------------------------

# --- 모델 로드 및 세션 상태 초기화 ---
@st.cache_resource
def load_model():
    model_path = os.path.join("models", "best_model_pipeline.pkl")
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            return model
        except Exception as e:
            print(f"모델 로딩 중 오류 발생: {e}")
            return None
    else:
        print(f"경고: '{model_path}' 에서 모델 파일을 찾을 수 없습니다.")
        return None


if 'model' not in st.session_state:
    st.session_state.model = load_model()
if 'student_info_df' not in st.session_state:
    st.session_state.student_info_df = None
if 'form_input_original' not in st.session_state:
    st.session_state.form_input_original = None
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
# ---------------------------------------------

LOGO_PATH = os.path.join("img", "logo.png")
IMG1_PATH = os.path.join("img", "img1.png")


def image_to_base64_data_uri(img_path):
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            buffered = BytesIO()
            img_format = img.format.upper() if img.format else ("PNG" if img_path.lower().endswith(".png") else "JPEG")
            if img_format == 'JPEG' and img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(buffered, format=img_format)
            encoded_string = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/{img_format.lower()};base64,{encoded_string}"
        except Exception as e:
            print(f"Error encoding image {img_path}: {e}")
            return ""
    return ""


logo_data_uri = image_to_base64_data_uri(LOGO_PATH)
hero_bg_img_data_uri = image_to_base64_data_uri(IMG1_PATH)

# CSS
st.markdown(
    f"""
    <style>
    /* 기본 Streamlit 패딩 및 헤더 제거 */
    .main .block-container {{ padding: 0 !important; max-width: 100%; }}
    .st-emotion-cache-ckbrp0, .st-emotion-cache-t1wise {{ padding-left: 0 !important; padding-right: 0 !important; }}
    .stApp > header {{ display: none; }}

    /* 헤더 스타일 */
    .header-container {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 20px 100px; background-color: #fff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 100%; position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
    }}
    .logo-img {{ height: 30px; width: auto; }}
    .nav-menu ul {{ list-style: none; margin: 0; padding: 0; display: flex; }}
    .nav-menu li {{ margin-left: 30px; }}
    .nav-menu a {{ text-decoration: none; color: #333; font-weight: bold; font-size: 16px; padding: 8px 12px; border-radius: 4px; transition: all 0.3s ease; }}
    .nav-menu a:hover {{ color: #007bff; background-color: #f0f0f0; }}
    .nav-menu a[href="/input_form"] {{ cursor: pointer; }}

    /* 히어로 섹션 스타일 */
    .hero-section-wrapper {{ /* 이 div가 실제 배경과 컨텐츠를 포함 */
        width: 100vw;
        height: 75vh;
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url({hero_bg_img_data_uri if hero_bg_img_data_uri else ""});
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: white;
        padding: 20px;
        margin-top: 80px; /* 헤더 높이만큼 여백 */
    }}
    .hero-section-wrapper h2 {{
        font-size: 2.8em;
        font-weight: bold;
        margin-bottom: 15px;
        color: #fff !important;
    }}
    .hero-section-wrapper h3 {{
        font-size: 1.6em;
        font-weight: 300;
        margin-bottom: 40px; /* 버튼과의 간격 증가 */
        color: #f0f0f0 !important;
        max-width: 700px;
        line-height: 1.5;
    }}
    /* 히어로 섹션 내 Streamlit 버튼 스타일 */
    .hero-section-wrapper .stButton>button {{
        background-color: white !important;
        color: #007bff !important;
        padding: 14px 50px !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        font-size: 1.1em !important;
        border: 2px solid white !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }}
    .hero-section-wrapper .stButton>button:hover {{
        background-color: #007bff !important;
        color: white !important;
        border-color: #007bff !important;
        transform: scale(1.05) !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.25) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- 헤더 렌더링 ---
if logo_data_uri:
    st.markdown(
        f"""
        <div class="header-container">
            <div class="logo">
                <a href="/" target="_self">
                    <img src="{logo_data_uri}" class="logo-img" alt="PLAY DATA Logo">
                </a>
            </div>
            <nav class="nav-menu">
                <ul>
                    <li><a href="#">백엔드 캠프</a></li>
                    <li><a href="#">취업지원</a></li>
                    <li><a href="#">스토리</a></li>
                    <li><a href="#">캠퍼스투어</a></li>
                    <li><a href="#">파트너</a></li>
                    <li><a href="#">프리코스</a></li>
                    <li><a href="/input_form" target="_self">학생관리</a></li>
                    <li><a href="#">로그인</a></li>
                </ul>
            </nav>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.error("로고 이미지를 로드할 수 없습니다.")

# --- 히어로 섹션 ---
if hero_bg_img_data_uri:
    # st.markdown을 사용하여 HTML 구조를 만들고, 그 안에는 텍스트만 넣습니다.
    # Streamlit 버튼은 Python 코드에서 별도로 생성합니다.
    st.markdown(
        f"""
        <div class="hero-section-wrapper">
            <h2>PLAY DATA와 함께</h2>
            <h3>개발자로 첫걸음을 내딛는 모든 학생 여러분을 응원합니다.</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    # 버튼을 위한 별도의 st.container 또는 st.columns를 사용 (CSS 클래스를 직접 적용하기 어려움)
    # 대신, 버튼을 hero-section-wrapper 바로 아래에 배치하고 CSS로 위치 조정 시도
    # (이전 답변에서 이 부분이 혼란을 드린 것 같습니다.)
    # 가장 간단한 방법은, 버튼을 이 markdown 바로 아래에 배치하고,
    # CSS에서 .hero-section-wrapper에 position:relative를 주고,
    # 버튼을 담을 div(st.markdown으로 생성)에 position:absolute 및 bottom, left 등으로 위치를 잡는 것입니다.
    # 또는, Streamlit의 레이아웃 기능을 최대한 활용합니다.

    # 버튼을 히어로 섹션의 일부처럼 보이게 하기 위한 컨테이너
    # 이 컨테이너의 스타일을 CSS에서 조정하여 버튼 위치를 맞춥니다.
    # (이전 답변의 margin-top: -150px; 와 유사한 방식이지만, 더 명확한 구조로)
    st.markdown(
        """
        <style>
            .hero-button-area {
                width: 100%;
                text-align: center;
                margin-top: -100px; /* 히어로 섹션 텍스트 아래로 끌어올림 (값 조정 필요) */
                position: relative; /* z-index 적용 위해 */
                z-index: 3; /* 다른 히어로 요소들보다 위에 */
            }
        </style>
        <div class="hero-button-area">
        """, unsafe_allow_html=True
    )
    cols_hero_button = st.columns([2, 1, 2])  # 중앙 정렬용
    with cols_hero_button[1]:
        if st.button("학생 학업 여정 예측 시작 →", key="hero_button_on_image"):
            st.switch_page("pages/input_form.py")
    st.markdown("</div>", unsafe_allow_html=True)


else:  # 배경 이미지 로드 실패 시
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color: #333; margin-top: 50px;'>PLAY DATA와 함께</h2>",
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color: #555;'>개발자로 첫걸음을 내딛는 모든 학생 여러분을 응원합니다.</h3>",
                unsafe_allow_html=True)
    cols_button_no_img_app_final = st.columns([1.5, 1, 1.5])
    with cols_button_no_img_app_final[1]:
        if st.button("학생 정보 입력 및 예측 시작 →", key="hero_button_start_no_img_app_final_v2"):
            st.switch_page("pages/input_form.py")

# --- 사이드바 ---
st.sidebar.title("탐색 메뉴")
st.sidebar.page_link("app.py", label="🏠 홈", icon="🏠")
st.sidebar.page_link("pages/input_form.py", label="🧑‍🎓 학생 정보 입력", icon="🧑‍🎓")
st.sidebar.page_link("pages/result.py", label="📈 예측 결과 보기", icon="📈")

if st.session_state.get('model') is None:
    st.sidebar.error("⚠️ 모델 로딩 실패!")
else:
    st.sidebar.success("✅ 예측 모델 준비 완료")