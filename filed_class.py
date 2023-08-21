from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import random

# 머신러닝 모델 학습, return model
def title_class_traindata():
    df = pd.read_csv('C:/Users/이다솜/Desktop/sw/univNote_new/campuspick.csv', encoding='utf-8', dtype={'title':str, 'f':int}, header=0)
    titles = df.iloc[:, 0].tolist()
    fields = df.iloc[:, 1].tolist()
    
    titles_train, titles_test, fields_train, fields_test = train_test_split(titles, fields, test_size=0.2, random_state=42)
    
    vectorizer = TfidfVectorizer() 
    vectorizer.fit(titles_train)
    titles_train_vec = vectorizer.transform(titles_train)
    titles_test_vec = vectorizer.transform(titles_test)
    model = MultinomialNB()
    
    param_dist = {'alpha': [0.01, 0.1, 1, 10, 100]}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    random_search = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=5, scoring='accuracy', cv=cv, random_state=42)
    random_search.fit(titles_train_vec, fields_train)

    best_alpha = random_search.best_params_['alpha']
    # print("Best alpha value:", best_alpha)

    model.set_params(alpha=best_alpha)
    model.fit(titles_train_vec, fields_train)
    
    # fields_pred = model.predict(titles_test_vec)
    # report = classification_report(fields_test, fields_pred)
    # print("Classification Report:")
    # print(report)

    return vectorizer, model
    
# 사용자 학과의 분야 찾기, reuturn user_field_index
def close_major(your_major) :
    
  from difflib import get_close_matches

  major_list = ['건축공학과', '건축학과', '교통공학과', 
                '도시공학과', '토목공학과', '해양공학과', '환경공학과', 
                '기계공학과', '기계설계공학과', '미래자동차학과', '자동차공학과', 
                '전기공학과', '전자공학과', '제어계측공학과', '항공우주공학과', 
                '항공운항학과', '농생물학과', '동물자원학과', '원예학과', 
                '조경학과', '간호학과', '물리치료학과', '응급구조학과', 
                '임상병리학과', '재활치료학과', '치기공학과', '치위생학과', 
                '식품영양학과', '의류학과', '수의학과', ' 약학과', 
                '의예과', '치의예과', '한의예과', '대기과학과', 
                '물리학과', '생명과학과', '수학과', '지질학과', 
                '천문 학과', '통계학과', '화학과', '과학교육과', 
                '물리교육과', '생물교육과', '수학교육과', '지구과학교육과', 
                '화학교육과', '멀티미디어학과', '빅데이터학과', '산업공학과', 
                '소프트웨어학과', '융합학과', '인공지능학과', '정보보안 학과', 
                '정보통신공학과', '컴퓨터공학과', '생명공학과', '섬유공학과', 
                '식품공학과', '신소재공학과', '에너지자원 공학과', '재료공학과', 
                '화장품과학과', '화장품공학과', '경영학과', '경제학과', 
                '금융보험학과', '무역유통학과', '세무회계학과', '호텔관광경영학과', 
                '광고홍보학과', '언론정보학과', '정보미디어학과', '가정교육과', 
                '교육학과', '유아교육과', '초등교육과', '국제학과', 
                '법학과', '보건행정학과', '정치외교학과', '행정학과', 
                '사회복지학과', '사회학과', '심리학과', '아동학과', 
                '지리학과', '항공서비스학과', '국어국문학과', '노어노문학과', 
                '독어독문학과', '불어불문학과', '스페인어학과', '영어영문학과', 
                '일어일문학과', '중어중문학과', '통번역학과', '한문학과', 
                ' 고고학과', '문헌정보학과', '문화재보존학과', '문화콘텐츠학과',
                '사학과', '인류학과', '철학과', '국어교육과', ' 불어교육과',
                '사회교육과', '역사교육과', '영어교육과', '윤리교육과', 
                '지리교육과', '시각디자인학과', '산업디자인학과', '영상디자인학과',
                '패션디자인학과', '체육학과', '경호학과', '스포츠산업학과',
                '스포츠지도학과', '바둑학과', 'e스포츠학과', '피아노학과', 
                '성악학과', '작곡과', '아트앤멀티미디어작곡', '영화과',
                '뮤지컬과', '실용음악과', '공연예술학과', '무용과', 
                '실용무용과', '무도학과', '스포츠레저과', '연기과',
                '연극과', '영상학과', '모델과', '사진과',
                '광고사진영상학과', '사진영상학과', '만화과',
                '애니메이션과']
  n = 1 # 최대 문자 매칭 개수
  cutoff = 0.6 # 유사도 하한
  
  # 학과 분야
  zero_all = [
    '약학과', '의예과', '치의예과', '한의예과',
    '간호학과', '물리치료학과', '응급구조학과', '임상병리학과',
    '재활치료학과', '치기공학과', '치위생학과'
  ]
  one_humanities = [
    '고고학과', '문헌정보학과', '문화재보존학과', '문화컨텐츠학과',
    '사학과', '인류학과', '철학과', '국어교육과',
    '불어교육과', '사회교육과', '역사교육과', '영어교육과', 
    '윤리교육과', '지리교육과', '국어국문학과', '노어노문학과',
    '독어독문학과', '불어불문학과', '스페인어학과', '영어영문학과',
    '일어일문학과', '중어중문학과', '통번역학과', '한문학과',
    '교육학과', '유아교육과'
    ]
  two_socialscience = [
    '국제학과', '보건행정학과', '정치외교학과', '법학과',
    '행정학과', '사회복지학과', '사회학과', '심리학과',
    '아동학과', '지리학과', '항공서비스학과', '가정교육과',
    '초등교육과', '광고홍보학과', '언론정보학과', '정보미디어학과',
    '호텔관광경영학과'
  ]
  three_business = [
    '경영학과', '경제학과', '금융보험학과', '무역유통학과',
    '세무회계학과'
  ]
  four_engine = [
    '생명공학과', '섬유공학과', '신소재공학과', '에너지자원공학과',
    '재료공학과', '화장품공학과', '멀티미디어학과', '산업공학과',
    '소프트웨어학과', '융합학과', '인공지능학과', '정보보안학과',
    '정보통신공학과', '컴퓨터공학과', '기계공학과', '기계설비공학과',
    '미래자동차학과', '자동차공학과', '전기공학과', '전자공학과',
    '제어계측공학과', '항공우주공학과', '항공운항학과', '교통공학과',
    '도시공학과'
  ]
  five_naturalscience = [
    '식품공학과', '화장품과학과', '과학교육과', '물리교육과',
    '생물교육과', '수학교육과', '지구과학교육과', '화학교육과',
    '대기과학과', '통계학과', '화학과', '식품영양학과',
    '물리학과', '생명과학과', '수학과', '지질학과', 
    '천문학과', '농생물학과', '동물자원학과', '원예학과',
    '조경학과', '환경공학과', '해양공학과'
  ]
  six_architecture = [
    '건축공학과', '건축학과', '토목공하과'
  ]
  seven_art = [
    '의류학과', '시각디자인학과', '산업디자인학과', '영상디자인학과',
    '패션디자인학과', '체육학과', '경호학과', '스포츠산업학과',
    '스포츠지도학과', '바둑학과', 'e스포츠학과', '피아노학과', 
    '성악학과', '작곡과', '아트앤멀티미디어작곡', '영화과',
    '뮤지컬과', '실용음악과', '공연예술학과', '무용과', 
    '실용무용과', '무도학과', '스포츠레저과', '연기과',
    '연극과', '영상학과', '모델과', '사진과',
    '광고사진영상학과', '사진영상학과', '만화과',
    '애니메이션과'
  ]
  
  fields = [zero_all, one_humanities, two_socialscience, three_business,
              four_engine, five_naturalscience, six_architecture, seven_art]

  # 분야 번호 매기기
  field_list = {major: field_number for field_number, field in enumerate(fields) for major in field}

  # 유사한 학과 목록 조회
  close_majors = get_close_matches(your_major, major_list, n, cutoff)

  if close_majors:
      closest_major = close_majors[0]
      user_field_index = field_list.get(closest_major, -1)  # -1은 분야를 찾지 못한 경우를 나타냄
    #   print(f"가장 유사한 학과: {closest_major}")
    #   print(f"해당 학과의 분야 번호: {user_field_index}")
  else:
      user_field_index = 0
    #   print("유사한 학과를 찾을 수 없습니다.")
  
  return user_field_index

# 대외활동 크롤링, return activity_result_list 
def open_activity(start_index=0) :
    
    url = "https://www.campuspick.com/activity"
    driver = webdriver.Chrome() # 드라이버 시작, 시스템 환경변수에 경로 설정해서 경로 따로 지정 안함
    driver.get(url) # 캠퍼스픽 사이트 가져오기
    driver.implicitly_wait(10) # 웹 페이지가 로딩될 떄까지 최대 10초 대기
    
    activity_result_list = []
    scroll_count = 0
    max_scroll_count = 2
    
    while scroll_count < max_scroll_count :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 스크롤
        time.sleep(1)  # 스크롤 한번 하고 대기시간
        scroll_count += 1
    
    html = driver.page_source # 웹페이지의 소스코드 가져오기
    soup = BeautifulSoup(html, 'html.parser') # 파싱하기
    open_activity_list = soup.select('a.top') # 정보 있는 요소 가져오기
    
    if start_index >= len(open_activity_list) : # 10개씩 가져오기
        driver.close()
        return activity_result_list
    
    for open_activity in open_activity_list[start_index : start_index+20] :
        
        title = open_activity.select_one('h2').text # 제목
        dday_element = open_activity.select_one('p.info span.dday') # 디데이
        dday = dday_element.text.strip() if dday_element else 'No D-day' # 디데이
        if dday == '마감' : # 마감이면 안가져오기
            continue
        link = 'https://www.campuspick.com' + open_activity['href']  # 링크
        image_url = open_activity.select_one('figure')['data-image'] # 이미지
    
        open_activity_info = {
            'title' : title,
            'dday' : dday,
            'link' : link,
            'image_url' : image_url,
        }
        activity_result_list.append(open_activity_info)
    driver.close() # 드라이버 닫기
    
    return activity_result_list
    
# 공모전 크롤링, return contest_result_list
def open_contest(start_index=0) :
    
    url = "https://www.campuspick.com/contest"
    driver = webdriver.Chrome() # 드라이버 시작, 시스템 환경변수에 경로 설정해서 경로 따로 지정 안함
    driver.get(url) # 캠퍼스픽 사이트 가져오기
    driver.implicitly_wait(10) # 웹 페이지가 로딩될 떄까지 최대 10초 대기
    
    contest_result_list = []
    scroll_count = 0
    max_scroll_count = 2
    
    while scroll_count < max_scroll_count :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 스크롤
        time.sleep(1)  # 스크롤 한번 하고 대기시간
        scroll_count += 1
    
    html = driver.page_source # 웹페이지의 소스코드 가져오기
    soup = BeautifulSoup(html, 'html.parser') # 파싱하기
    open_contest_list = soup.select('a.top') # 정보 있는 요소 가져오기
    
    if start_index >= len(open_contest_list) : # 10개씩 가져오기
        driver.close()
        return contest_result_list
    
    for open_contest in open_contest_list[start_index : start_index+20] :
        
        title = open_contest.select_one('h2').text # 제목
        dday_element = open_contest.select_one('p.info span.dday') # 디데이
        dday = dday_element.text.strip() if dday_element else 'No D-day' # 디데이
        if dday == '마감' : # 마감이면 안가져오기
            continue
        link = 'https://www.campuspick.com' + open_contest['href']  # 링크
        image_url = open_contest.select_one('figure')['data-image'] # 이미지
    
        open_contest_info = {
            'title' : title,
            'dday' : dday,
            'link' : link,
            'image_url' : image_url,
        }
        contest_result_list.append(open_contest_info)
    driver.close() # 드라이버 닫기
    
    return contest_result_list

# 문자열 이모티콘 제거
def remove_special_characters(text):
    clean_text = re.sub(r'[^\w\s]', '', text)
    return clean_text


# 대외활동 크롤링 결과 제목 + 공모전 크롤링 결과 제목, return activity_contest_result_list
def activity_contest_result() :
    activity_result_list = open_activity()
    contest_result_list = open_contest()
    activity_contest_results = activity_result_list + contest_result_list
    
    return activity_contest_results

# 크롤링된 활동의 분야 예측, return title_field_index
def title_class_predict(vectorizer, model, activity_contest_results) :
    new_title_list = [remove_special_characters(item['title']) for item in activity_contest_results]
    new_list_vec = vectorizer.transform(new_title_list)
    title_field_index = model.predict(new_list_vec).tolist()
    
    return title_field_index


# 사용자의 분야와 활동 제목의 분야가 같은 활동만 가져오기
def get_matching_activities(activity_contest_results, your_major):
    matching_activities = []
    vectorizer, model = title_class_traindata()
    title_field_index = title_class_predict(vectorizer, model, activity_contest_results) 
    
    for i, item in enumerate(activity_contest_results):
        if title_field_index[i] == 0 or title_field_index[i] == your_major:
            matching_activities.append(item)
    
    random_matching_activities = random.sample(matching_activities, 5)
    # for j in random_matching_activities : 
    #     print(j)
            
    return random_matching_activities


# main함수
# activity_contest_results = activity_contest_result()
# your_major = input("당신의 전공을 입력하세요: ")
# your_major = close_major(your_major)
# random_matching_activities = get_matching_activities(activity_contest_results, your_major)
    
# 분야 인덱스
# 1. 인문  2. 사회과학  3. 경영  4. 공학  5. 자연과학  6. 건축  7. 예술  8. 전체
