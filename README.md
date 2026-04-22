# Multi-source Local Place Page Builder

지역 + 업종(예: 정발산동 + 법률사무소) 데이터를 바탕으로
정보성 포스팅(절차/체크리스트/FAQ + 지역 업체 목록)을 자동 생성합니다.

## 1) 설치

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`.env`에 API 키를 입력하면 API 수집 파이프라인도 사용할 수 있습니다.

---

## 2) API 없이 포스팅 먼저 보기 (추천 시작점)

아래 명령 1개로 샘플 데이터 기반 포스팅을 생성할 수 있습니다.

```bash
python scripts/build_pages.py \
  --region 정발산동 \
  --keyword 법률사무소 \
  --input data/sample_정발산동_법률사무소.json
```

생성 결과:

- `output/정발산동_법률사무소.html`

미리보기:

```bash
python3 -m http.server 5500
# 브라우저에서 http://localhost:5500/output/정발산동_법률사무소.html
```

---

## 3) API 연동해서 실제 데이터 수집

```bash
python scripts/fetch_google.py --region 정발산동 --keyword 법률사무소
python scripts/fetch_kakao.py --region 정발산동 --keyword 법률사무소
python scripts/fetch_naver.py --region 정발산동 --keyword 법률사무소
```

병합 후 포스팅 생성:

```bash
python scripts/merge_places.py --region 정발산동 --keyword 법률사무소
python scripts/build_pages.py --region 정발산동 --keyword 법률사무소
```

---

## 4) 주의사항

- 각 API 제공사 약관/요금/쿼터를 확인하세요.
- 정보성 페이지라면 광고/제휴 링크 고지 문구를 명확히 표시하세요.
- 법률/의료/금융 주제는 결과 보장형 표현을 피하고, 사실 기반 안내 중심으로 작성하세요.
