# simpleGals Showcase (simplegals.github.io)

One photo set, rendered three ways by [simpleGals](https://pypi.org/project/simplegals/):
a dark theme (stock), a bright inverse (forked CSS), and "retro-fruit", a 2010
Apple-style web gallery rebuilt as a custom template. A branded landing page ties
them together.

## Layout

- `shared/in/` the one photo set. The only binaries in git. Replace these with your
  own shots; nothing else changes.
- `galleries/<slug>/` one `simpleGal.json` per gallery; `in` symlinks to `shared/in`.
- `templates/` the landing (`index.html.j2`) plus the `bright` and `retro-fruit`
  template dirs.
- `site.json` landing configuration (title, tagline, hero, per-card badge/blurb).
- `build_index.py` renders the landing and assembles `_site/`.

## Build locally

    python -m venv .venv && .venv/bin/pip install "simplegals>=0.4.0"
    scripts/build_local.sh
    open _site/index.html

Derived `out/`, `.meta/`, and `_site/` are never committed; CI rebuilds them.

## Adding your photos

Drop images into `shared/in/`, optionally set each gallery's `cover` in its
`simpleGal.json` (the `dark` cover doubles as the site hero), and rebuild.
