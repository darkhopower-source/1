"""Fetch places from Kakao Local API."""
import argparse
import os

import requests

from common import DATA_DIR, load_env_file, save_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True)
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--limit", type=int, default=15)
    args = parser.parse_args()

    load_env_file()
    key = os.getenv("KAKAO_REST_API_KEY")
    if not key:
        raise SystemExit("KAKAO_REST_API_KEY가 필요합니다 (.env 참고)")

    query = f"{args.region} {args.keyword}"
    resp = requests.get(
        "https://dapi.kakao.com/v2/local/search/keyword.json",
        headers={"Authorization": f"KakaoAK {key}"},
        params={"query": query, "size": args.limit},
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()

    places = []
    for d in data.get("documents", []):
        places.append(
            {
                "name": d.get("place_name"),
                "address": d.get("road_address_name") or d.get("address_name"),
                "phone": d.get("phone") or None,
                "lat": float(d["y"]) if d.get("y") else None,
                "lng": float(d["x"]) if d.get("x") else None,
                "source": "kakao",
                "map_url": d.get("place_url"),
            }
        )

    out = DATA_DIR / f"kakao_{args.region}_{args.keyword}.json"
    save_json(out, places)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
