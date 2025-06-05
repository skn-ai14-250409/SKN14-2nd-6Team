import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import json
import os
import base64
from io import BytesIO
from PIL import Image
import sys

# 프로젝트 루트 경로를 sys.path에 추가
current_dir_result = os.path.dirname(os.path.abspath(__file__))
project_root_result = os.path.dirname(current_dir_result)
if project_root_result not in sys.path:
    sys.path.append(project_root_result)

from utils import mappings

# --- 이미지 경로 설정 ---
IMG_DIR_RESULT_PAGE = os.path.join(project_root_result, "img")
LOGO_PATH_RESULT_PAGE = os.path.join(IMG_DIR_RESULT_PAGE, "logo.png")
USER_IMG_PATH_RESULT_PAGE = os.path.join(IMG_DIR_RESULT_PAGE, "user_img.png")
COURSE_AVG_JSON_PATH = os.path.join(project_root_result, "data", "course_averages.json")
DATASET_PATH_FOR_DIST_RESULT = os.path.join(project_root_result, "data", "dataset.csv")

st.set_page_config(
    page_title="PLAY DATA - 예측 결과",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS ---
st.markdown(
    """
    <style>
    /* ... (이전과 동일한 CSS 코드) ... */
    .reportview-container { background: #fff; max-width: 100%; overflow-x: hidden; }
    .main .block-container { padding-right: 100px; padding-left: 100px; padding-bottom: 50px; max-width: 100%;}
    .st-emotion-cache-ckbrp0 { padding-left: 100px !important; padding-right: 100px !important; }
    .st-emotion-cache-t1wise { padding-left: 100px !important; padding-right: 100px !important; }
    @media (min-width: calc(736px + 8rem)) {
        .main .block-container, .st-emotion-cache-ckbrp0, .st-emotion-cache-t1wise {
            padding-left: 120px !important; padding-right: 120px !important;
        }
    }
    .stApp > header { display: none; }
    .header-container { display: flex; justify-content: space-between; align-items: center; padding: 20px 100px; background-color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 100%; position: fixed; top: 0; left: 0; right: 0; z-index: 9999; }
    .logo-img { height: 30px; width: auto; }
    .nav-menu ul { list-style: none; margin: 0; padding: 0; display: flex; }
    .nav-menu li { margin-left: 30px; }
    .nav-menu a { text-decoration: none; color: #333; font-weight: bold; font-size: 16px; padding: 8px 12px; border-radius: 4px; transition: all 0.3s ease; }
    .nav-menu a:hover { color: #007bff; background-color: #f0f0f0; }

    .student-name-title-result { font-weight:bold; font-size:28px; margin-bottom:25px; color: #004080; text-align: center; padding-bottom:15px; border-bottom: 2px solid #004080;}

    .profile-section-container-result { display: flex; align-items: flex-start; gap: 30px; margin-bottom: 25px; padding: 20px; background-color: #f8f9fa; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.05);}
    .profile-image-area-result { flex-basis: 220px; flex-shrink: 0; text-align: center; }
    .profile-img-display-result { width:160px; height:160px; border-radius:50%; object-fit:cover; border: 4px solid #007bff; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom:10px;}
    .student-name-under-img-result { font-weight:bold; font-size:22px; color: #333; margin-top:5px;}

    .student-info-tables-container-result { flex-grow: 1; }
    .info-table-custom-result {width:100%; border-collapse:collapse; margin-bottom:0; font-size:15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-radius: 8px; overflow:hidden;}
    .info-table-custom-result th, .info-table-custom-result td {border:1px solid #e0e0e0; background:#ffffff; padding:10px 12px; text-align:left; }
    .info-table-custom-result th {background:#f0f2f5; font-weight:600; color: #495057;}
    .info-table-custom-result tr:nth-child(even) td { background-color: #f8f9fa; }

    .prediction-card-result { background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.08); margin-top: 15px;}
    .prediction-card-title-result { font-size: 1.4em; font-weight: bold; margin-bottom: 10px; color: #0055A4;}
    .highlight-text-dropout-result { color: crimson; font-size: 1.6em; font-weight: bold; }
    .highlight-text-graduate-result { color: mediumseagreen; font-size: 1.6em; font-weight: bold; }
    .advice-section-result { font-size: 1.0em; line-height: 1.6; color: #333; margin-top: 10px;}

    h3.analysis-title-result { color: #0055A4; font-size: 1.8em; margin-top: 40px; margin-bottom: 20px; border-bottom: 2px solid #0055A4; padding-bottom: 8px;}
    .stTabs [data-baseweb="tab-list"] { gap: 20px; background-color: #e9ecef; border-radius: 8px; padding: 6px;}
	.stTabs [data-baseweb="tab"] { height: 45px; background-color: transparent; border-radius: 6px; font-weight: 500; font-size: 1.1em; color: #495057;}
	.stTabs [aria-selected="true"] { background-color: #007bff; color: white;}
    .stButton>button {
        background-color: #007bff !important; color: white !important;
        border: none; padding: 10px 24px !important; border-radius: 5px !important;
        font-weight: bold; margin-top: 20px !important;
    }
    .stButton>button:hover { background-color: #0056b3 !important; }
    .distribution-plot-container { margin-top: 20px; padding: 15px; background-color: #fdfdfd; border-radius: 8px; border: 1px solid #e0e0e0;}
    </style>
    """,
    unsafe_allow_html=True
)


# --- 이미지 로드 및 Base64 인코딩 함수 ---
def image_to_base64_for_result(img_path):  # 함수 이름 충돌 방지를 위해 변경
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            buffered = BytesIO()
            img_format = "PNG" if img_path.lower().endswith(".png") else "JPEG"
            if img.format: img_format = img.format.upper()
            if img_format == 'JPEG' and img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(buffered, format=img_format)
            encoded_string = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/{img_format.lower()};base64,{encoded_string}"
        except Exception as e:
            print(f"Error encoding image {img_path}: {e}")
            return ""
    return ""


logo_data_uri_res = image_to_base64_for_result(LOGO_PATH_RESULT_PAGE)
user_img_data_uri_res = image_to_base64_for_result(USER_IMG_PATH_RESULT_PAGE)

# --- 헤더 렌더링 ---
if logo_data_uri_res:
    st.markdown(
        f"""
        <div class="header-container">
            <div class="logo">
                 <a href="/" target="_self">
                    <img src="{logo_data_uri_res}" class="logo-img" alt="PLAY DATA Logo">
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
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

# --- 데이터 및 모델 확인 ---
if 'model' not in st.session_state or st.session_state.model is None:
    st.error("모델 로딩 오류.")
    st.stop()
if 'student_info_df' not in st.session_state or st.session_state.student_info_df is None:
    st.warning("학생 정보가 없습니다. '학생 정보 입력' 페이지에서 정보를 먼저 입력해주세요.")
    if st.button("정보 입력 페이지로 돌아가기", key="redirect_to_input_form_res_page"):  # 키 추가
        st.switch_page("pages/input_form.py")
    st.stop()
if 'form_input_original' not in st.session_state or not st.session_state.form_input_original:
    st.warning("표시할 학생 원본 정보가 없습니다.")
    if st.button("정보 입력 페이지로 돌아가기", key="redirect_to_input_form_no_original_res_page"):  # 키 추가
        st.switch_page("pages/input_form.py")
    st.stop()

# 세션 상태에서 변수 가져오기 (일관된 변수명 사용)
model_loaded = st.session_state.model
student_df_for_prediction = st.session_state.student_info_df  # 이 변수를 일관되게 사용
student_original_labels = st.session_state.form_input_original
student_name_display = student_original_labels.get("Student Name", "정보 없음")

# --- 예측 수행 ---
try:
    probabilities = model_loaded.predict_proba(student_df_for_prediction)
    prediction = model_loaded.predict(student_df_for_prediction)[0]
    prob_dropout = probabilities[0, 0]
    prob_graduate = probabilities[0, 1]
except Exception as e:
    st.error(f"예측 실행 중 오류: {e}")
    st.stop()

# --- 학생 정보 및 예측 결과 표시 ---
st.markdown(f"<div class='student-name-title-result'>{student_name_display} 님의 학업 성취도 예측 결과</div>",
            unsafe_allow_html=True)

st.markdown("<div class='profile-section-container-result'>", unsafe_allow_html=True)
st.markdown("<div class='profile-image-area-result'>", unsafe_allow_html=True)
if user_img_data_uri_res:
    st.markdown(f'<img src="{user_img_data_uri_res}" class="profile-img-display-result" alt="User Image">',
                unsafe_allow_html=True)
else:
    st.markdown(
        f'<div class="profile-img-display-result" style="background:#e9ecef; display:flex; align-items:center; justify-content:center;"><span style="font-size:1.3em; color:#adb5bd;">No Img</span></div>',
        unsafe_allow_html=True)
st.markdown(f"<div class='student-name-under-img-result'>{student_name_display}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='student-info-tables-container-result'>", unsafe_allow_html=True)
table_html_content = '<table class="info-table-custom-result">'
display_keys_map_content = mappings.get_feature_details_for_display()
display_order_keys_content = [
    'Course', 'Age', 'Gender', 'Marital status', 'Previous qualification',
    "Mother's occupation", "Father's occupation", 'Daytime/evening attendance',
    'Displaced', 'Educational special needs', 'Debtor',
    'Tuition fees up to date', 'Scholarship holder',
    'Curricular units 1st sem (approved)', 'Curricular units 1st sem (grade)',
    'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)'
]
for i in range(0, len(display_order_keys_content), 2):
    table_html_content += "<tr>"
    key1 = display_order_keys_content[i]
    label1 = display_keys_map_content.get(key1, {"label": key1})["label"]
    value1 = student_original_labels.get(key1, 'N/A')
    if isinstance(value1, float): value1 = f"{value1:.2f}"
    table_html_content += f"<th>{label1}</th><td>{value1}</td>"
    if i + 1 < len(display_order_keys_content):
        key2 = display_order_keys_content[i + 1]
        label2 = display_keys_map_content.get(key2, {"label": key2})["label"]
        value2 = student_original_labels.get(key2, 'N/A')
        if isinstance(value2, float): value2 = f"{value2:.2f}"
        table_html_content += f"<th>{label2}</th><td>{value2}</td>"
    else:
        table_html_content += "<th></th><td></td>"
    table_html_content += "</tr>"
table_html_content += "</table>"
st.markdown(table_html_content, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='prediction-card-result'>", unsafe_allow_html=True)
st.markdown("<div class='prediction-card-title-result'>종합 예측 및 교사 조언</div>", unsafe_allow_html=True)
if prediction == 1:
    st.markdown(f"<p class='highlight-text-graduate'>🎓 졸업이 예상됩니다.</p>", unsafe_allow_html=True)
    if prob_graduate > prob_dropout and prob_graduate > 0.6:
        st.balloons()
        st.toast('🎉 훌륭한 학생입니다! 졸업 가능성이 매우 높습니다! 🎉', icon='🥳')
    advice_content = "이 학생은 학업을 성공적으로 마칠 가능성이 높습니다..."  # (이전과 동일한 조언 내용)
    if prob_graduate >= 0.75:
        advice_content = "👍 **매우 긍정적:** " + advice_content + " 추가적인 심화 학습 기회를 제공하는 것을 고려해보세요."
    elif prob_graduate >= 0.6:
        advice_content = "긍정적: " + advice_content
    else:
        advice_content = "주의 관찰: 졸업이 예상되지만, 안심하기는 이릅니다. 꾸준한 관심과 지원이 필요합니다."
    st.markdown(f"<div class='advice-section-result'>{advice_content}</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<p class='highlight-text-dropout'>😥 중퇴가 예상됩니다.</p>", unsafe_allow_html=True)
    advice_content = "이 학생은 학업 중도 포기 가능성이 있습니다..."  # (이전과 동일한 조언 내용)
    if prob_dropout >= 0.75:
        advice_content = "🚨 **긴급 상담 필요:** 중퇴 위험이 매우 높습니다. 즉각적인 개별 상담을 통해 어려움을 파악하고, 맞춤형 학습 지원 및 정서적 지원 방안을 마련해야 합니다."
    elif prob_dropout >= 0.6:
        advice_content = "⚠️ **주의 및 상담 권고:** " + advice_content
    else:
        advice_content = "관찰 필요: 중퇴가 예상되지만, 아직 변화의 여지가 있습니다. 학생의 강점을 격려하고 약점을 보완할 수 있도록 지원해주세요."
    st.markdown(f"<div class='advice-section-result'>{advice_content}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 상세 분석 탭 ---
st.markdown("<h3 class='analysis-title-result'>상세 분석 자료</h3>", unsafe_allow_html=True)
tab_proba, tab_grades, tab_factors = st.tabs(["📊 예측 확률 분포", "📚 학업 성취도 분석", "⚠️ 주요 영향 요인"])

with tab_proba:
    st.markdown("<h5>중퇴 및 졸업 예측 확률</h5>", unsafe_allow_html=True)
    fig_gauge_dropout = go.Figure(go.Indicator(
        mode="gauge+number", value=prob_dropout * 100,
        number={'suffix': "%", 'font': {'size': 40}},
        title={'text': "중퇴 가능성 지표", 'font': {'size': 20, 'color': '#333'}},
        gauge={'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
               'bar': {'color': "crimson" if prob_dropout * 100 > 70 else (
                   "orange" if prob_dropout * 100 > 40 else "mediumseagreen")},
               'bgcolor': "white", 'borderwidth': 2, 'bordercolor': "gray",
               'steps': [{'range': [0, 40], 'color': 'rgba(40, 167, 69, 0.15)'},
                         {'range': [40, 70], 'color': 'rgba(255, 193, 7, 0.15)'},
                         {'range': [70, 100], 'color': 'rgba(220, 53, 69, 0.15)'}],
               'threshold': {'line': {'color': "black", 'width': 3}, 'thickness': 0.8, 'value': prob_dropout * 100}}))
    fig_gauge_dropout.update_layout(height=280, margin={'t': 50, 'b': 30, 'l': 30, 'r': 30},
                                    paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_gauge_dropout, use_container_width=True)
    st.metric(label="🎓 졸업 확률", value=f"{prob_graduate:.1%}")

with tab_grades:
    st.markdown("<h5>학생 성적과 과정 평균 비교</h5>", unsafe_allow_html=True)
    # 여기서부터 변수명을 일관되게 수정합니다.
    current_student_course_code = str(student_df_for_prediction['Course'].iloc[0])
    current_student_grade_1st = student_df_for_prediction['Curricular units 1st sem (grade)'].iloc[0]
    current_student_grade_2nd = student_df_for_prediction['Curricular units 2nd sem (grade)'].iloc[0]
    current_student_avg_grade = (current_student_grade_1st + current_student_grade_2nd) / 2 if (
                                                                                                           current_student_grade_1st + current_student_grade_2nd) > 0 else 0.0


    @st.cache_data
    def load_course_averages_for_grades_tab():
        try:
            with open(COURSE_AVG_JSON_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None


    course_averages_data = load_course_averages_for_grades_tab()  # 변수명 단순화
    if course_averages_data:
        course_specific_averages = course_averages_data.get(current_student_course_code,
                                                            course_averages_data.get('overall'))
        if course_specific_averages:
            class_avg_1 = course_specific_averages.get('sem1_avg', 12.0)
            class_avg_2 = course_specific_averages.get('sem2_avg', 12.0)
            class_avg_o = course_specific_averages.get('annual_avg', 12.0)

            categories_plot = ['1학기 성적', '2학기 성적', '연 평균 성적']
            student_grades_for_plot = [current_student_grade_1st, current_student_grade_2nd, current_student_avg_grade]
            course_avg_for_plot = [class_avg_1, class_avg_2, class_avg_o]

            fig_grades = go.Figure()  # 변수명 단순화
            fig_grades.add_trace(go.Bar(name='해당 학생', x=categories_plot, y=student_grades_for_plot,
                                        marker_color='royalblue', text=[f"{g:.2f}" for g in student_grades_for_plot],
                                        textposition='outside', textfont_size=12))
            course_label_plot = mappings.course_map.get(int(current_student_course_code), current_student_course_code)
            fig_grades.add_trace(go.Bar(name=f"과정 '{course_label_plot}' 평균", x=categories_plot, y=course_avg_for_plot,
                                        marker_color='lightsalmon', text=[f"{g:.2f}" for g in course_avg_for_plot],
                                        textposition='outside', textfont_size=12))
            fig_grades.update_layout(
                barmode='group', yaxis_title="평균 성적", legend_title_text='구분', height=380,
                yaxis_range=[0, 20], legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=60, b=20),
                title_text="학기별 성적 비교", title_x=0.5
            )
            st.plotly_chart(fig_grades, use_container_width=True)

            st.markdown("<div class='distribution-plot-container'>", unsafe_allow_html=True)
            st.markdown("<h6>과정 내 학기별 성적 분포 (Box Plot)</h6>", unsafe_allow_html=True)
            st.markdown(
                "<p style='font-size:0.9em; color:grey;'>Box Plot은 과정 내 다른 학생들의 성적 분포와 현재 학생의 위치(붉은 별)를 보여줍니다.</p>",
                unsafe_allow_html=True)


            @st.cache_data
            def get_course_grade_distribution_result(course_code_str_param):
                try:
                    df_dist = pd.read_csv(DATASET_PATH_FOR_DIST_RESULT)
                    df_dist_sem1 = df_dist[(df_dist['Course'] == int(course_code_str_param)) & (
                                df_dist['Curricular units 1st sem (grade)'] > 0) & (
                                                       df_dist['Curricular units 1st sem (grade)'] <= 20)][
                        'Curricular units 1st sem (grade)']
                    df_dist_sem2 = df_dist[(df_dist['Course'] == int(course_code_str_param)) & (
                                df_dist['Curricular units 2nd sem (grade)'] > 0) & (
                                                       df_dist['Curricular units 2nd sem (grade)'] <= 20)][
                        'Curricular units 2nd sem (grade)']
                    return df_dist_sem1, df_dist_sem2
                except:
                    return pd.Series(dtype='float64'), pd.Series(dtype='float64')


            course_grades_sem1_dist, course_grades_sem2_dist = get_course_grade_distribution_result(
                current_student_course_code)  # 변수명 변경

            if not course_grades_sem1_dist.empty or not course_grades_sem2_dist.empty:
                fig_dist = go.Figure()  # 변수명 변경
                if not course_grades_sem1_dist.empty:
                    fig_dist.add_trace(go.Box(y=course_grades_sem1_dist, name='1학기 과정 분포', marker_color='lightblue',
                                              boxpoints='outliers'))
                    fig_dist.add_trace(go.Scatter(x=['1학기 과정 분포'], y=[current_student_grade_1st], mode='markers',
                                                  marker=dict(color='red', size=10, symbol='star'), name='학생 1학기 성적'))
                if not course_grades_sem2_dist.empty:
                    fig_dist.add_trace(go.Box(y=course_grades_sem2_dist, name='2학기 과정 분포', marker_color='lightcoral',
                                              boxpoints='outliers'))
                    fig_dist.add_trace(go.Scatter(x=['2학기 과정 분포'], y=[current_student_grade_2nd], mode='markers',
                                                  marker=dict(color='darkred', size=10, symbol='star'),
                                                  name='학생 2학기 성적'))
                fig_dist.update_layout(yaxis_title="성적", height=400, showlegend=True,
                                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                                       margin=dict(t=50))
                st.plotly_chart(fig_dist, use_container_width=True)
            else:
                st.info("해당 과정의 다른 학생 성적 데이터가 충분하지 않아 분포도를 표시할 수 없습니다.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("과정 평균 성적 정보를 찾을 수 없습니다 (성적 비교 그래프).")
    else:
        st.warning("과정별 평균 성적 데이터를 로드하지 못했습니다 (성적 비교 그래프).")

with tab_factors:
    st.markdown("<h5>예측에 영향을 미치는 주요 요인 (예시)</h5>", unsafe_allow_html=True)
    st.info("아래는 모델 예측에 영향을 미쳤을 수 있는 학생의 주요 특성입니다. 실제 모델은 더 복잡한 관계를 고려합니다.")
    factors_display = []  # 변수명 단순화
    # 원본 입력값 (한글 레이블)은 student_original_labels에서 가져옴
    if student_original_labels.get('Tuition fees up to date') == '아니오':
        factors_display.append(("🔴 등록금 미납", "등록금 미납은 중퇴 위험을 높일 수 있습니다."))
    if student_original_labels.get('Debtor') == '예':
        factors_display.append(("🔴 학자금 연체", "학자금 연체는 학업 지속에 부정적 영향을 줄 수 있습니다."))

    # 예측에 사용된 DataFrame (숫자값)에서 성적 정보 가져오기
    s1_approved = student_df_for_prediction['Curricular units 1st sem (approved)'].iloc[0]
    s1_grade = student_df_for_prediction['Curricular units 1st sem (grade)'].iloc[0]
    if s1_approved < 2 or s1_grade < 10.0:
        factors_display.append(("🟡 1학기 학업 부진", f"1학기 이수 학점({s1_approved}개) 또는 평균 성적({s1_grade:.2f}점)이 낮아 주의가 필요합니다."))

    if student_original_labels.get('Scholarship holder') == '수혜' and prediction == 1:  # 변수명 일관성
        factors_display.append(("🟢 장학금 수혜", "장학금 수혜는 학업 성취에 긍정적 요인입니다."))

    if not factors_display:
        st.write("현재 정보로는 특별히 강조되는 위험/긍정 요인이 명확하지 않습니다.")
    else:
        for factor_title, factor_desc in factors_display:
            with st.expander(factor_title):
                st.write(factor_desc)
    st.caption("이 분석은 일반적인 경향에 기반한 예시이며, 실제 모델은 더 많은 변수를 고려합니다.")

st.markdown("<hr style='margin-top:40px; margin-bottom:20px;'>", unsafe_allow_html=True)
if st.button("다른 학생 정보 입력", use_container_width=True, key="go_back_to_input_btn_result_final_v4"):
    st.session_state.student_info_df = None
    st.session_state.form_input_original = None
    st.switch_page("pages/input_form.py")