import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import json # JSON 파일 로드를 위해 추가
import os   # 파일 경로 처리를 위해 추가

st.header("📈 예측 결과")

# 모델 로드 확인
if 'model' not in st.session_state or st.session_state.model is None:
    st.error("모델 로딩에 실패했습니다. 메인 페이지(app.py)를 먼저 실행하거나, 모델 파일을 확인해주세요.")
    if st.button("메인 페이지로 돌아가기"):
        st.switch_page("app.py")
    st.stop()

# 학생 정보가 입력되었는지 확인
if 'student_info_df' not in st.session_state or st.session_state.student_info_df is None:
    st.warning("먼저 '학생 정보 입력' 페이지에서 정보를 입력하고 '예측 결과 보기' 버튼을 눌러주세요.")
    if st.button("정보 입력 페이지로 돌아가기"):
        st.switch_page("pages/2_🧑‍🎓_학생_정보_입력.py")
    st.stop()


model = st.session_state.model
student_df_for_prediction = st.session_state.student_info_df

st.subheader("입력된 학생 정보 요약")
st.dataframe(student_df_for_prediction, use_container_width=True)

try:
    # 예측 확률 및 클래스
    probabilities = model.predict_proba(student_df_for_prediction)
    prediction = model.predict(student_df_for_prediction)[0]

    # 클래스 0: Dropout, 클래스 1: Graduate
    prob_dropout = probabilities[0, 0]
    prob_graduate = probabilities[0, 1]

    st.session_state.prediction_proba = {'Dropout': prob_dropout, 'Graduate': prob_graduate}
    st.session_state.prediction_class = prediction

except Exception as e:
    st.error(f"예측 실행 중 오류가 발생했습니다: {e}")
    st.stop()


st.subheader("예측된 학업 성취도")

col1, col2 = st.columns([1, 2])

with col1:
    if prediction == 1: # Graduate
        st.success("🎓 졸업 예상")
        if prob_graduate > prob_dropout: # 졸업 가능성이 더 높을 때만
            st.balloons()
            st.toast('🎉 훌륭한 학생입니다! 졸업 가능성이 높습니다! 🎉', icon='🥳')
    else: # Dropout
        st.error("😥 중퇴 예상")

with col2:
    if prediction == 1:
        st.markdown("#### 🥳 훌륭한 학생입니다. GREAT!")
        st.markdown("이 학생은 학업을 성공적으로 마칠 가능성이 높습니다. 지속적인 격려와 관심을 보여주세요.")
    else:
        st.markdown("#### ⚠️ **상담이 필요한 학생입니다.**")
        st.markdown("이 학생은 학업 중도 포기 가능성이 있습니다. 선제적인 상담과 지원을 통해 학업을 지속할 수 있도록 도와주세요.")

st.markdown("---")
st.subheader("학업 성적 분석 (입력 학생 vs 과정 평균)")

# 입력된 학생의 1학기, 2학기 성적 및 과정 코드 가져오기
student_course_code = str(student_df_for_prediction['Course'].iloc[0]) # JSON 키와 맞추기 위해 문자열로
student_grade_1st = student_df_for_prediction['Curricular units 1st sem (grade)'].iloc[0]
student_grade_2nd = student_df_for_prediction['Curricular units 2nd sem (grade)'].iloc[0]
student_avg_grade = (student_grade_1st + student_grade_2nd) / 2 if (student_grade_1st + student_grade_2nd) > 0 else 0.0

# 과정별 평균 성적 데이터 로드 함수 (JSON 파일 사용)
@st.cache_data # JSON 파일 내용은 자주 바뀌지 않으므로 캐싱
def load_course_averages():
    # JSON 파일 경로 (app.py 또는 프로젝트 루트 기준으로 상대 경로 설정 필요)
    # 현재 스크립트(3_....py)는 pages 폴더 안에 있으므로, 상위 폴더로 이동 후 data 폴더로 접근
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'course_averages.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"과정별 평균 성적 파일({json_path})을 찾을 수 없습니다. `data_analayze.py`를 실행해주세요.")
        return None
    except json.JSONDecodeError:
        st.error(f"과정별 평균 성적 파일({json_path})의 JSON 형식이 올바르지 않습니다.")
        return None
    except Exception as e:
        st.error(f"과정별 평균 성적 파일 로드 중 오류: {e}")
        return None

course_averages_data = load_course_averages()

if course_averages_data:
    # 학생의 과정에 해당하는 평균 성적 가져오기
    # 해당 과정 코드가 JSON에 없으면 'overall' 평균 사용
    course_specific_averages = course_averages_data.get(student_course_code, course_averages_data.get('overall'))

    if course_specific_averages:
        class_avg_grade_1st = course_specific_averages.get('sem1_avg', 12.0) # 기본값
        class_avg_grade_2nd = course_specific_averages.get('sem2_avg', 12.0) # 기본값
        class_avg_overall = course_specific_averages.get('annual_avg', 12.0) # 기본값

        # 성적 비교 그래프 생성
        grade_categories = ['1학기 성적', '2학기 성적', '연 평균 성적']
        student_grades = [student_grade_1st, student_grade_2nd, student_avg_grade]
        course_average_grades_for_plot = [class_avg_grade_1st, class_avg_grade_2nd, class_avg_overall]

        fig_grades = go.Figure(data=[
            go.Bar(name='해당 학생', x=grade_categories, y=student_grades, marker_color='royalblue', text=[f"{g:.2f}" for g in student_grades], textposition='auto'),
            go.Bar(name=f"과정 {student_course_code} 평균" if student_course_code in course_averages_data else "전체 과정 평균",
                   x=grade_categories, y=course_average_grades_for_plot, marker_color='lightsalmon', text=[f"{g:.2f}" for g in course_average_grades_for_plot], textposition='auto')
        ])
        fig_grades.update_layout(
            barmode='group',
            title_text='학생 성적과 과정 평균 비교',
            yaxis_title="평균 성적",
            legend_title_text='구분',
            height=450
        )
        fig_grades.update_yaxes(range=[0, 20])
        st.plotly_chart(fig_grades, use_container_width=True)
    else:
        st.warning("학생의 과정 코드에 대한 평균 성적 정보를 찾을 수 없습니다 (overall 정보도 없음). 그래프를 표시할 수 없습니다.")
else:
    st.warning("과정별 평균 성적 데이터를 로드하지 못했습니다. 그래프를 표시할 수 없습니다.")


st.markdown("---")
st.subheader("중퇴 및 졸업 예측 확률") # 기존 통계 자료 (변경 없음)

labels = ['중퇴 확률', '졸업 확률']
values = [prob_dropout, prob_graduate]

fig_proba = go.Figure()
fig_proba.add_trace(go.Bar(
    y=['확률'],
    x=[values[0]],
    name=labels[0],
    orientation='h',
    marker=dict(color='rgba(255, 0, 0, 0.6)'),
    text=[f"{values[0]:.2%}"], textposition='inside'
))
fig_proba.add_trace(go.Bar(
    y=['확률'],
    x=[values[1]],
    name=labels[1],
    orientation='h',
    marker=dict(color='rgba(0, 128, 0, 0.6)'),
    text=[f"{values[1]:.2%}"], textposition='inside'
))

fig_proba.update_layout(
    barmode='stack',
    title_text='중퇴 및 졸업 예측 확률',
    xaxis_title="확률",
    yaxis_title="",
    height=200,
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(tickformat=".0%")
)
st.plotly_chart(fig_proba, use_container_width=True)

st.markdown("---")
if st.button("다른 학생 정보로 새로 예측하기", use_container_width=True):
    # 세션 상태 초기화
    st.session_state.student_info_df = None
    st.session_state.prediction_proba = None
    st.session_state.prediction_class = None
    st.switch_page("pages/2_🧑‍🎓_학생_정보_입력.py")