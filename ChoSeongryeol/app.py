
import streamlit as st
from PIL import Image
import os


LOGO_PATH = os.path.join("./image/logo.png")
IMG1_PATH = os.path.join("./image/img1.png")

st.set_page_config(
    page_title="PLAY DATA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    .reportview-container {
        background: #fff; /* 전체 배경색 */
    }
    .main .block-container {
        padding-top: 0rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 0rem;
    }
    .stApp > header {
        display: none; /* Streamlit 기본 헤더 숨기기 */
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 40px;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 100%;
        position: fixed; /* 헤더 고정 */
        top: 0;
        left: 0;
        z-index: 999; /* 다른 요소 위에 오도록 */
    }
    .logo-img {
        height: 30px; /* 로고 이미지 높이 */
        width: auto;
    }
    .nav-menu ul {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
    }
    .nav-menu li {
        margin-left: 30px;
    }
    .nav-menu a {
        text-decoration: none;
        color: #333;
        font-weight: bold;
        font-size: 16px;
    }
    .hero-section {
        position: relative;
        width: 100vw; /* 뷰포트 너비 전체 사용 */
        height: 700px; /* 이미지 높이 */
        overflow: hidden;
        margin-top: 60px; /* 헤더 높이만큼 마진 주기 */
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .background-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(60%); /* 이미지 어둡게 처리 */
        position: absolute;
        top: 0;
        left: 0;
        z-index: 1;
    }
    .overlay-text {
        position: relative; /* relative로 변경하여 z-index 적용 */
        color: #fff;
        text-align: center;
        z-index: 2; /* 이미지보다 위에 오도록 */
        padding: 20px;
    }
    .overlay-text h1 {
        font-size: 3.5em;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .overlay-text h2 {
        font-size: 2.5em;
        margin-bottom: 5px;
        font-weight: bold;
    }
    .overlay-text h3 {
        font-size: 2em;
        margin-top: 5px;
        font-weight: bold;
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
                <li><a href="/?page=pages/input_form" target="_self">학생관리</a></li>
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
            <h1>PLAY DATA에서</h1>
            <h2>개발자 커리어로 출발하는 모든 학생들을</h2>
            <h3>응원합니다.</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("학생관리"):
    st.switch_page("pages/2_second.py")