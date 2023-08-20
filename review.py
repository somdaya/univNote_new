# 상세페이지

from selenium import webdriver
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

def review() : # 후기글 크롤링
    
    keyword = input("후기를 검색할 활동을 입력하세요: ")
    
    review_keyword = f'"{keyword} 후기"' # 검색결과에 특정 검색어가 무조건 포함되게

    baseUrl = 'https://www.google.com/search?q=' # 구글 링크
    plusUrl = quote_plus(review_keyword) # 검색어 링크
    url = baseUrl + plusUrl

    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)

    html = driver.page_source # 웹페이지의 소스코드 가져오기
    soup = BeautifulSoup(html, 'html.parser') # 파싱하기
    result_list = []

    no_results_message = soup.select("div.card-section") # 검색결과 없을 때
    if no_results_message : # 검색결과가 없으면
        driver.quit() # 창 닫음
        return result_list # 빈 리스트 반환

    else : # 검색결과 있으면
        review_list = soup.select('div.MjjYud') # 검색결과가 제목, 링크 담고있는 요소 선택

        for review in review_list :
            
            title_element = review.select_one('h3.LC20lb.MBeuO.DKV0Md') # 제목 요소
            text_element = review.select_one('.VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc.lEBKkf') # 줄거리 요소
            date_element = review.select_one('span.MUxGbd.wuQ4Ob.WZ8Tjf span') # 작성날짜 요소
            link_element = review.select_one('a')['href'] # 링크 요소
            
            # 4개의 요소 중 null되는게 없으면
            if title_element == None or text_element == None or date_element == None or link_element == None :
                continue
            else :
                title = title_element.get_text(strip=True) if title_element else None # 제목
                text = text_element.get_text(strip=True) if text_element else None # 줄거리
                date = date_element.get_text(strip=True) if date_element else None # 작성날짜
                link = link_element # 링크
            
                review_info = {
                    'title' : title,
                    'text' : text,
                    'date' : date,
                    'link' : link
                }
                result_list.append(review_info)
        driver.quit()
        
        return result_list
    
