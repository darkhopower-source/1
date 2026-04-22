"""Merge place lists from google/kakao/naver by normalized name+address."""
import argparse
import re
from collections import defaultdict

from common import DATA_DIR, load_json, save_json


def norm(s: str | None) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", "", s).lower()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True)
    parser.add_argument("--keyword", required=True)
    args = parser.parse_args()

    files = [
        DATA_DIR / f"google_{args.region}_{args.keyword}.json",
        DATA_DIR / f"kakao_{args.region}_{args.keyword}.json",
        DATA_DIR / f"naver_{args.region}_{args.keyword}.json",
    ]

    merged = {}
    sources = defaultdict(set)

    for f in files:
        if not f.exists():
            continue
        for p in load_json(f):
            key = f"{norm(p.get('name'))}|{norm(p.get('address'))}"
            if key not in merged:
                merged[key] = {
                    "name": p.get("name"),
                    "address": p.get("address"),
                    "phone": p.get("phone"),
                    "lat": p.get("lat"),
                    "lng": p.get("lng"),
                    "map_url": p.get("map_url"),
                }
            else:
                for field in ["phone", "lat", "lng", "map_url"]:
                    if not merged[key].get(field) and p.get(field):
                        merged[key][field] = p[field]
            sources[key].add(p.get("source"))

    result = []
    for key, item in merged.items():
        item["sources"] = sorted(s for s in sources[key] if s)
        item["confidence"] = len(item["sources"])
        result.append(item)

    result.sort(key=lambda x: (-x["confidence"], x.get("name") or ""))
    out = DATA_DIR / f"merged_{args.region}_{args.keyword}.json"
    save_json(out, result)
    print(f"saved: {out} ({len(result)} places)")


if __name__ == "__main__":
    main()
