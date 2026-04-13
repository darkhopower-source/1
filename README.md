# Multi-source Local Place Page Builder

정발산동 같은 지역 + 업종(예: 법률사무소) 키워드로
Google/Kakao/Naver API 데이터를 모아 병합하고 HTML 페이지를 자동 생성하는 예제입니다.

## 1) 설치

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`.env`에 API 키를 입력하세요.

## 2) 데이터 수집

```bash
python scripts/fetch_google.py --region 정발산동 --keyword 법률사무소
python scripts/fetch_kakao.py --region 정발산동 --keyword 법률사무소
python scripts/fetch_naver.py --region 정발산동 --keyword 법률사무소
```

## 3) 병합 + 페이지 생성

```bash
python scripts/merge_places.py --region 정발산동 --keyword 법률사무소
python scripts/build_pages.py --region 정발산동 --keyword 법률사무소
```

생성 결과: `output/정발산동_법률사무소.html`

## 4) 주의사항

- 각 API 제공사 약관/요금/쿼터를 확인하세요.
- 정보성 페이지라면 광고/제휴 링크 고지 문구를 명확히 표시하세요.
