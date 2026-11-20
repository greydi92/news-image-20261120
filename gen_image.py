#!/usr/bin/env python3
"""Render the 20 November 2026 world-news front page as entry.png.

Build-time script only. It runs here on this workstation with Pillow and
the DejaVu fonts; the graded entry, main.py, merely copies the finished
PNG, so grading needs nothing but the Python standard library. The
drawing is fully deterministic: fixed text, fixed geometry, no clock,
no network, no randomness, so the same inputs always give the same
bytes.

Stories verified as happening, or first reported, on Friday
20 November 2026 (sources in README.md):
  1. Trump pushes the Iran war decision to 2027 (Reuters)
  2. Trump, Putin and Xi issue a joint peace declaration (BBC)
  3. Cyclone Akvan makes landfall near Gopalpur, Odisha (IMD / The Hindu)
  4. Anthropic shares jump 17% on their first day of trading (The Hindu)
  5. GTA VI sales pass $1.8 billion, beating The Odyssey (Mezha)
  6. A tanker catches fire after hitting a mine east of the Strait
     of Hormuz (Daily Baku)
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (24, 30, 40)
MUTED = (82, 80, 74)
NAVY = (24, 48, 88)
CRIMSON = (168, 42, 34)
GOLD = (214, 162, 58)
GOLD_DARK = (146, 100, 20)
CARD = (255, 255, 255)
RULE = (203, 196, 175)
SLATE = (100, 102, 98)

BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, face, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if face.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_text(text, sizes, max_w, max_lines, path):
    """Biggest size from sizes whose wrap needs at most max_lines lines."""
    for size in sizes:
        face = font(path, size)
        lines = wrap(text, face, max_w)
        if len(lines) <= max_lines:
            return face, lines
    face = font(path, sizes[-1])
    return face, wrap(text, face, max_w)[:max_lines]


def tint(rgb, frac=0.86):
    """Blend a colour toward white."""
    return tuple(int(round(c * (1.0 - frac) + 255 * frac)) for c in rgb)


# ---------------------------------------------------------------- pictograms
# Each draws a flat symbol centred on (cx, cy) inside a square of
# half-size s, in colour col.

def pic_hourglass(d, cx, cy, s, col):
    # waiting clock: an hourglass for a decision pushed into next year
    d.polygon([(cx - 30, cy - 40), (cx + 30, cy - 40), (cx, cy),
               (cx + 30, cy + 40), (cx - 30, cy + 40), (cx, cy)],
              outline=col, width=7)
    d.line([cx - 38, cy - 40, cx + 38, cy - 40], fill=col, width=7)
    d.line([cx - 38, cy + 40, cx + 38, cy + 40], fill=col, width=7)
    d.polygon([(cx - 12, cy - 12), (cx + 12, cy - 12), (cx, cy + 2)],
              fill=col)
    d.polygon([(cx - 8, cy + 8), (cx + 8, cy + 8), (cx, cy + 24)],
              fill=col)


def pic_document(d, cx, cy, s, col):
    # a signed declaration: page, three seal dots, ribbon
    d.rectangle([cx - 34, cy - 44, cx + 34, cy + 44], outline=col, width=6)
    d.line([cx - 22, cy - 28, cx + 22, cy - 28], fill=col, width=5)
    d.line([cx - 22, cy - 14, cx + 22, cy - 14], fill=col, width=5)
    d.line([cx - 22, cy, cx + 22, cy], fill=col, width=5)
    for px in (cx - 20, cx, cx + 20):
        d.ellipse([px - 8, cy + 16, px + 8, cy + 32], fill=col)
    d.line([cx, cy + 32, cx, cy + 42], fill=col, width=5)
    d.polygon([(cx, cy + 42), (cx - 11, cy + 56), (cx, cy + 49),
               (cx + 11, cy + 56)], fill=col)


def pic_spiral(d, cx, cy, s, col):
    # cyclone: concentric spiral arcs winding into the eye
    for i, r in enumerate((14, 26, 38, 50)):
        start = 20 + i * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 250,
              fill=col, width=7)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=col)


def pic_chart(d, cx, cy, s, col):
    # market debut: three rising bars and a climbing arrow
    d.rectangle([cx - 40, cy + 18, cx - 16, cy + 46], fill=col)
    d.rectangle([cx - 8, cy - 2, cx + 16, cy + 46], fill=col)
    d.rectangle([cx + 24, cy - 26, cx + 48, cy + 46], fill=col)
    d.line([cx - 50, cy - 34, cx + 20, cy - 44], fill=col, width=5)
    d.polygon([(cx + 30, cy - 52), (cx + 8, cy - 48),
               (cx + 24, cy - 30)], fill=col)


def pic_gamepad(d, cx, cy, s, col):
    # game controller with cross pad and action buttons
    d.rounded_rectangle([cx - 46, cy - 24, cx + 46, cy + 24], radius=16,
                        outline=col, width=6)
    d.line([cx - 32, cy - 18, cx - 32, cy + 18], fill=col, width=5)
    d.line([cx - 41, cy, cx - 23, cy], fill=col, width=5)
    for bx, by in ((cx + 22, cy - 10), (cx + 34, cy + 2),
                   (cx + 22, cy + 12), (cx + 10, cy + 2)):
        d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=col)


def pic_tanker(d, cx, cy, s, col):
    # tanker at sea with a spiked mine and a flame above it
    d.polygon([(cx - 48, cy + 6), (cx + 48, cy + 6), (cx + 36, cy + 34),
               (cx - 36, cy + 34)], fill=col)
    d.rectangle([cx - 14, cy - 18, cx + 14, cy + 6], fill=col)
    d.line([cx - 52, cy + 44, cx + 52, cy + 44], fill=col, width=4)
    mx, my = cx + 44, cy - 34
    d.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=col)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        d.line([mx + dx * 10, my + dy * 10, mx + dx * 20, my + dy * 20],
               fill=col, width=4)
    d.polygon([(cx - 30, cy - 22), (cx - 18, cy - 48), (cx - 8, cy - 22)],
              fill=col)
    d.polygon([(cx - 14, cy - 22), (cx - 4, cy - 56), (cx + 8, cy - 22)],
              fill=col)


# ------------------------------------------------------------------- stories
# (kicker, headline, standfirst, accent, pictogram)
STORIES = [
    ("DIPLOMACY \u00b7 WASHINGTON",
     "TRUMP PUSHES IRAN WAR DECISION TO 2027",
     "No rush, he says \u2014 he will \u201csee what happens\u201d after "
     "January 1, as the Gulf war drags on.",
     CRIMSON, pic_hourglass),
    ("DIPLOMACY \u00b7 SHENZHEN",
     "TRUMP, PUTIN AND XI ISSUE PEACE DECLARATION",
     "The three leaders release a joint declaration a day after their "
     "historic three-way summit.",
     NAVY, pic_document),
    ("WEATHER \u00b7 INDIA",
     "CYCLONE AKVAN HITS THE ODISHA COAST",
     "Landfall near Gopalpur at noon, gusts to 110 km/h. Some 300,000 "
     "people evacuated; 69 trains cancelled.",
     (12, 110, 102), pic_spiral),
    ("BUSINESS \u00b7 TECH",
     "ANTHROPIC JUMPS 17% ON MARKET DEBUT",
     "The AI firm's shares close sharply higher on their first day of "
     "trading, valuing it near $1.5 trillion.",
     GOLD_DARK, pic_chart),
    ("CULTURE \u00b7 GAMING",
     "GTA VI SALES PASS $1.8 BILLION",
     "Rockstar's game overtakes The Odyssey's entire global box-office "
     "run within a day of release.",
     (102, 68, 148), pic_gamepad),
    ("THE GULF",
     "TANKER CATCHES FIRE AFTER HITTING A MINE",
     "A blaze east of the Strait of Hormuz as Gulf tensions run high "
     "and shipping stays on edge.",
     (44, 122, 48), pic_tanker),
]


def draw_card(d, x, y, w, h, story):
    kicker, headline, standfirst, accent, pic = story
    d.rounded_rectangle([x, y, x + w, y + h], radius=10,
                        fill=CARD, outline=RULE, width=2)
    # tinted icon band across the top of the card
    d.rounded_rectangle([x + 2, y + 2, x + w - 2, y + 118], radius=8,
                        fill=tint(accent, 0.86))
    pic(d, x + w // 2, y + 59, 46, accent)
    d.line([x + 12, y + 118, x + w - 12, y + 118], fill=RULE, width=2)

    tx = x + 16
    tw = w - 32
    d.text((tx, y + 132), kicker, font=font(BOLD_PATH, 15), fill=accent)
    hface, hrows = fit_text(headline, [27, 25, 23], tw, 3, BOLD_PATH)
    hy = y + 158
    for row in hrows:
        d.text((tx, hy), row, font=hface, fill=INK)
        hy += int(hface.size * 1.18)
    dface, drows = fit_text(standfirst, [17, 16], tw, 4, PLAIN_PATH)
    dy = hy + 6
    for row in drows:
        d.text((tx, dy), row, font=dface, fill=MUTED)
        dy += int(dface.size * 1.3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([20, 20, 1004, 168], fill=NAVY)
    d.rectangle([20, 168, 1004, 174], fill=CRIMSON)
    over = font(BOLD_PATH, 22)
    overline = "THE WORLD IN ONE PICTURE"
    d.text(((W - over.getlength(overline)) / 2, 34), overline,
           font=over, fill=GOLD)
    date_face = font(BOLD_PATH, 72)
    date_text = "20 NOVEMBER 2026"
    d.text(((W - date_face.getlength(date_text)) / 2, 62), date_text,
           font=date_face, fill=CARD)
    under = font(BOLD_PATH, 22)
    underline = "FRIDAY  \u00b7  SIX STORIES THAT DEFINED THE DAY"
    d.text(((W - under.getlength(underline)) / 2, 138), underline,
           font=under, fill=GOLD)

    # story grid: three columns, two rows
    cw, ch = 316, 384
    gap = 12
    for i, story in enumerate(STORIES):
        col, row = i % 3, i // 3
        x = 20 + col * (cw + gap)
        y = 190 + row * (ch + gap)
        draw_card(d, x, y, cw, ch, story)

    # footer
    foot = font(BOLD_PATH, 16)
    footer = "SIX STORIES FROM FRIDAY 20 NOVEMBER 2026"
    d.text(((W - foot.getlength(footer)) / 2, 984), footer,
           font=foot, fill=SLATE)

    img.save(OUT_PATH, format="PNG", optimize=True)
    print("wrote", OUT_PATH, os.path.getsize(OUT_PATH), "bytes")


if __name__ == "__main__":
    main()
