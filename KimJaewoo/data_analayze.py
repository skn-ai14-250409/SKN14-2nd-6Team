import pandas as pd
import numpy as np
import json  # JSON 파일로 저장하기 위해
import os
# 데이터셋 로드
df = pd.read_csv('data/dataset.csv')  # 실제 파일 경로로 수정

# Target 변환 (분석에 필요하면)
target_map = {'Dropout': 0, 'Graduate': 1, 'Enrolled': 2}
df['Target_Encoded'] = df['Target'].map(target_map)

# 유효한 성적만 필터링 (0점은 제외, 0~20점 사이)
df_valid_grades_sem1 = df[(df['Curricular units 1st sem (grade)'] > 0) & (df['Curricular units 1st sem (grade)'] <= 20)]
df_valid_grades_sem2 = df[(df['Curricular units 2nd sem (grade)'] > 0) & (df['Curricular units 2nd sem (grade)'] <= 20)]

# 과정(Course)별 1학기 평균 성적 계산
course_avg_sem1 = df_valid_grades_sem1.groupby('Course')['Curricular units 1st sem (grade)'].mean().round(2).to_dict()

# 과정(Course)별 2학기 평균 성적 계산
course_avg_sem2 = df_valid_grades_sem2.groupby('Course')['Curricular units 2nd sem (grade)'].mean().round(2).to_dict()

# 전체 과정에 대한 평균 (특정 과정 데이터가 없을 경우 대비)
overall_avg_sem1 = round(df_valid_grades_sem1['Curricular units 1st sem (grade)'].mean(),
                         2) if not df_valid_grades_sem1.empty else 12.0  # 기본값
overall_avg_sem2 = round(df_valid_grades_sem2['Curricular units 2nd sem (grade)'].mean(),
                         2) if not df_valid_grades_sem2.empty else 12.0  # 기본값

# 과정별 연평균 성적 계산을 위한 데이터 준비
course_annual_averages = {}
all_courses = df['Course'].unique()

for course_code in all_courses:
    grades_for_course_sem1 = df_valid_grades_sem1[df_valid_grades_sem1['Course'] == course_code][
        'Curricular units 1st sem (grade)']
    grades_for_course_sem2 = df_valid_grades_sem2[df_valid_grades_sem2['Course'] == course_code][
        'Curricular units 2nd sem (grade)']

    # 각 학생의 연평균 계산 (두 학기 성적이 모두 있는 경우)
    student_annual_grades = []
    # Course 코드가 같은 학생들의 1학기, 2학기 성적을 가져와서 학생별 연평균 계산
    # (더 정교한 매칭 로직이 필요할 수 있으나, 여기서는 과정별 전체 평균을 사용)
    # 여기서는 간단하게 각 학기 평균을 사용합니다.

    avg1 = course_avg_sem1.get(course_code, overall_avg_sem1)
    avg2 = course_avg_sem2.get(course_code, overall_avg_sem2)

    if avg1 > 0 and avg2 > 0:
        course_annual_averages[course_code] = round((avg1 + avg2) / 2, 2)
    elif avg1 > 0:
        course_annual_averages[course_code] = avg1
    elif avg2 > 0:
        course_annual_averages[course_code] = avg2
    else:  # 두 학기 모두 유효한 평균이 없는 경우
        course_annual_averages[course_code] = round((overall_avg_sem1 + overall_avg_sem2) / 2, 2)

# 최종적으로 사용할 딕셔너리 생성
# course_class_averages = {
#     course: {
#         'sem1_avg': course_avg_sem1.get(course, overall_avg_sem1),
#         'sem2_avg': course_avg_sem2.get(course, overall_avg_sem2),
#         'annual_avg': course_annual_averages.get(course, round((overall_avg_sem1 + overall_avg_sem2) / 2, 2))
#     }
#     for course in all_courses
# }

# 각 과정 ID를 문자열 키로 변경 (JSON 호환성)
course_class_averages_str_keys = {
    str(course): {
        'sem1_avg': course_avg_sem1.get(course, overall_avg_sem1),
        'sem2_avg': course_avg_sem2.get(course, overall_avg_sem2),
        'annual_avg': course_annual_averages.get(course, round((overall_avg_sem1 + overall_avg_sem2) / 2, 2))
    }
    for course in all_courses
}
# 전체 평균도 추가 (특정 Course 코드가 없을 경우 대비)
course_class_averages_str_keys['overall'] = {
    'sem1_avg': overall_avg_sem1,
    'sem2_avg': overall_avg_sem2,
    'annual_avg': round((overall_avg_sem1 + overall_avg_sem2) / 2, 2)
}

# 결과를 JSON 파일로 저장 (예: student_predictor/data/course_averages.json)
output_path = os.path.join('data', 'course_averages.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(course_class_averages_str_keys, f, ensure_ascii=False, indent=4)

print(f"과정별 평균 성적 데이터가 '{output_path}'에 저장되었습니다.")
# print(course_class_averages_str_keys)