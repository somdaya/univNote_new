# 더보기_연합동아리

from bs4 import BeautifulSoup
from selenium import webdriver
import time

def plus_club(start_index=0) : # 더보기_연합동아리 
    
    url = "https://www.campuspick.com/club" # 캠퍼스픽 ur
    l
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    driver = webdriver.Chrome(options=chrome_options) # 드라이버 시작
    
    driver.get(url) # 캠퍼스픽 사이트 가져오기
    driver.implicitly_wait(10) # 웹 페이지가 로딩될 떄까지 최대 10초 대기
    
    result_list = []
    scroll_count = 0
    max_scroll_count = 5
    
    while scroll_count < max_scroll_count :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 스크롤
        time.sleep(1)  # 스크롤 한번 하고 대기시간
        scroll_count += 1
    
    html = driver.page_source # 웹페이지의 소스코드 가져오기
    soup = BeautifulSoup(html, 'html.parser') # 파싱하기
    plus_club_list = soup.select('a.item') # 정보 있는 요소 가져오기
    
    if start_index >= len(plus_club_list) : # 20개씩 가져오기
        driver.close()
        return result_list

    for plus_club in plus_club_list[start_index : start_index+20] :
        
        title_element = plus_club.select_one('h2') # 제목
        if title_element : # 제목 있으면
            title = title_element.text # 제목 가져오기
        else : # 제목 없으면
            continue # 넘기기
        dday_element = plus_club.select_one('p.info span.dday') # 디데이
        dday = dday_element.text.strip() if dday_element else 'No D-day' # 디데이
        if dday == '마감' : # 마감이면 안가져오기
            continue
        link = 'https://www.campuspick.com' + plus_club['href']  # 링크
        image_url = plus_club.select_one('figure')['data-image'] # 이미지
        name = plus_club.select_one('p.profile').text
        
        plus_club_info = {
            'name' : name,
            'title' : title,
            'dday' : dday,
            'link' : link,
            'image_url' : image_url,
        }
        result_list.append(plus_club_info)

    driver.close() # 드라이버 닫기 
    
    return result_list