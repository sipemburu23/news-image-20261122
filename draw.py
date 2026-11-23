#!/usr/bin/env python3
"""Draw the news-image-20261122 front page: 'The World in One Day' --
Sunday 22 November 2026. 33 stories, 13 drawn. Original code, written
from scratch for this edition (layout modelled on the ed-21 v4 front page,
all scenes and all text new). Renders entry.png (1024x1024)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

# ---- palette: light cream paper, dark ink (ed-21 lesson: no dark boxes) ----
CREAM = (245, 240, 230)
CREAM2 = (238, 231, 214)
INK = (28, 23, 16)
INK_SOFT = (74, 66, 54)
RED = (140, 29, 24)
NAVY = (34, 64, 94)
NAVY_LT = (217, 226, 236)
GOLD = (184, 138, 47)
GOLD_LT = (232, 217, 168)
SAGE = (223, 232, 217)
SAGE_DK = (120, 150, 120)
LAND = (63, 109, 82)
LAND_DK = (46, 84, 62)
SEA = (233, 226, 207)
RULE = (196, 182, 152)
WHITE = (252, 250, 245)
TAG_BG = (232, 224, 200)

F_DEJAVU = "/usr/share/fonts/truetype/dejavu"
F_LIB = "/usr/share/fonts/truetype/liberation"
F_PLAYFAIR = os.path.join(HERE, "fonts", "PlayfairDisplay.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


def serif_b(size):
    return F(f"{F_DEJAVU}/DejaVuSerif-Bold.ttf", size)


def serif(size):
    return F(f"{F_DEJAVU}/DejaVuSerif.ttf", size)


def serif_i(size):
    return F(f"{F_LIB}/LiberationSerif-Italic.ttf", size)


def sans(size):
    return F(f"{F_LIB}/LiberationSans-Regular.ttf", size)


def sans_b(size):
    return F(f"{F_LIB}/LiberationSans-Bold.ttf", size)


def playfair(size):
    return F(F_PLAYFAIR, size)


# ---- text helpers -----------------------------------------------------------
def wrap(text, font, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, font, fill, lh, align="left", width=None):
    """Draw wrapped lines; returns y just below the last line."""
    for ln in lines:
        if align == "center" and width is not None:
            d.text((x + (width - font.getlength(ln)) / 2, y), ln, font=font, fill=fill)
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def text_h(lines, lh):
    return len(lines) * lh


# ---- content (facts from research only) -------------------------------------
LEADS = [
    {
        "n": 1,
        "scene": "cop31day",
        "headline": "COP31 collapses \u2014 no deal in Antalya",
        "deck": ("After a record ~44 hours of overtime, the EU and a host of "
                 "nations reject the Antalya Pact \u2014 the first COP to end "
                 "without a deal since 2009."),
        "tag": "CONFIRMED \u00b7 Reuters / AP",
    },
    {
        "n": 2,
        "scene": "hormuz",
        "headline": "Two tankers hit by mines near Hormuz",
        "deck": ("Iran\u2019s Revolutionary Guard says two supertankers caught "
                 "fire north of Ghanam Island; one huge carrier is claimed "
                 "sunk \u2014 a claim no one else has confirmed."),
        "tag": "REPORTED \u00b7 IRGC claim",
    },
    {
        "n": 3,
        "scene": "dymer",
        "headline": "Drone flattens flats in Dymer \u2014 boy, 7, pulled alive",
        "deck": ("A Russian drone destroys part of a five-storey block near "
                 "Kyiv before dawn; rescuers pull 7-year-old Davyd alive "
                 "from the rubble after about 14 hours."),
        "tag": "CONFIRMED \u00b7 BBC / AP",
    },
]

CARDS = [
    {
        "n": 4, "scene": "dems",
        "headline": "Democrats take 258 House seats",
        "deck": "Hubbard flips NC-5 by ~330 votes \u2014 the largest Dem majority since 1992.",
        "tag": "CONFIRMED",
    },
    {
        "n": 5, "scene": "merkury",
        "headline": "Russian corvette hit off Benghazi",
        "deck": "Suspected drone strike sets the Merkury ablaze; 10+ wounded.",
        "tag": "REPORTED",
    },
    {
        "n": 6, "scene": "candy",
        "headline": "34 missing in Indonesia candy factory fire",
        "deck": "A candy factory fire in Cikande leaves 3 dead and 34 missing.",
        "tag": "CONFIRMED",
    },
    {
        "n": 7, "scene": "alcaraz",
        "headline": "Alcaraz wins first ATP Finals title",
        "deck": "Alcaraz beats Zverev 6-2, 7-6(7) \u2014 a 5-0 week and a record $5.171m.",
        "tag": "CONFIRMED",
    },
    {
        "n": 8, "scene": "shuri",
        "headline": "Shuri Castle rises again after 7 years",
        "deck": "Okinawa\u2019s Seiden hall restored seven years after the 2019 fire.",
        "tag": "CONFIRMED",
    },
    {
        "n": 9, "scene": "nepal",
        "headline": "Nepal\u2019s PM lands in New Delhi",
        "deck": "Shah, 36, arrives on his first bilateral trip since taking office.",
        "tag": "CONFIRMED",
    },
    {
        "n": 10, "scene": "westbank",
        "headline": "Settlers burn 12 cars in West Bank",
        "deck": "Arson hits five villages; Eisenkot calls it \u201cJewish terrorism\u201d.",
        "tag": "CONFIRMED \u00b7 Eisenkot",
    },
    {
        "n": 11, "scene": "lowy",
        "headline": "US\u2013China power gap narrows to 5.3",
        "deck": "The Lowy Index records the smallest US lead over China since 2018.",
        "tag": "CONFIRMED \u00b7 Lowy Institute",
    },
    {
        "n": 12, "scene": "nvidia",
        "headline": "Bessent presses Nvidia on China chips",
        "deck": "Bessent seeks answers on chip sales to China; 879,868 were approved.",
        "tag": "OFFICIAL",
    },
    {
        "n": 13, "scene": "cricket",
        "headline": "India piles up 720/9 in Wellington",
        "deck": "India declares 720/9, a record in New Zealand; hosts close on 119/2.",
        "tag": "CONFIRMED",
    },
]

BRIEFS = [
    (14, "Delta outage delays 1,600+ flights"),
    (15, "China cuts margin ratio to 80%"),
    (16, "Drone strikes kill 4 in Khartoum"),
    (17, "Ebola response hit by Congo fighting"),
    (18, "Molly Meldrum dies aged 83"),
    (19, "Australia\u2019s flash PMI falls to 46.1"),
    (20, "Poland: Russia tried to kill Kyivstoner"),
    (21, "Iran unveils double missile launcher"),
    (22, "BJP MP Wadkute dies at 72"),
    (23, "Bessent warns Fed not to overtighten"),
    (24, "Army to detonate lead azide in Iowa"),
    (25, "India, China conclude border talks"),
    (26, "S. Korea education minister quits"),
    (27, "Thitikul wins third straight $4m title"),
    (28, "Brazil storm toll: 5 dead, 25,212 hit"),
    (29, "Peru quake: 1 dead, 152 homes lost"),
    (30, "FBI probes suspected NCIC hack"),
    (31, "Poland: all three objects were Kh-101s"),
    (32, "Liverpool thrash 10-man United 4-0"),
    (33, "Price wins fourth Grand Slam of Darts"),
]

NUMBERS = [
    ("44", "hours COP31 ran overtime, a record"),
    ("258", "Democratic seats in the US House"),
    ("1,600+", "Delta flights delayed by an outage"),
    ("34", "workers missing in the Indonesia fire"),
    ("$5.171m", "Alcaraz\u2019s record winner\u2019s payout"),
    ("5.3", "points, the narrowest US\u2013China gap since 2018"),
]

TIMELINE = [
    ("~00:00 UTC", "COP31 releases its third draft; settlers burn cars"),
    ("02:30 UTC", "Seoul: Education Minister Choi offers to resign"),
    ("03:00 UTC", "Dymer: a Russian drone hits a five-storey block"),
    ("~05:00 UTC", "Wellington: India declares 720/9; NZ closes on 119/2"),
    ("13:12 UTC", "Okinawa: the Shuri Castle restoration ceremony"),
    ("~17:00 UTC", "Turin: Alcaraz beats Zverev for his first ATP title"),
    ("20:30 UTC", "Atlanta: Delta restores systems after 1,600+ delays"),
]

REGIONS = [("ASIA", 8), ("AMERICAS", 8), ("EUROPE", 6), ("AFRICA", 3),
           ("OCEANIA", 3), ("MIDDLE EAST", 3), ("GLOBAL", 2)]

DATECHECK = (
    "Left out as Saturday 21 November\u2019s news: Iran\u2019s missile strike "
    "on US bases in Bahrain, COP31 still in overtime with no deal, the "
    "capture of \u2018El Chapo Isidro\u2019 in Sinaloa, Trump\u2019s 10% "
    "credit-card cap pledge, the ICE arrests on a Seattle jet bridge, "
    "Taiwan\u2019s warning to Canada, the NYT report on China\u2019s spy agency "
    "chasing AI chips, Paolo Bulgari\u2019s death at 89, the Scott Reef "
    "festival in Perth, and cricketer Yuzvendra Chahal joining the BJP."
)
NOTYET = ("Not yet: Kyiv\u2019s confirmation that sea drones sank the Merkury, "
          "the Dymer toll rising to 11, and the India\u2013New Zealand Test "
          "ending in a draw.")

FOOTER1 = ("Sources: Reuters, AP, BBC, Al Jazeera, Lowy Institute, ATP, LPGA, "
           "WHO, CDC, COEN-INDECI, UKMTO, CBS, The Indian Express.")
FOOTER2 = ("Every story from Sunday 22 November 2026 \u00b7 Claims are labelled "
           "CONFIRMED / OFFICIAL / REPORTED / FORECAST \u00b7 See DATE CHECK "
           "for what was left out.")


# ---- scene painters (all original vector drawings, all BRIGHT daylight) ----
def _sky(d, box, top, bottom):
    x0, y0, x1, y1 = box
    for i in range(y1 - y0):
        t = i / max(1, (y1 - y0 - 1))
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def _sun(d, x, y, r=12):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 214, 110))
    d.ellipse([x - r + 4, y - r + 4, x + r - 4, y + r - 4], fill=(255, 236, 170))
    for dx, dy in [(0, -r - 5), (0, r + 5), (-r - 5, 0), (r + 5, 0)]:
        d.line([(x, y), (x + dx, y + dy)], fill=(255, 214, 110), width=2)


def scene_cop31day(d, box):
    # Bright plenary hall in daylight: sun through big windows, flags,
    # podium with gavel, delegates walking out.
    _sky(d, box, (168, 205, 232), (232, 226, 204))
    x0, y0, x1, y1 = box
    _sun(d, x1 - 34, y0 + 18, 11)
    # big windows with blue sky
    for wx in (x0 + 12, x0 + 66, x0 + 120):
        d.rectangle([wx, y0 + 8, wx + 44, y0 + 40], fill=(150, 196, 228))
        d.rectangle([wx, y0 + 8, wx + 44, y0 + 40], outline=(120, 100, 70), width=2)
        d.line([(wx + 22, y0 + 8), (wx + 22, y0 + 40)], fill=(120, 100, 70), width=1)
    # sunbeams through the windows
    d.polygon([(x0 + 20, y0 + 40), (x0 + 52, y0 + 40), (x0 + 84, y1 - 10), (x0 + 44, y1 - 10)],
              fill=(255, 240, 190))
    # screen: COP31
    d.rectangle([x0 + 176, y0 + 10, x1 - 14, y0 + 40], fill=(34, 64, 94))
    d.rectangle([x0 + 176, y0 + 10, x1 - 14, y0 + 40], outline=(250, 244, 220), width=2)
    d.text((x0 + 186, y0 + 16), "COP31", font=sans_b(18), fill=(250, 244, 220))
    # flags row
    for i, col in enumerate([(200, 60, 50), (40, 90, 160), (240, 200, 60),
                             (60, 140, 90), (150, 60, 140), (220, 120, 40)]):
        fx = x0 + 180 + i * 20
        d.rectangle([fx, y0 + 46, fx + 14, y0 + 54], fill=col)
        d.line([(fx + 7, y0 + 46), (fx + 7, y0 + 60)], fill=(90, 70, 50), width=1)
    # podium with gavel + speaker
    d.rectangle([x0 + 120, y0 + 56, x0 + 168, y1 - 12], fill=(120, 90, 60))
    d.rectangle([x0 + 120, y0 + 56, x0 + 168, y0 + 62], fill=(90, 66, 44))
    d.ellipse([x0 + 138, y0 + 40, x0 + 150, y0 + 52], fill=(60, 48, 40))
    d.rectangle([x0 + 134, y0 + 50, x0 + 154, y1 - 12], fill=(40, 50, 70))
    d.line([(x0 + 160, y0 + 52), (x0 + 172, y0 + 46)], fill=(90, 66, 44), width=3)
    d.ellipse([x0 + 170, y0 + 42, x0 + 176, y0 + 48], fill=(90, 66, 44))
    # delegates: rows of desks and heads, some standing to leave
    for row, ry in enumerate((y1 - 30, y1 - 14)):
        for cx in range(x0 + 10, x0 + 110, 22):
            d.ellipse([cx, ry - 6, cx + 8, ry + 2], fill=(60, 48, 40) if row else (90, 70, 52))
            d.rectangle([cx - 4, ry + 2, cx + 12, ry + 8], fill=(120, 90, 60))
    for cx in range(x1 - 96, x1 - 10, 24):
        d.ellipse([cx, y1 - 40, cx + 8, y1 - 32], fill=(60, 48, 40))
        d.rectangle([cx - 4, y1 - 32, cx + 12, y1 - 12], fill=(90, 70, 52))
    d.rectangle([x0, y1 - 4, x1, y1], fill=(96, 72, 48))


def scene_hormuz(d, box):
    # Bright blue sea in daylight: two supertankers, black smoke from one,
    # small patrol boat, hilly coast in the distance.
    _sky(d, box, (140, 198, 232), (214, 232, 240))
    x0, y0, x1, y1 = box
    _sun(d, x0 + 30, y0 + 16, 10)
    # distant hilly coast
    d.polygon([(x0, y1 - 40), (x0 + 60, y1 - 62), (x0 + 130, y1 - 46),
               (x0 + 200, y1 - 60), (x1, y1 - 42), (x1, y1 - 34), (x0, y1 - 34)],
              fill=(150, 160, 140))
    # sea
    d.rectangle([x0, y1 - 36, x1, y1], fill=(52, 104, 138))
    for wy in (y1 - 28, y1 - 18, y1 - 8):
        for wx in range(x0 + 6, x1 - 6, 34):
            d.arc([wx, wy - 4, wx + 22, wy + 4], start=200, end=340, fill=(220, 235, 240), width=2)
    # tanker 1 (left, smoking)
    sx0, sy = x0 + 30, y1 - 56
    d.polygon([(sx0, sy), (sx0 + 110, sy), (sx0 + 102, sy + 20), (sx0 + 8, sy + 20)],
              fill=(140, 40, 32))
    d.rectangle([sx0 + 14, sy - 16, sx0 + 40, sy], fill=(240, 238, 230))
    d.rectangle([sx0 + 46, sy - 16, sx0 + 72, sy], fill=(200, 170, 90))
    d.rectangle([sx0 + 78, sy - 16, sx0 + 100, sy], fill=(90, 120, 90))
    # black smoke column + fire
    d.ellipse([sx0 + 46, sy - 46, sx0 + 74, sy - 16], fill=(70, 66, 62))
    d.ellipse([sx0 + 56, sy - 58, sx0 + 82, sy - 30], fill=(90, 86, 82))
    d.ellipse([sx0 + 52, sy - 26, sx0 + 66, sy - 12], fill=(255, 150, 50))
    d.ellipse([sx0 + 56, sy - 20, sx0 + 64, sy - 12], fill=(255, 210, 110))
    # tanker 2 (right, intact)
    tx0, ty = x1 - 130, y1 - 52
    d.polygon([(tx0, ty), (tx0 + 100, ty), (tx0 + 92, ty + 18), (tx0 + 8, ty + 18)],
              fill=(60, 70, 90))
    d.rectangle([tx0 + 12, ty - 14, tx0 + 36, ty], fill=(240, 238, 230))
    d.rectangle([tx0 + 42, ty - 14, tx0 + 64, ty], fill=(200, 170, 90))
    d.rectangle([tx0 + 68, ty - 26, tx0 + 84, ty - 14], fill=(240, 238, 230))
    # small patrol boat
    d.polygon([(x1 - 44, y1 - 12), (x1 - 16, y1 - 12), (x1 - 22, y1 - 4), (x1 - 38, y1 - 4)],
              fill=(230, 140, 40))
    d.rectangle([x1 - 38, y1 - 20, x1 - 24, y1 - 12], fill=(250, 248, 242))


def scene_dymer(d, box):
    # Bright daylight rescue in the rubble: blue sky, broken apartment
    # block, orange rescue workers lifting a child, excavator arm.
    _sky(d, box, (150, 200, 234), (228, 230, 208))
    x0, y0, x1, y1 = box
    _sun(d, x1 - 30, y0 + 16, 10)
    # ruined apartment block: standing part + collapsed slabs
    d.rectangle([x0 + 14, y0 + 18, x0 + 110, y1 - 12], fill=(196, 182, 160))
    for wy in (y0 + 30, y0 + 46, y0 + 62):
        for wx in (x0 + 24, x0 + 54, x0 + 84):
            d.rectangle([wx, wy, wx + 16, wy + 10], fill=(120, 160, 190))
    d.rectangle([x0 + 14, y0 + 18, x0 + 110, y0 + 24], fill=(150, 60, 48))
    # collapsed section: tilted slabs + dust
    d.polygon([(x0 + 116, y1 - 12), (x0 + 150, y1 - 44), (x0 + 178, y1 - 12)], fill=(170, 152, 128))
    d.polygon([(x0 + 150, y1 - 44), (x0 + 186, y1 - 60), (x0 + 196, y1 - 12)], fill=(150, 132, 108))
    d.ellipse([x0 + 190, y1 - 34, x0 + 220, y1 - 12], fill=(220, 205, 180))
    d.ellipse([x0 + 210, y1 - 26, x0 + 232, y1 - 10], fill=(228, 214, 190))
    # excavator arm
    d.line([(x1 - 70, y1 - 12), (x1 - 40, y1 - 52)], fill=(240, 180, 40), width=5)
    d.line([(x1 - 40, y1 - 52), (x1 - 18, y1 - 34)], fill=(240, 180, 40), width=4)
    d.rectangle([x1 - 84, y1 - 26, x1 - 56, y1 - 12], fill=(240, 180, 40))
    # rescue workers in orange lifting a child on a stretcher
    for wx in (x0 + 130, x0 + 168):
        d.ellipse([wx, y1 - 34, wx + 8, y1 - 26], fill=(240, 200, 160))
        d.rectangle([wx - 2, y1 - 26, wx + 10, y1 - 12], fill=(240, 110, 30))
    d.rectangle([x0 + 128, y1 - 22, x0 + 182, y1 - 18], fill=(200, 200, 190))
    d.ellipse([x0 + 150, y1 - 28, x0 + 158, y1 - 22], fill=(240, 200, 160))
    d.rectangle([x0 + 146, y1 - 22, x0 + 164, y1 - 18], fill=(120, 160, 200))
    # onlookers + ground
    d.rectangle([x0, y1 - 8, x1, y1], fill=(150, 130, 100))
    for ox in (x0 + 220, x0 + 244, x0 + 268):
        d.ellipse([ox, y1 - 26, ox + 7, y1 - 19], fill=(90, 70, 60))
        d.rectangle([ox - 1, y1 - 19, ox + 8, y1 - 8], fill=(90, 110, 140))


def scene_dems(d, box):
    # Bright polling scene: ballot box, ballot papers, US flag stripes.
    _sky(d, box, (210, 228, 240), (240, 232, 212))
    x0, y0, x1, y1 = box
    # flag stripes on the wall
    for i, col in enumerate([(180, 40, 40), (250, 250, 248)] * 3):
        d.rectangle([x0 + 14, y0 + 10 + i * 8, x1 - 14, y0 + 18 + i * 8], fill=col)
    d.rectangle([x0 + 14, y0 + 10, x0 + 66, y0 + 34], fill=(34, 64, 120))
    for sy in (y0 + 14, y0 + 22, y0 + 30):
        for sx in (x0 + 20, x0 + 32, x0 + 44, x0 + 56):
            d.ellipse([sx, sy, sx + 2, sy + 2], fill=(250, 250, 248))
    # ballot box
    d.rectangle([x0 + 110, y0 + 46, x0 + 210, y1 - 12], fill=(34, 64, 120))
    d.rectangle([x0 + 110, y0 + 46, x0 + 210, y0 + 54], fill=(24, 48, 90))
    d.rectangle([x0 + 146, y0 + 48, x0 + 174, y0 + 52], fill=(20, 20, 24))
    d.text((x0 + 126, y0 + 62), "VOTE", font=sans_b(16), fill=(250, 250, 248))
    # ballot paper going in + checkmark
    d.polygon([(x0 + 146, y0 + 30), (x0 + 174, y0 + 30), (x0 + 174, y0 + 48),
               (x0 + 146, y0 + 48)], fill=(252, 250, 244))
    d.line([(x0 + 150, y0 + 38), (x0 + 156, y0 + 44), (x0 + 170, y0 + 32)],
           fill=(40, 140, 60), width=3)
    # second ballot + hand
    d.rectangle([x0 + 220, y0 + 52, x0 + 262, y0 + 80], fill=(252, 250, 244))
    d.line([(x0 + 224, y0 + 60), (x0 + 258, y0 + 60)], fill=(120, 110, 96), width=1)
    d.line([(x0 + 224, y0 + 68), (x0 + 250, y0 + 68)], fill=(120, 110, 96), width=1)
    d.rectangle([x0, y1 - 6, x1, y1], fill=(120, 100, 70))


def scene_merkury(d, box):
    # Bright blue sea: grey corvette smoking, small fire, drones in sky.
    _sky(d, box, (150, 200, 232), (222, 230, 238))
    x0, y0, x1, y1 = box
    _sun(d, x0 + 28, y0 + 14, 9)
    d.rectangle([x0, y1 - 34, x1, y1], fill=(64, 110, 140))
    for wy in (y1 - 28, y1 - 18, y1 - 8):
        for wx in range(x0 + 6, x1 - 6, 34):
            d.arc([wx, wy - 4, wx + 22, wy + 4], start=200, end=340, fill=(220, 235, 240), width=2)
    # corvette
    sx0, sy = x0 + 40, y1 - 54
    d.polygon([(sx0, sy), (sx0 + 120, sy), (sx0 + 112, sy + 20), (sx0 + 8, sy + 20)],
              fill=(110, 116, 122))
    d.rectangle([sx0 + 16, sy - 14, sx0 + 44, sy], fill=(240, 238, 230))
    d.rectangle([sx0 + 50, sy - 14, sx0 + 78, sy], fill=(90, 120, 90))
    d.rectangle([sx0 + 84, sy - 24, sx0 + 100, sy - 14], fill=(240, 238, 230))
    d.rectangle([sx0 + 88, sy - 34, sx0 + 92, sy - 24], fill=(90, 90, 90))
    # smoke + fire amidships
    d.ellipse([sx0 + 52, sy - 44, sx0 + 80, sy - 14], fill=(90, 84, 78))
    d.ellipse([sx0 + 62, sy - 56, sx0 + 88, sy - 28], fill=(110, 104, 98))
    d.ellipse([sx0 + 58, sy - 24, sx0 + 72, sy - 10], fill=(255, 150, 50))
    d.ellipse([sx0 + 62, sy - 18, sx0 + 70, sy - 10], fill=(255, 210, 110))
    # drones in the sky
    for (dx, dy) in [(x1 - 60, y0 + 14), (x1 - 34, y0 + 26), (x0 + 24, y0 + 18)]:
        d.ellipse([dx - 4, dy - 3, dx + 4, dy + 3], fill=(30, 30, 34))
        d.line([(dx - 9, dy), (dx + 9, dy)], fill=(30, 30, 34), width=1)
    # listing to one side + lifeboat
    d.polygon([(x1 - 46, y1 - 12), (x1 - 18, y1 - 12), (x1 - 24, y1 - 4), (x1 - 40, y1 - 4)],
              fill=(230, 140, 40))


def scene_candy(d, box):
    # Bright daylight factory fire: factory building, smoke, fire truck.
    _sky(d, box, (170, 208, 234), (232, 228, 208))
    x0, y0, x1, y1 = box
    _sun(d, x1 - 30, y0 + 14, 9)
    # factory building
    d.rectangle([x0 + 20, y0 + 34, x0 + 180, y1 - 14], fill=(200, 190, 170))
    d.rectangle([x0 + 20, y0 + 34, x0 + 180, y0 + 42], fill=(150, 60, 48))
    d.text((x0 + 34, y0 + 44), "PT FONUSA", font=sans_b(11), fill=(90, 70, 60))
    for wx in (x0 + 34, x0 + 66, x0 + 98, x0 + 130):
        d.rectangle([wx, y0 + 60, wx + 20, y0 + 74], fill=(120, 160, 190))
    d.rectangle([x0 + 20, y0 + 24, x0 + 34, y0 + 34], fill=(120, 110, 100))
    # smoke column
    d.ellipse([x0 + 100, y0 + 2, x0 + 132, y0 + 30], fill=(100, 94, 88))
    d.ellipse([x0 + 116, y0 - 6, x0 + 148, y0 + 20], fill=(120, 114, 108))
    d.ellipse([x0 + 130, y0 - 12, x0 + 158, y0 + 10], fill=(140, 134, 128))
    # fire truck with ladder
    d.rectangle([x1 - 92, y1 - 30, x1 - 16, y1 - 12], fill=(200, 40, 36))
    d.rectangle([x1 - 92, y1 - 30, x1 - 66, y1 - 12], fill=(220, 220, 214))
    d.ellipse([x1 - 82, y1 - 12, x1 - 72, y1 - 2], fill=(12, 12, 12))
    d.ellipse([x1 - 30, y1 - 12, x1 - 20, y1 - 2], fill=(12, 12, 12))
    d.line([(x1 - 70, y1 - 30), (x1 - 30, y0 + 26)], fill=(220, 220, 214), width=3)
    # hose water arc
    d.arc([x0 + 200, y0 + 30, x0 + 260, y0 + 70], start=300, end=20,
          fill=(150, 200, 230), width=2)
    # firefighters
    for fx in (x0 + 40, x0 + 64):
        d.ellipse([fx, y1 - 28, fx + 7, y1 - 21], fill=(240, 200, 160))
        d.rectangle([fx - 1, y1 - 21, fx + 8, y1 - 10], fill=(240, 180, 40))
    d.rectangle([x0, y1 - 6, x1, y1], fill=(120, 110, 96))


def scene_alcaraz(d, box):
    # Bright indoor tennis court: teal court, player lifting a gold trophy.
    _sky(d, box, (214, 230, 238), (240, 232, 214))
    x0, y0, x1, y1 = box
    # arena stands
    for row, ry in enumerate((y0 + 8, y0 + 20)):
        for cx in range(x0 + 10, x1 - 10, 18):
            d.ellipse([cx, ry, cx + 6, ry + 6], fill=(90, 90, 110) if row else (140, 140, 160))
    # court
    d.rectangle([x0, y1 - 40, x1, y1], fill=(40, 130, 110))
    d.rectangle([x0, y1 - 40, x1, y1 - 34], fill=(250, 250, 248))
    d.line([(x0, y1 - 22), (x1, y1 - 22)], fill=(250, 250, 248), width=1)
    # net
    d.line([(x0 + 120, y1 - 40), (x1 - 40, y1 - 40)], fill=(40, 40, 44), width=2)
    d.rectangle([x0 + 120, y1 - 46, x1 - 40, y1 - 40], fill=(250, 250, 248))
    # player lifting trophy
    px = x0 + 60
    d.ellipse([px, y1 - 66, px + 10, y1 - 56], fill=(200, 160, 120))
    d.rectangle([px - 2, y1 - 56, px + 12, y1 - 40], fill=(250, 250, 248))
    d.line([(px + 2, y1 - 54), (px - 8, y1 - 72)], fill=(200, 160, 120), width=3)
    d.line([(px + 8, y1 - 54), (px + 18, y1 - 72)], fill=(200, 160, 120), width=3)
    # gold trophy
    d.ellipse([px + 8, y1 - 84, px + 24, y1 - 70], fill=(255, 200, 60))
    d.rectangle([px + 13, y1 - 70, px + 19, y1 - 64], fill=(220, 160, 40))
    d.arc([px + 4, y1 - 84, px + 14, y1 - 70], start=90, end=270, fill=(255, 200, 60), width=2)
    d.arc([px + 18, y1 - 84, px + 28, y1 - 70], start=270, end=90, fill=(255, 200, 60), width=2)
    # tennis ball + racket
    d.ellipse([x1 - 40, y1 - 58, x1 - 28, y1 - 46], fill=(200, 230, 60))
    d.ellipse([x1 - 60, y0 + 44, x1 - 44, y0 + 60], fill=(60, 60, 66))
    d.line([(x1 - 52, y0 + 60), (x1 - 40, y1 - 44)], fill=(120, 90, 60), width=3)


def scene_shuri(d, box):
    # Bright vermilion castle under a blue sky: red tiled roof, white
    # walls, stone steps, guests, green trees.
    _sky(d, box, (140, 198, 232), (228, 232, 210))
    x0, y0, x1, y1 = box
    _sun(d, x1 - 28, y0 + 14, 10)
    # green hill
    d.polygon([(x0, y1 - 24), (x0 + 90, y1 - 52), (x0 + 200, y1 - 50), (x1, y1 - 26),
               (x1, y1), (x0, y1)], fill=(110, 160, 100))
    # castle: white walls + vermilion roof
    d.rectangle([x0 + 84, y0 + 34, x0 + 236, y1 - 24], fill=(252, 248, 240))
    d.rectangle([x0 + 84, y0 + 34, x0 + 236, y0 + 40], fill=(190, 60, 44))
    d.polygon([(x0 + 76, y0 + 34), (x0 + 160, y0 + 12), (x0 + 244, y0 + 34)],
              fill=(200, 50, 40))
    d.rectangle([x0 + 76, y0 + 32, x0 + 244, y0 + 36], fill=(150, 40, 32))
    # roof ridge ornaments
    d.ellipse([x0 + 152, y0 + 6, x0 + 168, y0 + 16], fill=(255, 200, 60))
    # windows + door
    for wx in (x0 + 100, x0 + 132, x0 + 188, x0 + 220):
        d.rectangle([wx, y0 + 48, wx + 12, y0 + 62], fill=(90, 60, 50))
    d.rectangle([x0 + 152, y0 + 56, x0 + 168, y1 - 24], fill=(120, 70, 50))
    # stone steps
    for i in range(4):
        d.rectangle([x0 + 140 - i * 6, y1 - 24 + i * 5, x0 + 180 + i * 6, y1 - 19 + i * 5],
                    fill=(200, 190, 170))
    # guests
    for gx in (x0 + 30, x0 + 52, x1 - 44, x1 - 22):
        d.ellipse([gx, y1 - 30, gx + 7, y1 - 23], fill=(60, 48, 40))
        d.rectangle([gx - 1, y1 - 23, gx + 8, y1 - 12], fill=(200, 60, 50))
    # pine trees
    for tx in (x0 + 12, x1 - 16):
        d.polygon([(tx, y1 - 50), (tx + 8, y1 - 70), (tx + 16, y1 - 50)], fill=(50, 110, 60))
        d.rectangle([tx + 6, y1 - 50, tx + 10, y1 - 40], fill=(90, 70, 50))


def scene_nepal(d, box):
    # Bright airport arrival: white plane landing, runway, Nepal + India flags.
    _sky(d, box, (150, 200, 234), (230, 228, 208))
    x0, y0, x1, y1 = box
    _sun(d, x0 + 28, y0 + 14, 9)
    # clouds
    for (cx, cy) in [(x0 + 90, y0 + 14), (x0 + 200, y0 + 22)]:
        d.ellipse([cx, cy, cx + 34, cy + 10], fill=(250, 250, 248))
        d.ellipse([cx + 10, cy - 5, cx + 26, cy + 6], fill=(250, 250, 248))
    # plane
    px, py = x0 + 150, y0 + 40
    d.ellipse([px - 60, py - 10, px + 60, py + 10], fill=(250, 250, 248))
    d.polygon([(px + 56, py - 8), (px + 88, py - 20), (px + 88, py - 6)], fill=(230, 230, 224))
    d.polygon([(px - 10, py - 8), (px + 4, py - 28), (px + 16, py - 8)], fill=(230, 230, 224))
    d.polygon([(px - 10, py + 8), (px + 2, py + 24), (px + 12, py + 8)], fill=(230, 230, 224))
    for wx in range(px - 44, px + 40, 14):
        d.rectangle([wx, py - 4, wx + 8, py + 2], fill=(60, 120, 180))
    # runway + red carpet
    d.rectangle([x0, y1 - 18, x1, y1], fill=(90, 90, 96))
    d.rectangle([x0 + 120, y1 - 18, x0 + 200, y1 - 6], fill=(190, 40, 44))
    for rx in range(x0 + 10, x1 - 10, 30):
        d.rectangle([rx, y1 - 12, rx + 16, y1 - 9], fill=(250, 250, 248))
    # flags: Nepal (crimson double pennant) + India (saffron/white/green)
    d.polygon([(x0 + 30, y0 + 52), (x0 + 52, y0 + 58), (x0 + 30, y0 + 64)], fill=(200, 40, 60))
    d.polygon([(x0 + 30, y0 + 64), (x0 + 48, y0 + 69), (x0 + 30, y0 + 74)], fill=(200, 40, 60))
    d.line([(x0 + 30, y0 + 52), (x0 + 30, y1 - 18)], fill=(90, 70, 50), width=2)
    fx, fy = x1 - 58, y0 + 52
    d.rectangle([fx, fy, fx + 30, fy + 7], fill=(255, 150, 40))
    d.rectangle([fx, fy + 7, fx + 30, fy + 14], fill=(250, 250, 248))
    d.rectangle([fx, fy + 14, fx + 30, fy + 21], fill=(40, 140, 60))
    d.ellipse([fx + 12, fy + 8, fx + 18, fy + 14], fill=(34, 64, 120))
    d.line([(fx, fy), (fx, fy + 26)], fill=(90, 70, 50), width=2)


def scene_westbank(d, box):
    # Pale dawn: village road, burning cars, smoke, stone houses.
    _sky(d, box, (232, 208, 178), (240, 220, 196))
    x0, y0, x1, y1 = box
    # rising sun, low
    d.ellipse([x1 - 44, y0 + 30, x1 - 16, y0 + 58], fill=(255, 200, 110))
    # stone houses on a hill
    for (hx, hw, hh) in [(x0 + 10, 44, 22), (x0 + 60, 38, 30), (x0 + 104, 40, 20)]:
        d.rectangle([hx, y1 - 34 - hh, hx + hw, y1 - 34], fill=(200, 186, 158))
        d.rectangle([hx + 8, y1 - 34 - hh + 8, hx + 16, y1 - 34 - hh + 16], fill=(90, 70, 50))
    # road
    d.rectangle([x0, y1 - 34, x1, y1], fill=(120, 110, 96))
    for rx in range(x0 + 10, x1 - 10, 36):
        d.rectangle([rx, y1 - 20, rx + 18, y1 - 17], fill=(240, 236, 224))
    # two burning cars
    for cx in (x0 + 40, x0 + 150):
        d.rectangle([cx, y1 - 52, cx + 56, y1 - 38], fill=(150, 40, 36))
        d.rectangle([cx + 8, y1 - 62, cx + 36, y1 - 52], fill=(120, 30, 28))
        d.ellipse([cx + 8, y1 - 40, cx + 18, y1 - 30], fill=(12, 12, 12))
        d.ellipse([cx + 38, y1 - 40, cx + 48, y1 - 30], fill=(12, 12, 12))
        d.ellipse([cx + 14, y1 - 66, cx + 30, y1 - 50], fill=(255, 150, 50))
        d.ellipse([cx + 18, y1 - 60, cx + 28, y1 - 50], fill=(255, 210, 110))
        d.ellipse([cx + 20, y1 - 80, cx + 44, y1 - 58], fill=(90, 84, 78))
    # third car, intact, at the far end
    d.rectangle([x1 - 52, y1 - 48, x1 - 8, y1 - 36], fill=(60, 90, 130))
    d.rectangle([x1 - 44, y1 - 56, x1 - 20, y1 - 48], fill=(50, 70, 110))


def scene_lowy(d, box):
    # Bright chart: two bars (US navy tall, China red slightly shorter),
    # a dashed gap line labelled 5.3, small Asia map hint.
    _sky(d, box, (236, 232, 216), (222, 226, 232))
    x0, y0, x1, y1 = box
    # gridlines
    for gy in (y0 + 18, y0 + 34, y0 + 50):
        d.line([(x0 + 16, gy), (x1 - 16, gy)], fill=(200, 196, 180), width=1)
    # US bar (78.9) and China bar (73.6)
    d.rectangle([x0 + 60, y0 + 20, x0 + 104, y1 - 16], fill=(34, 64, 120))
    d.rectangle([x0 + 130, y0 + 26, x0 + 174, y1 - 16], fill=(200, 50, 44))
    d.text((x0 + 64, y0 + 6), "78.9", font=sans_b(11), fill=(34, 64, 120))
    d.text((x0 + 134, y0 + 12), "73.6", font=sans_b(11), fill=(200, 50, 44))
    d.text((x0 + 68, y1 - 14), "US", font=sans_b(11), fill=(250, 250, 248))
    d.text((x0 + 138, y1 - 14), "CN", font=sans_b(11), fill=(250, 250, 248))
    # gap arrow between the bar tops
    d.line([(x0 + 104, y0 + 23), (x0 + 130, y0 + 23)], fill=(184, 138, 47), width=2)
    d.text((x0 + 186, y0 + 16), "gap 5.3", font=sans_b(11), fill=(140, 100, 30))
    # rising trend line + small map dots
    d.line([(x0 + 20, y0 + 62), (x0 + 60, y0 + 52), (x0 + 110, y0 + 56),
            (x0 + 160, y0 + 44), (x0 + 210, y0 + 46)], fill=(60, 140, 90), width=2)
    for (mx, my) in [(x1 - 60, y0 + 60), (x1 - 44, y0 + 54), (x1 - 30, y0 + 66)]:
        d.ellipse([mx, my, mx + 5, my + 5], fill=(63, 109, 82))
    d.rectangle([x0, y1 - 4, x1, y1], fill=(120, 100, 70))


def scene_nvidia(d, box):
    # Bright: big semiconductor chip on a light bench, circuit traces.
    _sky(d, box, (228, 232, 238), (240, 234, 218))
    x0, y0, x1, y1 = box
    # circuit traces
    for ty in (y0 + 16, y0 + 30, y0 + 70):
        d.line([(x0 + 10, ty), (x1 - 10, ty)], fill=(180, 190, 200), width=1)
        for tx in range(x0 + 30, x1 - 20, 40):
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=(140, 160, 180))
    # chip body
    cx0, cy0, cx1, cy1 = x0 + 110, y0 + 22, x0 + 210, y0 + 78
    d.rectangle([cx0, cy0, cx1, cy1], fill=(24, 32, 40))
    d.rectangle([cx0 + 8, cy0 + 8, cx1 - 8, cy1 - 8], fill=(40, 54, 66))
    d.text((cx0 + 22, cy0 + 22), "H200", font=sans_b(16), fill=(120, 200, 120))
    # gold pins on all sides
    for px in range(cx0 + 12, cx1 - 8, 14):
        d.rectangle([px, cy0 - 6, px + 5, cy0], fill=(220, 180, 60))
        d.rectangle([px, cy1, px + 5, cy1 + 6], fill=(220, 180, 60))
    for py in range(cy0 + 12, cy1 - 8, 14):
        d.rectangle([cx0 - 6, py, cx0, py + 5], fill=(220, 180, 60))
        d.rectangle([cx1, py, cx1 + 6, py + 5], fill=(220, 180, 60))
    # small flags + document hint
    d.rectangle([x0 + 18, y0 + 44, x0 + 58, y0 + 72], fill=(252, 250, 244))
    d.rectangle([x0 + 18, y0 + 44, x0 + 58, y0 + 72], outline=(120, 110, 96), width=1)
    d.line([(x0 + 24, y0 + 52), (x0 + 52, y0 + 52)], fill=(140, 30, 26), width=2)
    d.line([(x0 + 24, y0 + 60), (x0 + 48, y0 + 60)], fill=(120, 110, 96), width=1)
    d.line([(x0 + 24, y0 + 66), (x0 + 52, y0 + 66)], fill=(120, 110, 96), width=1)
    d.rectangle([x1 - 62, y0 + 44, x1 - 22, y0 + 72], fill=(34, 64, 94))
    d.text((x1 - 56, y0 + 52), "879,868", font=sans_b(10), fill=(250, 250, 248))


def scene_cricket(d, box):
    # Bright green cricket field in daylight: batsman, stumps, scoreboard.
    _sky(d, box, (150, 200, 234), (228, 232, 210))
    x0, y0, x1, y1 = box
    _sun(d, x1 - 28, y0 + 14, 9)
    # stands
    for cx in range(x0 + 10, x1 - 10, 18):
        d.ellipse([cx, y0 + 10, cx + 6, y0 + 16], fill=(120, 120, 140))
    # outfield + pitch
    d.rectangle([x0, y1 - 44, x1, y1], fill=(70, 150, 80))
    d.rectangle([x0 + 110, y1 - 44, x0 + 210, y1], fill=(210, 190, 150))
    d.line([(x0 + 160, y1 - 44), (x0 + 160, y1)], fill=(250, 250, 248), width=2)
    # scoreboard
    d.rectangle([x0 + 12, y0 + 22, x0 + 92, y0 + 52], fill=(24, 32, 40))
    d.text((x0 + 20, y0 + 28), "720/9", font=sans_b(16), fill=(255, 220, 80))
    # stumps
    for sx in (x0 + 150, x0 + 156, x0 + 162):
        d.line([(sx, y1 - 30), (sx, y1 - 16)], fill=(240, 220, 140), width=2)
    d.line([(x0 + 150, y1 - 30), (x0 + 164, y1 - 30)], fill=(240, 220, 140), width=2)
    # batsman in white, mid-swing
    bx = x0 + 200
    d.ellipse([bx, y1 - 62, bx + 10, y1 - 52], fill=(200, 160, 120))
    d.rectangle([bx - 2, y1 - 52, bx + 12, y1 - 34], fill=(250, 250, 248))
    d.line([(bx + 4, y1 - 50), (bx - 10, y1 - 66)], fill=(200, 160, 120), width=3)
    d.line([(bx + 8, y1 - 50), (bx + 22, y1 - 64)], fill=(200, 160, 120), width=3)
    d.polygon([(bx + 20, y1 - 66), (bx + 30, y1 - 56), (bx + 24, y1 - 50)],
              fill=(200, 170, 110))
    # ball in flight + fielder
    d.ellipse([x1 - 40, y0 + 34, x1 - 30, y0 + 44], fill=(200, 40, 40))
    d.ellipse([x1 - 70, y1 - 40, x1 - 62, y1 - 32], fill=(240, 200, 160))
    d.rectangle([x1 - 72, y1 - 32, x1 - 60, y1 - 14], fill=(40, 90, 160))


SCENES = {
    "cop31day": scene_cop31day, "hormuz": scene_hormuz, "dymer": scene_dymer,
    "dems": scene_dems, "merkury": scene_merkury, "candy": scene_candy,
    "alcaraz": scene_alcaraz, "shuri": scene_shuri, "nepal": scene_nepal,
    "westbank": scene_westbank, "lowy": scene_lowy, "nvidia": scene_nvidia,
    "cricket": scene_cricket,
}


# ---- world map (rough equirectangular continents, solid land) ---------------
# lon -175..185 -> x ; lat 75..-55 -> y  (map box passed in)
def _lonlat(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 175) / 360.0 * (x1 - x0)
    y = y0 + (75 - lat) / 130.0 * (y1 - y0)
    return (x, y)


CONTINENTS = {
    # (lon, lat) rough outlines
    "north_america": [(-168, 66), (-140, 70), (-120, 72), (-95, 69), (-82, 66),
                      (-76, 62), (-65, 60), (-60, 52), (-55, 47), (-70, 44),
                      (-75, 35), (-80, 32), (-81, 26), (-90, 21), (-97, 16),
                      (-92, 14), (-83, 9), (-79, 9), (-86, 13), (-94, 17),
                      (-105, 20), (-110, 23), (-114, 29), (-122, 37),
                      (-124, 42), (-125, 49), (-135, 58), (-152, 60), (-165, 60)],
    "greenland": [(-58, 64), (-45, 60), (-32, 68), (-22, 70), (-30, 76),
                  (-55, 80), (-68, 76), (-62, 70)],
    "south_america": [(-79, 9), (-72, 12), (-64, 11), (-60, 8), (-52, 5),
                      (-50, 0), (-44, -3), (-35, -8), (-40, -20), (-48, -28),
                      (-57, -38), (-65, -45), (-68, -52), (-70, -54),
                      (-73, -44), (-73, -30), (-70, -18), (-77, -12), (-81, -6),
                      (-81, 0), (-80, 4)],
    "africa": [(-17, 15), (-17, 21), (-10, 31), (0, 36), (10, 37), (20, 32),
               (30, 31), (32, 31), (35, 28), (39, 21), (43, 12), (51, 11),
               (48, 2), (40, -5), (40, -15), (36, -26), (32, -29), (26, -34),
               (19, -35), (15, -27), (12, -18), (13, -10), (9, -1), (9, 4),
               (-8, 4), (-13, 8), (-17, 12)],
    "eurasia": [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (5, 53),
                (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60),
                (30, 62), (32, 70), (45, 68), (60, 69), (75, 72), (90, 75),
                (110, 74), (130, 72), (150, 70), (170, 66), (178, 65),
                (170, 60), (162, 56), (156, 51), (142, 50), (140, 40),
                (135, 35), (130, 33), (127, 35), (122, 38), (120, 32),
                (115, 23), (108, 18), (105, 9), (100, 8), (98, 12),
                (95, 16), (92, 21), (89, 22), (86, 20), (80, 15), (77, 8),
                (74, 20), (70, 22), (66, 25), (61, 25), (57, 26), (52, 27),
                (50, 29), (48, 30), (44, 29), (42, 27), (39, 21), (35, 29),
                (36, 36), (30, 36), (26, 38), (23, 36), (19, 40), (15, 44),
                (12, 44), (8, 44), (3, 43), (0, 39), (-2, 37), (-6, 36),
                (-9, 37)],
    "uk": [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51)],
    "japan": [(130, 31), (132, 34), (136, 35), (139, 38), (141, 42), (143, 44),
              (141, 40), (138, 35), (134, 34), (131, 33)],
    "australia": [(114, -22), (114, -32), (118, -35), (124, -33), (130, -32),
                  (135, -35), (140, -38), (146, -39), (150, -37), (153, -27),
                  (150, -22), (146, -19), (142, -11), (136, -12), (132, -12),
                  (126, -14), (122, -17), (118, -20)],
    "nz": [(167, -45), (171, -42), (174, -39), (177, -38), (174, -41),
           (170, -44), (167, -46)],
    "borneo": [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (112, -3),
               (109, -2)],
    "new_guinea": [(131, -1), (136, -2), (141, -3), (146, -6), (147, -9),
                   (141, -8), (136, -5), (132, -3)],
    "madagascar": [(44, -16), (47, -15), (50, -16), (47, -24), (44, -25),
                   (43, -20)],
}


def draw_map(d, box):
    d.rectangle(box, fill=SEA)
    for name, pts in CONTINENTS.items():
        poly = [_lonlat(lon, lat, box) for lon, lat in pts]
        d.polygon(poly, fill=LAND)
    # equator hint
    x0, y0, x1, y1 = box
    ey = _lonlat(0, 0, box)[1]
    d.line([(x0, ey), (x1, ey)], fill=(210, 200, 170), width=1)


def paste_scene(img, name, box):
    """Render a scene on a fixed 320x90 canvas, then cover-crop it into box."""
    x0, y0, x1, y1 = (int(v) for v in box)
    w, h = x1 - x0, y1 - y0
    art = Image.new("RGB", (320, 90), CREAM)
    sd = ImageDraw.Draw(art)
    SCENES[name](sd, (0, 0, 320, 90))
    scale = max(w / 320.0, h / 90.0)
    nw, nh = int(320 * scale + 0.5), int(90 * scale + 0.5)
    art = art.resize((nw, nh), Image.LANCZOS)
    ox, oy = (nw - w) // 2, (nh - h) // 2
    img.paste(art.crop((ox, oy, ox + w, oy + h)), (x0, y0))


# ---- pin positions (lon, lat) — checked against real geography --------------
PINS = {
    1: (30.71, 36.90),    # Antalya — COP31
    2: (56.50, 26.60),    # Strait of Hormuz, near Ghanam Island
    3: (30.30, 50.78),    # Dymer, Kyiv oblast
    4: (-80.24, 36.10),   # Winston-Salem, NC (district NC-5)
    5: (20.07, 32.12),    # Benghazi — Merkury
    6: (106.32, -6.22),   # Cikande, Banten — candy factory fire
    7: (7.69, 45.07),     # Turin — Alcaraz
    8: (127.72, 26.22),   # Naha, Okinawa — Shuri Castle
    9: (77.21, 28.61),    # New Delhi — Nepal PM
    10: (35.30, 31.99),   # Kafr Malik, West Bank
    11: (151.21, -33.87),  # Sydney — Lowy Institute
    12: (-77.04, 38.90),  # Washington, D.C. — Nvidia/Bessent
    13: (174.78, -41.29),  # Wellington — India Test
}
# Crowded clusters: numbered pins sit at spread-out display positions with
# a leader line to the true spot (small navy dot). Display positions were
# chosen so no two pin circles (r=10) overlap.
PIN_DISPLAY = {
    1: (44, 42),     # Antalya — shown over the E Mediterranean
    2: (70, 8),      # Hormuz — shown over the Arabian Sea
    3: (28, 64),     # Dymer — shown over the N Black Sea
    4: (-96, 46),    # Winston-Salem — shown over the US interior
    5: (14, 28),     # Benghazi — shown over the central Med
    7: (-6, 54),     # Turin — shown over the W Mediterranean
    9: (78, 38),     # New Delhi — shown over N India
    10: (44, 8),     # Kafr Malik — shown over the Gulf of Aden
    11: (146, -28),  # Sydney — shown over E Australia
    12: (-66, 40),   # Washington — shown over the W Atlantic
    13: (168, -38),  # Wellington — shown over the S Pacific
}
DOTS = {
    14: (-84.4, 33.75), 15: (121.5, 31.2), 16: (32.5, 15.6),
    17: (29.5, 1.5), 18: (145.0, -37.8), 19: (151.2, -33.9),
    20: (21.0, 52.2), 21: (51.4, 35.7), 22: (77.2, 28.6),
    23: (-77.0, 38.9), 24: (-91.2, 41.0), 25: (92.0, 28.5),
    26: (127.0, 37.5), 27: (-81.8, 26.1), 28: (-53.8, -29.0),
    29: (-76.0, -11.2), 30: (-80.0, 36.5), 31: (22.8, 50.1),
    32: (-2.96, 53.43), 33: (-2.12, 52.59),
}


# ---- layout -------------------------------------------------------------------
MX = 24                      # side margin
CW = W - 2 * MX              # 976 content width
LEAD_ART_H = 80
CARD_ART_H = 55


def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    y = 10
    log = []

    # -- kicker ---------------------------------------------------------------
    d.text((MX, y), "THE WORLD IN ONE DAY", font=sans_b(11), fill=INK)
    right = "33 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE FROM THIS SUNDAY"
    d.text((W - MX - sans_b(11).getlength(right), y), right, font=sans_b(11), fill=INK_SOFT)
    d.line([(MX, y + 14), (W - MX, y + 14)], fill=RULE, width=1)
    y += 15
    log.append(("kicker", y))

    # -- masthead ---------------------------------------------------------------
    # Playfair 70: text is ~800 px wide on a 976 px content width (one line).
    # Advance is computed from the font metrics (ascent + descent + gap) so
    # the long "y" descenders of "Sunday"/"November" clear the sub-headline:
    # at 50 px the old fixed advance (52) let the "y" tail of "Saturday"
    # reach y=96 and touch the "C" of COP31 in the sub-headline at y=84.
    mast = "Sunday 22 November 2026"
    mf = playfair(70)
    d.text(((W - mf.getlength(mast)) / 2, y), mast, font=mf, fill=INK, stroke_width=1)
    ma, md = mf.getmetrics()
    y += ma + md + 2
    log.append(("masthead", y))

    # -- sub-headline -------------------------------------------------------------
    sub = ("COP31 collapses with no deal  \u00b7  Two tankers hit by mines near "
           "Hormuz  \u00b7  Drone flattens flats in Dymer")
    sf = serif_i(15)
    d.text(((W - sf.getlength(sub)) / 2, y), sub, font=sf, fill=RED)
    y += 20
    log.append(("subhead", y))

    # -- region bar ---------------------------------------------------------------
    seg_w = CW / len(REGIONS)
    seg_cols = [GOLD_LT, SAGE, NAVY_LT, GOLD_LT, SAGE, NAVY_LT, GOLD_LT]
    for i, ((name, n), col) in enumerate(zip(REGIONS, seg_cols)):
        x0 = MX + i * seg_w
        d.rectangle([x0, y, x0 + seg_w - 1, y + 18], fill=col)
        lab = f"{name} {n}"
        lf = sans_b(13)
        d.text((x0 + (seg_w - lf.getlength(lab)) / 2, y + 3), lab, font=lf, fill=INK)
    y += 18 + 2
    log.append(("regions", y))

    # -- THE DAY IN UTC -------------------------------------------------------------
    d.text((MX, y), "THE DAY IN UTC", font=sans_b(11), fill=NAVY)
    y += 10
    cell_w = CW / len(TIMELINE)
    for i, (t, lab) in enumerate(TIMELINE):
        x0 = MX + i * cell_w
        if i:
            d.line([(x0, y), (x0, y + 30)], fill=RULE, width=1)
        d.text((x0 + 4, y), t, font=sans_b(13), fill=INK)
        ll = wrap(lab, sans(10), cell_w - 8)
        draw_lines(d, ll[:2], x0 + 4, y + 14, sans(10), INK_SOFT, 11)
    y += 38 + 0
    log.append(("utc", y))

    # -- THE DAY IN NUMBERS ---------------------------------------------------------
    d.text((MX, y), "THE DAY IN NUMBERS", font=sans_b(11), fill=NAVY)
    y += 10
    cell_w = CW / len(NUMBERS)
    for i, (num, lab) in enumerate(NUMBERS):
        x0 = MX + i * cell_w
        if i:
            d.line([(x0, y), (x0, y + 44)], fill=RULE, width=1)
        nf = serif_b(23)
        d.text((x0 + 4, y), num, font=nf, fill=RED)
        ll = wrap(lab, sans(10), cell_w - 8)
        draw_lines(d, ll[:2], x0 + 4, y + 26, sans(10), INK_SOFT, 11)
    y += 50 + 0
    log.append(("numbers", y))

    # -- 3 lead cards ---------------------------------------------------------------
    lead_w = (CW - 2 * 10) / 3
    lead_x = [MX + i * (lead_w + 10) for i in range(3)]
    lead_top = y
    lead_bottom = y
    for i, lead in enumerate(LEADS):
        x0 = lead_x[i]
        x1 = x0 + lead_w
        # art
        paste_scene(img, lead["scene"], (x0, y, x1, y + LEAD_ART_H))
        d.rectangle([x0, y, x1, y + LEAD_ART_H], outline=RULE, width=1)
        # number badge on the art
        bx, by = x0 + 6, y + 6
        d.ellipse([bx, by, bx + 22, by + 22], fill=RED)
        d.text((bx + 6, by + 4), str(lead["n"]), font=sans_b(13), fill=WHITE)
        ty = y + LEAD_ART_H + 5
        hf = serif_b(17)
        hl = wrap(lead["headline"], hf, lead_w)
        ty = draw_lines(d, hl, x0, ty, hf, INK, 19)
        df = sans(12)
        dl = wrap(lead["deck"], df, lead_w)
        ty = draw_lines(d, dl, x0, ty + 1, df, INK_SOFT, 13)
        tf = sans_b(10)
        d.text((x0, ty + 2), lead["tag"], font=tf, fill=NAVY)
        lead_bottom = max(lead_bottom, ty + 2 + 13)
    y = lead_bottom + 10
    log.append(("leads", y))

    # -- 10 numbered cards, 2 rows x 5 ----------------------------------------------
    card_w = (CW - 4 * 8) / 5
    card_top = y
    for row in range(2):
        row_bottom = y
        for col in range(5):
            card = CARDS[row * 5 + col]
            x0 = MX + col * (card_w + 8)
            x1 = x0 + card_w
            paste_scene(img, card["scene"], (x0, y, x1, y + CARD_ART_H))
            d.rectangle([x0, y, x1, y + CARD_ART_H], outline=RULE, width=1)
            bx, by = x0 + 4, y + 4
            d.ellipse([bx, by, bx + 19, by + 19], fill=NAVY)
            d.text((bx + 5, by + 3), str(card["n"]), font=sans_b(11), fill=WHITE)
            ty = y + CARD_ART_H + 4
            hf = serif_b(12)
            hl = wrap(card["headline"], hf, card_w)
            ty = draw_lines(d, hl, x0, ty, hf, INK, 13.5)
            df = sans(11)
            dl = wrap(card["deck"], df, card_w)
            ty = draw_lines(d, dl, x0, ty + 0, df, INK_SOFT, 12)
            tf = sans_b(9)
            d.text((x0, ty + 1), card["tag"], font=tf, fill=NAVY)
            row_bottom = max(row_bottom, ty + 1 + 12)
        y = row_bottom + 2
    y += 4
    log.append(("cards", y))

    # -- map (left) + briefs (right) --------------------------------------------------
    sec_top = y
    map_x0, map_x1 = MX, MX + 336
    brief_x0 = MX + 352
    # map panel
    d.text((map_x0, y), "WHERE IT HAPPENED", font=sans_b(12), fill=NAVY)
    d.text((map_x0, y + 15), "numbers match the stories", font=sans(10), fill=INK_SOFT)
    map_box = (map_x0 + 2, y + 30, map_x1 - 2, y + 130)
    draw_map(d, map_box)
    d.rectangle(map_box, outline=RULE, width=1)
    for n, (lon, lat) in PINS.items():
        px, py = _lonlat(lon, lat, map_box)
        if n in PIN_DISPLAY:
            dx, dy = _lonlat(*PIN_DISPLAY[n], map_box)
            d.line([(px, py), (dx, dy)], fill=INK_SOFT, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=NAVY)
            px, py = dx, dy
        d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED, outline=WHITE, width=1)
        nf = sans_b(10)
        t = str(n)
        d.text((px - nf.getlength(t) / 2, py - 6), t, font=nf, fill=WHITE)
    for n, (lon, lat) in DOTS.items():
        px, py = _lonlat(lon, lat, map_box)
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=NAVY)
    # legend under the map
    ly = map_box[3] + 4
    leg = ("CONFIRMED verified  \u00b7  OFFICIAL an official statement  \u00b7  "
           "REPORTED reported, not fully verified  \u00b7  FORECAST a projection")
    ll = wrap(leg, sans(10), map_x1 - map_x0)
    draw_lines(d, ll, map_x0, ly, sans(10), INK_SOFT, 12)
    # briefs
    d.text((brief_x0, y), "THE REST OF THE DAY", font=sans_b(12), fill=NAVY)
    col_w = (W - MX - brief_x0 - 12) / 2
    bf = sans(14)
    by = y + 15
    for ci in range(2):
        bx = brief_x0 + ci * (col_w + 12)
        ry = by
        for (n, txt) in BRIEFS[ci * 10:(ci + 1) * 10]:
            line = f"{n}. {txt}"
            d.text((bx, ry), line, font=bf, fill=INK)
            ry += 15
    y = sec_top + 175 + 4
    log.append(("map+briefs", y))

    # -- DATE CHECK (prose, date named once) -------------------------------------------
    dc_top = y
    d.rectangle([MX, y, W - MX, y + 96], fill=CREAM2, outline=RULE, width=1)
    d.text((MX + 10, y + 6), "DATE CHECK", font=sans_b(12), fill=RED)
    pf = sans(13)
    pl = wrap(DATECHECK, pf, CW - 20)
    py = draw_lines(d, pl, MX + 10, y + 22, pf, INK, 14.5)
    nf = sans_b(12)
    nl = wrap(NOTYET, nf, CW - 20)
    draw_lines(d, nl, MX + 10, py + 2, nf, NAVY, 14)
    y = dc_top + 96 + 4
    log.append(("datecheck", y))

    # -- footer -------------------------------------------------------------------------
    ff = sans(12)
    fl1 = wrap(FOOTER1, ff, CW)
    fy = draw_lines(d, fl1, MX, y, ff, INK_SOFT, 12.5)
    fl2 = wrap(FOOTER2, ff, CW)
    fy = draw_lines(d, fl2, MX, fy, ff, INK_SOFT, 12.5)
    y = fy
    log.append(("footer", y))
    print("LAYOUT:", log, "total height used:", y, "of", H)
    return img


if __name__ == "__main__":
    out = render()
    out.save(os.path.join(HERE, "entry.png"))
    print("saved entry.png", out.size)
