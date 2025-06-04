import joblib
import os

def load_model(model_path='models/best_model.pkl'):
    model = joblib.load(model_path)
    return model

# models/best_model.pkl 경로(기본값)에 저장되어 있는 학습된 머신러닝 모델을 메모리로 불러와서,
# 이 모델을 다른 코드(예: result.py)에서 예측(predict 또는 predict_proba)에 사용할 수 있도록 준비하는 역할