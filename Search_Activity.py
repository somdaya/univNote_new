# 검색_대외활동

from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver

# 한번에 10개씩 가져오고, 다음 10개 가져올려면 start_index=10, 그 다음 10개 가져올려면 start_index=20 ---
def search_activity(keyword='',start_index=0) : # 대외활동 검색 함수
    
    baseUrl = 'https://www.campuspick.com/activity?keyword=' # 캠퍼스픽 링크
    plusUrl = quote_plus(keyword) # 검색어 링크
    url = baseUrl + plusUrl # 전체 링크
    
    # 크롬 드라이버
    driver = webdriver.Chrome() # 드라이버 시작, 시스템 환경변수에 경로 설정해서 경로 따로 지정 안함
    driver.get(url) # 캠퍼스픽 사이트 가져오기
    driver.implicitly_wait(10) # 웹 페이지가 로딩될 떄까지 최대 10초 대기

    html = driver.page_source # 웹페이지의 소스코드 가져오기
    soup = BeautifulSoup(html, 'html.parser') # 파싱하기
    search_activity_list = soup.select('a.top') # 검색결과가 제목, 링크 담고있는 요소 선택
    
    result_list = [] # 크롤링 결과 담을 리스트
    
    # 시작 인덱스가 리스트 범위를 벗어나면 함수 종료
    if start_index >= len(search_activity_list) :
        driver.close()
        return result_list
    
    for search_activity in search_activity_list[start_index : start_index+10] : # 10개씩 가져오기
        title = search_activity.select_one('h2').text # 제목 
        company = search_activity.select_one('p.company').text # 주최기관
        dday_element = search_activity.select_one('p.info span.dday') # 디데이
        dday = dday_element.text.strip() if dday_element else 'No D-day' # 디데이
        if dday == '마감' : # 마감이면 안가져오기
            continue
        link = 'https://www.campuspick.com' + search_activity['href'] # 링크
        image_url = search_activity.select_one('figure')['data-image'] # 이미지 url 가져오기
        
        search_activity_info = {
            'title' : title,
            'company' : company,
            'dday' : dday,
            'link' : link,
            'image_url' : image_url,
        }
        result_list.append(search_activity_info)
        
    driver.close() # 드라이버 닫기
    return result_list # 함수값 반환
