# main.py

import os
import time
import csv
from selenium import webdriver
from config import RESULTS_DIR, CHECKED_URLS_DIR
from crawler import (
    get_driver,
    get_all_category_links,
    get_product_urls_from_page,
    get_image_urls_from_product
)
from ocr_utils import (
    extract_text_from_image_url,
    detect_prohibited_words,
    load_prohibited_words
)

# 금칙어 로딩
prohibited_words = load_prohibited_words()

# 결과 폴더 준비
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(CHECKED_URLS_DIR, exist_ok=True)

# Selenium 드라이버 시작
driver = webdriver.Chrome()
get_driver(driver)

# 전체 카테고리 수집
category_list = get_all_category_links(driver)

# 카테고리별 반복
for cate in category_list:
    cate_name = cate['name']
    cate_url = cate['url']
    print(f"\n==== [{cate_name}] 검사 시작 ====")

    # 검사한 URL 기록 파일 로드
    checked_file = os.path.join(CHECKED_URLS_DIR, f"{cate_name}.txt")
    if os.path.exists(checked_file):
        with open(checked_file, "r", encoding="utf-8") as f:
            checked_urls = set(line.strip() for line in f)
    else:
        checked_urls = set()

    results = []
    page = 1
    max_pages = 80
    prev_ids = set()

    # 페이지 반복
    while page <= max_pages:
        list_url = cate_url + (f"&page={page}" if page > 1 else "")
        product_urls = get_product_urls_from_page(driver, list_url)

        if not product_urls:
            print(f"{page}페이지에 상품 없음")
            break

        # 중복 체크용 ID 집합
        curr_ids = set(url.split("/goods/")[-1].split("?")[0] for url in product_urls)
        if curr_ids == prev_ids:
            print(f"{page}페이지부터 상품 ID 반복, 중단")
            break
        prev_ids = curr_ids.copy()

        print(f"== {cate_name} {page}페이지 상품 {len(product_urls)}개 검사 ==")

        for url in product_urls:
            if url in checked_urls:
                continue

            image_urls = get_image_urls_from_product(driver, url)

            for img_url in image_urls:
                text = extract_text_from_image_url(img_url)
                found = detect_prohibited_words(text, prohibited_words)

                if found:
                    result = {
                        "카테고리": cate_name,
                        "상품URL": url,
                        "이미지URL": img_url,
                        "문제텍스트": text.strip().replace('\n', ' '),
                        "금칙어": ','.join(found)
                    }
                    results.append(result)
                    print(f"  금칙어 발견: {found} | URL: {url}")

            checked_urls.add(url)

        page += 1

    # CSV 저장
    if results:
        csv_path = os.path.join(RESULTS_DIR, f"{cate_name}_result.csv")
        with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"[{cate_name}] CSV 저장 완료 ({len(results)}건)")

    # 검사 완료 URL 저장
    with open(checked_file, "w", encoding="utf-8") as f:
        for url in sorted(checked_urls):
            f.write(url + "\n")

driver.quit()
print("\n✅ 전체 카테고리 검사 완료!")