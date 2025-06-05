import os
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import RandomizedSearchCV
import joblib
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# 📍 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # /train 상위
DATA_PATH = os.path.join(BASE_DIR, "data", "dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# ✅ 데이터 로드
df = pd.read_csv(DATA_PATH)

# ✅ 불필요한 컬럼 제거
drop_cols = [
    'Application mode', 'Application order', 'Nationality',
    "Mother's qualification", "Father's qualification", 'International',
    'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
    'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (without evaluations)',
    'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)',
    'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (without evaluations)',
    'Unemployment rate', 'Inflation rate', 'GDP'
]
df.drop(columns=drop_cols, inplace=True)

# ✅ 타겟 변수 매핑
df['Target'] = df['Target'].map({'Dropout': 0, 'Graduate': 1, 'Enrolled': 2})
df = df[df['Target'] != 2]  # Enrolled 제거

# ✅ 특성 및 타겟 분리
X = df.drop('Target', axis=1)
y = df['Target']

# ✅ 학습/검증/테스트 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42, stratify=y_train)

# ✅ 범주형 & 수치형 변수 지정
categorical_cols = [
    'Marital status', 'Course', 'Daytime/evening attendance',
    'Previous qualification', "Mother's occupation", "Father's occupation",
    'Displaced', 'Educational special needs', 'Debtor',
    'Tuition fees up to date', 'Gender', 'Scholarship holder'
]

numeric_cols = [
    'Age',
    'Curricular units 1st sem (approved)',
    'Curricular units 1st sem (grade)',
    'Curricular units 2nd sem (approved)',
    'Curricular units 2nd sem (grade)'
]

# ✅ 전처리 파이프라인
numeric_transformer = Pipeline([('scaler', StandardScaler())])
categorical_transformer = Pipeline([('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_cols),
    ('cat', categorical_transformer, categorical_cols)
]).set_output(transform='pandas')

# ✅ 전체 파이프라인
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression())
])

# ✅ 모델 후보 + 하이퍼파라미터
param_grid = [
    {
        'classifier': [LogisticRegression(max_iter=1000, random_state=42)],
        'classifier__C': [0.01, 0.1, 1, 10],
        'classifier__solver': ['liblinear', 'lbfgs'],
    },
    {
        'classifier': [SVC(probability=True, random_state=42)],
        'classifier__kernel': ['linear', 'rbf'],
        'classifier__C': [0.1, 1, 10],
    },
    {
        'classifier': [KNeighborsClassifier()],
        'classifier__n_neighbors': [3, 5, 7],
        'classifier__weights': ['uniform', 'distance'],
    },
    {
        'classifier': [RandomForestClassifier(random_state=42)],
        'classifier__n_estimators': [100, 200],
        'classifier__max_depth': [None, 10, 20],
    },
    {
        'classifier': [XGBClassifier(eval_metric='logloss', random_state=42, n_jobs=-1)],
        'classifier__n_estimators': [100, 200],
        'classifier__max_depth': [3, 5],
        'classifier__learning_rate': [0.05, 0.1],
    },
    {
        'classifier': [LGBMClassifier(random_state=42, verbose=-1, n_jobs=-1)],
        'classifier__n_estimators': [100, 200],
        'classifier__max_depth': [-1, 5, 10],
        'classifier__learning_rate': [0.01, 0.05, 0.1],
    },
    {
        'classifier': [CatBoostClassifier(verbose=0, random_state=42)],
        'classifier__iterations': [100, 200],
        'classifier__depth': [4, 6, 8],
        'classifier__learning_rate': [0.01, 0.05, 0.1],
    },
]

# ✅ RandomizedSearchCV 설정
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid_search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=param_grid,
    cv=cv,
    scoring='accuracy',
    n_jobs=-1,
    verbose=2
)

# ✅ 모델 학습
grid_search.fit(X_train, y_train)

# ✅ 결과 출력
print(f"\n✅ Best Validation Score: {grid_search.best_score_:.4f}")
print(f"✅ Best Params: {grid_search.best_params_}")

# ✅ 최종 검증 정확도
val_score = grid_search.score(X_val, y_val)
print(f"✅ Validation Accuracy: {val_score:.4f}")

# ✅ 최종 모델 저장 (전체 파이프라인)
best_model = grid_search.best_estimator_
joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.pkl"))

print(f"\n📁 전체 모델 파이프라인이 저장되었습니다: models/best_model.pkl")
