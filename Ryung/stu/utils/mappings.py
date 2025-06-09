# mappings.py

marital_status_map = {
    1: '미혼', 2: '기혼', 3: '사별', 4: '이혼', 5: '사실혼', 6: '법적 분리'
}

course_map = {
    1: '바이오연료생산기술', 2: '애니메이션 및 멀티미디어 디자인', 3: '사회복지학(야간)',
    4: '농업학', 5: '커뮤니케이션 디자인', 6: '수의간호학', 7: '정보공학', 8: '말산업학',
    9: '경영학', 10: '사회복지학', 11: '관광학', 12: '간호학', 13: '구강위생학',
    14: '광고 및 마케팅 경영학', 15: '언론 및 커뮤니케이션', 16: '기초교육학', 17: '경영학(야간)'
}

previous_qualification_map = {
    1: '고졸', 2: '학사', 3: '학위', 4: '석사', 5: '박사',
    6: '대학 수강', 7: '12학년 미이수', 8: '11학년 미이수', 9: '11학년 기타',
    10: '10학년', 11: '10학년 미이수', 12: '기초 3주기', 13: '기초 2주기',
    14: '기술 전문', 15: '학위(1주기)', 16: '전문기술과정', 17: '석사(2주기)'
}

occupation_map = { # 수정
    1: '학생',
    2: '입법/행정 임원',
    3: '지적/과학 전문가',
    4: '중간 기술자',
    5: '행정직',
    6: '서비스/보안/판매',
    7: '농업/어업/임업',
    8: '산업/건설/장인',
    9: '기계조작/조립',
    10: '비숙련 노동자',
    11: '군 전문가',
    12: '기타',
    14: '장교',
    15: '육군 중사',
    16: '기타 군인',
    17: '행정/상업 서비스 책임자',
    18: '호텔/케이터링/무역 서비스 책임자',
    19: '물리/수학/공학 전문가',
    20: '보건 전문가',
    21: '교사',
    22: '재무/회계/행정 전문가',
    23: '중급 이공계 기술자',
    24: '중급 보건 기술자',
    25: '법률/사회/문화 중급 기술자',
    26: '정보통신 기술자',
    27: '사무/비서/데이터 처리',
    28: '회계/통계/금융 서비스 종사자',
    29: '기타 관리지원직',
    30: '개인 서비스 종사자',
    31: '판매자',
    32: '개인 의료 종사자',
    33: '보호/보안 서비스 담당자',
    34: '숙련 농업/축산 생산자',
    35: '자급자족형 농부/어부/수렵인',
    36: '숙련 건설 노동자',
    37: '금속가공 숙련 노동자',
    38: '전기/전자 숙련 노동자',
    39: '식품/목공/의류 등 숙련자',
    40: '공장/기계 조작원',
    41: '조립 작업자',
    42: '차량/이동 장비 운전자',
    43: '농림어업 비숙련 노동자',
    44: '건설/제조/운송 비숙련 노동자',
    45: '조리 보조원',
    46: '거리 판매 및 서비스 제공자'
}

yes_no_map = {0: '아니오', 1: '예'}
gender_map = {0: '여성', 1: '남성'}
attendance_map = {0: '야간', 1: '주간'}
scholarship_holder_map = {0: '미수혜', 1: '수혜'}

target_map = {0: '중퇴', 1: '졸업'}

# Reverse mappings for converting from Korean text to numeric values
marital_status_map_reverse = {v: k for k, v in marital_status_map.items()}
course_map_reverse = {v: k for k, v in course_map.items()}
previous_qualification_map_reverse = {v: k for k, v in previous_qualification_map.items()}
occupation_map_reverse = {v: k for k, v in occupation_map.items()}
yes_no_map_reverse = {v: k for k, v in yes_no_map.items()}
gender_map_reverse = {v: k for k, v in gender_map.items()}
attendance_map_reverse = {v: k for k, v in attendance_map.items()}
scholarship_holder_map_reverse = {v: k for k, v in scholarship_holder_map.items()}

