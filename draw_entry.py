#!/usr/bin/env python3
"""Draw the 22 November 2026 front page for news-image-20261122.

Fresh artwork for this day only: a newspaper front page with a lead story
(COP31 collapse) and a 2x2 grid of four more stories. Uses Pillow and the
DejaVu fonts installed on the system. Output is deterministic: no random
numbers, no timestamps, no network.
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (244, 239, 227)
NAVY = (24, 33, 62)
GOLD = (222, 158, 32)
RED = (158, 28, 28)
INK = (28, 26, 22)
GREY = (110, 104, 90)
SKY = (214, 230, 240)
SAND = (232, 214, 170)

FDIR = "/usr/share/fonts/truetype/dejavu/"
SERIF = FDIR + "DejaVuSerif-Bold.ttf"
SERIF_R = FDIR + "DejaVuSerif.ttf"
SANS = FDIR + "DejaVuSans.ttf"
SANS_B = FDIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit in `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, fnt):
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + int(fnt.size * 1.5)


def thumb_frame(draw, x, y, w, h, caption):
    draw.rectangle([x, y, x + w, y + h], outline=NAVY, width=2)
    cap_f = font(SANS_B, 15)
    tw = draw.textlength(caption, font=cap_f)
    draw.rectangle([x, y + h - 24, x + tw + 16, y + h], fill=NAVY)
    draw.text((x + 8, y + h - 22), caption, font=cap_f, fill=(255, 255, 255))


def lead_art(draw, x, y, w, h):
    """Cracked dry earth under a harsh sun: the climate talks fail."""
    draw.rectangle([x, y, x + w, y + h], fill=(246, 214, 150))
    # sun
    cx, cy, r = x + w - 90, y + 62, 42
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 120, 30))
    draw.ellipse([cx - r + 12, cy - r + 12, cx + r - 12, cy + r - 12],
                 fill=(244, 164, 54))
    # cracked ground
    gy = y + h - 78
    draw.rectangle([x, y + h - 78, x + w, y + h], fill=(196, 148, 92))
    draw.line([(x + 30, gy), (x + 90, gy + 26), (x + 70, gy + 52),
               (x + 130, gy + 78)], fill=(120, 78, 44), width=4)
    draw.line([(x + 200, gy), (x + 240, gy + 30), (x + 210, gy + 60),
               (x + 260, gy + 78)], fill=(120, 78, 44), width=4)
    draw.line([(x + 340, gy), (x + 380, gy + 24), (x + 350, gy + 50),
               (x + 410, gy + 78)], fill=(120, 78, 44), width=4)
    # empty chairs / broken talks: two small flags crossed out
    draw.line([(x + 60, y + 40), (x + 60, y + 120)], fill=(90, 70, 50), width=3)
    draw.polygon([(x + 60, y + 40), (x + 110, y + 52), (x + 60, y + 66)],
                 fill=(90, 130, 200))
    draw.line([(x + 60, y + 40), (x + 110, y + 66)], fill=RED, width=4)
    thumb_frame(draw, x, y, w, h, "NO DEAL IN ANTALYA")


def iran_art(draw, x, y, w, h):
    """Missile arcs over a desert base at dusk."""
    draw.rectangle([x, y, x + w, y + h], fill=(58, 48, 78))
    # ground
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(140, 110, 70))
    # base blocks
    draw.rectangle([x + 14, y + h - 62, x + 52, y + h - 34], fill=(200, 190, 170))
    draw.rectangle([x + 60, y + h - 52, x + 96, y + h - 34], fill=(180, 168, 148))
    # radar dish
    draw.line([(x + 118, y + h - 34), (x + 118, y + h - 66)], fill=(220, 220, 220), width=3)
    draw.pieslice([x + 104, y + h - 84, x + 132, y + h - 56], 180, 360,
                  fill=(220, 220, 220))
    # missile arcs
    draw.arc([x + 34, y - 6, x + 96, y + 56], 200, 340, fill=(255, 190, 60), width=4)
    draw.arc([x + 78, y + 2, x + 140, y + 64], 200, 340, fill=(255, 120, 40), width=4)
    draw.ellipse([x + 88, y + 44, x + 96, y + 52], fill=(255, 220, 120))
    thumb_frame(draw, x, y, w, h, "AL-RIFFA")


def mexico_art(draw, x, y, w, h):
    """A sheriff star on a wanted-poster background."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 226, 196))
    draw.rectangle([x + 6, y + 6, x + w - 6, y + h - 6], outline=(150, 120, 70), width=2)
    # star badge
    cx, cy = x + w // 2, y + h // 2 - 6
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = 42 if i % 2 == 0 else 18
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=(200, 160, 60), outline=(140, 100, 30))
    draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(238, 226, 196),
                 outline=(140, 100, 30), width=2)
    thumb_frame(draw, x, y, w, h, "SINALOA")


def kyiv_art(draw, x, y, w, h):
    """Apartment block hit at night, smoke rising."""
    draw.rectangle([x, y, x + w, y + h], fill=(38, 44, 66))
    # block
    draw.rectangle([x + 34, y + 26, x + 116, y + h - 22], fill=(150, 140, 130))
    for row in range(3):
        for col in range(3):
            wx, wy = x + 44 + col * 26, y + 38 + row * 26
            lit = (row, col) != (1, 1)
            draw.rectangle([wx, wy, wx + 14, wy + 14],
                           fill=(255, 210, 110) if lit else (40, 40, 40))
    # blast hole
    draw.ellipse([x + 60, y + 60, x + 96, y + 96], fill=(30, 30, 34))
    # smoke
    draw.ellipse([x + 58, y + 6, x + 88, y + 30], fill=(120, 120, 125))
    draw.ellipse([x + 76, y - 4, x + 108, y + 20], fill=(100, 100, 105))
    # drone dots
    draw.ellipse([x + 12, y + 14, x + 16, y + 18], fill=(255, 190, 60))
    draw.ellipse([x + 130, y + 22, x + 134, y + 26], fill=(255, 190, 60))
    thumb_frame(draw, x, y, w, h, "DYMER")


def trade_art(draw, x, y, w, h):
    """EU circle of stars beside a rising bar chart."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # EU flag block
    draw.rectangle([x + 10, y + 10, x + 66, y + 52], fill=(30, 60, 140))
    import math
    for i in range(12):
        ang = -math.pi / 2 + i * math.pi / 6
        sx = x + 38 + 16 * math.cos(ang)
        sy = y + 31 + 16 * math.sin(ang)
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
    # rising bars
    bars = [(74, 62), (92, 48), (110, 34), (128, 18)]
    for bx, bh in bars:
        draw.rectangle([x + bx, y + h - 14 - bh, x + bx + 14, y + h - 14],
                       fill=(30, 120, 70))
    draw.line([(x + 72, y + h - 16), (x + 146, y + h - 16)], fill=NAVY, width=2)
    thumb_frame(draw, x, y, w, h, "98.5% TARIFF-FREE")


def grid_cell(draw, x, y, w, art_fn, kicker_text, headline, deck):
    tw, th = 150, 112
    art_fn(draw, x, y, tw, th)
    tx = x + tw + 14
    twd = w - tw - 14
    yy = kicker(draw, tx, y + 2, kicker_text, font(SANS_B, 16))
    yy = draw_wrapped(draw, tx, yy, headline, font(SERIF, 29), twd, INK, 36)
    draw_wrapped(draw, tx, yy + 4, deck, font(SANS, 16), twd, INK, 21)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.text((W // 2, 8), "THE WORLD TODAY", font=font(SERIF, 62),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 72), "SUNDAY 22 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=GOLD, anchor="ma")
    d.rectangle([0, 112, W, 118], fill=GOLD)

    d.text((W // 2, 130), "FIVE STORIES THAT DEFINED THE DAY",
           font=font(SANS, 17), fill=GREY, anchor="ma")

    # Lead story: COP31
    lx, ly = 36, 168
    lw = 462
    yy = kicker(d, lx, ly, "CLIMATE  ·  ANTALYA  ·  TURKEY", font(SANS_B, 18))
    yy = draw_wrapped(d, lx, yy, "COP31 talks collapse in Antalya",
                      font(SERIF, 40), lw, INK, 50)
    draw_wrapped(d, lx, yy + 8,
                 "The summit ends in failure on Sunday after a standoff "
                 "over fossil fuels. The EU and others objected to a final "
                 "deal that never mentions fossil fuels, so no agreement "
                 "at all.",
                 font(SERIF_R, 19), lw, INK, 25)
    lead_art(d, 522, 168, 466, 238)

    # Divider
    d.line([(36, 440), (988, 440)], fill=INK, width=2)

    # Grid row 1
    grid_cell(d, 36, 470, 460, iran_art, "IRAN  ·  BAHRAIN",
              "Iran strikes US bases in Bahrain",
              "The Guard launches a missile-and-drone assault on the "
              "Al-Riffa and Awali bases, claiming two US Patriot radars "
              "destroyed; two people are hurt.")
    grid_cell(d, 528, 470, 460, mexico_art, "MEXICO",
              "Mexico captures cartel boss \u201cEl Chapo Isidro\u201d",
              "Special forces seize Fausto Isidro Meza Flores in a bloody "
              "Sinaloa raid that leaves at least 11 dead, including four "
              "soldiers.")

    # Grid row 2
    grid_cell(d, 36, 700, 460, kyiv_art, "UKRAINE",
              "Russian drone strike destroys Kyiv apartment block",
              "In Dymer, at least 8 are killed and 14 are missing under "
              "the rubble, after 186 drones attacked overnight into "
              "Sunday.")
    grid_cell(d, 528, 700, 460, trade_art, "TRADE",
              "EU and Indonesia sign landmark trade deal",
              "After almost 10 years of talks, tariffs are scrapped on up "
              "to 98.5% of goods.")

    # Footer
    d.line([(36, 968), (988, 968)], fill=INK, width=2)
    d.text((W // 2, 980), "THE WORLD TODAY  \u2022  22 NOVEMBER 2026",
           font=font(SANS, 16), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
