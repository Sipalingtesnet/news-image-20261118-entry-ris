#!/usr/bin/env python3
"""Generate entry.png — "THE WORLD IN ONE DAY", 18 November 2026.

A 1024x1024 editorial poster built only from Pillow primitives:
  * Masthead: the date in huge bold type + the poster title.
  * Five illustrated story panels (drawn scenes + headline + caption).
  * A footer strip with the three secondary headlines.

Run with the build venv python:
    /data/home/makefun/news-image-venv/bin/python tools/generate_image.py
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
W = H = 1024
OUT = Path(__file__).resolve().parent.parent / "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
F_REG = f"{FONT_DIR}/DejaVuSans.ttf"

NAVY = (11, 27, 51)          # #0B1B33 background
NAVY_MID = (24, 48, 90)
NAVY_LIGHT = (18, 38, 74)    # footer / panel scene background
CREAM = (246, 241, 228)
WHITE = (255, 255, 255)
INK = (16, 30, 55)           # dark text on the warm panels
GOLD = (229, 195, 84)

# Warm accents, one per panel
AMBER = (232, 163, 61)
CORAL = (239, 106, 82)
TEAL = (51, 166, 156)
GOLDY = (229, 194, 61)
ORANGE = (237, 138, 62)
ACCENTS = [AMBER, CORAL, TEAL, GOLDY, ORANGE]

# Layout
PANEL_X0 = 13
PANEL_GAP = 12
PANEL_W = 190
PANEL_H = 560
PANEL_Y0 = 170
CARD_R = 10
PAD = 8


# ----------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------
def _font(path, size):
    return ImageFont.truetype(path, size)


def _tw(draw, text, f):
    """Text width in pixels."""
    l, _, r, _ = draw.textbbox((0, 0), text, font=f)
    return r - l


def shade(color, factor=0.72):
    return tuple(int(c * factor) for c in color)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; keeps '•' glued to the previous word and breaks
    over-long hyphenated tokens at their hyphens."""
    lines, cur = [], ""
    for tok in text.split():
        if tok == "•":
            cur = (cur + " • ").strip()
            continue
        trial = (cur + " " + tok).strip() if cur else tok
        fits = _tw(draw, trial, f) <= max_w
        if fits:
            cur = trial
            continue
        if "-" in tok:
            sub = tok.split("-")
            for k in range(len(sub) - 1, 0, -1):
                head = "-".join(sub[:k]) + "-"
                rest = "-".join(sub[k:])
                head_full = (cur + " " + head).strip()
                if _tw(draw, head_full, f) <= max_w:
                    lines.append(head_full)
                    cur = rest
                    break
            else:
                if cur:
                    lines.append(cur)
                cur = tok
            continue
        if cur:
            lines.append(cur)
        cur = tok
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, box_w, box_h, path, start, minimum, max_lines, gap):
    """Shrink the font until the wrapped text fits box_h with <= max_lines."""
    size = start
    while size >= minimum:
        f = _font(path, size)
        lines = wrap(draw, text, f, box_w)
        if len(lines) <= max_lines:
            total = len(lines) * size + (len(lines) - 1) * gap
            if total <= box_h:
                return f, lines
        size -= 1
    f = _font(path, minimum)
    return f, wrap(draw, text, f, box_w)


def draw_block(draw, lines, f, cx, top, box_h, color, gap):
    """Draw centered lines, vertically centered inside the given box."""
    lh = f.size + gap
    total = len(lines) * lh - gap
    y0 = top + max(0, (box_h - total) // 2)
    for i, ln in enumerate(lines):
        cy = y0 + lh * i + f.size / 2
        draw.text((cx, cy), ln, font=f, fill=color, anchor="mm")


def arrow(draw, x0, y0, x1, y1, color, width=5, head=10):
    """Thick arrow from (x0, y0) to (x1, y1)."""
    draw.line((x0, y0, x1, y1), fill=color, width=width)
    dx, dy = x1 - x0, y1 - y0
    length = max(1.0, (dx * dx + dy * dy) ** 0.5)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    tip = (x1 + ux * head, y1 + uy * head)
    draw.polygon(
        [
            tip,
            (tip[0] - ux * head + px * head * 0.6, tip[1] - uy * head + py * head * 0.6),
            (tip[0] - ux * head - px * head * 0.6, tip[1] - uy * head - py * head * 0.6),
        ],
        fill=color,
    )


# ----------------------------------------------------------------------------
# Scenes (PIL primitives only)
# ----------------------------------------------------------------------------
def scene_manila(d, x, y, w, h):
    """Manila skyline + US and Philippine flags."""
    # sun
    d.ellipse((x + w * 0.72, y + h * 0.10, x + w * 0.72 + 30, y + h * 0.10 + 30),
              fill=(250, 205, 100))
    # skyline silhouettes
    base = y + h - 44
    widths = [24, 16, 34, 18, 26, 20]
    heights = [52, 84, 70, 96, 40, 60]
    cx = x + 6
    for bw, bh in zip(widths, heights):
        d.rectangle((cx, base - bh, cx + bw, base), fill=NAVY)
        if bh > 70:  # antenna on the tall towers
            d.line((cx + bw / 2, base - bh, cx + bw / 2, base - bh - 12),
                   fill=NAVY, width=2)
        cx += bw + 7
    # sea band
    d.rectangle((x, base + 4, x + w, y + h), fill=NAVY)
    # US flag (left)
    px = x + 10
    d.line((px, y + 6, px, y + 6 + 64), fill=NAVY, width=3)
    fx, fy = px + 4, y + 8
    d.rectangle((fx, fy, fx + 32, fy + 20), fill=WHITE)
    for i in range(3):
        d.rectangle((fx, fy + i * 6, fx + 32, fy + i * 6 + 3), fill=(205, 70, 60))
    d.rectangle((fx, fy, fx + 14, fy + 9), fill=(58, 70, 150))
    # Philippine flag (right)
    px2 = x + w - 10
    d.line((px2, y + 6, px2, y + 6 + 64), fill=NAVY, width=3)
    fx2, fy2 = px2 - 36, y + 8
    d.rectangle((fx2, fy2, fx2 + 32, fy2 + 20), fill=(58, 70, 150))
    d.rectangle((fx2, fy2 + 10, fx2 + 32, fy2 + 20), fill=(205, 70, 60))
    d.ellipse((fx2 + 13, fy2 + 5, fx2 + 19, fy2 + 11), fill=(245, 200, 60))


def scene_bridge(d, x, y, w, h):
    """Crimea bridge over water with an explosion."""
    water_y = y + h - 58
    # water
    d.rectangle((x, water_y + 10, x + w, y + h), fill=NAVY)
    pts = [(x + i * 12, water_y + 8 - (2 if (i // 1) % 2 else -2)) for i in range(w // 12 + 1)]
    pts.append((x + w, water_y + 8))
    d.line(pts, fill=NAVY, width=3)
    # pylons
    for px in (x + w * 0.26, x + w * 0.74):
        d.polygon(
            [
                (px - 6, water_y),
                (px + 6, water_y),
                (px + 4, y + h * 0.10),
                (px - 4, y + h * 0.10),
            ],
            fill=NAVY,
        )
    # deck
    d.line((x, water_y - 4, x + w, water_y - 4), fill=NAVY, width=8)
    # cables
    for px in (x + w * 0.26, x + w * 0.74):
        top = (px, y + h * 0.10)
        for dx in (16, 34, 52, 70):
            d.line((top, (px + dx, water_y - 4)), fill=NAVY, width=2)
            d.line((top, (px - dx, water_y - 4)), fill=NAVY, width=2)
    # explosion at mid-span
    ex, ey = x + w * 0.5, y + h * 0.42
    d.ellipse((ex - 22, ey - 16, ex + 22, ey + 16), fill=(240, 120, 40))
    d.ellipse((ex - 14, ey - 11, ex + 14, ey + 11), fill=(250, 170, 50))
    d.ellipse((ex - 7, ey - 6, ex + 7, ey + 6), fill=(255, 232, 120))
    for a in range(0, 360, 45):
        r = 26
        sx = ex + r * math.cos(math.radians(a))
        sy = ey + r * math.sin(math.radians(a))
        d.line((ex, ey, sx, sy), fill=(250, 200, 70), width=3)
    # smoke
    for i, (ox, oy, r) in enumerate(((ex + 10, ey - 30, 9), (ex + 24, ey - 42, 12),
                                     (ex + 42, ey - 50, 14))):
        d.ellipse((ox - r, oy - r, ox + r, oy + r), fill=(120 + i * 8, 120 + i * 8, 128))


def scene_tanker(d, x, y, w, h):
    """LPG tanker on waves."""
    # waves (two rows of half-circles)
    for row, yb in ((y + h - 44, y + h - 24), (y + h - 18, y + h + 2)):
        for cx in range(x - 8, x + w + 8, 20):
            d.arc((cx - 10, yb - 10, cx + 10, yb + 10), 180, 360, fill=NAVY, width=3)
    # hull
    hull_top = y + h - 46
    d.polygon(
        [
            (x + w * 0.18, hull_top),
            (x + w * 0.82, hull_top),
            (x + w * 0.74, y + h - 4),
            (x + w * 0.26, y + h - 4),
        ],
        fill=NAVY,
    )
    # deck
    d.line((x + w * 0.20, hull_top - 6, x + w * 0.80, hull_top - 6), fill=NAVY, width=3)
    # LPG tanks (white spheres)
    for i, tx in enumerate((x + w * 0.28, x + w * 0.46, x + w * 0.64)):
        r = 13 - i * 2
        d.ellipse((tx - r, hull_top - 18 - r, tx + r, hull_top - 18 + r),
                  fill=CREAM, outline=NAVY, width=3)
    # bridge block + funnel
    bx, by = x + w * 0.76, hull_top - 22
    d.rectangle((bx, by, bx + 12, hull_top - 2), fill=NAVY)
    d.rectangle((bx + 2, by - 14, bx + 10, by - 2), fill=NAVY)
    # smoke
    for i, (oy, r) in enumerate(((by - 24, 5), (by - 34, 7), (by - 42, 6))):
        d.ellipse((bx + 2 - r, oy - r, bx + 2 + r, oy + r),
                  fill=(120 + i * 8, 120 + i * 8, 128))


def scene_cyclone(d, x, y, w, h):
    """Cyclone spiral with rain over a coast."""
    cx, cy = x + w * 0.55, y + h * 0.40
    for t in range(0, 660, 11):
        r = 5 + t * 0.115
        px = cx + r * math.cos(math.radians(t))
        py = cy + r * math.sin(math.radians(t))
        dot = max(1.6, 5.0 - t * 0.006)
        d.ellipse((px - dot, py - dot, px + dot, py + dot),
                  fill=(CREAM if (t // 55) % 2 else NAVY))
    # rain dashes
    for i in range(9):
        rx = x + 8 + i * 19
        ry = y + h * 0.52 + (i % 4) * 8
        d.line((rx, ry, rx - 5, ry + 13), fill=CREAM, width=2)
    # coast with a few buildings
    coast = y + h - 16
    d.polygon(
        [(x, y + h), (x, coast - 6), (x + 30, coast), (x + 62, coast - 8),
         (x + 96, coast - 2), (x + w, coast - 9), (x + w, y + h)],
        fill=NAVY,
    )
    for i, (hx, hh) in enumerate(((x + 40, 16), (x + 76, 22), (x + 128, 14))):
        d.rectangle((hx, coast - hh, hx + 10, coast), fill=NAVY)


def scene_handshake(d, x, y, w, h):
    """Canada-China trade: flags, handshake, trade arrows."""
    # Canada flag (left)
    px, py = x + 10, y + 6
    d.line((px, py, px, py + 56), fill=NAVY, width=3)
    fx, fy = px + 4, py + 4
    d.rectangle((fx, fy, fx + 30, fy + 20), fill=WHITE)
    d.rectangle((fx, fy, fx + 7, fy + 20), fill=(220, 60, 60))
    d.rectangle((fx + 23, fy, fx + 30, fy + 20), fill=(220, 60, 60))
    # China flag (right)
    px2, py2 = x + w - 10, y + 6
    d.line((px2, py2, px2, py2 + 56), fill=NAVY, width=3)
    fx2, fy2 = px2 - 34, py2 + 4
    d.rectangle((fx2, fy2, fx2 + 30, fy2 + 20), fill=(220, 50, 50))
    d.ellipse((fx2 + 5, fy2 + 4, fx2 + 9, fy2 + 8), fill=(250, 210, 70))
    d.ellipse((fx2 + 12, fy2 + 2, fx2 + 15, fy2 + 6), fill=(250, 210, 70))
    # sleeves
    d.polygon(
        [(x + 2, y + h * 0.78), (x + w * 0.46, y + h * 0.50),
         (x + w * 0.58, y + h * 0.58), (x + 14, y + h * 0.86)],
        fill=NAVY,
    )
    d.polygon(
        [(x + w - 2, y + h * 0.78), (x + w * 0.54, y + h * 0.50),
         (x + w * 0.42, y + h * 0.58), (x + w - 14, y + h * 0.86)],
        fill=NAVY,
    )
    # clasped hands
    hx, hy = x + w * 0.5, y + h * 0.56
    d.ellipse((hx - 20, hy - 13, hx + 4, hy + 15), fill=CREAM, outline=NAVY, width=3)
    d.ellipse((hx - 4, hy - 13, hx + 20, hy + 15), fill=CREAM, outline=NAVY, width=3)
    for i in range(3):
        d.line((hx - 16 + i * 14, hy - 9, hx - 12 + i * 14, hy - 3), fill=NAVY, width=2)
    # trade arrows
    arrow(d, x + w * 0.16, y + h * 0.30, x + w * 0.80, y + h * 0.30, NAVY, width=5, head=9)
    arrow(d, x + w * 0.84, y + h * 0.38, x + w * 0.20, y + h * 0.38, NAVY, width=5, head=9)


SCENES = [scene_manila, scene_bridge, scene_tanker, scene_cyclone, scene_handshake]

STORIES = [
    ("TRUMP LANDS IN MANILA",
     "US president arrives for Quad talks ahead of China visit; ASEAN summit under way."),
    ("CRIMEA BRIDGE HIT AGAIN",
     "Ukraine strikes the bridge a 2nd day; Russia hits bridges in Kyiv, cutting water and power."),
    ("TANKER ATTACKED IN HORMUZ",
     "MT TARA GAS hit in the Strait; 21 of 24 Indian crew evacuated safely to Khasab."),
    ("CYCLONE AKVAN BEARS DOWN",
     "Storm intensifies over Bay of Bengal; Andhra Pradesh and Odisha on high alert."),
    ("CANADA-CHINA TRADE DEAL",
     "Xi meets Carney as Ottawa and Beijing extend trade deals ahead of APEC."),
]


# ----------------------------------------------------------------------------
# Compose the poster
# ----------------------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # --- masthead ----------------------------------------------------------
    date_f, date_lines = fit_text(d, "WEDNESDAY 18 NOVEMBER 2026", W - 24, 96,
                                  F_BOLD, 64, 40, 1, 0)
    d.text((W / 2, 82), date_lines[0], font=date_f, fill=CREAM, anchor="mm")
    sub_f, sub_lines = fit_text(d, "THE WORLD IN ONE DAY", W - 40, 48,
                                F_BOLD, 40, 22, 1, 0)
    d.text((W / 2, 132), sub_lines[0], font=sub_f, fill=GOLD, anchor="mm")
    # masthead underline
    d.rectangle((40, 152, W - 40, 156), fill=GOLD)

    # --- story panels ------------------------------------------------------
    for i, ((head, cap), accent) in enumerate(zip(STORIES, ACCENTS)):
        x0 = PANEL_X0 + i * (PANEL_W + PANEL_GAP)
        y0 = PANEL_Y0
        # card
        d.rounded_rectangle((x0, y0, x0 + PANEL_W, y0 + PANEL_H), radius=CARD_R,
                            fill=accent, outline=NAVY, width=3)
        # scene
        sx, sy, sw, sh = x0 + PAD, y0 + PAD, PANEL_W - 2 * PAD, 246
        d.rectangle((sx, sy, sx + sw, sy + sh), fill=shade(accent))
        SCENES[i](d, sx, sy, sw, sh)
        # rule
        d.rectangle((sx, sy + sh + 6, sx + sw, sy + sh + 8), fill=INK)
        # headline
        hx, hy, hw, hh = x0 + 10, y0 + 272, PANEL_W - 20, 134
        hf, hlines = fit_text(d, head, hw, hh, F_BOLD, 30, 16, 3, 4)
        draw_block(d, hlines, hf, x0 + PANEL_W / 2, hy, hh, INK, 4)
        # caption
        cx0, cy0, cw, ch = x0 + 10, y0 + 414, PANEL_W - 20, 138
        cf, clines = fit_text(d, cap, cw, ch, F_REG, 15, 11, 6, 3)
        draw_block(d, clines, cf, x0 + PANEL_W / 2, cy0, ch, INK, 3)

    # --- accent dots between panels and footer -----------------------------
    for i, accent in enumerate(ACCENTS):
        dcx = PANEL_X0 + i * (PANEL_W + PANEL_GAP) + PANEL_W / 2
        d.ellipse((dcx - 5, 786, dcx + 5, 796), fill=accent)

    # --- footer strip ------------------------------------------------------
    d.rectangle((0, 894, W, 1024), fill=NAVY_LIGHT)
    d.rectangle((0, 888, W, 894), fill=GOLD)
    footer_lines = [
        "Britain sanctions Israeli settlement firms •",
        "MS Dhoni retires from IPL, to mentor Chennai Super Kings •",
        "India re-elected to ITU Council 2027-2030",
    ]
    fsize = 24
    while fsize >= 15:
        f = _font(F_BOLD, fsize)
        if all(_tw(d, ln, f) <= W - 60 for ln in footer_lines) \
                and len(footer_lines) * fsize + (len(footer_lines) - 1) * 8 <= 116:
            break
        fsize -= 1
    ff = _font(F_BOLD, fsize)
    draw_block(d, footer_lines, ff, W / 2, 898, 126, CREAM, 8)

    img.save(OUT, "PNG")
    return OUT


if __name__ == "__main__":
    out = build()
    print(f"wrote {out} ({out.stat().st_size} bytes)")