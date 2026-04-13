"""Fetch places from Naver Local Search API."""
import argparse
import os

import requests

from common import DATA_DIR, load_env_file, save_json


def strip_html(text: str | None) -> str | None:
    if not text:
        return text
    return text.replace("<b>", "").replace("</b>", "")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True)
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    load_env_file()
    cid = os.getenv("NAVER_CLIENT_ID")
    secret = os.getenv("NAVER_CLIENT_SECRET")
    if not cid or not secret:
        raise SystemExit("NAVER_CLIENT_ID / NAVER_CLIENT_SECRET가 필요합니다 (.env 참고)")

    query = f"{args.region} {args.keyword}"
    resp = requests.get(
        "https://openapi.naver.com/v1/search/local.json",
        headers={"X-Naver-Client-Id": cid, "X-Naver-Client-Secret": secret},
        params={"query": query, "display": args.limit, "sort": "random"},
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()

    places = []
    for it in data.get("items", []):
        places.append(
            {
                "name": strip_html(it.get("title")),
                "address": it.get("roadAddress") or it.get("address"),
                "phone": it.get("telephone") or None,
                "lat": None,
                "lng": None,
                "source": "naver",
                "map_url": it.get("link") or None,
            }
        )

    out = DATA_DIR / f"naver_{args.region}_{args.keyword}.json"
    save_json(out, places)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
