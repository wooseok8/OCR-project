# 🛡️ OCR 기반 금칙어 검출 시스템

쇼핑엔티몰 상품 이미지에서 금칙어를 자동 탐지하고 결과를 CSV로 저장하는 Python 기반 OCR 자동화 시스템입니다.

---

## 📌 주요 기능

- 쇼핑엔티몰 전체 카테고리 순회
- 상품 상세 이미지에서 텍스트 추출 (Tesseract OCR)
- 금칙어 포함 여부 자동 판별
- 검출된 상품 결과 CSV 저장
- OCR 실패 이미지 저장
- 중복 검사 방지를 위한 URL 기록

---

## 🛠️ 설치 및 실행

### 1. 가상환경 구성 (Python 3.10 이상)

```bash
python -m venv venv
.\venv\Scripts\activate
2. 패키지 설치
bash
복사
편집
pip install -r requirements.txt
3. Tesseract 설치
Tesseract 다운로드 (UB Mannheim)

설치 시 한국어 언어팩(kor) 포함

설치 후 config.py에서 경로 설정:

python
복사
편집
TESSERACT_PATH = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
4. 실행
bash
복사
편집
python main.py
🗂️ 프로젝트 구조
bash
복사
편집
ocr_prohibited_checker/
├── data/
│   ├── prohibited_words.txt         # 금칙어 리스트
│   └── checked_urls/                # 중복 검사된 상품 기록
├── results/                         # 금칙어 포함 상품 CSV 저장
├── screenshots/                     # OCR 실패 이미지 저장
├── config.py                        # 설정 모듈
├── crawler.py                       # 크롤링 로직
├── ocr_utils.py                     # OCR 및 탐지 로직
├── main.py                          # 실행 메인 흐름
├── requirements.txt                 # 패키지 목록
└── README.md                        # 설명서
📄 결과 예시
🔹 data/prohibited_words.txt
txt
복사
편집
도박
성인용품
불법
무료나눔
위조
🔹 results/패션_20250626.csv
상품명	상품URL	이미지URL	OCR 텍스트	검출된 금칙어
예시 상품	https://...	https://...	...도박...	도박

🔹 data/checked_urls/패션.txt
arduino
복사
편집
https://www.shoppingntmall.com/product/1234
https://www.shoppingntmall.com/product/5678
⚠️ 참고사항
OCR 정확도는 이미지 품질에 따라 다릅니다.

금칙어는 **부분 포함(단순 문자열 포함)**으로 탐지합니다.

동일한 상품은 자동으로 건너뜁니다.

📜 라이선스
내부 자동화 시스템용 프로젝트입니다. 외부 상업적 사용 전 별도 협의 필요.

yaml
복사
편집

---

필요하시면 이걸 `.md` 파일로 저장하는 Python 스크립트도 바로 만들어드릴 수 있어요. 요청만 주세요!





