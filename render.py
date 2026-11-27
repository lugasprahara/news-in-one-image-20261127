#!/usr/bin/env python3
"""Render the news-image-20261127 entry: the world news of Friday 27 November
2026 in a single 1024x1024 image, in the "rich v2" house format.

Layout: paper background, teal + coral accents; the date huge at top-left; a
coral block with the story count; one wide hero panel; a 3x4 grid of story
panels; a strip of one-line briefs; a dark world map panel with numbered dots
matching the hero + panel numbers; a footer naming the sources.

Every story below was gathered from the day's reporting on 27 Nov 2026
(Reuters, AFP, Deutsche Welle, The Kyiv Independent, RFE/RL, Eco-Business,
ScienceDaily and the day's news digests). Run: python3 render.py
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 26
CONTENT_W = W - 2 * MARGIN

PAPER = (250, 246, 238)
INK = (30, 42, 50)
MUTED = (96, 104, 108)
TEAL = (11, 94, 99)
TEAL_SOFT = (233, 242, 239)
CORAL = (238, 90, 58)
PANEL_BG = (255, 255, 255)
BORDER = (216, 210, 196)
MAP_BG = (16, 42, 52)
LAND = (43, 94, 108)
DOT = (255, 122, 89)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
F_BOLD = f"{FONT_DIR}/LiberationSans-Bold.ttf"
F_REG = f"{FONT_DIR}/LiberationSans-Regular.ttf"


def font(size, bold=False):
    return ImageFont.truetype(F_BOLD if bold else F_REG, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, max_w, max_lines, start, min_size, bold=False):
    """Shrink the font until the wrapped text fits max_lines; return (font, lines)."""
    size = start
    while size > min_size:
        fnt = font(size, bold)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines, size
        size -= 1
    fnt = font(min_size, bold)
    return fnt, wrap(draw, text, fnt, max_w), min_size


# ---------------------------------------------------------------- stories ---
# (number, category, headline, summary) -- number 1 is the hero.
HERO = (
    "THE BIG STORY - MIDDLE EAST",
    "IRAN WAR WIDENS: TWO ITALIANS KILLED IN KUWAIT, TANKERS HIT MINES AT HORMUZ",
    "A drone strike on an air-defence site in Kuwait killed two Italian technicians; "
    "Kuwait and Italy blame Iran, which denies any role. Tehran says two tankers struck "
    "mines in the Strait of Hormuz, Brent crude climbed a third day to $96.57, and fears "
    "grow for the world's busiest oil route.",
)

PANELS = [
    (2, "EUROPE",
     "EU SUMMIT ENDS EARLY OVER UKRAINE LOAN",
     "Brussels summit ends a day early, still split over a 45bn-euro loan for Kyiv; "
     "the decision slips to December."),
    (3, "DIPLOMACY",
     "TRUMP PRESSES PUTIN AS KYIV BRACES",
     "Trump says he pressed Putin to pull back; Zelensky warns a new Russian mass "
     "strike is only days away."),
    (4, "WAR AT SEA",
     "UKRAINE HITS RUSSIAN SHIPS IN TWO SEAS",
     "Kyiv hits the cargo ship Sparta II off Finland and a corvette off Libya, far "
     "from the front line."),
    (5, "KOREA",
     "NORTH KOREA 'PAUSES' MISSILES FOR RUSSIA",
     "Ukrainian intelligence says Pyongyang has halted KN-23 missile deliveries "
     "to Moscow."),
    (6, "ECONOMY",
     "DE COS CHOSEN TO LEAD THE ECB",
     "European leaders pick Spain's Pablo Hernandez de Cos as the next president "
     "of the European Central Bank."),
    (7, "HEALTH",
     "CONGO EBOLA CASES PASS 12,000",
     "Cases pass 12,000 as fighting blocks aid teams from reaching patients in "
     "conflict zones."),
    (8, "BRITAIN",
     "UK NET MIGRATION LOWEST SINCE 1997",
     "Net migration drops to 77,000 in the year to June, down from a record "
     "944,000 in 2023."),
    (9, "UNITED STATES",
     "STORMS LEAVE A MILLION WITHOUT POWER",
     "Thanksgiving storms cut power to nearly a million homes; Macy's parade is "
     "postponed in New York."),
    (10, "AFRICA",
     "13 SOLDIERS KILLED IN NIGER ATTACK",
     "Gunmen hit a National Guard compound at Sanam, near the Mali border; 20 "
     "more soldiers are wounded."),
    (11, "NEW ZEALAND",
     "NZ COALITION ONE SEAT SHORT",
     "Final count gives the National-led bloc 65 of 130 seats, one short of "
     "governing alone."),
    (12, "TRADE",
     "PARTNERS REJECT US TARIFF CASE",
     "Trading partners reject Washington's new tariff case; the UN sees zero "
     "growth in sea trade."),
    (13, "SPORT",
     "THREE NFL FINISHES AT THE BUZZER",
     "Bills edge Chiefs 13-10 on a 57-yard kick; Bears and Eagles also win at "
     "the death on Thanksgiving."),
]

BRIEFS = [
    "DHAKA - Garment workers clash with police after rejecting a 36% wage rise as too little.",
    "OTTAWA - Canada's top court weighs Quebec's Bill 21 ban on religious symbols in public jobs.",
    "LONDON - Britain contacts 100,000 veterans to check military readiness.",
    "GAZA - Hamas weighs its response as Israeli strikes on the enclave escalate.",
    "WEST BANK - Israeli forces demolish some 50 structures in the farming village of Samra.",
    "BISSAU - Guinea-Bissau's transitional rulers postpone elections to November 2028.",
    "HASINA - Ousted Bangladeshi PM vows a 16 December return despite a death sentence.",
    "BUENOS AIRES - Argentina bars its central bank from printing money to fund spending.",
    "BERLIN - Germany plans borrowing above 210 billion euros in its 2027 budget.",
    "SEOUL - South Korean births jump 14.3% in nine months, a record rise.",
    "TAIWAN STRAIT - China tests an 800m floating bridge of civilian ships in landing drills.",
    "THE HAGUE - Netherlands vows to resist US curbs on ASML chip sales to China.",
    "CYBER - Microsoft: six hacker groups have adopted the ARTEX AI attack tool.",
    "PARIS - News agency AFP takes its content platform offline after a cyberattack.",
    "BOSTON - Harvard-led chip makes 120 times more UV light than earlier devices.",
    "SHIPPING - IMO members move to soften the industry's net-zero climate rules.",
    "BATUMI - Europa League game halted 30 minutes by clashes over a Palestinian flag.",
    "FINLAND - Campbell Wright is the first American to win a biathlon World Cup race.",
    "YEREVAN - Armenia says Russian border guards will fully withdraw in coming years.",
    "MARKETS - Bitcoin's long-dormant supply grows as the price hovers near $60,000.",
]

STORY_COUNT = 1 + len(PANELS) + len(BRIEFS)

# ------------------------------------------------------------- world map ----
# Coarse continent outlines as (lon, lat) polygons, drawn equirectangular.
LAND_POLYS = [
    # North America
    [(-168, 65), (-152, 70), (-140, 70), (-125, 71), (-112, 73), (-100, 73),
     (-93, 77), (-88, 72), (-84, 66), (-79, 69), (-76, 62), (-70, 58),
     (-64, 60), (-60, 55), (-64, 50), (-66, 45), (-70, 44), (-74, 40),
     (-76, 36), (-75, 32), (-80, 31), (-81, 26), (-84, 28), (-87, 30),
     (-90, 29), (-94, 29), (-97, 26), (-97, 20), (-94, 17), (-90, 14),
     (-86, 13), (-83, 9), (-79, 9), (-81, 13), (-84, 16), (-88, 16),
     (-91, 19), (-96, 16), (-102, 18), (-105, 21), (-108, 23), (-111, 26),
     (-114, 29), (-118, 33), (-122, 37), (-124, 42), (-124, 47), (-128, 52),
     (-133, 56), (-140, 60), (-152, 59), (-160, 58), (-166, 60)],
    # Greenland
    [(-46, 60), (-42, 65), (-32, 68), (-22, 70), (-19, 76), (-25, 80),
     (-40, 80), (-52, 78), (-56, 72), (-54, 66), (-52, 61)],
    # South America
    [(-77, 7), (-75, 10), (-72, 12), (-68, 11), (-62, 10), (-55, 6),
     (-51, 4), (-50, 1), (-44, -2), (-38, -5), (-35, -8), (-37, -11),
     (-39, -15), (-40, -21), (-45, -24), (-49, -28), (-52, -33), (-56, -38),
     (-60, -40), (-63, -42), (-65, -46), (-66, -50), (-68, -53), (-70, -54),
     (-72, -52), (-74, -49), (-74, -44), (-73, -39), (-72, -33), (-71, -28),
     (-70, -21), (-73, -16), (-76, -12), (-79, -7), (-81, -4), (-80, 1),
     (-78, 4), (-77, 6)],
    # Africa
    [(-17, 14), (-16, 19), (-15, 25), (-13, 28), (-10, 31), (-8, 33),
     (-6, 35), (-2, 35), (3, 37), (10, 37), (11, 34), (15, 32), (20, 32),
     (25, 32), (30, 31), (32, 30), (34, 28), (35, 24), (37, 22), (39, 20),
     (40, 16), (42, 13), (44, 11), (48, 11), (51, 11), (48, 8), (44, 4),
     (41, -1), (40, -6), (39, -12), (38, -18), (36, -22), (34, -26),
     (31, -30), (27, -33), (22, -35), (19, -34), (17, -31), (15, -27),
     (14, -22), (13, -17), (12, -13), (13, -8), (12, -4), (9, -1), (9, 3),
     (6, 4), (2, 6), (-3, 5), (-8, 4), (-12, 8), (-15, 11)],
    # Eurasia
    [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-5, 48), (-2, 50), (0, 51),
     (3, 53), (6, 53), (8, 55), (8, 57), (10, 58), (18, 56), (20, 58),
     (22, 60), (20, 62), (16, 64), (12, 66), (18, 68), (25, 71), (35, 70),
     (45, 68), (55, 68), (65, 69), (75, 71), (85, 73), (95, 76), (105, 77),
     (113, 74), (120, 73), (128, 72), (138, 72), (148, 71), (156, 70),
     (164, 70), (172, 67), (179, 66), (179, 63), (170, 61), (162, 59),
     (159, 53), (156, 51), (150, 46), (144, 44), (141, 41), (140, 37),
     (136, 35), (131, 33), (128, 33), (126, 36), (122, 37), (121, 34),
     (121, 30), (118, 26), (113, 23), (109, 20), (106, 17), (105, 10),
     (104, 6), (101, 6), (99, 9), (98, 13), (96, 16), (93, 18), (91, 22),
     (89, 22), (87, 21), (84, 19), (81, 16), (79, 13), (77, 9), (75, 12),
     (73, 17), (71, 21), (68, 23), (64, 25), (60, 25), (57, 26), (54, 27),
     (51, 29), (49, 30), (50, 27), (52, 25), (55, 25), (58, 23), (59, 22),
     (57, 19), (54, 17), (52, 15), (48, 14), (44, 13), (43, 12), (41, 16),
     (39, 20), (36, 24), (34, 28), (33, 30), (35, 32), (36, 36), (33, 36),
     (30, 36), (27, 37), (24, 38), (22, 38), (20, 40), (19, 42), (16, 41),
     (14, 42), (12, 44), (10, 44), (8, 44), (6, 43), (3, 43), (0, 39),
     (-2, 37), (-6, 36)],
    # Britain
    [(-5, 50), (-3, 52), (-3, 54), (-5, 56), (-4, 58), (-6, 58), (-8, 55),
     (-8, 53), (-6, 51)],
    # Iceland
    [(-22, 64), (-15, 64), (-14, 66), (-20, 66), (-23, 65)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 36), (141, 38),
     (141, 41), (142, 43), (143, 44), (145, 44), (143, 42), (141, 39),
     (140, 36), (138, 34), (135, 33), (132, 32)],
    # Indonesia / New Guinea pieces
    [(95, 5), (100, 1), (104, -2), (106, -5), (104, -4), (100, 0), (96, 4)],
    [(106, -6), (111, -7), (114, -8), (114, -9), (108, -8)],
    [(109, 1), (112, 3), (116, 4), (119, 2), (118, -1), (116, -3),
     (112, -3), (110, -1)],
    [(119, 0), (121, 1), (123, 0), (121, -2), (120, -4), (119, -2)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (149, -9), (147, -9),
     (142, -7), (137, -4), (132, -3)],
    # Philippines
    [(120, 13), (121, 15), (122, 17), (121, 18), (120, 16), (119, 14)],
    # Australia
    [(113, -22), (112, -26), (114, -31), (115, -34), (117, -35), (122, -34),
     (127, -32), (130, -32), (132, -32), (134, -33), (135, -35), (137, -35),
     (138, -36), (140, -38), (144, -38), (147, -38), (150, -37), (152, -33),
     (153, -29), (153, -25), (151, -21), (148, -19), (145, -15), (143, -13),
     (142, -11), (141, -15), (140, -18), (137, -16), (136, -13), (135, -12),
     (133, -11), (131, -12), (128, -13), (125, -15), (122, -17), (119, -20),
     (116, -21)],
    # New Zealand
    [(172, -41), (174, -39), (176, -37), (178, -38), (176, -40), (174, -42),
     (172, -43), (170, -45), (168, -47), (166, -46), (168, -43), (170, -42)],
    # Madagascar
    [(44, -13), (47, -14), (50, -16), (49, -19), (47, -22), (46, -25),
     (44, -25), (43, -21), (43, -17)],
]

# number -> (lon, lat, badge offset dx, dy)
DOTS = {
    1: (47.9, 29.4, 12, -2),      # hero: Kuwait / Hormuz
    2: (4.4, 50.8, 19, -16),      # Brussels
    3: (30.5, 50.5, 16, -4),      # Kyiv
    4: (19.5, 56.5, -6, -21),     # Baltic Sea
    5: (125.8, 39.0, 11, -4),     # Pyongyang
    6: (8.7, 50.1, 20, 16),       # Frankfurt
    7: (24.5, 0.5, 12, 2),        # DR Congo
    8: (-0.1, 51.5, -22, -16),    # London
    9: (-95.0, 37.0, -17, 9),     # US storms
    10: (7.5, 16.5, -15, 3),      # Niger
    11: (174.8, -41.3, -5, 12),   # Wellington
    12: (-77.0, 38.9, 13, 7),     # Washington
    13: (-83.1, 42.3, -11, -15),  # Detroit
}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- header ----
    d.text((MARGIN, 16), "27 NOVEMBER 2026", font=font(57, True), fill=INK)
    d.text((MARGIN, 88), "FRIDAY - THE WORLD IN ONE IMAGE",
           font=font(16, True), fill=TEAL)
    d.text((MARGIN, 88), "", font=font(16, True), fill=TEAL)
    # coral story-count block, top right
    bx0, by0, bx1, by1 = W - MARGIN - 162, 16, W - MARGIN, 102
    d.rectangle([bx0, by0, bx1, by1], fill=CORAL)
    num = str(STORY_COUNT)
    nf = font(42, True)
    nw = d.textlength(num, font=nf)
    d.text((bx0 + (162 - nw) / 2, by0 + 4), num, font=nf, fill=(255, 255, 255))
    sf = font(16, True)
    sw = d.textlength("STORIES", font=sf)
    d.text((bx0 + (162 - sw) / 2, by0 + 56), "STORIES", font=sf,
           fill=(255, 255, 255))
    d.rectangle([MARGIN, 112, W - MARGIN, 115], fill=TEAL)

    # ------------------------------------------------------------ hero ----
    hy0, hy1 = 124, 268
    d.rectangle([MARGIN, hy0, W - MARGIN, hy1], fill=TEAL_SOFT)
    d.rectangle([MARGIN, hy0, MARGIN + 8, hy1], fill=CORAL)
    hx = MARGIN + 26
    hw = W - MARGIN - hx
    d.text((hx, hy0 + 12), HERO[0], font=font(14, True), fill=CORAL)
    hf, hlines, _ = fit(d, HERO[1], hw, 2, 26, 20, bold=True)
    y = hy0 + 36
    for line in hlines:
        d.text((hx, y), line, font=hf, fill=INK)
        y += 30
    bf, blines, _ = fit(d, HERO[2], hw, 3, 15, 12)
    y += 4
    for line in blines:
        d.text((hx, y), line, font=bf, fill=INK)
        y += 19

    # ------------------------------------------------------------ grid ----
    gy0 = 280
    cols, rows = 3, 4
    gap = 10
    pw = (CONTENT_W - (cols - 1) * gap) // cols
    ph = 94
    for i, (num_, cat, head, summ) in enumerate(PANELS):
        r, c = divmod(i, cols)
        x0 = MARGIN + c * (pw + gap)
        y0 = gy0 + r * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rectangle([x0, y0, x1, y1], fill=PANEL_BG, outline=BORDER, width=1)
        d.rectangle([x0, y0, x1, y0 + 4], fill=TEAL if i % 2 == 0 else CORAL)
        # number chip
        cx, cy, cr = x0 + 17, y0 + 19, 10
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=CORAL)
        ns = str(num_)
        nf2 = font(11, True)
        d.text((cx - d.textlength(ns, font=nf2) / 2, cy - 7), ns, font=nf2,
               fill=(255, 255, 255))
        d.text((x0 + 34, y0 + 12), cat, font=font(11, True), fill=TEAL)
        inner_w = pw - 24
        hf2, hlines2, _ = fit(d, head, inner_w, 2, 15, 11, bold=True)
        y = y0 + 30
        for line in hlines2:
            d.text((x0 + 12, y), line, font=hf2, fill=INK)
            y += 18
        bf2, blines2, _ = fit(d, summ, inner_w, 2, 12, 9)
        y = y0 + 66
        for line in blines2:
            d.text((x0 + 12, y), line, font=bf2, fill=INK)
            y += 15

    # ------------------------------------------------- briefs + map -------
    by = gy0 + rows * ph + (rows - 1) * gap + 14  # 694
    d.text((MARGIN, by), "ALSO TODAY - AROUND THE WORLD IN BRIEF",
           font=font(14, True), fill=CORAL)
    briefs_x1 = 652
    col_w = (briefs_x1 - MARGIN - 12) // 2
    bf3 = font(11)
    row_h = 25
    for i, brief in enumerate(BRIEFS):
        r, c = divmod(i, 2)
        x0 = MARGIN + c * (col_w + 12)
        y0 = by + 26 + r * row_h
        lines = wrap(d, brief, bf3, col_w)
        ly = y0
        for line in lines[:2]:
            d.text((x0, ly), line, font=bf3, fill=INK)
            ly += 12

    # map panel
    mx0, my0, mx1, my1 = 664, by, W - MARGIN, 966
    d.rectangle([mx0, my0, mx1, my1], fill=MAP_BG)
    d.text((mx0 + 14, my0 + 10), "WHERE IT HAPPENED", font=font(13, True),
           fill=(255, 255, 255))
    map_x0, map_y0 = mx0 + 10, my0 + 36
    map_x1, map_y1 = mx1 - 10, my1 - 30
    lon0, lon1 = -168, 192
    lat_top, lat_bot = 82, -60

    def proj(lon, lat):
        x = map_x0 + (lon - lon0) / (lon1 - lon0) * (map_x1 - map_x0)
        yy = map_y0 + (lat_top - lat) / (lat_top - lat_bot) * (map_y1 - map_y0)
        return x, yy

    for poly in LAND_POLYS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND)
    nf3 = font(10, True)
    for num_, (lon, lat, dx, dy) in DOTS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=DOT)
        bx, byy = px + dx, py + dy
        if (bx, byy) != (px, py):
            d.line([px, py, bx, byy], fill=DOT, width=1)
        r = 9
        d.ellipse([bx - r, byy - r, bx + r, byy + r], fill=CORAL,
                  outline=(255, 255, 255), width=1)
        ns = str(num_)
        d.text((bx - d.textlength(ns, font=nf3) / 2, byy - 6), ns, font=nf3,
               fill=(255, 255, 255))
    d.text((mx0 + 14, my1 - 22), "Dots match the story numbers above.",
           font=font(10), fill=(178, 205, 211))

    # ---------------------------------------------------------- footer ----
    d.rectangle([MARGIN, 978, W - MARGIN, 980], fill=BORDER)
    d.text((MARGIN, 988),
           "Sources: Reuters - AFP - Deutsche Welle - The Kyiv Independent - "
           "RFE/RL - Eco-Business - ScienceDaily",
           font=font(11), fill=MUTED)
    right = "make.fun - news-image-20261127"
    rf = font(11)
    d.text((W - MARGIN - d.textlength(right, font=rf), 988), right, font=rf,
           fill=MUTED)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
