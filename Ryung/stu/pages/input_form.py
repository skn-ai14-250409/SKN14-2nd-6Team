import streamlit as st
from PIL import Image
import os
import joblib
import base64
import pandas as pd
from io import BytesIO
from utils import mappings

# 선택 옵션
gender_options = list(mappings.gender_map.values())
marital_status = list(mappings.marital_status_map.values())
attendance_options = list(mappings.attendance_map.values())
course_options = list(mappings.course_map.values())
qualification_options = list(mappings.previous_qualification_map.values())
occupation_options = list(mappings.occupation_map.values())
yes_no_options = list(mappings.yes_no_map.values())
scholarship_options = list(mappings.scholarship_holder_map.values())

LOGO_PATH = os.path.join("img", "logo.png")
LOGO2_PATH = os.path.join("img", "logo2.png")
USER_IMG_PATH = os.path.join("img", "user_img.png")

st.set_page_config(
    page_title="PLAY DATA - 학생 정보 입력",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 모델 로드를 세션 상태에서 관리
if 'model' not in st.session_state:
    try:
        model_path = os.path.join("models", "best_model.pkl")
        if os.path.exists(model_path):
            st.session_state.model = joblib.load(model_path)
        else:
            st.error("모델 파일을 찾을 수 없습니다.")
            st.session_state.model = None
    except Exception as e:
        st.error(f"모델 로드 중 오류 발생: {e}")
        st.session_state.model = None

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
    .logo-container a {
        display: flex;
        align-items: end;
        gap: 10px;
    }
    .st-emotion-cache-1ab9dzl {
        gap : 1rem;
    }
    .st-emotion-cache-1y8sre1 {
        align-items: center;
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
    .stButton button {
        background-color: #504197;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: calc(100% - 100px) !important;
        margin: 0 auto;
        display: block;

    }
    .stButton button:hover {
        background-color: #43367a;
    }
    .stTextInput input {
        height: 38px !important;
        padding: 0 10px !important;
        border-radius: 4px !important;
        border: 1px solid #ccc !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        height: 38px !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        height: 38px !important;
        padding: 0 10px !important;
        border-radius: 4px !important;
        border: 1px solid #ccc !important;
    }
    .st-emotion-cache-16tyu1 e194bff00 {
        height : 100%;
        display: flex;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 이미지 로드 및 base64 인코딩
try:
    logo_image = Image.open(LOGO_PATH)
    buffered = BytesIO()
    logo_image.save(buffered, format="PNG")
    logo_base64 = base64.b64encode(buffered.getvalue()).decode()
except FileNotFoundError:
    st.error(f"로고 파일 '{LOGO_PATH}'을(를) 찾을 수 없습니다.")
    st.stop()

try:
    logo2_image = Image.open(LOGO2_PATH)
    buffered = BytesIO()
    logo2_image.save(buffered, format="PNG")
    logo2_base64 = base64.b64encode(buffered.getvalue()).decode()
except FileNotFoundError:
    st.error(f"로고2 파일 '{LOGO2_PATH}'을(를) 찾을 수 없습니다.")
    st.stop()

try:
    user_img = Image.open(USER_IMG_PATH)
    buffered = BytesIO()
    user_img.save(buffered, format="PNG")
    user_img_base64 = base64.b64encode(buffered.getvalue()).decode()
except FileNotFoundError:
    st.error(f"유저 이미지 파일 '{USER_IMG_PATH}'을(를) 찾을 수 없습니다.")
    st.stop()

# 헤더 렌더링
st.markdown(
    f"""
    <div class="header-container">
        <div class="logo-container">
            <a href="/" target="_self">
                <img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="PLAY DATA Logo" style="cursor: pointer;" onclick="window.location.href = 'http://localhost:8501';">
                <img src="data:image/png;base64,{logo2_base64}" class="logo-img" alt="PLAY DATA Logo2" style="width: 100px; height: auto;">
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

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'input'

if 'student_name' not in st.session_state:
    st.session_state.student_name = ""

# 메인 컨텐츠

st.markdown('<h4 style="text-align: left; font-weight: bold;">학생 정보 입력</h4>', unsafe_allow_html=True)

col_img, col_info = st.columns([1, 2], gap="large")

# 프로필 이미지 섹션
with col_img:
    st.markdown(f"""
        <style>
            .profile-img-container {{
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                gap: 100px;
                padding: 35px;
            }}
            .user_img {{
                position: relative;
                width: 140px;
                height: 140px;
                border-radius: 50%;
                background: #F5F5F5;
                overflow: hidden;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .user-img {{
                width: 70%;
                display: block;
            }}
            .overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border-radius: 50%;
                background: rgba(0, 0, 0, 0.4);
                opacity: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                transition: opacity 0.3s ease;
            }}
            .user_img:hover .overlay {{
                opacity: 1;
            }}
            .plus-icon {{
                color: white;
                font-size: 40px;
                font-weight: bold;
                user-select: none;
            }}
        </style>
        <div class="profile-img-container">
            <div class="user_img">
                <img src="data:image/png;base64,{user_img_base64}" class="user-img" alt="User Image">
                <div class="overlay">
                    <div class="plus-icon">+</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 학생 이름 입력
    student_name = st.text_input("학생 이름", 
                               value=st.session_state.student_name,
                               placeholder="이름을 입력하세요",
                               key="name_input")
    st.session_state.student_name = student_name

# 정보 입력 섹션
with col_info:
    col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("##### 기본 정보")
    age = st.number_input("입학 나이", min_value=15, max_value=40, value=20)
    gender = st.selectbox("성별", gender_options)
    marital_status_selected = st.selectbox("결혼 상태", marital_status)

with col2:
    st.markdown("##### 학업 정보")
    course = st.selectbox("수강 전공", course_options)
    attendance = st.selectbox("주/야간 수업", attendance_options)
    prev_qualification = st.selectbox("이전 학력", qualification_options)

# 재정 및 환경 정보
st.markdown("####")
st.markdown("##### 재정 및 환경 정보")
col3, col4 = st.columns(2)

with col3:
    mother_job = st.selectbox("어머니 직업", occupation_options)
    father_job = st.selectbox("아버지 직업", occupation_options)
    displaced = st.selectbox("이재민 여부", yes_no_options)
    special_needs = st.selectbox("특수 교육 필요 여부", yes_no_options)

with col4:
    debtor = st.selectbox("연체 여부", yes_no_options)
    tuition = st.selectbox("등록금 납부 여부", yes_no_options)
    scholarship = st.selectbox("장학금 수혜 여부", scholarship_options)

# 성적 정보
st.markdown("####")
st.markdown("##### 성적 정보")
first_sem_approved = st.number_input("1학기 합격 과목 수", min_value=0, max_value=10, value=5)
first_sem_grade = st.number_input("1학기 성적 평균", min_value=0.0, max_value=20.0, value=12.5)
second_sem_approved = st.number_input("2학기 합격 과목 수", min_value=0, max_value=10, value=4)
second_sem_grade = st.number_input("2학기 성적 평균", min_value=0.0, max_value=20.0, value=11.0)

# 정보 확인하기 버튼
st.markdown("---")
# 예측 결과 확인 버튼
col_button1, col_button2, col_button3 = st.columns([1, 2, 1])
with col_button2:
    st.markdown("###")
    if st.button("예측 결과 확인", type="primary", use_container_width=True,
                 help="입력한 정보를 바탕으로 학생의 졸업 가능성을 예측합니다"):
        if not student_name.strip():
            st.error("학생 이름을 입력해주세요.")
        else:
            # 원본 폼 데이터 (표시용)
            form_input_original = {
                'Student Name': student_name,
                'Course': course,
                'Daytime/evening attendance': attendance,
                'Previous qualification': prev_qualification,
                "Mother's occupation": mother_job,
                "Father's occupation": father_job,
                'Displaced': displaced,
                'Educational special needs': special_needs,
                'Debtor': debtor,
                'Tuition fees up to date': tuition,
                'Gender': gender,
                'Marital status': marital_status_selected,
                'Scholarship holder': scholarship,
                'Age': age,
                'Curricular units 1st sem (approved)': first_sem_approved,
                'Curricular units 1st sem (grade)': first_sem_grade,
                'Curricular units 2nd sem (approved)': second_sem_approved,
                'Curricular units 2nd sem (grade)': second_sem_grade
            }
            
            # 모델 입력용 데이터 변환 (mappings 사용)
            model_input = {
                'Course': mappings.course_map_reverse.get(course, 9),
                'Daytime/evening attendance': mappings.attendance_map_reverse.get(attendance, 1),
                'Previous qualification': mappings.previous_qualification_map_reverse.get(prev_qualification, 1),
                "Mother's occupation": mappings.occupation_map_reverse.get(mother_job, 12),
                "Father's occupation": mappings.occupation_map_reverse.get(father_job, 12),
                'Displaced': mappings.yes_no_map_reverse.get(displaced, 0),
                'Educational special needs': mappings.yes_no_map_reverse.get(special_needs, 0),
                'Debtor': mappings.yes_no_map_reverse.get(debtor, 0),
                'Tuition fees up to date': mappings.yes_no_map_reverse.get(tuition, 1),
                'Gender': mappings.gender_map_reverse.get(gender, 0),
                'Marital status': mappings.marital_status_map_reverse.get(marital_status_selected, 1),
                'Scholarship holder': mappings.scholarship_holder_map_reverse.get(scholarship, 0),
                'Age': age,
                'Curricular units 1st sem (approved)': first_sem_approved,
                'Curricular units 1st sem (grade)': first_sem_grade,
                'Curricular units 2nd sem (approved)': second_sem_approved,
                'Curricular units 2nd sem (grade)': second_sem_grade
            }
            
            # DataFrame으로 변환
            student_df = pd.DataFrame([model_input])
            
            # 세션 상태에 저장
            st.session_state.form_input_original = form_input_original
            st.session_state.student_info_df = student_df
            
            # 성공 메시지와 함께 페이지 이동
            import time
            with st.spinner("데이터를 처리하고 있습니다..."):
                time.sleep(1)  # 1초 대기
            
            st.success("✅ 정보가 성공적으로 저장되었습니다!")
            st.info("🔄 예측 결과 페이지로 이동합니다...")
            
            # 페이지 이동
            time.sleep(0.5)  # 메시지를 보여주기 위한 짧은 대기
            st.switch_page("pages/result.py")

