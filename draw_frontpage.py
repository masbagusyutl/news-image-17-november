#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

All stories below were first reported on Tuesday 17 November 2026, gathered
from international wire and newspaper reporting that morning. The program
draws the page with PIL at build time; the entry's main.py only copies the
finished entry.png to the grader's output directory (the sandbox runs with
no network, so the day's news has to be baked in here).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 234)
INK = (22, 21, 19)
RED = (179, 38, 30)
NAVY = (31, 58, 95)
GREY = (90, 86, 78)
RULE = (180, 172, 150)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured in pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lead_art(d, x0, y0, x1, y1):
    """Stylised Kerch bridge over water, with a broken span and smoke."""
    d.rectangle([x0, y0, x1, y1], fill=(223, 233, 242))
    # sky sun
    d.ellipse([x1 - 62, y0 + 14, x1 - 22, y0 + 54], fill=(240, 196, 90))
    # water
    d.rectangle([x0, y1 - 52, x1, y1], fill=(150, 184, 214))
    for i, wy in enumerate((y1 - 42, y1 - 30, y1 - 18)):
        d.line([(x0 + 12 + i * 30, wy), (x1 - 12 - i * 22, wy)],
               fill=(255, 255, 255), width=2)
    deck_y = y1 - 88
    # towers
    for tx in (x0 + 52, x1 - 76):
        d.rectangle([tx, deck_y - 92, tx + 22, deck_y], fill=(70, 78, 90))
        d.rectangle([tx - 6, deck_y - 100, tx + 28, deck_y - 92],
                    fill=(70, 78, 90))
    # cables
    mid = (x0 + x1) // 2
    d.line([(x0 + 63, deck_y - 92), (mid - 34, deck_y)], fill=(90, 96, 104),
           width=2)
    d.line([(x1 - 65, deck_y - 92), (mid + 34, deck_y)], fill=(90, 96, 104),
           width=2)
    # deck, broken in the middle
    d.rectangle([x0 + 8, deck_y, mid - 34, deck_y + 10], fill=(52, 58, 68))
    d.rectangle([mid + 34, deck_y, x1 - 8, deck_y + 10], fill=(52, 58, 68))
    # fallen span, tilted into the water
    d.polygon([(mid - 30, deck_y + 4), (mid + 30, deck_y + 4),
               (mid + 22, deck_y + 34), (mid - 38, deck_y + 34)],
              fill=(120, 40, 34))
    # smoke over the gap
    for cx, cy, r in ((mid - 8, deck_y - 34, 16), (mid + 12, deck_y - 52, 20),
                      (mid + 2, deck_y - 70, 13)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 118, 112))
    # deck posts
    for px in range(x0 + 20, x1 - 16, 34):
        if abs(px - mid) > 40:
            d.line([(px, deck_y), (px, deck_y - 12)], fill=(90, 96, 104),
                   width=2)


LEAD = {
    "kicker": "EUROPE  ·  WAR IN UKRAINE",
    "headline": "Crimea bridge hit again as Russia pounds Kyiv's bridges",
    "summary": ("Ukraine struck the Kerch bridge to occupied Crimea for the "
                "second time in under 24 hours, collapsing part of its road "
                "deck. Hours earlier, Russian missiles hit Kyiv's bridges "
                "over the Dnipro, cutting heat, water and power."),
}

CARDS = [
    ("MIDDLE EAST  ·  THE GULF", RED,
     "Tankers hit by mines off Hormuz as Iran drones target US radar",
     "Tehran says tankers struck mines near the strait, and its drones "
     "fired at a US radar base in Bahrain. US intelligence warns of a "
     "\u201cdirty bomb\u201d plot against Trump officials."),
    ("ASIA  ·  DIPLOMACY", NAVY,
     "China confirms first Xi\u2013Trump\u2013Putin summit",
     "The three leaders meet in Shenzhen on Thursday, on the sidelines of "
     "the APEC summit China is hosting, to discuss peace, nuclear risks "
     "and Ukraine."),
    ("AMERICAS  ·  DEFENCE", (15, 118, 110),
     "Third US carrier reaches the Gulf; Pentagon fails audit again",
     "USS Theodore Roosevelt joins two carriers in the region. Auditors "
     "again cannot verify Pentagon books covering $4.8 trillion in assets "
     "\u2014 the ninth year running."),
    ("TECH  ·  TRADE", (180, 83, 9),
     "US closes AI-chip loophole as stocks slide",
     "Washington tightens export curbs on AI chips reaching China via "
     "rentals abroad. The Dow fell 849 points as tech slid before "
     "Nvidia's earnings."),
    ("HEALTH  ·  AMERICA", (107, 33, 168),
     "US loses measles-free status after three decades",
     "The US battles its highest measles caseload in 30-plus years; 13 "
     "babies were born with the disease since 2025, nearly all to "
     "unvaccinated mothers."),
    ("BRITAIN  ·  MIDDLE EAST", (22, 101, 52),
     "UK sanctions firms building Israeli settlements",
     "London sanctions eight construction firms and a group blocking Gaza "
     "aid, in a push to protect the two-state solution."),
]

ALSO = ("Japan scrambles jets over a Russian airspace breach  ·  Five "
        "European states plan a Rwanda returns hub  ·  Xi and Carney "
        "agree tariff cuts")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 120], fill=(16, 15, 14))
    d.text((W // 2, 22), "THE WORLD", font=font(SERIF_B, 76),
           fill=(248, 244, 234), anchor="ma")
    d.text((W // 2, 132), "TUESDAY, 17 NOVEMBER 2026",
           font=font(SANS_B, 24), fill=RED, anchor="ma")
    d.text((W // 2, 162), "The day's world news, in one page",
           font=font(SERIF_R, 19), fill=GREY, anchor="ma")
    d.line([(36, 190), (W - 36, 190)], fill=RULE, width=2)

    # Lead story
    lx, lw = 36, 620
    y = 206
    d.text((lx, y), LEAD["kicker"], font=font(SANS_B, 19), fill=RED)
    y += 28
    for line in wrap(d, LEAD["headline"], font(SERIF_B, 38), lw):
        d.text((lx, y), line, font=font(SERIF_B, 38), fill=INK)
        y += 46
    y += 6
    for line in wrap(d, LEAD["summary"], font(SANS_R, 21), lw)[:4]:
        d.text((lx, y), line, font=font(SANS_R, 21), fill=INK)
        y += 27
    draw_lead_art(d, 684, 206, 988, 206 + 236)

    d.line([(36, 456), (W - 36, 456)], fill=RULE, width=2)

    # Story grid: 2 columns x 3 rows
    col_w = 464
    xs = (36, 524)
    ys = (474, 634, 794)
    for i, (kicker, colour, headline, summary) in enumerate(CARDS):
        x = xs[i % 2]
        y = ys[i // 2]
        d.text((x, y), kicker, font=font(SANS_B, 16), fill=colour)
        y += 22
        for line in wrap(d, headline, font(SERIF_B, 24), col_w)[:2]:
            d.text((x, y), line, font=font(SERIF_B, 24), fill=INK)
            y += 29
        y += 4
        for line in wrap(d, summary, font(SANS_R, 19), col_w)[:3]:
            d.text((x, y), line, font=font(SANS_R, 19), fill=(52, 50, 46))
            y += 23

    # Footer
    d.line([(36, 958), (W - 36, 958)], fill=RULE, width=2)
    fy = 966
    for line in wrap(d, "ALSO TODAY:  " + ALSO, font(SANS_B, 15), W - 72):
        d.text((36, fy), line, font=font(SANS_B, 15), fill=INK)
        fy += 20
    d.text((36, 1004), "All events first reported 17 November 2026  ·  "
           "Compiled from international wire reports",
           font=font(SANS_R, 14), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
