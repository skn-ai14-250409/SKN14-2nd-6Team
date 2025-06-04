import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.model_loader import load_model
from utils import mappings
from PIL import Image
import base64
import io

# 로컬 이미지 로드
profile_image = Image.open("img/img2.jpg")

# 이미지를 Base64로 인코딩
# img2.jpg의 실제 형식에 따라 format="JPEG" 등으로 변경하세요.
buffered = io.BytesIO()
profile_image.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()
img_url = f"data:image/png;base64,{img_str}" # 이미지 형식에 맞게 image/png 또는 image/jpeg 지정

# 페이지 설정 (wide 레이아웃으로 넓게 사용)
st.set_page_config(layout="wide", page_title="학생 예측 결과")

# CSS 스타일 주입
st.markdown(
    """
    <style>
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

    .chart-and-text-container {
        display: flex;
        flex-direction: column; /* 세로 방향으로 정렬 (1열) */
        align-items: center; /* 가운데 정렬 */
        gap: 20px; /* 요소 사이 간격 */
        margin-top: 30px;
    }

    .chart-container {
        width: 100%; /* 부모 너비에 맞게 설정 */
        max-width: 400px; /* 차트의 최대 너비를 제한하여 너무 커지지 않게 */
    }

    .explanation-text {
        width: 100%; /* 부모 너비에 맞게 설정 */
        max-width: 600px; /* 텍스트 블록의 최대 너비를 제한하여 가독성 높임 */
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 1.1em;
        line-height: 1.6;
        color: #343a40;
        text-align: center; /* 텍스트도 중앙 정렬 (선택 사항) */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 역매핑 함수
def reverse_map(value, map_dict):
    return {v: k for k, v in map_dict.items()}.get(value)

# 입력 확인
if "form_input" not in st.session_state:
    st.warning("입력된 정보가 없습니다. 먼저 입력 페이지에서 정보를 제출하세요.")
    st.stop()

form = st.session_state["form_input"]
student_name = form.get("Student Name", "이름 없음")

# 역매핑 (한글 → 숫자)
mapped_input = {
    'Course': reverse_map(form['Course'], mappings.course_map),
    'Marital status': reverse_map(form['Marital status'], mappings.marital_status_map),
    'Daytime/evening attendance': reverse_map(form['Daytime/evening attendance'], mappings.attendance_map),
    'Previous qualification': reverse_map(form['Previous qualification'], mappings.previous_qualification_map),
    "Mother's occupation": reverse_map(form["Mother's occupation"], mappings.occupation_map),
    "Father's occupation": reverse_map(form["Father's occupation"], mappings.occupation_map),
    'Displaced': reverse_map(form['Displaced'], mappings.yes_no_map),
    'Educational special needs': reverse_map(form['Educational special needs'], mappings.yes_no_map),
    'Debtor': reverse_map(form['Debtor'], mappings.yes_no_map),
    'Tuition fees up to date': reverse_map(form['Tuition fees up to date'], mappings.yes_no_map),
    'Gender': reverse_map(form['Gender'], mappings.gender_map),
    'Scholarship holder': reverse_map(form['Scholarship holder'], mappings.scholarship_holder_map),
    'Age': form['Age at enrollment'],
    'Curricular units 1st sem (approved)': form['Curricular units 1st sem (approved)'],
    'Curricular units 1st sem (grade)': form['Curricular units 1st sem (grade)'],
    'Curricular units 2nd sem (approved)': form['Curricular units 2nd sem (approved)'],
    'Curricular units 2nd sem (grade)': form['Curricular units 2nd sem (grade)']
}

# 예측
model = load_model()
input_df = pd.DataFrame([mapped_input])

dropout_prob = round(model.predict_proba(input_df)[0][0] * 100, 2)
graduation_prob = round(model.predict_proba(input_df)[0][1] * 100, 2)

# ============================
# 전체 페이지 레이아웃 구성
# ============================
st.title("📈 학생 예측 결과")

# 상단에 학생 이름 정보 표시
st.markdown(f"<h2 class='profile-name-header'>{student_name}님 정보</h2>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 2.5])

with col_left:
    st.markdown(
        f"""
        <div class="profile-img-container">
            <img src="{img_url}" alt="Profile Image">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(f"<p class='profile-text'>{student_name}</p>", unsafe_allow_html=True)

    with st.container(border=False):
        st.markdown('<div class="profile-score-container">', unsafe_allow_html=True)
        score_col1, score_col2 = st.columns(2)
        with score_col1:
            st.markdown(f'<div class="score-item"><p>1학기 성적 평균 : <strong>{form["Curricular units 1st sem (grade)"]:.1f}점</strong></p></div>', unsafe_allow_html=True)
        with score_col2:
            st.markdown(f'<div class="score-item"><p>2학기 성적 평균 : <strong>{form["Curricular units 2nd sem (grade)"]:.1f}점</strong></p></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # 1. 학생 정보 테이블
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
                <td style="padding:12px;">{form['Course']}</td>
                <td>{form['Age at enrollment']}</td>
                <td>{form['Gender']}</td>
                <td>{form['Scholarship holder']}</td>
            </tr>
            <tr style="background-color:#e9ecef;">
                <th style="padding:12px;">이전 학력</th>
                <th>어머니 직업</th>
                <th>아버지 직업</th>
                <th>수업 형태</th>
            </tr>
            <tr>
                <td style="padding:12px;">{form['Previous qualification']}</td>
                <td>{form["Mother's occupation"]}</td>
                <td>{form["Father's occupation"]}</td>
                <td>{form['Daytime/evening attendance']}</td>
            </tr>
             <tr style="background-color:#e9ecef;">
                <th style="padding:12px;">채무</th>
                <th>등록금 납부</th>
                <th>전입 여부</th>
                <th>특수 교육</th>
            </tr>
            <tr>
                <td style="padding:12px;">{form["Debtor"]}</td>
                <td>{form["Tuition fees up to date"]}</td>
                <td>{form['Displaced']}</td>
                <td>{form['Educational special needs']}</td>
            </tr>
        </table>
        """,
        unsafe_allow_html=True
    )

    # 2. 위험 경고 메시지 (상단에 배치)
    if graduation_prob < 50:
        st.error("자퇴 위험이 높습니다.")
    elif graduation_prob < 75:
        st.warning("자퇴 가능성이 중간 수준입니다.")
    else:
        st.success("졸업 가능성이 높습니다!")

    # 3. 게이지 차트 및 요약 텍스트 (가로 배치)
    st.markdown(f"<h3 class='score-info-title' style='margin-top: 20px;'>자퇴 확률</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chart-and-text-container">', unsafe_allow_html=True)

    # 게이지 차트
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=dropout_prob,
        number={'suffix': "%", 'font': {'size': 48, 'color': '#333'}},
        title={'text': "자퇴 가능성", 'font': {'size': 20, 'color': '#555'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#007ACC"},
            'steps': [
                {'range': [0, 50], 'color': "#d4edda"},
                {'range': [50, 75], 'color': "#fff3cd"},
                {'range': [75, 100], 'color': "#dc3545"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': dropout_prob
            }
        }
    ))
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 요약 텍스트
    st.markdown(
        f"""
        <div class="explanation-text">
            <strong>{student_name}</strong>님의 자퇴 위험도가 <strong>{dropout_prob:.1f}%</strong>로 예측되어,
            현재 학업 지속에 어려움을 겪고 있을 가능성이 높습니다.
            매니저님과 선생님의 세심한 관심과 지원이 필요하며,
            학생의 학업 및 심리적 어려움을 함께 살펴보고 해결 방안을 모색해 주시면 좋겠습니다.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. 졸업/중도 이탈 가능성 요약
    st.markdown("---")
    col_prob1, col_prob2 = st.columns(2)
    with col_prob1:
        st.metric("🎓 졸업 가능성", f"{graduation_prob:.2f}%")
    with col_prob2:
        st.metric("⚠️ 중도 이탈 가능성", f"{dropout_prob:.2f}%")