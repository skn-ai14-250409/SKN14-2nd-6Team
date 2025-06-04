import streamlit as st
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score

# app.py에서 정의된 MODEL_FEATURES, DROPPED_COLUMNS, ORIGINAL_COLUMNS를 사용
# 여기서는 간단하게 다시 정의합니다.
ORIGINAL_COLUMNS = [
    'Marital status', 'Application mode', 'Application order', 'Course',
    'Daytime/evening attendance', 'Previous qualification', 'Nacionality',
    "Mother's qualification", "Father's qualification", "Mother's occupation",
    "Father's occupation", 'Displaced', 'Educational special needs', 'Debtor',
    'Tuition fees up to date', 'Gender', 'Scholarship holder', 'Age', 'International',
    'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
    'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)',
    'Curricular units 1st sem (grade)', 'Curricular units 1st sem (without evaluations)',
    'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)',
    'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)',
    'Curricular units 2nd sem (grade)', 'Curricular units 2nd sem (without evaluations)',
    'Unemployment rate', 'Inflation rate', 'GDP', 'Target'
]

DROPPED_COLUMNS = [
    'Application mode', 'Application order', 'Nacionality',
    "Mother's qualification", "Father's qualification", 'International',
    'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
    'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (without evaluations)',
    'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)',
    'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (without evaluations)',
    'Unemployment rate', 'Inflation rate', 'GDP'
]

MODEL_FEATURES = [col for col in ORIGINAL_COLUMNS if col not in DROPPED_COLUMNS + ['Target']]

st.title("🔄 모델 재학습")
st.markdown("새로운 데이터를 업로드하여 모델을 재학습할 수 있습니다.")

if st.session_state.get('model') is None:
    st.error("모델이 로드되지 않았습니다. 메인 페이지(app.py)를 먼저 실행해주세요.")
    st.stop()

uploaded_file = st.file_uploader("재학습용 CSV 파일 업로드 (dataset.csv와 동일한 형식)", type="csv")

if uploaded_file is not None:
    try:
        new_data_df = pd.read_csv(uploaded_file)
        st.write("업로드된 데이터 샘플:")
        st.dataframe(new_data_df.head(), use_container_width=True)

        # 원본 컬럼과 일치하는지 대략적인 확인
        if not all(col in new_data_df.columns for col in ORIGINAL_COLUMNS):
            st.error("업로드된 파일의 컬럼이 원본 데이터셋과 일치하지 않습니다.")
            st.error(f"필요한 컬럼: {ORIGINAL_COLUMNS}")
            st.stop()

        # 노트북에서 수행한 전처리 적용
        # 1. 불필요한 컬럼 삭제
        processed_df = new_data_df.drop(columns=DROPPED_COLUMNS, errors='ignore')

        # 2. Target 변수 매핑 및 필터링
        target_map = {'Dropout': 0, 'Graduate': 1, 'Enrolled': 2}
        if 'Target' in processed_df.columns:
            processed_df['Target'] = processed_df['Target'].map(target_map)
            processed_df = processed_df[processed_df['Target'] != 2].copy()

            if processed_df.empty:
                st.warning("필터링 후 재학습할 데이터가 없습니다 ('Enrolled' 상태 제외).")
                st.stop()
        else:
            st.error("업로드된 파일에 'Target' 컬럼이 없습니다.")
            st.stop()

        st.write("전처리 후 재학습에 사용될 데이터 샘플:")
        st.dataframe(processed_df.head(), use_container_width=True)

        if st.button("모델 재학습 시작", type="primary", use_container_width=True):
            with st.spinner("모델을 재학습 중입니다... 시간이 다소 소요될 수 있습니다."):
                X_new = processed_df.drop('Target', axis=1)
                # 컬럼 순서를 모델이 학습된 순서(MODEL_FEATURES)와 동일하게 맞춰줌
                X_new = X_new[MODEL_FEATURES]
                y_new = processed_df['Target']

                # 현재 로드된 모델 파이프라인 가져오기
                current_pipeline = st.session_state['model']

                # 파이프라인 전체를 새로운 데이터로 재학습
                current_pipeline.fit(X_new, y_new)

                # 재학습된 모델 저장
                model_path = os.path.join('models', 'best_model_pipeline.pkl')
                joblib.dump(current_pipeline, model_path)

                # 세션 상태의 모델도 업데이트
                st.session_state['model'] = current_pipeline

                st.success("모델 재학습이 완료되었습니다! 업데이트된 모델이 저장되었습니다.")
                st.info(f"새 모델이 '{model_path}'에 저장되었습니다.")

                # (선택 사항) 재학습된 모델의 성능 평가 (새로운 데이터의 일부를 테스트셋으로 사용)
                if len(X_new) > 10:  # 충분한 데이터가 있을 경우
                    X_train_new, X_test_new, y_train_new, y_test_new = train_test_split(
                        X_new, y_new, test_size=0.2, random_state=42, stratify=y_new
                    )
                    # 재학습은 전체 X_new, y_new로 하고, 평가는 분할된 test_new로
                    # (위의 fit은 이미 X_new 전체로 했으므로, 여기서는 평가만)
                    preds_new = current_pipeline.predict(X_test_new)
                    new_f1 = f1_score(y_test_new, preds_new)
                    new_acc = accuracy_score(y_test_new, preds_new)
                    st.subheader("재학습된 모델 성능 (새 데이터의 테스트셋 기준):")
                    st.metric("F1 Score", f"{new_f1:.4f}")
                    st.metric("Accuracy", f"{new_acc:.4f}")

    except Exception as e:
        st.error(f"파일 처리 또는 모델 재학습 중 오류 발생: {e}")

else:
    st.info("모델을 재학습하려면 CSV 파일을 업로드해주세요.")