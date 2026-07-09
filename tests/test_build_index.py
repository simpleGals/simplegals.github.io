import json

import pytest

import build_index


def _setup(root):
    (root / "templates").mkdir(parents=True)
    (root / "templates" / "index.html.j2").write_text(
        "TITLE={{ site.title }} HERO={{ hero }} VER={{ version }} "
        "{% for c in cards %}[{{ c.slug }}|{{ c.title }}|{{ c.badge }}|{{ c.image_count }}|{{ c.href }}|{{ c.cover_url }}]{% endfor %}",
        encoding="utf-8")
    (root / "site.json").write_text(json.dumps({
        "title": "Showcase", "tagline": "t", "pitch": "p", "chip": "c",
        "hero_gallery": "dark",
        "galleries": [{"slug": "dark", "badge": "stock template", "blurb": "b"}],
        "links": [],
    }), encoding="utf-8")
    g = root / "galleries" / "dark" / "out"
    g.mkdir(parents=True)
    (g / "gallery.json").write_text(json.dumps({
        "title": "Dark", "cover": "img-08_thumb.jpg", "cover_og": "img-08_og.jpg",
        "image_count": 36, "slug": "dark",
    }), encoding="utf-8")
    (g / "index.html").write_text("<html>dark</html>", encoding="utf-8")


def test_render_and_assemble(tmp_path):
    _setup(tmp_path)
    out = tmp_path / "_site"
    build_index.render(tmp_path, out)
    idx = (out / "index.html").read_text(encoding="utf-8")
    assert "TITLE=Showcase" in idx
    assert "HERO=dark/img-08_og.jpg" in idx
    assert "[dark|Dark|stock template|36|dark/index.html|dark/img-08_thumb.jpg]" in idx
    assert (out / "dark" / "index.html").exists()  # gallery out/ assembled into _site/<slug>/


def test_missing_manifest_fails_loudly(tmp_path):
    _setup(tmp_path)
    (tmp_path / "galleries" / "dark" / "out" / "gallery.json").unlink()
    with pytest.raises(SystemExit):
        build_index.render(tmp_path, tmp_path / "_site")
