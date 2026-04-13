"""Build a simple HTML page from merged data."""
import argparse
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from common import DATA_DIR, ROOT, load_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True)
    parser.add_argument("--keyword", required=True)
    args = parser.parse_args()

    src = DATA_DIR / f"merged_{args.region}_{args.keyword}.json"
    places = load_json(src)

    env = Environment(
        loader=FileSystemLoader(str(ROOT / "templates")),
        autoescape=select_autoescape(["html", "xml"]),
    )
    tmpl = env.get_template("page.html.j2")

    html = tmpl.render(
        region=args.region,
        keyword=args.keyword,
        places=places,
        updated_at=date.today().isoformat(),
    )

    out = ROOT / "output" / f"{args.region}_{args.keyword}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
