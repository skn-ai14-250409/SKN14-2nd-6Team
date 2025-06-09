import streamlit as st
from PIL import Image
import os

LOGO_PATH = os.path.join("img", "logo.png")
IMG1_PATH = os.path.join("img", "img1.png")

st.set_page_config(
    page_title="PLAY DATA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    .reportview-container {
        background: #fff;
        max-width: 100%;
        overflow-x: hidden;
    }
    .main .block-container {
        padding-right: 0;
        padding-left: 0;
        padding-bottom: 0;
        max-width: 100%;
    }
    .st-emotion-cache-ckbrp0 {
        width: 1206.4px;
        position: relative;
        flex: 1 1 0%;
        flex-direction: column;
    }
    .st-emotion-cache-t1wise {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    @media (min-width: calc(736px + 8rem)) {
        .st-emotion-cache-t1wise {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
    }
    .stApp > header {
        display: none;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 25px 120px;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
    }
    .logo-img {
        height: 30px;
        width: auto;
    }
    .nav-menu ul {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
    }
    .nav-menu li {
        background: none;
        border: none;
        padding: 8px 12px;
        font: inherit;
        color: #333;
        font-weight: bold;
        font-size: 14px;
        cursor: pointer;
        border-radius: 4px;
        transition: all 0.3s ease;
        
    }
    .nav-menu a {
        text-decoration: none;
        color: #333;
        font-weight: bold;
        font-size: 14px;
    }
    .nav-menu li:hover {
        color: #666;
        background-color: #f5f5f5;
    }
    .hero-section {
        position: relative;
        width: 100%;
        height: 700px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        padding: 0;
        margin-left: 0;
        margin-right: 0;
    }
    .background-img {
        width: 120vw;
        height: 120vh;
        object-fit: cover;
        filter: brightness(60%);
        position: absolute;
        z-index: 1;
    }
    .overlay-text {
        position: relative;
        color: #fff;
        text-align: center;
        z-index: 2;
        padding: 20px;
        width: 100%;
        margin-top: -200px;
    }
    .overlay-text h1 {
        font-size: 3.5em;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .overlay-text h2 {
        font-size: 2.5em;
        font-weight: bold;
    }
    .overlay-text h3 {
        font-size: 2em;
        margin-top: 0;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .tour-button {
        display: inline-flex;
        align-items: center;
        background-color: white;
        color: #333;
        padding: 12px 60px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: bold;
        font-size: 18px;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    .tour-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .tour-button .arrow {
        margin-left: 10px;
        transition: transform 0.3s ease;
    }
    .tour-button:hover .arrow {
        transform: translateX(5px);
    }
    .st-emotion-cache-1m02ktg {
        width: 1280px;
        position: relative;
        flex: 1 1 0%;
        flex-direction: column;
    }
    .st-emotion-cache-bm2z3a {
        display: flex;
        width: 100%;
        -webkit-box-align: center;
    }
    .stButton button {
        display: none;  /* Streamlit 버튼 숨기기 */
    }
    .nav-menu a[href="#student-management"] {
        cursor: pointer;
    }
    .nav-menu button {
        background: none;
        border: none;
        padding: 0;
        font: inherit;
        color: #333;
        font-weight: bold;
        font-size: 14px;
        cursor: pointer;
    }
    .nav-menu button:hover {
        color: #666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 1. 헤더 섹션
try:
    logo_image = Image.open(LOGO_PATH)
except FileNotFoundError:
    st.error(f"로고 파일 '{LOGO_PATH}'을(를) 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    st.stop()

# === 정확한 Base64 인코딩 방법 ===
import base64
from io import BytesIO

# 로고 이미지 Base64 인코딩
buffered = BytesIO()
logo_image.save(buffered, format="PNG")
logo_base64 = base64.b64encode(buffered.getvalue()).decode()

st.markdown(
    f"""
    <div class="header-container">
        <div class="logo">
            <img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="PLAY DATA Logo">
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


# 2. 히어로 섹션 (배경 이미지 및 오버레이 텍스트)
try:
    img1_image = Image.open(IMG1_PATH)
except FileNotFoundError:
    st.error(f"배경 이미지 파일 '{IMG1_PATH}'을(를) 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    st.stop()

# 배경 이미지 Base64 인코딩
buffered_bg = BytesIO()
img1_image.save(buffered_bg, format="PNG")
img1_base64 = base64.b64encode(buffered_bg.getvalue()).decode()

st.markdown(
    f"""
    <div class="hero-section">
        <img src="data:image/jpeg;base64,{img1_base64}" class="background-img" alt="PLAY DATA Interior">
        <div class="overlay-text">
            <h2>PLAY DATA와 함께</h2>
            <h3>개발자로 첫걸음을 내딛는 모든 학생 여러분을 응원합니다.</h3>
            <button class="tour-button" id="tour-button">
                둘러보기
                <span class="arrow">→</span>
            </button>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 페이지 네비게이션 버튼들
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🧑‍🎓 학생 정보 입력", key="student_input", use_container_width=True):
        st.switch_page("pages/input_form.py")

with col2:
    if st.button("📊 예측 결과 보기", key="view_results", use_container_width=True):
        if 'form_input_original' not in st.session_state:
            st.error("먼저 학생 정보를 입력해주세요.")
        else:
            st.switch_page("pages/result.py")

with col3:
    if st.button("🏠 메인으로", key="home", use_container_width=True):
        st.rerun()

# 숨겨진 둘러보기 버튼 (HTML 버튼과 연결)
if st.button("둘러보기", key="tour_button", help="학생 정보 입력 페이지로 이동합니다"):
    st.switch_page("pages/input_form.py")

# JavaScript로 HTML 버튼과 Streamlit 버튼 연결
st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const tourButton = document.getElementById('tour-button');
        if (tourButton) {
            tourButton.addEventListener('click', function() {
                // Streamlit 버튼 클릭 시뮬레이션
                const streamlitButton = window.parent.document.querySelector('[data-testid="baseButton-secondary"][title*="둘러보기"]');
                if (streamlitButton) {
                    streamlitButton.click();
                }
            });
        }
    });
    </script>
""", unsafe_allow_html=True)

