# pages/3_📈_학생_예측_결과.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import base64
import io
import os
import sys

# 프로젝트 루트 경로를 sys.path에 추가 (mappings.py 임포트를 위해)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from utils import mappings

# --- 이미지 경로 설정 ---
IMG_DIR_RESULT = os.path.join(project_root, "img")
PROFILE_IMG_PATH = os.path.join(IMG_DIR_RESULT, "user_img.png")

LOGO_PATH = os.path.join("img", "logo.png")

st.set_page_config(
    page_title="PLAY DATA - 예측 결과",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
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
    /* 전체 페이지 배경색 */
    .stApp {
        background-color: #f8f9fa;
    }

    /* 제목 스타일 */
    h1 {
        color: #343a40;
        font-size: 2.5em;
        margin-bottom: 30px;
        text-align: center;
    }

    /* 정보 테이블 스타일 */
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        overflow: hidden; /* border-radius 적용을 위해 */
    }
    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #dee2e6;
        font-size: 0.95em;
    }
    th {
        background-color: #e9ecef;
        color: #495057;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    tr:hover {
        background-color: #e2e6ea;
    }

    /* Streamlit 기본 경고/성공/에러 메시지 스타일 */
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        font-weight: bold;
        font-size: 1.1em;
    }
    .stAlert.error {
        background-color: #f8d7da;
        color: #721c24;
        border-color: #f5c6cb;
    }
    .stAlert.warning {
        background-color: #fff3cd;
        color: #856404;
        border-color: #ffeeba;
    }
    .stAlert.success {
        background-color: #d4edda;
        color: #155724;
        border-color: #c3e6cb;
    }

    /* 게이지 차트 제목 및 숫자 스타일 */
    .gauge .number {
        font-size: 3em !important;
        color: #333 !important;
    }
    .gauge .title {
        font-size: 1.2em !important;
        color: #555 !important;
    }

    /* 메트릭 스타일 */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.2em !important;
        font-weight: bold;
        color: #007ACC !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.1em !important;
        color: #6c757d;
        margin-bottom: 10px;
    }

    /* 섹션 제목 */
    h3 {
        color: #343a40;
        font-size: 1.7em;
        margin-top: 30px;
        margin-bottom: 20px;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 10px;
    }

    /* 새로운 레이아웃을 위한 스타일 */
    .profile-img-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background-color: #e0e0e0;
        overflow: hidden;
        margin: 20px auto 10px auto;
        border: 3px solid #007ACC;
    }
    .profile-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .profile-text {
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
        color: #343a40;
        margin-bottom: 30px;
    }
    .profile-name-header {
        text-align: left; /* 좌측 정렬 */
        font-size: 2em; /* 크기 조정 */
        color: #343a40;
        margin-top: 0;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #e9ecef;
    }

    .score-info-title {
        color: #343a40;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
        text-align: center;
    }
    .score-item p {
        margin: 5px 0;
        font-size: 1em;
        color: #555;
    }
    .score-item strong {
        color: #007ACC;
        font-size: 1.1em;
    }
    /* 게이지 차트 및 설명 텍스트를 위한 2열 레이아웃 컨테이너 */
    .chart-and-text-container {
        display: flex; /* Flexbox 활성화 */
        flex-direction: row; /* 가로 방향으로 정렬 (2열) */
        flex-wrap: wrap; /* 공간 부족 시 줄 바꿈 허용 */
        justify-content: center; /* 가운데 정렬 */
        align-items: flex-start; /* 아이템들을 상단에 정렬 */
        gap: 30px; /* 요소 사이 간격 */
        margin-top: 30px;
    }

    .chart-container {
        flex: 1; /* 가용한 공간을 차지하도록 설정 */
        min-width: 300px; /* 차트의 최소 너비 설정 */
        max-width: 45%; /* 부모 너비의 최대 45%를 차지하도록 제한 */
    }

    .explanation-text {
        flex: 1.5; /* 차트보다 더 많은 공간을 차지하도록 설정 (예: 1.5배) */
        min-width: 350px; /* 텍스트 블록의 최소 너비 설정 */
        max-width: 50%; /* 부모 너비의 최대 50%를 차지하도록 제한 */
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 1.1em;
        line-height: 1.6;
        color: #343a40;
        text-align: left; /* 텍스트는 왼쪽 정렬이 더 자연스러움 */
    }

    /* 반응형 디자인: 작은 화면에서는 다시 1열로 (차트와 텍스트) */
    @media (max-width: 768px) {
        .chart-and-text-container {
            flex-direction: column; /* 세로 방향으로 정렬 */
            align-items: center; /* 가운데 정렬 */
        }
        .chart-container, .explanation-text {
            width: 100%; /* 전체 너비 차지 */
            max-width: 90%; /* 너무 붙지 않게 최대 너비 조정 */
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 헤더 렌더링 (맨 위에서 실행)
try:
    logo_image = Image.open(LOGO_PATH)
    buffered = io.BytesIO()
    logo_image.save(buffered, format="PNG")
    logo_base64 = base64.b64encode(buffered.getvalue()).decode()
except FileNotFoundError:
    logo_base64 = ""

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

# 메인 컨텐츠
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)

# 모델 로드 확인 (st.session_state.model 사용)
model = st.session_state.get('model', None)
student_df_for_prediction = st.session_state.student_info_df
form_original_labels = st.session_state.form_input_original # 표시용 원본 입력값
student_name = form_original_labels.get("Student Name", "정보 없음")

# 학생 정보 예시 (실제 데이터로 대체)
profile_img_path = os.path.join('img', 'user_img.png')

# 학생 정보 딕셔너리 (실제 데이터로 대체)
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

# 표 데이터 생성
info_table = [
    ['전공', student_info['전공'], '입학 나이', student_info['입학 나이']],
    ['이전 학력', student_info['이전 학력'], '어머니 직업', student_info['어머니 직업']],
    ['성별', student_info['성별'], '장학금', student_info['장학금'], '수업 형태', student_info['수업 형태']],
    ['아버지 직업', student_info['아버지 직업'], '채무', student_info['채무'], '등록금 납부', student_info['등록금 납부']],
]

# 레이아웃: 좌(이미지+이름), 우(정보 표)
col_img, col_info = st.columns([1, 2], gap="large")

with col_img:
    st.markdown(f'<div style="font-weight:bold; font-size:20px; margin-bottom:20px;">{student_name} 님 정보</div>', unsafe_allow_html=True)
    if os.path.exists(profile_img_path):
        st.image(profile_img_path, width=180, use_column_width=False, caption=None, output_format='auto')
    else:
        st.image('https://via.placeholder.com/180?text=No+Image', width=180)

with col_info:
    st.markdown('<style>th, td {padding: 8px 16px; text-align: left;} .info-table {width:100%; border-collapse:collapse;} .info-table td, .info-table th {border:1px solid #eee; background:#fafafa;} .info-table th {background:#f5f5f5; font-weight:bold;}</style>', unsafe_allow_html=True)
    table_html = f'''
    <table class="info-table">
        <tr><td>전공</td><td>{student_info['전공']}</td><td>입학 나이</td><td>{student_info['입학 나이']}</td></tr>
        <tr><td>이전 학력</td><td>{student_info['이전 학력']}</td><td>어머니 직업</td><td>{student_info['어머니 직업']}</td></tr>
        <tr><td>성별</td><td>{student_info['성별']}</td><td>장학금</td><td>{student_info['장학금']}</td><td>수업 형태</td><td>{student_info['수업 형태']}</td></tr>
        <tr><td>아버지 직업</td><td>{student_info['아버지 직업']}</td><td>채무</td><td>{student_info['채무']}</td><td>등록금 납부</td><td>{student_info['등록금 납부']}</td></tr>
    </table>
    '''
    st.markdown(table_html, unsafe_allow_html=True)

try:
    # 예측 확률 및 클래스
    probabilities = model.predict_proba(student_df_for_prediction)
    prediction_numeric = model.predict(student_df_for_prediction)[0] # 0 또는 1

    # 예측된 숫자값을 다시 한글로 (결과 표시용)
    predicted_status_label = mappings.target_map.get(prediction_numeric, "알 수 없음")

    # 클래스 0: Dropout, 클래스 1: Graduate
    prob_dropout_pct = round(probabilities[0, 0] * 100, 2)
    prob_graduate_pct = round(probabilities[0, 1] * 100, 2)

except Exception as e:
    st.error(f"예측 실행 중 오류가 발생했습니다: {e}")
    st.exception(e)
    st.stop()


# ============================
# 전체 페이지 레이아웃 구성
# ============================
st.title("📈 학생 예측 결과")

st.markdown(f"<h2 class='profile-name-header'>{student_name}님 정보 및 예측 결과</h2>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 2.5]) # 좌우 컬럼 비율

with col_left:
    if img_url: # 이미지가 정상적으로 로드되었을 경우에만 표시
        st.markdown(
            f"""
            <div class="profile-img-container">
                <img src="{img_url}" alt="Profile Image">
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown(f"<p class='profile-text'>{student_name}</p>", unsafe_allow_html=True)

    with st.container(border=False): # border=False는 Streamlit 1.25.0 이상
        score_col1, score_col2 = st.columns(2) # Added columns for score items
        with score_col1:
            st.markdown(f'<div class="score-item"><p>1학기 성적 평균 : <strong>{form_original_labels["Curricular units 1st sem (grade)"]:.1f}점</strong></p></div>', unsafe_allow_html=True)
        with score_col2:
            st.markdown(f'<div class="score-item"><p>2학기 성적 평균 : <strong>{form_original_labels["Curricular units 2nd sem (grade)"]:.1f}점</strong></p></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # 1. 학생 정보 테이블 (st.session_state.form_input_original 사용)
    st.markdown(
        f"""
        <table style="width:100%; border:1px solid #ddd; border-collapse: collapse; table-layout: fixed;">
            <tr style="background-color:#e9ecef;">
                <th style="padding:12px; width:25%;">전공</th>
                <th style="width:25%;">입학 나이</th>
                <th style="width:25%;">성별</th>
                <th style="width:25%;">장학금</th>
            </tr>
            <tr>
                <td style="padding:12px;">{form_original_labels['Course']}</td>
                <td>{form_original_labels['Age']}</td>
                <td>{form_original_labels['Gender']}</td>
                <td>{form_original_labels['Scholarship holder']}</td>
            </tr>
            <tr style="background-color:#e9ecef;">
                <th style="padding:12px;">이전 학력</th>
                <th>어머니 직업</th>
                <th>아버지 직업</th>
                <th>수업 형태</th>
            </tr>
            <tr>
                <td style="padding:12px;">{form_original_labels['Previous qualification']}</td>
                <td>{form_original_labels["Mother's occupation"]}</td>
                <td>{form_original_labels["Father's occupation"]}</td>
                <td>{form_original_labels['Daytime/evening attendance']}</td>
            </tr>
            <tr style="background-color:#e9ecef;">
                <th style="padding:12px;">채무</th>
                <th>등록금 납부</th>
                <th>전입 여부</th> <th>특수 교육</th>
            </tr>
            <tr>
                <td style="padding:12px;">{form_original_labels["Debtor"]}</td>
                <td>{form_original_labels["Tuition fees up to date"]}</td>
                <td>{form_original_labels['Displaced']}</td>
                <td>{form_original_labels['Educational special needs']}</td>
            </tr>
        </table>
        """,
        unsafe_allow_html=True
    )

    # 2. 예측 결과 및 조언 메시지 (adapted from second_script.py's alert style)
    st.markdown("---")
    st.subheader("💡 예측 요약 및 조언")
    if prediction_numeric == 1: # Graduate
        st.success(f"🎉 **{student_name}님은 졸업 가능성이 높습니다 (졸업 확률: {prob_graduate_pct}%)**")
        st.markdown("훌륭합니다! 이 학생은 학업을 성공적으로 마칠 것으로 예상됩니다. 지속적인 격려와 함께, 혹시 모를 어려움은 없는지 주기적으로 관심을 가져주시면 더욱 좋겠습니다.")
    else: # Dropout
        st.error(f"⚠️ **{student_name}님은 중퇴 위험이 높습니다 (중퇴 확률: {prob_dropout_pct}%)**")
        st.markdown("주의가 필요합니다. 이 학생은 학업 중도 포기 가능성이 높게 예측되었습니다. **상담이 필요한 학생입니다.** 학생의 학업적, 개인적 어려움을 파악하고 맞춤형 지원 방안을 모색하는 것이 중요합니다.")

# --- 2열 섹션 시작: 게이지 차트 및 요약 텍스트 ---
st.markdown(f"<h3 class='score-info-title' style='margin-top: 30px;'>상세 예측 확률</h3>", unsafe_allow_html=True)
st.markdown('<div class="chart-and-text-container">', unsafe_allow_html=True)

# 게이지 차트
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=prob_dropout_pct, # 중퇴 확률을 게이지로 표시
    number={'suffix': "%", 'font': {'size': 48, 'color': '#333'}},
    title={'text': "중퇴 가능성 지표", 'font': {'size': 20, 'color': '#555'}},
    gauge={
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "#007ACC" if prob_dropout_pct < 50 else ("#ffc107" if prob_dropout_pct < 75 else "#dc3545")},
        'steps': [
            {'range': [0, 50], 'color': "#d4edda"},    # 낮음 (녹색 계열)
            {'range': [50, 75], 'color': "#fff3cd"},   # 중간 (노랑 계열)
            {'range': [75, 100], 'color': "#f8d7da"}    # 높음 (빨강 계열)
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': prob_dropout_pct
        }
    }
))
fig_gauge.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    height=280,
    paper_bgcolor="rgba(0,0,0,0)", # 배경 투명
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_gauge, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True) # .chart-container 닫기

# 요약 텍스트
explanation = f"""
<strong>{student_name}</strong>님의 예측된 중퇴 확률은 <strong>{prob_dropout_pct:.1f}%</strong>이며,
졸업 확률은 <strong>{prob_graduate_pct:.1f}%</strong>입니다.
"""
if prediction_numeric == 0: # 중퇴 예측
    explanation += """
    <br>이 결과는 학생이 현재 학업에 어려움을 겪고 있을 수 있음을 시사합니다.
    적극적인 면담을 통해 어려움을 파악하고, 필요한 학업적 지원, 심리 상담 연계, 또는
    학습 환경 개선 등의 조치를 고려해볼 수 있습니다.
    """
else: # 졸업 예측
    explanation += """
    <br>이 결과는 학생이 현재 학업을 잘 수행하고 있음을 나타냅니다.
    지속적인 관심과 격려를 통해 현재의 긍정적인 학업 태도를 유지할 수 있도록 지원해주세요.
    """

st.markdown(
    f"""
    <div class="explanation-text">
        {explanation}
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True) # .chart-and-text-container 닫기
# --- 2열 섹션 끝 ---

# --- 1열 섹션 시작: 예측 결과 요약 (Metrics) ---
st.markdown("---")
st.markdown(f"<h3 class='score-info-title'>예측 결과 요약</h3>", unsafe_allow_html=True)
col_prob1, col_prob2 = st.columns(2)
with col_prob1:
    st.metric("🎓 졸업 가능성", f"{prob_graduate_pct:.2f}%")
with col_prob2:
    st.metric("⚠️ 중도 이탈 가능성", f"{prob_dropout_pct:.2f}%")
# --- 1열 섹션 끝 ---

st.markdown("---")
if st.button("다른 학생 정보 입력하기", use_container_width=True, key="go_back_to_input_btn"):
    # 세션 상태 초기화: 새로운 예측을 위해 이전 입력값과 예측 결과를 지웁니다.
    st.session_state.student_info_df = None
    st.session_state.form_input_original = None
    # '학생 정보 입력' 페이지로 이동합니다.
    st.switch_page("pages/input_form.py")