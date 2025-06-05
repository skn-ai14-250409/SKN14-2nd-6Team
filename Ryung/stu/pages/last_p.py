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


PROFILE_IMG_PATH = os.path.join("img", "user_img.png")

# base64 인코딩
try:
    user_img = Image.open(PROFILE_IMG_PATH)
    buffered = BytesIO()
    user_img.save(buffered, format="PNG")
    user_img_base64 = base64.b64encode(buffered.getvalue()).decode()
    user_img_url = f"data:image/png;base64,{user_img_base64}"
except FileNotFoundError:
    user_img_url = "https://via.placeholder.com/120x120.png?text=+"


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
    
    .st-emotion-cache-16tyu1 table {
        margin-bottom : 0 !important;
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

# 헤더와 겹치지 않게 충분한 여백 추가
st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
st.markdown(f'<div style="font-weight:bold; font-size:20px; margin-bottom:20px;">{student_name} 님 정보</div>',
            unsafe_allow_html=True)
st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

# 전체 너비 및 컬럼 비율 input_form.py와 맞춤
col_img, col_info = st.columns([1, 2], gap="large")

with col_img:
    st.markdown(
        """
         <div style="display:flex; justify-content:center; align-items:center; height:220px;">
            <div style="width:180px; height:180px; border-radius:50%; background:#e0e0e0; display:flex; align-items:center; justify-content:center;">
                <img src="{user_img_url}" style="width:120px; height:120px; border-radius:50%; object-fit:cover;" />
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

with col_info:
    # 표 아래 자퇴 확률 섹션 추가
    # 자퇴 확률 섹션 (3개 영역)
    st.markdown("""
    <style>
    .flex-row-3col { display: flex; flex-direction: row; gap: 0px; margin-top: 40px; }
    .flex-item-left { flex: 1; min-width: 180px; max-width: 220px; background: #fff; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; padding: 30px 0 30px 0; }
    .flex-item-center { flex: 1.2; min-width: 320px; max-width: 400px; display: flex; align-items: center; justify-content: center; background: #fff; }
    .flex-item-right { flex: 1.5; min-width: 320px; max-width: 520px; background: #f8f8f8; padding: 30px 30px 30px 30px; border-radius: 8px; font-size: 1.05em; color: #222; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; margin-left: 30px; }
    .flex-item-right b, .flex-item-right strong { font-size: 1.1em; }
    .flex-item-right .highlight { color: #dc3545; font-weight: bold; }
    .flex-item-right .bold { font-weight: bold; }
    @media (max-width: 900px) {
        .flex-row-3col { flex-direction: column; }
        .flex-item-left, .flex-item-center, .flex-item-right { max-width: 100%; width: 100%; margin-left: 0; }
    }
    </style>
    """, unsafe_allow_html=True)

    avg_grade_1st = 14.8
    avg_grade_2nd = 18.2
    prob_dropout_pct = 79.7
    student_name = "김의령"


    st.markdown('<div class="flex-row-3col">', unsafe_allow_html=True)

    # 왼쪽: 제목+성적
    st.markdown(f'''
    <div class="flex-item-left">
        <div style="font-size:1.25em; font-weight:bold; margin-bottom:18px;">자퇴 확률</div>
        <div style="font-size:1.05em; margin-bottom:6px;">1학기 성적 평균 : <b>{avg_grade_1st} 점</b></div>
        <div style="font-size:1.05em;">2학기 성적 평균 : <b>{avg_grade_2nd} 점</b></div>
    </div>
    ''', unsafe_allow_html=True)

    # 가운데: 게이지 차트
    st.markdown('<div class="flex-item-center">', unsafe_allow_html=True)
    import plotly.graph_objects as go
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob_dropout_pct,
        number={'suffix': "%", 'font': {'size': 48, 'color': '#888'}},
        title={'text': "", 'font': {'size': 1}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#dc3545" if prob_dropout_pct >= 75 else ("#ffc107" if prob_dropout_pct >= 50 else "#28a745")},
            'steps': [
                {'range': [0, 50], 'color': "rgba(40, 167, 69, 0.2)"},
                {'range': [50, 75], 'color': "rgba(255, 193, 7, 0.2)"},
                {'range': [75, 100], 'color': "rgba(220, 53, 69, 0.2)"}
            ],
            'threshold': {'line': {'color': "black", 'width': 2}, 'thickness': 0.8, 'value': prob_dropout_pct }
        }
    ))
    fig_gauge.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=220, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 오른쪽: 설명 텍스트
    st.markdown(f'''
    <div class="flex-item-right">
        <div style="font-size:1.1em; font-weight:bold; margin-bottom:10px;"><b>{student_name}</b> 님의 자퇴 위험도가 <span class="highlight">{prob_dropout_pct}%</span>로 예측되어,</div>
        <div>현재 학업 지속에 <span class="bold">어려움을</span> 겪고 있을 가능성이 높습니다.<br>매니저님과 선생님의 <span class="bold">세심한 관심과 지원</span>이 필요하며,<br>학생의 학업 및 심리적 어려움을 함께 살펴보고 해결 방안을 모색해 주시면 좋겠습니다.</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


col_img, col_info = st.columns([1], gap="large")

with col_info:
    # 표 아래 자퇴 확률 섹션 추가
    # 자퇴 확률 섹션 (3개 영역)
    st.markdown("""
    <style>
    .flex-row-3col { display: flex; flex-direction: row; gap: 0px; margin-top: 40px; }
    .flex-item-left { flex: 1; min-width: 180px; max-width: 220px; background: #fff; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; padding: 30px 0 30px 0; }
    .flex-item-center { flex: 1.2; min-width: 320px; max-width: 400px; display: flex; align-items: center; justify-content: center; background: #fff; }
    .flex-item-right { flex: 1.5; min-width: 320px; max-width: 520px; background: #f8f8f8; padding: 30px 30px 30px 30px; border-radius: 8px; font-size: 1.05em; color: #222; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; margin-left: 30px; }
    .flex-item-right b, .flex-item-right strong { font-size: 1.1em; }
    .flex-item-right .highlight { color: #dc3545; font-weight: bold; }
    .flex-item-right .bold { font-weight: bold; }
    @media (max-width: 900px) {
        .flex-row-3col { flex-direction: column; }
        .flex-item-left, .flex-item-center, .flex-item-right { max-width: 100%; width: 100%; margin-left: 0; }
    }
    </style>
    """, unsafe_allow_html=True)

    avg_grade_1st = 14.8
    avg_grade_2nd = 18.2
    prob_dropout_pct = 79.7
    student_name = "김의령"


    st.markdown('<div class="flex-row-3col">', unsafe_allow_html=True)

    # 왼쪽: 제목+성적
    st.markdown(f'''
    <div class="flex-item-left">
        <div style="font-size:1.25em; font-weight:bold; margin-bottom:18px;">자퇴 확률</div>
        <div style="font-size:1.05em; margin-bottom:6px;">1학기 성적 평균 : <b>{avg_grade_1st} 점</b></div>
        <div style="font-size:1.05em;">2학기 성적 평균 : <b>{avg_grade_2nd} 점</b></div>
    </div>
    ''', unsafe_allow_html=True)

    # 가운데: 게이지 차트
    st.markdown('<div class="flex-item-center">', unsafe_allow_html=True)
    import plotly.graph_objects as go
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob_dropout_pct,
        number={'suffix': "%", 'font': {'size': 48, 'color': '#888'}},
        title={'text': "", 'font': {'size': 1}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#dc3545" if prob_dropout_pct >= 75 else ("#ffc107" if prob_dropout_pct >= 50 else "#28a745")},
            'steps': [
                {'range': [0, 50], 'color': "rgba(40, 167, 69, 0.2)"},
                {'range': [50, 75], 'color': "rgba(255, 193, 7, 0.2)"},
                {'range': [75, 100], 'color': "rgba(220, 53, 69, 0.2)"}
            ],
            'threshold': {'line': {'color': "black", 'width': 2}, 'thickness': 0.8, 'value': prob_dropout_pct }
        }
    ))
    fig_gauge.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=220, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 오른쪽: 설명 텍스트
    st.markdown(f'''
    <div class="flex-item-right">
        <div style="font-size:1.1em; font-weight:bold; margin-bottom:10px;"><b>{student_name}</b> 님의 자퇴 위험도가 <span class="highlight">{prob_dropout_pct}%</span>로 예측되어,</div>
        <div>현재 학업 지속에 <span class="bold">어려움을</span> 겪고 있을 가능성이 높습니다.<br>매니저님과 선생님의 <span class="bold">세심한 관심과 지원</span>이 필요하며,<br>학생의 학업 및 심리적 어려움을 함께 살펴보고 해결 방안을 모색해 주시면 좋겠습니다.</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
