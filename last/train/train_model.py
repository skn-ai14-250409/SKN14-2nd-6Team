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

#  절대 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # /train 상위
DATA_PATH = os.path.join(BASE_DIR, "data", "dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

#  데이터 로드
df = pd.read_csv(DATA_PATH)

# 불필요한 컬럼(열) 삭제
df = df.drop(['Application mode'], axis=1)
df = df.drop(['Application order'], axis=1)
df = df.drop(['Nationality'], axis=1)
df = df.drop(['Mother\'s qualification'], axis=1)
df = df.drop(['Father\'s qualification'], axis=1)
df = df.drop(['International'], axis=1)
df = df.drop(['Curricular units 1st sem (credited)'], axis=1)
df = df.drop(['Curricular units 1st sem (enrolled)'], axis=1)
df = df.drop(['Curricular units 1st sem (evaluations)'], axis=1)
df = df.drop(['Curricular units 1st sem (without evaluations)'], axis=1)
df = df.drop(['Curricular units 2nd sem (credited)'], axis=1)
df = df.drop(['Curricular units 2nd sem (enrolled)'], axis=1)
df = df.drop(['Curricular units 2nd sem (evaluations)'], axis=1)
df = df.drop(['Curricular units 2nd sem (without evaluations)'], axis=1)
df = df.drop(['Unemployment rate'], axis=1)
df = df.drop(['Inflation rate'], axis=1)
df = df.drop(['GDP'], axis=1)

# 타겟 변수 매핑
df['Target'] = df['Target'].map({'Dropout': 0, 'Graduate': 1, 'Enrolled': 2})
df = df[df['Target'] != 2]  # Enrolled 제거

X = df.drop('Target', axis=1)
y = df['Target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42, stratify=y_train)

#%%
from sklearn.ensemble import RandomForestClassifier
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


# 범주형 변수 목록 (사용자 정의)
cat_cols = [
    'Marital status',
    'Course',
    'Daytime/evening attendance',
    'Previous qualification',
    "Mother's occupation",
    "Father's occupation",
    'Displaced',
    'Educational special needs',
    'Debtor',
    'Tuition fees up to date',
    'Gender',
    'Scholarship holder'
]

# 수치형 변수 목록 (cat_cols 제외한 나머지)

num_cols = [
    'Age',
    'Curricular units 1st sem (approved)',
    'Curricular units 1st sem (grade)',
    'Curricular units 2nd sem (approved)',
    'Curricular units 2nd sem (grade)'
]


# 전처리 파이프라인 정의
numeric_transformer = Pipeline([('scaler', StandardScaler())])

categorical_transformer = Pipeline([('onehot', OneHotEncoder(handle_unknown='ignore',sparse_output=False))])

preprocessor = ColumnTransformer([('num', numeric_transformer, num_cols),('cat', categorical_transformer, cat_cols)]).set_output(transform='pandas')

# 파이프라인 정의 (scaler 대신 preprocessor)
pipeline = Pipeline([('preprocessor', preprocessor),('classifier', LogisticRegression())])

param_grid = [
  # LogisticRegression
  {
        'classifier': [LogisticRegression(max_iter=1000, random_state=42)],
        'classifier__C': [0.01, 0.1, 1, 10],
        'classifier__solver': ['liblinear', 'lbfgs'],
    },
  # SVC
  {
        'classifier': [SVC(random_state=42)],
        'classifier__kernel': ['linear', 'rbf'],
        'classifier__C': [0.1, 1, 10],
    },
  # KNeighborsClassifier
  {
        'classifier': [KNeighborsClassifier()],
        'classifier__n_neighbors': [3, 5, 7],
        'classifier__weights': ['uniform', 'distance'],
    },

  # RandomForestClassifier (전처리 그대로 둬도 무방, 스케일링 영향 적음)
  {
        'classifier': [RandomForestClassifier(random_state=42)],
        'classifier__n_estimators': [100, 200, 300],
        'classifier__max_depth': [None, 10, 20],
    },
  # XGBClassifier
  {
        'classifier': [XGBClassifier(eval_metric='logloss', random_state=42, n_jobs=-1)],
        'classifier__n_estimators': [100, 200, 300, 500],
        'classifier__max_depth': [3, 5, 7, 9],
        'classifier__learning_rate': [0.05, 0.1, 0.2],
     },
  # LGBMClassifier
  {
        'classifier': [LGBMClassifier(random_state=42, n_jobs=-1, verbose=-1, feature_name='auto')],
        'classifier__n_estimators': [100, 200, 300, 400],
        'classifier__max_depth': [-1, 5, 10, 10],
        'classifier__num_leaves': [20, 31, 40, 50],
        'classifier__learning_rate': [0.01, 0.05, 0.1],
        'classifier__subsample': [0.7, 0.8, 0.9, 1.0],
        'classifier__colsample_bytree': [0.7, 0.8, 0.9, 1.0],
        'classifier__reg_alpha': [0, 0.1, 0.01],
        'classifier__reg_lambda': [0, 0.1, 0.01]
    },
  # CatBoostClassifier
  {
        'classifier': [CatBoostClassifier(verbose=0, random_state=42)],
        'classifier__iterations': [50, 100, 200, 500],
        'classifier__depth': [4, 6, 8 ,10],
        'classifier__learning_rate': [0.01, 0.05,  0.1],
    }
]


cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid_search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=param_grid,
    cv=cv,
    n_jobs=-1,
    verbose=2,
    scoring='f1'
)

grid_search.fit(X_train, y_train)

print(f"Best Validation Score: {grid_search.best_score_:.4f}")
print(f"Best Params: {grid_search.best_params_}")

val_score = grid_search.score(X_val, y_val)
print(f"Validation Accuracy with best params: {val_score:.4f}")


# 최종 모델 저장 (전체 파이프라인)
best_model = grid_search.best_estimator_
joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.pkl"))

print(f"\n전체 모델 파이프라인이 저장되었습니다: models/best_model.pkl")