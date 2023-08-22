# 상세페이지

from selenium import webdriver
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import re

# 특수문자 제거
def remove_special_characters(text):
    clean_text = re.sub(r'[^\w\s]', '', text)
    return clean_text

# 특정단어 제거
def remove_words_numbers(text):
    words_to_remove = ['모집', '참가', '합니다', '2023년', '공고', '공지']
    
    patterns_to_remove = ['제\d기', '제\d회', '\d기']

    for word in words_to_remove:
        text = text.replace(word, "")
    for pattern in patterns_to_remove:
        text = re.sub(pattern, '', text)
    text = re.sub(r'\d+', '', text)

    return text

def review(keyword='') : # 후기글 크롤링
    
    clean_txt_1 = remove_special_characters(keyword)
    clean_txt_2 = remove_words_numbers(clean_txt_1).strip()
    
    review_keyword = f'"{clean_txt_2} 후기"'

    baseUrl = 'https://www.google.com/search?q=' # 구글 링크
    plusUrl = quote_plus(review_keyword) # 검색어 링크
    url = baseUrl + plusUrl

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    driver = webdriver.Chrome(options=chrome_options) # 드라이버 시작
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
                
                if date:
                    text = text.replace(date, '')  # date를 text에서 제거
                    text = text.replace('—', '')
                    
                review_info = {
                    'title' : title,
                    'text' : text,
                    'date' : date,
                    'link' : link
                }
                result_list.append(review_info)
        driver.quit()
        return result_list
    
