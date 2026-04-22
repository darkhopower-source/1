"""Fetch places from Google Places Text Search API.
Usage:
  python scripts/fetch_google.py --region 정발산동 --keyword 법률사무소
"""
import argparse
import os
from urllib.parse import urlencode

import requests

from common import DATA_DIR, load_env_file, save_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True)
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    load_env_file()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit("GOOGLE_API_KEY가 필요합니다 (.env 참고)")

    query = f"{args.region} {args.keyword}"
    params = {"query": query, "key": api_key, "language": "ko"}
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?" + urlencode(params)
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    places = []
    for item in data.get("results", [])[: args.limit]:
        loc = item.get("geometry", {}).get("location", {})
        places.append(
            {
                "name": item.get("name"),
                "address": item.get("formatted_address"),
                "phone": None,
                "lat": loc.get("lat"),
                "lng": loc.get("lng"),
                "source": "google",
                "map_url": f"https://www.google.com/maps/search/?api=1&query={loc.get('lat')},{loc.get('lng')}" if loc else None,
            }
        )

    out = DATA_DIR / f"google_{args.region}_{args.keyword}.json"
    save_json(out, places)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
