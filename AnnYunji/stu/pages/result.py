import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.model_loader import load_model
from utils import mappings

# 역매핑 함수
def reverse_map(value, map_dict):
    return {v: k for k, v in map_dict.items()}.get(value)

# 입력 확인
if "form_input" not in st.session_state:
    st.warning("입력된 정보가 없습니다. 먼저 입력 페이지에서 정보를 제출하세요.")
    st.stop()

form = st.session_state["form_input"]

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
    'Age': form['Age at enrollment'],  # train_model.py 기준 컬럼명
    'Curricular units 1st sem (approved)': form['Curricular units 1st sem (approved)'],
    'Curricular units 1st sem (grade)': form['Curricular units 1st sem (grade)'],
    'Curricular units 2nd sem (approved)': form['Curricular units 2nd sem (approved)'],
    'Curricular units 2nd sem (grade)': form['Curricular units 2nd sem (grade)']
}

# 예측
model = load_model()
input_df = pd.DataFrame([mapped_input])
graduation_prob = round(model.predict_proba(input_df)[0][1] * 100, 2)  # Graduate
dropout_prob = round(100 - graduation_prob, 2)

# ============================
# 1. 학생 정보 테이블
# ============================
st.title("📈 학생 예측 결과")
st.markdown(
    f"""
    <table style="width:100%; border:1px solid #ddd; border-collapse: collapse; table-layout: fixed;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding:8px; width:20%;">전공</th>
            <th style="width:20%;">입학 나이</th>
            <th style="width:20%;">성별</th>
            <th style="width:20%;">장학금</th>
            <th style="width:20%;">수업 형태</th>
        </tr>
        <tr>
            <td style="padding:8px;">{form['Course']}</td>
            <td>{form['Age at enrollment']}</td>
            <td>{form['Gender']}</td>
            <td>{form['Scholarship holder']}</td>
            <td>{form['Daytime/evening attendance']}</td>
        </tr>
        <tr style="background-color:#f2f2f2;">
            <th style="padding:8px;">이전 학력</th>
            <th>어머니 직업</th>
            <th>아버지 직업</th>
            <th>채무</th>
            <th>등록금 납부</th>
        </tr>
        <tr>
            <td style="padding:8px;">{form['Previous qualification']}</td>
            <td>{form["Mother's occupation"]}</td>
            <td>{form["Father's occupation"]}</td>
            <td>{form["Debtor"]}</td>
            <td>{form["Tuition fees up to date"]}</td>
        </tr>
    </table>
    """,
    unsafe_allow_html=True
)

# ============================
# 2. 위험 경고 메시지
# ============================
if graduation_prob < 50:
    st.error("❗ 자퇴 위험이 높습니다.")
elif graduation_prob < 75:
    st.warning("⚠️ 자퇴 가능성이 중간 수준입니다.")
else:
    st.success("🎉 졸업 가능성이 높습니다!")

# ============================
# 3. 졸업 확률 게이지 차트
# ============================
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=dropout_prob,
    number={'suffix': "%"},
    title={'text': "중퇴 가능성"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "#007ACC"},
        'steps': [
            {'range': [0, 50], 'color': "#f8d7da"},
            {'range': [50, 75], 'color': "#fff3cd"},
            {'range': [75, 100], 'color': "#d4edda"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': dropout_prob
        }
    }
))
fig.update_layout(margin=dict(l=40, r=40, t=40, b=40), height=300)
st.plotly_chart(fig, use_container_width=True)

# ============================
# 4. 요약 텍스트 출력
# ============================
col1, col2 = st.columns(2)
with col1:
    st.metric("🎓 졸업 가능성", f"{graduation_prob:.2f}%")
with col2:
    st.metric("⚠️ 중도 이탈 가능성", f"{dropout_prob:.2f}%")
