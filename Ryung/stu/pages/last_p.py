import streamlit as st
import os
from PIL import Image
import base64
from io import BytesIO

LOGO_PATH = os.path.join("img", "logo.png")

st.set_page_config(
    page_title="PLAY DATA - 마지막 페이지",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링 (input_form.py와 동일)
st.markdown(
    """
    <style>
    .reportview-container {
        background: #fff;
        max-width: 100%;
        overflow-x: hidden;
    }
    .main .block-container {
        padding-right: 220px;
        padding-left: 220px;
        padding-bottom: 0;
        max-width: 100%;
    }
    .st-emotion-cache-ckbrp0 {
        position: relative;
        flex: 1 1 0%;
        flex-direction: column;
        padding-left: 220px !important;
        padding-right: 220px !important;
    }
    .st-emotion-cache-t1wise {
        padding-left: 220px !important;
        padding-right: 220px !important;
    }
    @media (min-width: calc(736px + 8rem)) {
        .st-emotion-cache-t1wise {
            padding-left: 240px !important;
            padding-right: 240px !important;
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
        z-index: 9999;
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
        gap: 20px;
    }
    .nav-menu li {
        margin: 0;
    }
    .nav-menu a {
        text-decoration: none;
        color: #333;
        font-weight: bold;
        font-size: 14px;
        padding: 8px 12px;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    .nav-menu a:hover {
        color: #666;
        background-color: #f5f5f5;
    }
    .nav-menu button {
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
    .nav-menu button:hover {
        color: #666;
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 로고 이미지 base64 인코딩
try:
    logo_image = Image.open(LOGO_PATH)
    buffered = BytesIO()
    logo_image.save(buffered, format="PNG")
    logo_base64 = base64.b64encode(buffered.getvalue()).decode()
except FileNotFoundError:
    logo_base64 = ""

# 헤더 렌더링 (input_form.py와 동일)
st.markdown(
    f"""
    <div class="header-container">
        <div class="logo">
            <a href="/" target="_self">
                <img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="PLAY DATA Logo">
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
                <li><a href="#">학생관리</a></li>
                <li><a href="#">로그인</a></li>
            </ul>
        </nav>
    </div>
    """,
    unsafe_allow_html=True
)

# 헤더와 겹치지 않게 충분한 여백 추가
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

# 학생 정보 예시 (실제 데이터로 대체)
student_name = '김의령'
student_info = {
    '전공': '바이오연료생산기술',
    '입학 나이': '21',
    '이전 학력': '고졸',
    '어머니 직업': '학생',
    '성별': '여성',
    '장학금': '미수혜',
    '수업 형태': '야간',
    '아버지 직업': '학생',
    '채무': '아니오',
    '등록금 납부': '아니오',
}

# 전체 너비 및 컬럼 비율 input_form.py와 맞춤
col_img, col_info = st.columns([1, 2], gap="large")

with col_img:
    st.markdown(f'<div style="font-weight:bold; font-size:20px; margin-bottom:20px;">{student_name} 님 정보</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="display:flex; justify-content:center; align-items:center; height:220px;">
            <div style="width:180px; height:180px; border-radius:50%; background:#e0e0e0; display:flex; align-items:center; justify-content:center;">
                <img src="https://via.placeholder.com/120x120.png?text=+" style="width:120px; height:120px; border-radius:50%; object-fit:cover;" />
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_info:
    st.markdown('''
    <style>
    .info-table2, .info-table3 {width:100%; border-collapse:collapse; margin-bottom:0;}
    .info-table2 th, .info-table2 td {width:50%; border:1px solid #eee; background:#fafafa; padding:12px 16px; text-align:left; font-size:15px;}
    .info-table2 th {background:#f5f5f5; font-weight:bold;}
    .info-table3 th, .info-table3 td {width:33.33%; border:1px solid #eee; background:#fafafa; padding:12px 16px; text-align:left; font-size:15px;}
    .info-table3 th {background:#f5f5f5; font-weight:bold;}
    .info-table2 {margin-bottom:0; border-bottom:none;}
    .info-table3 {margin-top:0; border-top:none;}
    </style>
    ''', unsafe_allow_html=True)
    table2_html = f'''
    <table class="info-table2">
        <tr><th>전공</th><th>입학 나이</th></tr>
        <tr><td>{student_info['전공']}</td><td>{student_info['입학 나이']}</td></tr>
        <tr><th>이전 학력</th><th>어머니 직업</th></tr>
        <tr><td>{student_info['이전 학력']}</td><td>{student_info['어머니 직업']}</td></tr>
    </table>
    '''
    table3_html = f'''
    <table class="info-table3">
        <tr><th>성별</th><th>장학금</th><th>수업 형태</th></tr>
        <tr><td>{student_info['성별']}</td><td>{student_info['장학금']}</td><td>{student_info['수업 형태']}</td></tr>
        <tr><th>아버지 직업</th><th>채무</th><th>등록금 납부</th></tr>
        <tr><td>{student_info['아버지 직업']}</td><td>{student_info['채무']}</td><td>{student_info['등록금 납부']}</td></tr>
    </table>
    '''
    st.markdown(table2_html + table3_html, unsafe_allow_html=True)
