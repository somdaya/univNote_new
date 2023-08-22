# 연합동아리 인기공고

from bs4 import BeautifulSoup
from selenium import webdriver

def best_club() : # 연합동아리 인기공고
    
    url = "https://www.campuspick.com/club"
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    driver = webdriver.Chrome(options=chrome_options) # 드라이버 시작
    
    driver.get(url) # 캠퍼스픽 사이트 가져오기
    driver.implicitly_wait(10) # 웹 페이지가 로딩될 떄까지 최대 10초 대기
    
    html = driver.page_source # 웹페이지의 소스코드 가져오기
    soup = BeautifulSoup(html, 'html.parser') # 파싱하기
    
    like_clubs = soup.select('div.items a.item') # 인기공고 부분 
    result_list = []

    for i, like_club in enumerate(like_clubs):
        
        if i == 4:  # 4개만 크롤링
            break   
        
        title = like_club.select_one('h3').text # 제목
        dday_element = like_club.select_one('p.info span.dday') # 디데이
        dday = dday_element.text.strip() if dday_element else 'No D-day' # 디데이
        if dday == '마감' : # 마감이면 안가져오기
            continue
        link = 'https://www.campuspick.com' + like_club['href']  # 링크
        image_url = like_club.select_one('figure')['data-image'] # 이미지 url 가져오기

        driver.get(link)
        detail_html = driver.page_source
        detail_soup = BeautifulSoup(detail_html, 'html.parser')
        name = detail_soup.select_one('h1').text
        
        like_club_info = {
            'name' : name,
            'title' : title,
            'dday' : dday,
            'link' : link,
            'image_url' : image_url,
        }
        
        result_list.append(like_club_info)
    driver.close() # 드라이버 닫기
    
    return result_list