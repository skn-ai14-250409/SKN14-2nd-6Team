import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import json
import os

# --- 페이지 상단: 가독성 위한 CSS 추가 (선택 사항) ---
st.markdown("""
<style>
    /* 전체적인 폰트 및 앱 배경 등 (필요시) */
    /* .stApp { background-color: #f0f2f6; } */

    /* 주요 제목 폰트 크기 및 색상 */
    h1 {
        color: #004080; /* 남색 계열 */
    }
    h2 {
        color: #0055A4; /* 약간 밝은 남색 */
        border-bottom: 2px solid #0055A4;
        padding-bottom: 5px;
    }
    h3 {
        color: #0077CC; /* 더 밝은 파란색 */
    }

    /* 정보 카드 스타일 */
    .info-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .info-card-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #333333;
        margin-bottom: 10px;
    }
    .highlight-dropout {
        color: crimson;
        font-weight: bold;
    }
    .highlight-graduate {
        color: lightseagreen;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)
# ----------------------------------------------------

st.header("📈 예측 결과 및 심층 분석")  # 헤더 텍스트 수정

# 모델 로드 확인 (기존 코드)
if 'model' not in st.session_state or st.session_state.model is None:
    st.error("모델 로딩에 실패했습니다. 메인 페이지(app.py)를 먼저 실행하거나, 모델 파일을 확인해주세요.")
    if st.button("메인 페이지로 돌아가기"):
        st.switch_page("app.py")
    st.stop()

# 학생 정보가 입력되었는지 확인 (기존 코드)
if 'student_info_df' not in st.session_state or st.session_state.student_info_df is None:
    st.warning("먼저 '학생 정보 입력' 페이지에서 정보를 입력하고 '예측 결과 보기' 버튼을 눌러주세요.")
    if st.button("정보 입력 페이지로 돌아가기"):
        st.switch_page("pages/2_🧑‍🎓_학생_정보_입력.py")
    st.stop()

model = st.session_state.model
student_df_for_prediction = st.session_state.student_info_df

st.subheader("📝 입력된 학생 정보 요약")
st.dataframe(student_df_for_prediction, use_container_width=True)

try:
    probabilities = model.predict_proba(student_df_for_prediction)
    prediction = model.predict(student_df_for_prediction)[0]
    prob_dropout = probabilities[0, 0]
    prob_graduate = probabilities[0, 1]
    st.session_state.prediction_proba = {'Dropout': prob_dropout, 'Graduate': prob_graduate}
    st.session_state.prediction_class = prediction
except Exception as e:
    st.error(f"예측 실행 중 오류가 발생했습니다: {e}")
    st.stop()

st.markdown("---")
st.subheader("🎯 예측 결과 요약")

# 정보 카드를 사용하여 결과 표시
col_pred1, col_pred2 = st.columns(2)

with col_pred1:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("<p class='info-card-title'>예상 학업 성취도</p>", unsafe_allow_html=True)
    if prediction == 1:
        st.markdown(f"## <span class='highlight-graduate'>🎓 졸업 예상</span>", unsafe_allow_html=True)
        if prob_graduate > prob_dropout and prob_graduate > 0.6:  # 졸업 확률이 더 높고 일정 수준 이상일 때만
            st.balloons()
            st.toast('🎉 훌륭한 학생입니다! 졸업 가능성이 매우 높습니다! 🎉', icon='🥳')
    else:
        st.markdown(f"## <span class='highlight-dropout'>😥 중퇴 예상</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pred2:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("<p class='info-card-title'>교사 조언</p>", unsafe_allow_html=True)
    if prediction == 1:
        if prob_graduate >= 0.75:
            st.success(
                "👍 **매우 긍정적:** 이 학생은 학업을 성공적으로 마칠 가능성이 매우 높습니다. 현재의 학습 태도와 성과를 유지하도록 격려하고, 추가적인 심화 학습 기회를 제공하는 것을 고려해보세요.")
        elif prob_graduate >= 0.6:
            st.info("긍정적: 졸업 가능성이 높습니다. 지속적인 관심과 격려가 학생의 성공적인 학업 마무리에 도움이 될 것입니다.")
        else:
            st.info("주의 관찰: 졸업이 예상되지만, 안심하기는 이릅니다. 꾸준한 관심과 지원이 필요합니다.")
    else:
        if prob_dropout >= 0.75:
            st.error("🚨 **긴급 상담 필요:** 중퇴 위험이 매우 높습니다. 즉각적인 개별 상담을 통해 어려움을 파악하고, 맞춤형 학습 지원 및 정서적 지원 방안을 마련해야 합니다.")
        elif prob_dropout >= 0.6:
            st.warning("⚠️ **주의 및 상담 권고:** 중퇴 가능성이 있습니다. 학생의 학업 상황 및 학교 생활에 어려움은 없는지 면밀히 관찰하고, 예방적 상담을 진행하는 것이 좋습니다.")
        else:
            st.warning("관찰 필요: 중퇴가 예상되지만, 아직 변화의 여지가 있습니다. 학생의 강점을 격려하고 약점을 보완할 수 있도록 지원해주세요.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📊 상세 예측 확률 및 성적 분석")

# 탭을 사용하여 정보 분리
tab1, tab2, tab3 = st.tabs(["확률 분포", "성적 비교", "주요 영향 요인 (예시)"])

with tab1:
    st.markdown("#### 중퇴 및 졸업 예측 확률")
    labels = ['중퇴 확률', '졸업 확률']
    values = [prob_dropout, prob_graduate]

    fig_proba = go.Figure()
    fig_proba.add_trace(go.Bar(
        y=['확률'], x=[values[0]], name=labels[0], orientation='h',
        marker=dict(color='crimson', line=dict(color='darkred', width=1)),
        text=[f"{values[0]:.1%}"], textposition='inside', insidetextanchor='middle'
    ))
    fig_proba.add_trace(go.Bar(
        y=['확률'], x=[values[1]], name=labels[1], orientation='h',
        marker=dict(color='lightseagreen', line=dict(color='darkgreen', width=1)),
        text=[f"{values[1]:.1%}"], textposition='inside', insidetextanchor='middle'
    ))
    fig_proba.update_layout(
        barmode='stack',
        title_text='예측 확률 분포',
        xaxis_title="확률",
        height=180,
        margin=dict(l=10, r=10, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(tickformat=".0%", range=[0, 1]),
        yaxis_visible=False,  # y축 레이블 숨기기
        paper_bgcolor='rgba(0,0,0,0)',  # 배경 투명
        plot_bgcolor='rgba(0,0,0,0)',  # 배경 투명
        font=dict(color="#333")
    )
    st.plotly_chart(fig_proba, use_container_width=True)

with tab2:
    st.markdown("#### 학생 성적과 과정 평균 비교")
    student_course_code = str(student_df_for_prediction['Course'].iloc[0])
    student_grade_1st = student_df_for_prediction['Curricular units 1st sem (grade)'].iloc[0]
    student_grade_2nd = student_df_for_prediction['Curricular units 2nd sem (grade)'].iloc[0]
    student_avg_grade = (student_grade_1st + student_grade_2nd) / 2 if (
                                                                                   student_grade_1st + student_grade_2nd) > 0 else 0.0


    @st.cache_data
    def load_course_averages_tab():
        json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'course_averages.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None  # 간단한 오류 처리


    course_averages_data = load_course_averages_tab()

    if course_averages_data:
        course_specific_averages = course_averages_data.get(student_course_code, course_averages_data.get('overall'))
        if course_specific_averages:
            class_avg_grade_1st = course_specific_averages.get('sem1_avg', 12.0)
            class_avg_grade_2nd = course_specific_averages.get('sem2_avg', 12.0)
            class_avg_overall = course_specific_averages.get('annual_avg', 12.0)

            grade_categories = ['1학기 성적', '2학기 성적', '연 평균 성적']
            student_grades = [student_grade_1st, student_grade_2nd, student_avg_grade]
            course_average_grades_for_plot = [class_avg_grade_1st, class_avg_grade_2nd, class_avg_overall]

            fig_grades = go.Figure()
            fig_grades.add_trace(go.Bar(name='해당 학생', x=grade_categories, y=student_grades,
                                        marker_color='royalblue', text=[f"{g:.2f}" for g in student_grades],
                                        textposition='outside'))  # 막대 바깥쪽에 텍스트 표시
            fig_grades.add_trace(go.Bar(
                name=f"과정 {student_course_code} 평균" if student_course_code in course_averages_data else "전체 과정 평균",
                x=grade_categories, y=course_average_grades_for_plot,
                marker_color='lightsalmon', text=[f"{g:.2f}" for g in course_average_grades_for_plot],
                textposition='outside'))
            fig_grades.update_layout(
                barmode='group',
                title_text='성적 비교',
                yaxis_title="평균 성적",
                legend_title_text='구분',
                height=400,
                yaxis_range=[0, 20]  # Y축 범위 0~20으로 고정
            )
            st.plotly_chart(fig_grades, use_container_width=True)
        else:
            st.warning("학생의 과정 코드에 대한 평균 성적 정보를 찾을 수 없습니다.")
    else:
        st.warning("과정별 평균 성적 데이터를 로드하지 못했습니다.")

with tab3:
    st.markdown("#### 중퇴/졸업 예측에 영향을 미치는 주요 요인 (예시)")
    st.info("""
    이 섹션은 모델의 예측에 어떤 학생 정보들이 중요하게 작용했는지 대략적으로 보여줍니다.
    실제로는 모델 해석 기법(SHAP, LIME 등)을 사용하여 더 정확한 요인 분석이 가능합니다.
    아래는 일반적인 경향성을 나타내는 예시입니다.
    """)

    # 예시: 학생의 특성 중 중요도가 높을 것으로 예상되는 몇 가지를 선택하여 표시
    # 실제 중요도는 모델 학습 결과(feature importances)를 봐야 함
    # 여기서는 입력된 값과 일반적인 경향을 바탕으로 메시지 구성

    # 간단한 규칙 기반으로 영향 요인 추론 (데모용)
    factors = []
    if student_df_for_prediction['Tuition fees up to date'].iloc[0] == 0:
        factors.append(("🔴 등록금 미납 여부", "등록금 미납은 중퇴 위험을 높이는 주요 요인 중 하나입니다."))
    if student_df_for_prediction['Debtor'].iloc[0] == 1:
        factors.append(("🔴 학자금 연체 여부", "학자금 연체 또한 학업 지속에 어려움을 줄 수 있습니다."))

    avg_approved_1st = student_df_for_prediction['Curricular units 1st sem (approved)'].iloc[0]
    avg_grade_1st = student_df_for_prediction['Curricular units 1st sem (grade)'].iloc[0]
    avg_approved_2nd = student_df_for_prediction['Curricular units 2nd sem (approved)'].iloc[0]
    avg_grade_2nd = student_df_for_prediction['Curricular units 2nd sem (grade)'].iloc[0]

    if avg_approved_1st < 3 or avg_grade_1st < 10.0:  # 예시 임계값
        factors.append(("🟡 1학기 학업 성취도",
                        f"1학기 합격 과목 수({avg_approved_1st}개) 또는 평균 성적({avg_grade_1st:.2f}점)이 낮은 편입니다. 이는 초기 적응의 어려움을 나타낼 수 있습니다."))
    if avg_approved_2nd < 3 or avg_grade_2nd < 10.0:
        factors.append(("🟡 2학기 학업 성취도",
                        f"2학기 합격 과목 수({avg_approved_2nd}개) 또는 평균 성적({avg_grade_2nd:.2f}점)이 낮은 편입니다. 학업 부진이 지속될 경우 주의가 필요합니다."))

    if student_df_for_prediction['Scholarship holder'].iloc[0] == 1 and prediction == 1:
        factors.append(("🟢 장학금 수혜", "장학금 수혜는 학업 지속에 긍정적인 영향을 미치는 경향이 있습니다."))
    elif student_df_for_prediction['Scholarship holder'].iloc[0] == 0 and prediction == 0:
        factors.append(("⚪️ 장학금 미수혜", "장학금 미수혜가 직접적인 원인은 아니지만, 경제적 부담을 고려할 수 있습니다."))

    if not factors:
        st.write("현재 입력된 정보에서는 특별히 두드러지는 위험/긍정 요인이 명확하지 않거나, 모델이 복합적인 요인을 고려했을 수 있습니다. 전반적인 예측 확률을 참고해주세요.")
    else:
        for factor_title, factor_desc in factors:
            with st.expander(factor_title):
                st.write(factor_desc)

    st.caption("주의: 위 분석은 단순화된 예시이며, 실제 모델은 더 많은 변수를 복합적으로 고려합니다. 정확한 요인 분석은 모델 해석 도구를 사용해야 합니다.")

st.markdown("---")
if st.button("다른 학생 정보로 새로 예측하기", use_container_width=True):
    st.session_state.student_info_df = None
    st.session_state.prediction_proba = None
    st.session_state.prediction_class = None
    st.switch_page("pages/2_🧑‍🎓_학생_정보_입력.py")