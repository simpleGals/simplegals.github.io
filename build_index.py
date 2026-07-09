#!/usr/bin/env python3
"""Assemble the simpleGals Showcase.

Reads site.json and each gallery's out/gallery.json (never simpleGals output
naming directly), renders templates/index.html.j2, and writes a deployable
_site/ tree. Seed of a future meta-gallery tool.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

try:
    from simplegals import __version__ as SG_VERSION
except Exception:  # pragma: no cover - simplegals always present in CI/build
    SG_VERSION = ""

ROOT = Path(__file__).resolve().parent


def _load_gallery(root: Path, slug: str) -> dict:
    manifest = root / "galleries" / slug / "out" / "gallery.json"
    if not manifest.exists():
        raise SystemExit(f"missing manifest: {manifest} (build the gallery first)")
    return json.loads(manifest.read_text(encoding="utf-8"))


def _cards(root: Path, site: dict) -> list[dict]:
    cards = []
    for entry in site["galleries"]:
        slug = entry["slug"]
        g = _load_gallery(root, slug)
        cover = g.get("cover")
        cards.append({
            "slug": slug,
            "title": g.get("title", slug),
            "image_count": g.get("image_count", 0),
            "badge": entry["badge"],
            "blurb": entry["blurb"],
            "href": f"{slug}/index.html",
            "cover_url": f"{slug}/{cover}" if cover else None,
        })
    return cards


def _hero(root: Path, site: dict) -> str | None:
    slug = site.get("hero_gallery")
    if not slug:
        return None
    g = _load_gallery(root, slug)
    return f"{slug}/{g['cover_og']}" if g.get("cover_og") else None


def render(root: Path, out_dir: Path) -> None:
    site = json.loads((root / "site.json").read_text(encoding="utf-8"))
    cards = _cards(root, site)
    env = Environment(loader=FileSystemLoader(str(root / "templates")),
                      autoescape=select_autoescape(["html", "j2"]))
    html = env.get_template("index.html.j2").render(
        site=site, cards=cards, hero=_hero(root, site), version=SG_VERSION)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    for entry in site["galleries"]:
        slug = entry["slug"]
        shutil.copytree(root / "galleries" / slug / "out", out_dir / slug, dirs_exist_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the simpleGals Showcase into _site/")
    ap.add_argument("--out", default=str(ROOT / "_site"))
    args = ap.parse_args()
    render(ROOT, Path(args.out))
    print(f"Built site into {args.out}")


if __name__ == "__main__":
    main()
