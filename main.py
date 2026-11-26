# SPDX-License-Identifier: MIT
"""news-image-20261126 — one 1024x1024 newspaper front page for 26 Nov 2026.

Deterministic: no network, no clock, no randomness. Running twice writes
identical bytes. Output goes to $MAKEFUN_OUTPUT_DIR/entry.png.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 245, 239)
INK = (12, 12, 12)
GREY = (90, 90, 88)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit in `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, leading=18, color=INK):
    """Draw a wrapped paragraph; returns y after the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2):
    draw.line([(x0, y), (x1, y)], fill=INK, width=width)


def draw_ship(draw, x, y, w, h):
    """Ink-style container ship at anchor, with a dock crane and waves."""
    # dock crane on the left quay
    cx = x + 34
    draw.line([(cx, y + 30), (cx, y + h - 78)], fill=INK, width=3)
    draw.line([(cx, y + 34), (cx + 92, y + 58)], fill=INK, width=3)
    draw.line([(cx + 92, y + 58), (cx + 92, y + h - 78)], fill=INK, width=2)
    draw.line([(cx + 92, y + 58), (cx + 92, y + 84)], fill=INK, width=1)
    draw.rectangle([cx + 84, y + 84, cx + 100, y + 96], outline=INK, width=2)
    # bridge tower
    draw.rectangle([x + w - 120, y + 18, x + w - 78, y + h - 74], outline=INK, width=2)
    for i in range(3):
        draw.line([(x + w - 116, y + 30 + i * 14), (x + w - 82, y + 30 + i * 14)],
                  fill=INK, width=2)
    draw.line([(x + w - 99, y + 18), (x + w - 99, y + 4)], fill=INK, width=2)
    draw.line([(x + w - 99, y + 4), (x + w - 88, y + 10)], fill=INK, width=2)
    # container stacks
    top = y + 34
    for r in range(3):
        for c in range(6):
            cx0 = x + 150 + c * 62
            cy0 = top + r * 26
            draw.rectangle([cx0, cy0, cx0 + 58, cy0 + 24], outline=INK, width=2)
            for gx in range(1, 4):
                draw.line([(cx0 + gx * 14, cy0), (cx0 + gx * 14, cy0 + 24)],
                          fill=INK, width=1)
    # hull
    hull = [(x + 8, y + h - 74), (x + w - 8, y + h - 74),
            (x + w - 60, y + h - 18), (x + 60, y + h - 18)]
    draw.polygon(hull, fill=INK)
    draw.rectangle([x + 8, y + h - 74, x + w - 8, y + h - 68], fill=INK)
    # portholes
    for i in range(7):
        px = x + 120 + i * 58
        draw.ellipse([px, y + h - 58, px + 9, y + h - 49],
                     fill=PAPER, outline=PAPER)
    # waves (kept inside the illustration box)
    for k in range(9):
        wx = x + 10 + k * 62
        draw.arc([wx, y + h - 10, wx + 56, y + h + 2], 0, 180, fill=INK, width=2)


def draw_rocket_station(draw, x, y, w, h):
    """Ink-style rocket climbing past a small space station."""
    # station: spine + panels
    draw.line([(x + 150, y + 20), (x + 150, y + 96)], fill=INK, width=4)
    for px0, py0 in ((x + 96, y + 30), (x + 178, y + 30),
                     (x + 96, y + 62), (x + 178, y + 62)):
        draw.rectangle([px0, py0, px0 + 52, py0 + 22], outline=INK, width=2)
        draw.line([(px0 + 26, py0), (px0 + 26, py0 + 22)], fill=INK, width=1)
        draw.line([(px0, py0 + 11), (px0 + 52, py0 + 11)], fill=INK, width=1)
    draw.ellipse([x + 138, y + 44, x + 162, y + 68], outline=INK, width=2)
    draw.line([(x + 150, y + 96), (x + 150, y + 108)], fill=INK, width=2)
    # ringed planet
    draw.ellipse([x + 216, y + 92, x + 252, y + 128], outline=INK, width=2)
    draw.line([(x + 204, y + 122), (x + 264, y + 98)], fill=INK, width=2)
    # rocket (compact, flame stays inside the box)
    rx, ry = x + 20, y + 56
    body = [(rx + 18, ry), (rx + 36, ry + 22), (rx + 36, ry + 78),
            (rx + 18, ry + 92), (rx, ry + 78), (rx, ry + 22)]
    draw.polygon(body, outline=INK, width=2)
    draw.ellipse([rx + 12, ry + 34, rx + 24, ry + 46], outline=INK, width=2)
    draw.polygon([(rx, ry + 78), (rx - 14, ry + 100), (rx + 6, ry + 88)],
                 outline=INK, width=2)
    draw.polygon([(rx + 36, ry + 78), (rx + 50, ry + 100), (rx + 30, ry + 88)],
                 outline=INK, width=2)
    # flame + smoke
    draw.polygon([(rx + 10, ry + 92), (rx + 26, ry + 92), (rx + 18, ry + 112)],
                 fill=INK)
    for sx, sy in ((x + 8, y + 118), (x + 44, y + 124), (x + 26, y + 134)):
        draw.ellipse([sx, sy, sx + 14, sy + 10], outline=INK, width=1)
    # stars
    for sx, sy in ((x + 90, y + 8), (x + 250, y + 12), (x + 70, y + 120),
                   (x + 262, y + 60)):
        draw.line([(sx - 5, sy), (sx + 5, sy)], fill=INK, width=2)
        draw.line([(sx, sy - 5), (sx, sy + 5)], fill=INK, width=2)


def draw_chart(draw, x, y, w, h):
    """Small falling-market bar chart."""
    draw.line([(x, y + h), (x + w, y + h)], fill=INK, width=2)
    draw.line([(x, y), (x, y + h)], fill=INK, width=2)
    heights = [62, 54, 58, 44, 48, 34, 38, 22, 26, 12]
    bw = w // len(heights)
    for i, hh in enumerate(heights):
        draw.rectangle([x + 4 + i * bw, y + h - hh,
                        x + 4 + (i + 1) * bw - 4, y + h], fill=INK)
    draw.line([(x + 4, y + 10), (x + w - 4, y + h - 14)], fill=INK, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36                      # margin
    right = W - mx

    # ---- masthead ------------------------------------------------------
    f_mast = font(SERIF_B, 84)
    title = "THE DAILY GLOBE"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 22), title, font=f_mast, fill=INK)
    rule(d, mx, 122, right, 3)
    f_date = font(SERIF, 20)
    date = "THURSDAY, 26 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 132), date, font=f_date, fill=INK)
    f_small = font(SANS, 15)
    d.text((mx, 134), "VOL. I — No. 330", font=f_small, fill=INK)
    d.text((right - d.textlength("PRICE: ONE STORY A DAY", font=f_small), 134),
           "PRICE: ONE STORY A DAY", font=f_small, fill=INK)
    rule(d, mx, 164, right, 2)

    # ---- lead story (left) ---------------------------------------------
    lead_w = 640
    lx = mx
    f_lead = font(SERIF_B, 46)
    y = 182
    for line in ["U.S. READIES NEW", "TARIFF PLAN FOR", "TRADING PARTNERS"]:
        d.text((lx, y), line, font=f_lead, fill=INK)
        y += 54
    f_sub = font(SERIF_I, 22)
    y = para(d, (lx, y + 6),
             "White House weighs duties on a wide range of imports — "
             "and a lower rate if a deal is struck.",
             f_sub, lead_w, leading=28, color=INK)
    draw_ship(d, lx, y + 8, lead_w, 168)
    y += 182
    f_body = font(SERIF, 15)
    y = para(d, (lx, y),
             "WASHINGTON — The United States is preparing to unveil a plan "
             "for new tariffs on trading partners around the world, "
             "officials said, in a move aimed at reshaping long-standing "
             "trade terms. The proposal would set duties on a broad set of "
             "imports, with room to lower them where deals are reached.",
             f_body, lead_w, leading=20)

    # ---- right column ----------------------------------------------------
    col_x = mx + lead_w + 24
    col_w = right - col_x
    rule_v = col_x - 12
    d.line([(rule_v, 182), (rule_v, 700)], fill=INK, width=2)
    f_col = font(SERIF_B, 30)
    y2 = 182
    for line in ["FIRST PAKISTANI", "ASTRONAUT", "REACHES", "TIANGONG"]:
        d.text((col_x, y2), line, font=f_col, fill=INK)
        y2 += 36
    draw_rocket_station(d, col_x, y2 + 4, col_w, 168)
    y2 += 180
    y2 = para(d, (col_x, y2),
              "BEIJING — A Pakistani astronaut has joined the crew of "
              "China's Tiangong space station, the first foreign national "
              "to fly aboard the orbital outpost. The payload specialist "
              "arrived on the Shenzhou-24 mission and will run science "
              "experiments in microgravity. Officials called the flight a "
              "milestone for Pakistan's space programme.",
              f_body, col_w, leading=20)

    # ---- three bottom stories --------------------------------------------
    rule(d, mx, 716, right, 2)
    bw3 = (right - mx - 48) // 3
    f_h3 = font(SERIF_B, 21)
    f_b3 = font(SERIF, 14)
    stories = [
        ("NASDAQ TUMBLES AS AI STOCKS SELL OFF",
         "Tech shares slide into the holiday break as investors weigh "
         "rates and earnings.",
         "chart"),
        ("INDIA MARKS 18 YEARS SINCE 26/11 ATTACKS",
         "Ceremonies across Mumbai honour the victims of the 2008 "
         "attacks, as the nation also marks Constitution Day.",
         None),
        ("AUSTRALIA, SOLOMONS SIGN SECURITY PACT",
         "The new treaty covers defence cooperation and regional "
         "stability. Leaders met in Honiara to seal the deal.",
         None),
    ]
    for i, (head, body, art) in enumerate(stories):
        x = mx + i * (bw3 + 24)
        if i:
            d.line([(x - 12, 730), (x - 12, 900)], fill=INK, width=1)
        yy = 730
        for line in wrap(d, head, f_h3, bw3):
            d.text((x, yy), line, font=f_h3, fill=INK)
            yy += 26
        if art == "chart":
            draw_chart(d, x, yy + 4, bw3, 56)
            yy += 66
        yy = para(d, (x, yy + 6), body, f_b3, bw3, leading=18)

    # ---- bottom ticker -----------------------------------------------------
    rule(d, mx, 922, right, 2)
    d.rectangle([mx, 936, right, 984], fill=INK)
    f_tick = font(SERIF_B, 14)
    tick = ("THANKSGIVING TRAVEL HIT BY STORMS  •  BANGLADESH RAISES "
            "GARMENT WAGE 36%  •  GUKESH DRAWS")
    tw = d.textlength(tick, font=f_tick)
    d.text(((W - tw) / 2, 948), tick, font=f_tick, fill=PAPER)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
