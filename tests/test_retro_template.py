from pathlib import Path

from simplegals.core.config import Layout, ProjectConfig
from simplegals.core.template import render_gallery

RETRO = Path(__file__).resolve().parent.parent / "templates" / "retro-fruit"


def _records(out, names):
    out.mkdir(parents=True, exist_ok=True)
    recs = []
    for n in names:
        stem = Path(n).stem
        (out / n).write_bytes(b"X")
        (out / f"{stem}_thumb.jpg").write_bytes(b"X")
        recs.append({
            "filename": n, "output_path": n, "thumb_path": f"{stem}_thumb.jpg",
            "display_path": n, "caption": "", "alt": "", "include": True,
            "date": "2026-01-01", "size": "1 MiB", "og_path": None, "exif": None,
            "item_page": f"{stem}_item.html",
        })
    return recs


def test_retro_renders_assets_grid_and_position(tmp_path):
    out = tmp_path / "out"
    cfg = ProjectConfig(title="Retro-fruit", layout=Layout(columns=3, rows=10),
                        template=str(RETRO), social_previews=False, exif_display=False)
    render_gallery(out, cfg, _records(out, [f"{i}.jpg" for i in range(1, 4)]))
    # assets copied by 0.4.0
    assert (out / "assets" / "button_gradient.png").exists()
    assert (out / "assets" / "previous0.png").exists()
    # grid page: image count in the nav bar, thumbnails linked
    grid = (out / "index.html").read_text(encoding="utf-8")
    assert "3&nbsp;images" in grid
    assert 'href="1_item.html"' in grid
    # first item: prev disabled, next enabled, position line
    item = (out / "1_item.html").read_text(encoding="utf-8")
    assert "assets/previous0.png" in item
    assert "assets/next1.png" in item
    assert "Page: 1 of 3 (33%)" in item
    # last item: next disabled
    last = (out / "3_item.html").read_text(encoding="utf-8")
    assert "assets/next0.png" in last
    assert "Page: 3 of 3 (100%)" in last
