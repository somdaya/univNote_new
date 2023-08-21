# 공모전 인기공고

from bs4 import BeautifulSoup
from selenium import webdriver

def best_contest() : # 공모전 인기공고
    url = "https://www.campuspick.com/contest"
    driver = webdriver.Chrome() # 드라이버 시작, 시스템 환경변수에 경로 설정해서 경로 따로 지정 안함
    driver.get(url) # 캠퍼스픽 사이트 가져오기
    driver.implicitly_wait(10) # 웹 페이지가 로딩될 떄까지 최대 10초 대기
    
    html = driver.page_source # 웹페이지의 소스코드 가져오기
    soup = BeautifulSoup(html, 'html.parser') # 파싱하기
    
    like_contests = soup.select('div.items a.item') # 인기공고 부분
    result_list = []

    for i, like_contest in enumerate(like_contests):
        
        if i == 4:  # 4개만 크롤링
            break
        
        title = like_contest.select_one('h3').text # 제목
        dday_element = like_contest.select_one('p.info span.dday') # 디데이
        dday = dday_element.text.strip() if dday_element else 'No D-day' # 디데이
        if dday == '마감' : # 마감이면 안가져오기
            continue
        link = 'https://www.campuspick.com' + like_contest['href']  # 링크
        image_url = like_contest.select_one('figure')['data-image'] # 이미지 url 가져오기
        
        like_contest_info = {
            'title' : title,
            'dday' : dday,
            'link' : link,
            'image_url' : image_url,
        }
        
        result_list.append(like_contest_info) 
    driver.close() # 드라이버 닫기
    
    return result_list