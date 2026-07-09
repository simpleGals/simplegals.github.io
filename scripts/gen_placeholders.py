#!/usr/bin/env python3
"""Generate throwaway placeholder photos into shared/in/.

These prove the build pipeline. Replace them with real shots by clearing
shared/in/ and dropping your own images; nothing else changes.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

IN = Path(__file__).resolve().parent.parent / "shared" / "in"
SIZES = [(1600, 1067), (1067, 1600), (1600, 1200), (1400, 1400)]
PALETTE = [(31, 41, 61), (61, 31, 51), (31, 61, 45), (61, 52, 26),
           (20, 40, 70), (70, 30, 40), (40, 60, 30)]


def _font(px: int):
    for path in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(path, px)
        except Exception:
            continue
    return ImageFont.load_default()


def main() -> None:
    IN.mkdir(parents=True, exist_ok=True)
    for i in range(1, 37):
        w, h = SIZES[i % len(SIZES)]
        base = PALETTE[i % len(PALETTE)]
        img = Image.new("RGB", (w, h), base)
        d = ImageDraw.Draw(img)
        for y in range(h):
            t = y / h
            d.line([(0, y), (w, y)], fill=tuple(min(255, int(c * (0.55 + 0.7 * t))) for c in base))
        label = f"{i:02d}"
        font = _font(int(h * 0.30))
        box = d.textbbox((0, 0), label, font=font)
        d.text(((w - (box[2] - box[0])) / 2, (h - (box[3] - box[1])) / 2 - box[1]),
               label, fill=(245, 245, 245), font=font)
        img.save(IN / f"img-{i:02d}.jpg", quality=85)
    print(f"wrote 36 images to {IN}")


if __name__ == "__main__":
    main()
