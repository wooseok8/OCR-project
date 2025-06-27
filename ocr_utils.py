# ocr_utils.py

import requests
from PIL import Image
from io import BytesIO
import pytesseract
import os
from config import (
    TESSERACT_PATH,
    PROHIBITED_WORDS_PATH,
    SCREENSHOTS_DIR,
    OCR_LANG
)

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def load_prohibited_words():
    """금칙어 목록 불러오기"""
    with open(PROHIBITED_WORDS_PATH, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def extract_text_from_image_url(image_url):
    """이미지 URL에서 텍스트 추출 (메모리 상 처리)"""
    try:
        resp = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(resp.content))
        text = pytesseract.image_to_string(image, lang=OCR_LANG)
        return text
    except Exception as e:
        print(f"[OCR 실패] {image_url}: {e}")
        save_failed_image(image_url)
        return ""

def save_failed_image(image_url):
    """OCR 실패 이미지 저장 (디버깅용)"""
    try:
        resp = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(resp.content))
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        filename = os.path.join(SCREENSHOTS_DIR, os.path.basename(image_url).split("?")[0])
        image.save(filename)
    except Exception as e:
        print(f" > 실패 이미지 저장 실패: {e}")

def detect_prohibited_words(text, prohibited_words):
    """텍스트에서 금칙어 포함 여부 확인"""
    return [word for word in prohibited_words if word in text]
