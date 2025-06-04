import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
student_df_for_prediction = st.session_state.student_info_df # 저장된 DataFrame 사용

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
        st.balloons()
    else: # Dropout
        st.error("😥 중퇴 예상")

with col2:
    if prediction == 1:
        st.markdown("#### 🥳 훌륭한 학생입니다. GREAT!")
        st.markdown("이 학생은 학업을 성공적으로 마칠 가능성이 높습니다. 지속적인 격려와 관심을 보여주세요.")
    else:
        st.markdown("#### ⚠️ **상담이 필요한 학생입니다.**")
        st.markdown("이 학생은 학업 중도 포기 가능성이 있습니다. 선제적인 상담과 지원을 통해 학업을 지속할 수 있도록 도와주세요.")

st.subheader("중퇴 및 졸업 예측 확률")

labels = ['중퇴 확률', '졸업 확률']
values = [prob_dropout, prob_graduate]

fig = go.Figure([go.Bar(x=labels, y=values, marker_color=['crimson', 'lightseagreen'])])
fig.update_layout(
    title_text='예측 확률 시각화',
    yaxis_title="확률",
    height=400
)
fig.update_yaxes(range=[0, 1])
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
if st.button("다른 학생 정보로 새로 예측하기", use_container_width=True):
    # 세션 상태 초기화
    st.session_state.student_info_df = None
    st.session_state.prediction_proba = None
    st.session_state.prediction_class = None
    st.switch_page("pages/2_🧑‍🎓_학생_정보_입력.py")