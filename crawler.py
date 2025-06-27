import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_CATEGORY_NAME = "TV쇼핑/적립"  # 필요 시 여전히 단일 타겟 지정 가능

def get_driver(driver):
    """홈페이지 접속 후 Selenium 드라이버 반환"""
    driver.get("https://www.shoppingntmall.com/")
    time.sleep(2)
    return driver

def get_all_category_links(driver):
    """전체 카테고리 링크들을 수집"""
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    category_links = []

    for a in soup.select('a[href]'):
        text = a.get_text(strip=True)
        href = a['href']
        # 유효한 카테고리 링크만 필터링
        if '/category/g-list-cate/' in href and text and text != "전체 카테고리":
            abs_url = "https://www.shoppingntmall.com" + href if not href.startswith('http') else href
            # URL 뒤에 최신순 정렬 조건 추가
            if "ctgSort=" not in abs_url:
                abs_url += ("&" if "?" in abs_url else "?") + "ctgSort=newProductOrder"
            # 이름 정제 (파일명에 안전하게 사용 가능하도록)
            safe_name = re.sub(r'[\\/*?:"<>|]', "_", text)
            # 중복 제거
            if abs_url not in [c['url'] for c in category_links]:
                category_links.append({'name': safe_name, 'url': abs_url})

    return category_links

def get_category_url(driver):
    """단일 타겟 카테고리 URL (TV쇼핑/적립)만 반환"""
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for a in soup.find_all('a', href=True):
        if a.get_text(strip=True) == BASE_CATEGORY_NAME and '/category/g-list-cate/' in a['href']:
            url = a['href']
            if "ctgSort=" not in url:
                url += ("&" if "?" in url else "?") + "ctgSort=newProductOrder"
            return "https://www.shoppingntmall.com" + url
    return None

def get_product_urls_from_page(driver, list_url):
    """카테고리 리스트 페이지에서 상품 상세 페이지 URL 수집"""
    driver.get(list_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find_all('div', class_='prd-info')

    product_urls = []
    for item in items:
        link_tag = item.select_one('a[href]')
        if link_tag and link_tag.has_attr('href'):
            url = link_tag['href']
            if not url.startswith("http"):
                url = "https://www.shoppingntmall.com" + url
            product_urls.append(url)
    return product_urls

def get_image_urls_from_product(driver, product_url):
    """상품 상세페이지 iframe 내부의 이미지 URL 수집"""
    image_urls = []
    try:
        driver.get(product_url)
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "goodsDtExplImgIfr"))
        )
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        imgs = soup.find_all('img')
        for img in imgs:
            src = img.get('src')
            if src and src.startswith("http"):
                image_urls.append(src)
        driver.switch_to.default_content()
    except Exception as e:
        print(f"[상세페이지 파싱 오류] {product_url}: {e}")
    return image_urls
