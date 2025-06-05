import streamlit as st
import os
from PIL import Image
import base64
from io import BytesIO
from utils.model_loader import load_model
from utils import mappings

st.set_page_config(
    page_title="PLAY DATA - 예측 결과",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 로고 이미지 경로 설정
LOGO_PATH = os.path.join("img", "logo.png")

# 세션 상태에서 데이터 가져오기
if 'model' not in st.session_state:
    st.error("모델이 로드되지 않았습니다.")
    st.stop()

if 'student_info_df' not in st.session_state:
    st.error("학생 정보가 없습니다.")
    st.stop()

if 'form_input_original' not in st.session_state:
    st.error("입력된 정보가 없습니다.")
    st.stop()

# 필요한 데이터 가져오기
model = st.session_state.model
student_df_for_prediction = st.session_state.student_info_df
form_original_labels = st.session_state.form_input_original
student_name = form_original_labels.get("Student Name", "정보 없음")

# 예측 실행
try:
    # 예측 확률 및 클래스
    probabilities = model.predict_proba(student_df_for_prediction)
    prediction_numeric = model.predict(student_df_for_prediction)[0]  # 0 또는 1

    # 예측된 숫자값을 다시 한글로 (결과 표시용)
    predicted_status_label = mappings.target_map.get(prediction_numeric, "알 수 없음")

    # 클래스 0: Dropout, 클래스 1: Graduate
    prob_dropout_pct = round(probabilities[0, 0] * 100, 2)
    prob_graduate_pct = round(probabilities[0, 1] * 100, 2)

except Exception as e:
    st.error(f"예측 실행 중 오류가 발생했습니다: {e}")
    st.exception(e)
    st.stop()

##@#-------------------------------

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
# student_name = '김의령'
# student_info = {
#     '전공': '바이오연료생산기술',
#     '입학 나이': '21',
#     '이전 학력': '고졸',
#     '어머니 직업': '학생',
#     '성별': '여성',
#     '장학금': '미수혜',
#     '수업 형태': '야간',
#     '아버지 직업': '학생',
#     '채무': '아니오',
#     '등록금 납부': '아니오',
#     '1학기 성적 평균': 14.8,
#     '2학기 성적 평균': 18.2,
#     '자퇴확률': 79.7
# }

# avg_grade_1st = student_info['1학기 성적 평균']
# avg_grade_2nd = student_info['2학기 성적 평균']
# prob_dropout_pct = student_info['자퇴확률']


# 헤더와 겹치지 않게 충분한 여백 추가
st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
st.markdown(f'<div style="font-weight:bold; font-size:20px; margin-bottom:20px;">{student_name} 님 정보</div>',
            unsafe_allow_html=True)
st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

# 전체 너비 및 컬럼 비율 input_form.py와 맞춤
col_img, col_info = st.columns([1, 2], gap="large")

with col_img:
    st.markdown(
        f"""
         <div style="display:flex; justify-content:center; align-items:center; height:220px;">
            <div style="width:160px; height:160px; border-radius:50%; background:#e0e0e0; display:flex; align-items:center; justify-content:center;">
                <img src="{user_img_url}" style="width:100px; height:100px; object-fit:cover;" />
            </div>
            
         </div>
        """,
        unsafe_allow_html=True
    )

with col_info:
    st.markdown('''
    <style>
    .info-table2, .info-table3 {width:100%; border-collapse:collapse; margin-bottom:0;}
    .info-table2 th, .info-table2 td {width:50%; border:1px solid #eee; background:#fafafa;  text-align:left; font-size:15px;}
    .info-table2 th {background:#f5f5f5; font-weight:bold;}
    .info-table3 th, .info-table3 td {width:33.33%; border:1px solid #eee; background:#fafafa; text-align:left; font-size:15px;}
    .info-table3 th {background:#f5f5f5; font-weight:bold;}
    .info-table2 {margin-bottom:0; border-bottom:none;}
    .info-table3 {margin-top:0; border-top:none;}
    </style>
    ''', unsafe_allow_html=True)
    table2_html = f'''
    <table class="info-table2">
        <tr><th>전공</th><th>입학 나이</th></tr>
        <tr><td>{form_original_labels['Course']}</td><td>{form_original_labels['Age']}</td></tr>
        <tr><th>이전 학력</th><th>어머니 직업</th></tr>
        <tr><td>{form_original_labels['Previous qualification']}</td><td>{form_original_labels["Mother's occupation"]}</td></tr>
    </table>
    '''

    table3_html = f'''
    <table class="info-table3">
        <tr><th>성별</th><th>장학금</th><th>수업 형태</th></tr>
        <tr><td>{form_original_labels['Gender']}</td><td>{form_original_labels['Scholarship holder']}</td><td>{form_original_labels['Daytime/evening attendance']}</td></tr>
        <tr><th>아버지 직업</th><th>채무</th><th>등록금 납부</th></tr>
        <tr><td>{form_original_labels["Father's occupation"]}</td><td>{form_original_labels["Debtor"]}</td><td>{form_original_labels["Tuition fees up to date"]}</td></tr>
    </table>
    '''
    st.markdown(table2_html + table3_html, unsafe_allow_html=True)




# --- row 구분선 (선택) ---
st.markdown("<hr style='margin:40px 0 30px 0;'>", unsafe_allow_html=True)
st.markdown('<div style="font-size:1.25em; font-weight:bold; margin-bottom:18px;">자퇴 확률</div>', unsafe_allow_html=True)
# --- 두 번째 row: 자퇴 확률 (왼쪽: 성적/제목, 가운데: 게이지, 오른쪽: 설명) ---
col_left, col_mid, col_right = st.columns([0.7, 1.0, 1.6], gap="medium")
with col_left:
    # 왼쪽: 성적
    st.markdown(f'''
    <div style="display: flex; flex-direction: column; align-items: flex-start; min-height: 220px;">
        <div style="font-size:1.05em; margin-bottom:6px;">1학기 성적 평균 : <b>{form_original_labels["Curricular units 1st sem (grade)"]:.1f}  점</b></div>
        <div style="font-size:1.05em;">2학기 성적 평균 : <b>{form_original_labels["Curricular units 2nd sem (grade)"]:.1f} 점</b></div>
    </div>
    ''', unsafe_allow_html=True)

with col_mid:
    # 가운데: 게이지 차트
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

with col_right:
    # 오른쪽: 설명 텍스트
    if prob_dropout_pct < 25:
        message = f'''
        <div style="background: #f8f8f8; padding: 30px; border-radius: 8px; font-size: 1.0em; color: #222; display: flex; flex-direction: column; justify-content: center; min-height: 160px;">
            <div style="font-size:1.0em; font-weight:bold; margin-bottom:10px;"><b>{student_name}</b> 님의 자퇴 위험도가 <span style="color: #28a745; font-weight: bold;">{prob_dropout_pct}%</span>로 예측되었습니다.</div>
            <div>학업 지속에 문제가 없으며, 현재 매우 안정적으로 학교생활을 하고 있을 가능성이 높습니다.<br>꾸준한 학업 참여를 격려하며, 학생이 긍정적인 학교생활을 유지할 수 있도록 관심을 이어가 주세요.</div>
        </div>
        '''
    elif prob_dropout_pct < 50:
        message = f'''
        <div style="background: #f8f8f8; padding: 30px; border-radius: 8px; font-size: 1.0em; color: #222; display: flex; flex-direction: column; justify-content: center; min-height: 160px;">
            <div style="font-size:1.0em; font-weight:bold; margin-bottom:10px;"><b>{student_name}</b> 님의 자퇴 위험도가 <span style="color: #28a745; font-weight: bold;">{prob_dropout_pct}%</span>로 예측되었습니다.</div>
            <div>학업 지속에 큰 문제는 없어 보이나, 일부 작은 어려움이 있을 수 있습니다.<br>학생의 고민이나 생활 리듬을 주기적으로 살펴보며, 문제가 발생하기 전에 예방할 수 있도록 관심을 가져주세요.</div>
        </div>
        '''
    elif prob_dropout_pct < 75:
        message = f'''
        <div style="background: #f8f8f8; padding: 30px; border-radius: 8px; font-size: 1.0em; color: #222; display: flex; flex-direction: column; justify-content: center; min-height: 160px;">
            <div style="font-size:1.0em; font-weight:bold; margin-bottom:10px;"><b>{student_name}</b> 님의 자퇴 위험도가 <span style="color: #ffc107; font-weight: bold;">{prob_dropout_pct}%</span>로 예측되었습니다.</div>
            <div>학업 지속에 중간 정도의 어려움을 겪고 있을 가능성이 있습니다.<br>학생의 학업 태도, 생활 패턴, 심리 상태 등을 함께 살펴보며, 적절한 상담과 지원 방안을 마련해 주세요.</div>
        </div>
        '''
    elif prob_dropout_pct < 100:
        message = f'''
        <div style="background: #f8f8f8; padding: 30px; border-radius: 8px; font-size: 1.0em; color: #222; display: flex; flex-direction: column; justify-content: center; min-height: 160px;">
            <div style="font-size:1.0em; font-weight:bold; margin-bottom:10px;"><b>{student_name}</b> 님의 자퇴 위험도가 <span style="color: #dc3545; font-weight: bold;">{prob_dropout_pct}%</span>로 예측되었습니다.</div>
            <div>학업 지속에 상당한 어려움을 겪고 있을 가능성이 높습니다.<br>매니저님과 선생님의 세심한 관심과 지원이 필요하며, 학생의 학업 및 심리적 어려움을 함께 살펴보고 해결 방안을 모색해 주시면 좋겠습니다.</div>
        </div>
        '''
    else:
        message = f'''
        <div style="background: #f8f8f8; padding: 30px; border-radius: 8px; font-size: 1.0em; color: #222; display: flex; flex-direction: column; justify-content: center; min-height: 160px;">
            <div style="font-size:1.0em; font-weight:bold; margin-bottom:10px;"><b>{student_name}</b> 님의 자퇴 위험도가 <span style="color: #dc3545; font-weight: bold;">{prob_dropout_pct}%</span>로 예측되었습니다.</div>
            <div>현재 학업 지속이 매우 어렵고, 자퇴 위험이 가장 높은 상태로 판단됩니다.<br>즉각적인 관심과 적극적인 상담, 맞춤형 지원이 반드시 필요합니다. 학생의 학업 및 심리적 상태를 면밀히 파악해 문제 해결을 위한 지원을 부탁드립니다.</div>
        </div>
        '''
    
    st.markdown(message, unsafe_allow_html=True)