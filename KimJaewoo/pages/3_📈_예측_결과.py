import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import base64
import io
import os # os import 추가
import sys # sys import 추가

# 프로젝트 루트 경로를 sys.path에 추가 (mappings.py 임포트를 위해)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

import mappings # mappings.py 임포트

# --- 이미지 경로 설정 ---
BASE_DIR_RESULT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR_RESULT = os.path.join(os.path.dirname(BASE_DIR_RESULT), "img") # pages 폴더의 부모의 img
PROFILE_IMG_PATH = os.path.join(IMG_DIR_RESULT, "img2.jpg")


# 로컬 이미지 로드 및 Base64 인코딩 함수
def get_image_base64(image_path):
    try:
        profile_image = Image.open(image_path)
        buffered = io.BytesIO()
        # 이미지 형식에 따라 format 변경 (PNG, JPEG 등)
        img_format = profile_image.format if profile_image.format else "PNG"
        if img_format.upper() == "JPG": img_format = "JPEG" # PIL은 JPG를 JPEG로 인식

        profile_image.save(buffered, format=img_format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/{img_format.lower()};base64,{img_str}"
    except FileNotFoundError:
        st.error(f"이미지 파일 '{image_path}'을(를) 찾을 수 없습니다.")
        return "" # 빈 문자열 반환 또는 기본 이미지 URL

img_url = get_image_base64(PROFILE_IMG_PATH)


# 페이지 설정 (wide 레이아웃으로 넓게 사용)
# st.set_page_config는 최상단 app.py에서 한번만 호출하는 것이 권장됨.
# 여기서는 기존 코드 유지를 위해 남겨두지만, app.py로 옮기는 것이 좋음.
# st.set_page_config(layout="wide", page_title="학생 예측 결과")

# CSS 스타일 주입 (기존 코드와 동일)
st.markdown(
    """
    <style>
    /* ... (제공해주신 CSS 스타일 그대로 유지) ... */
     .main .block-container { /* 메인 콘텐츠 영역 상단 패딩 조정 */
        padding-top: 1rem !important; /* 필요시 조정 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 모델 로드 확인 (st.session_state.model 사용)
if 'model' not in st.session_state or st.session_state.model is None:
    st.error("모델 로딩에 실패했습니다. 앱을 재시작하거나 메인 페이지로 돌아가 모델을 로드해주세요.")
    if st.button("메인 페이지로 돌아가기"):
        st.switch_page("app.py")
    st.stop()

# 학생 정보가 입력되었는지 확인
# st.session_state.student_info_df (모델 입력용)와 st.session_state.form_input_original (표시용) 확인
if 'student_info_df' not in st.session_state or st.session_state.student_info_df is None \
   or 'form_input_original' not in st.session_state or st.session_state.form_input_original is None:
    st.warning("입력된 정보가 없습니다. 먼저 '학생 정보 입력' 페이지에서 정보를 제출하세요.")
    if st.button("정보 입력 페이지로 돌아가기"):
        st.switch_page("pages/2_🧑‍🎓_학생_정보_입력.py")
    st.stop()

model = st.session_state.model
student_df_for_prediction = st.session_state.student_info_df
form_original_labels = st.session_state.form_input_original # 표시용 원본 입력값
student_name = form_original_labels.get("Student Name", "정보 없음")


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
        st.markdown('<div class="profile-score-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="score-item"><p>1학기 성적 평균 : <strong>{form_original_labels["Curricular units 1st sem (grade)"]:.1f}점</strong></p></div>', unsafe_allow_html=True)
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
                <th>거주지 이탈</th>
                <th>특수 교육</th>
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

    # 2. 예측 결과 및 조언 메시지
    st.markdown("---")
    st.subheader("💡 예측 요약 및 조언")
    if prediction_numeric == 1: # Graduate
        st.success(f"🎉 **{student_name}님은 졸업 가능성이 높습니다 (졸업 확률: {prob_graduate_pct}%)**")
        st.markdown("훌륭합니다! 이 학생은 학업을 성공적으로 마칠 것으로 예상됩니다. 지속적인 격려와 함께, 혹시 모를 어려움은 없는지 주기적으로 관심을 가져주시면 더욱 좋겠습니다.")
    else: # Dropout
        st.error(f"⚠️ **{student_name}님은 중퇴 위험이 높습니다 (중퇴 확률: {prob_dropout_pct}%)**")
        st.markdown("주의가 필요합니다. 이 학생은 학업 중도 포기 가능성이 높게 예측되었습니다. **상담이 필요한 학생입니다.** 학생의 학업적, 개인적 어려움을 파악하고 맞춤형 지원 방안을 모색하는 것이 중요합니다.")

    # 3. 게이지 차트 및 요약 텍스트
    st.markdown(f"<h3 class='score-info-title' style='margin-top: 30px;'>상세 예측 확률</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chart-and-text-container">', unsafe_allow_html=True)

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
                {'range': [75, 100], 'color': "#f8d7da"}   # 높음 (빨강 계열)
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
    st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown('</div>', unsafe_allow_html=True) # chart-and-text-container 닫기


    st.markdown("---")
    if st.button("다른 학생 정보 입력하기", use_container_width=True, key="go_back_to_input_btn"):
        # 세션 상태 초기화
        st.session_state.student_info_df = None
        st.session_state.form_input_original = None
        st.switch_page("pages/2_🧑‍🎓_학생_정보_입력.py")