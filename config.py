# config.py

import os

# ▶ Tesseract 실행 경로 (Windows 기준)
TESSERACT_PATH = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# ▶ ChromeDriver 자동 실행 설정
USE_WEBDRIVER_MANAGER = True  # True: 자동 다운로드 / False: 수동 경로 사용
CHROME_DRIVER_PATH = os.path.join("drivers", "chromedriver.exe")

# ▶ 쇼핑엔티몰 URL
BASE_URL = "https://www.shoppingntmall.com/"

# ▶ 금칙어 텍스트 파일 경로
PROHIBITED_WORDS_PATH = os.path.join("data", "prohibited_words.txt")

# ▶ 검사 완료된 URL 기록 저장 폴더
CHECKED_URLS_DIR = os.path.join("data", "checked_urls")

# ▶ OCR 실패 이미지 저장 경로
SCREENSHOTS_DIR = "screenshots"

# ▶ 금칙어 검출 결과 저장 폴더
RESULTS_DIR = "results"

# ▶ OCR 언어 설정 (한국어 + 영어 병용)
OCR_LANG = "kor+eng"
