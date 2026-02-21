"""
Master Data for Tamil Astro Matching Calculator
All data is structured for easy extension and maintenance.
"""

# ─────────────────────────────────────────────────────────────
# 27 Nakshatras with Rasi, Lord, Deity, Gana, Nadi, Yoni, Varna
# Each star has 4 Padhams (quarters)
# ─────────────────────────────────────────────────────────────

NAKSHATRAS = [
    {"id": 1,  "name": "Ashwini",       "tamil": "அசுவினி",    "rasi": "Mesha",      "lord": "Ketu",    "deity": "Ashwins",      "gana": "Deva",    "nadi": "Vata",    "yoni": "Horse",    "varna": "Vaishya",  "padhams": 4},
    {"id": 2,  "name": "Bharani",       "tamil": "பரணி",       "rasi": "Mesha",      "lord": "Shukra",  "deity": "Yama",         "gana": "Manushya","nadi": "Pitta",   "yoni": "Elephant", "varna": "Chandala", "padhams": 4},
    {"id": 3,  "name": "Krittika",      "tamil": "கிருத்திகை", "rasi": "Mesha/Vrishabha","lord": "Surya","deity": "Agni",        "gana": "Rakshasa","nadi": "Kapha",   "yoni": "Sheep",    "varna": "Brahmin",  "padhams": 4},
    {"id": 4,  "name": "Rohini",        "tamil": "ரோகிணி",     "rasi": "Vrishabha",  "lord": "Chandra", "deity": "Brahma",       "gana": "Manushya","nadi": "Kapha",   "yoni": "Snake",    "varna": "Shudra",   "padhams": 4},
    {"id": 5,  "name": "Mrigashira",    "tamil": "மிருகசீரிஷம்","rasi": "Vrishabha/Mithuna","lord": "Kuja","deity": "Soma",     "gana": "Deva",    "nadi": "Pitta",   "yoni": "Female Serpent","varna": "Vaishya","padhams": 4},
    {"id": 6,  "name": "Ardra",         "tamil": "திருவாதிரை", "rasi": "Mithuna",    "lord": "Rahu",    "deity": "Rudra",        "gana": "Manushya","nadi": "Vata",    "yoni": "Dog",      "varna": "Chandala", "padhams": 4},
    {"id": 7,  "name": "Punarvasu",     "tamil": "புனர்பூசம்", "rasi": "Mithuna/Kataka","lord": "Guru", "deity": "Aditi",        "gana": "Deva",    "nadi": "Vata",    "yoni": "Cat",      "varna": "Vaishya",  "padhams": 4},
    {"id": 8,  "name": "Pushya",        "tamil": "பூசம்",      "rasi": "Kataka",     "lord": "Shani",   "deity": "Brihaspati",   "gana": "Deva",    "nadi": "Pitta",   "yoni": "Sheep",    "varna": "Kshatriya","padhams": 4},
    {"id": 9,  "name": "Ashlesha",      "tamil": "ஆயில்யம்",  "rasi": "Kataka",     "lord": "Budha",   "deity": "Sarpa",        "gana": "Rakshasa","nadi": "Kapha",   "yoni": "Cat",      "varna": "Chandala", "padhams": 4},
    {"id": 10, "name": "Magha",         "tamil": "மகம்",       "rasi": "Simha",      "lord": "Ketu",    "deity": "Pitru",        "gana": "Rakshasa","nadi": "Vata",    "yoni": "Rat",      "varna": "Shudra",   "padhams": 4},
    {"id": 11, "name": "Purva Phalguni","tamil": "பூரம்",      "rasi": "Simha",      "lord": "Shukra",  "deity": "Aryaman",      "gana": "Manushya","nadi": "Pitta",   "yoni": "Rat",      "varna": "Brahmin",  "padhams": 4},
    {"id": 12, "name": "Uttara Phalguni","tamil": "உத்திரம்", "rasi": "Simha/Kanya","lord": "Surya",   "deity": "Bhaga",        "gana": "Manushya","nadi": "Kapha",   "yoni": "Bull",     "varna": "Kshatriya","padhams": 4},
    {"id": 13, "name": "Hasta",         "tamil": "அஸ்தம்",    "rasi": "Kanya",      "lord": "Chandra", "deity": "Savitr",       "gana": "Deva",    "nadi": "Vata",    "yoni": "Buffalo",  "varna": "Vaishya",  "padhams": 4},
    {"id": 14, "name": "Chitra",        "tamil": "சித்திரை",  "rasi": "Kanya/Tula", "lord": "Kuja",    "deity": "Vishwakarma",  "gana": "Rakshasa","nadi": "Pitta",   "yoni": "Female Tiger","varna": "Chandala","padhams": 4},
    {"id": 15, "name": "Swati",         "tamil": "சுவாதி",    "rasi": "Tula",       "lord": "Rahu",    "deity": "Vayu",         "gana": "Deva",    "nadi": "Kapha",   "yoni": "Buffalo",  "varna": "Chandala", "padhams": 4},
    {"id": 16, "name": "Vishakha",      "tamil": "விசாகம்",   "rasi": "Tula/Vrischika","lord": "Guru", "deity": "Indragni",     "gana": "Rakshasa","nadi": "Kapha",   "yoni": "Tiger",    "varna": "Chandala", "padhams": 4},
    {"id": 17, "name": "Anuradha",      "tamil": "அனுஷம்",   "rasi": "Vrischika",  "lord": "Shani",   "deity": "Mitra",        "gana": "Deva",    "nadi": "Pitta",   "yoni": "Deer",     "varna": "Shudra",   "padhams": 4},
    {"id": 18, "name": "Jyeshtha",      "tamil": "கேட்டை",    "rasi": "Vrischika",  "lord": "Budha",   "deity": "Indra",        "gana": "Rakshasa","nadi": "Vata",    "yoni": "Deer",     "varna": "Chandala", "padhams": 4},
    {"id": 19, "name": "Mula",          "tamil": "மூலம்",     "rasi": "Dhanus",     "lord": "Ketu",    "deity": "Nirrti",       "gana": "Rakshasa","nadi": "Kapha",   "yoni": "Dog",      "varna": "Chandala", "padhams": 4},
    {"id": 20, "name": "Purva Ashadha", "tamil": "பூராடம்",  "rasi": "Dhanus",     "lord": "Shukra",  "deity": "Apah",         "gana": "Manushya","nadi": "Pitta",   "yoni": "Monkey",   "varna": "Brahmin",  "padhams": 4},
    {"id": 21, "name": "Uttara Ashadha","tamil": "உத்திராடம்","rasi": "Dhanus/Makara","lord": "Surya", "deity": "Vishvedeva",   "gana": "Manushya","nadi": "Vata",    "yoni": "Mongoose", "varna": "Kshatriya","padhams": 4},
    {"id": 22, "name": "Shravana",      "tamil": "திருவோணம்", "rasi": "Makara",     "lord": "Chandra", "deity": "Vishnu",       "gana": "Deva",    "nadi": "Kapha",   "yoni": "Monkey",   "varna": "Chandala", "padhams": 4},
    {"id": 23, "name": "Dhanishta",     "tamil": "அவிட்டம்",  "rasi": "Makara/Kumbha","lord": "Kuja",  "deity": "Ashta Vasus",  "gana": "Rakshasa","nadi": "Pitta",   "yoni": "Lion",     "varna": "Chandala", "padhams": 4},
    {"id": 24, "name": "Shatabhisha",   "tamil": "சதயம்",     "rasi": "Kumbha",     "lord": "Rahu",    "deity": "Varuna",       "gana": "Rakshasa","nadi": "Vata",    "yoni": "Horse",    "varna": "Chandala", "padhams": 4},
    {"id": 25, "name": "Purva Bhadra",  "tamil": "பூரட்டாதி", "rasi": "Kumbha/Meena","lord": "Guru",  "deity": "Aja Ekapada",  "gana": "Manushya","nadi": "Pitta",   "yoni": "Lion",     "varna": "Brahmin",  "padhams": 4},
    {"id": 26, "name": "Uttara Bhadra", "tamil": "உத்திரட்டாதி","rasi": "Meena",   "lord": "Shani",   "deity": "Ahir Budhnya", "gana": "Manushya","nadi": "Kapha",   "yoni": "Cow",      "varna": "Kshatriya","padhams": 4},
    {"id": 27, "name": "Revati",        "tamil": "ரேவதி",     "rasi": "Meena",      "lord": "Budha",   "deity": "Pushan",       "gana": "Deva",    "nadi": "Vata",    "yoni": "Elephant", "varna": "Shudra",   "padhams": 4},
]

# ─────────────────────────────────────────────────────────────
# 12 Rasis (Zodiac Signs)
# ─────────────────────────────────────────────────────────────

RASIS = [
    {"id": 1,  "name": "Mesha",      "tamil": "மேஷம்",     "english": "Aries",       "element": "Fire",  "quality": "Cardinal", "lord": "Kuja"},
    {"id": 2,  "name": "Vrishabha",  "tamil": "ரிஷபம்",    "english": "Taurus",      "element": "Earth", "quality": "Fixed",    "lord": "Shukra"},
    {"id": 3,  "name": "Mithuna",    "tamil": "மிதுனம்",   "english": "Gemini",      "element": "Air",   "quality": "Mutable",  "lord": "Budha"},
    {"id": 4,  "name": "Kataka",     "tamil": "கடகம்",     "english": "Cancer",      "element": "Water", "quality": "Cardinal", "lord": "Chandra"},
    {"id": 5,  "name": "Simha",      "tamil": "சிம்மம்",   "english": "Leo",         "element": "Fire",  "quality": "Fixed",    "lord": "Surya"},
    {"id": 6,  "name": "Kanya",      "tamil": "கன்னி",     "english": "Virgo",       "element": "Earth", "quality": "Mutable",  "lord": "Budha"},
    {"id": 7,  "name": "Tula",       "tamil": "துலாம்",    "english": "Libra",       "element": "Air",   "quality": "Cardinal", "lord": "Shukra"},
    {"id": 8,  "name": "Vrischika",  "tamil": "விருச்சிகம்","english": "Scorpio",    "element": "Water", "quality": "Fixed",    "lord": "Kuja"},
    {"id": 9,  "name": "Dhanus",     "tamil": "தனுசு",     "english": "Sagittarius", "element": "Fire",  "quality": "Mutable",  "lord": "Guru"},
    {"id": 10, "name": "Makara",     "tamil": "மகரம்",     "english": "Capricorn",   "element": "Earth", "quality": "Cardinal", "lord": "Shani"},
    {"id": 11, "name": "Kumbha",     "tamil": "கும்பம்",   "english": "Aquarius",    "element": "Air",   "quality": "Fixed",    "lord": "Shani"},
    {"id": 12, "name": "Meena",      "tamil": "மீனம்",     "english": "Pisces",      "element": "Water", "quality": "Mutable",  "lord": "Guru"},
]

# ─────────────────────────────────────────────────────────────
# RASI COMPATIBILITY TABLE (Rajju / Rasi Porutham)
# 0=Incompatible, 1=Compatible, 2=Highly Compatible
# Row=Groom Rasi Index, Col=Bride Rasi Index (1-based mapped to 0-based)
# ─────────────────────────────────────────────────────────────

RASI_COMPATIBILITY = {
    # (groom_rasi_id, bride_rasi_id): score (0,1,2)
    # Key pairs where special rules apply
    # Based on traditional 12-sign relationship grid
    "pairs": {
        (1,1):2,(1,2):1,(1,3):1,(1,4):0,(1,5):2,(1,6):1,(1,7):0,(1,8):0,(1,9):2,(1,10):0,(1,11):1,(1,12):0,
        (2,1):1,(2,2):2,(2,3):1,(2,4):1,(2,5):1,(2,6):2,(2,7):1,(2,8):0,(2,9):0,(2,10):2,(2,11):0,(2,12):1,
        (3,1):1,(3,2):1,(3,3):2,(3,4):1,(3,5):0,(3,6):1,(3,7):2,(3,8):1,(3,9):1,(3,10):0,(3,11):2,(3,12):0,
        (4,1):0,(4,2):1,(4,3):1,(4,4):2,(4,5):1,(4,6):1,(4,7):1,(4,8):2,(4,9):0,(4,10):1,(4,11):0,(4,12):2,
        (5,1):2,(5,2):1,(5,3):0,(5,4):1,(5,5):2,(5,6):1,(5,7):0,(5,8):1,(5,9):2,(5,10):0,(5,11):1,(5,12):0,
        (6,1):1,(6,2):2,(6,3):1,(6,4):1,(6,5):1,(6,6):2,(6,7):1,(6,8):0,(6,9):0,(6,10):2,(6,11):0,(6,12):1,
        (7,1):0,(7,2):1,(7,3):2,(7,4):1,(7,5):0,(7,6):1,(7,7):2,(7,8):1,(7,9):1,(7,10):0,(7,11):2,(7,12):0,
        (8,1):0,(8,2):0,(8,3):1,(8,4):2,(8,5):1,(8,6):0,(8,7):1,(8,8):2,(8,9):0,(8,10):1,(8,11):0,(8,12):2,
        (9,1):2,(9,2):0,(9,3):1,(9,4):0,(9,5):2,(9,6):0,(9,7):1,(9,8):0,(9,9):2,(9,10):0,(9,11):1,(9,12):0,
        (10,1):0,(10,2):2,(10,3):0,(10,4):1,(10,5):0,(10,6):2,(10,7):0,(10,8):1,(10,9):0,(10,10):2,(10,11):0,(10,12):1,
        (11,1):1,(11,2):0,(11,3):2,(11,4):0,(11,5):1,(11,6):0,(11,7):2,(11,8):0,(11,9):1,(11,10):0,(11,11):2,(11,12):0,
        (12,1):0,(12,2):1,(12,3):0,(12,4):2,(12,5):0,(12,6):1,(12,7):0,(12,8):2,(12,9):0,(12,10):1,(12,11):0,(12,12):2,
    }
}

# ─────────────────────────────────────────────────────────────
# STAR (Nakshatra) COMPATIBILITY — Dina Porutham (Star count rule)
# Compatibility based on star number difference
# ─────────────────────────────────────────────────────────────

DINA_COMPATIBILITY = {
    "good_counts": [2, 4, 6, 8, 9],  # Count from bride's star to groom's star
    "max_score": 3,
    "description": "Dina Porutham — Health & Longevity"
}

# ─────────────────────────────────────────────────────────────
# GANA PORUTHAM TABLE
# Deva=1, Manushya=2, Rakshasa=3
# ─────────────────────────────────────────────────────────────

GANA_TABLE = {
    ("Deva", "Deva"):       {"score": 6, "compatibility": "Excellent"},
    ("Deva", "Manushya"):   {"score": 5, "compatibility": "Good"},
    ("Deva", "Rakshasa"):   {"score": 1, "compatibility": "Poor"},
    ("Manushya", "Deva"):   {"score": 5, "compatibility": "Good"},
    ("Manushya", "Manushya"):{"score": 6, "compatibility": "Excellent"},
    ("Manushya", "Rakshasa"):{"score": 0, "compatibility": "Very Poor"},
    ("Rakshasa", "Deva"):   {"score": 1, "compatibility": "Poor"},
    ("Rakshasa", "Manushya"):{"score": 0, "compatibility": "Very Poor"},
    ("Rakshasa", "Rakshasa"):{"score": 6, "compatibility": "Excellent"},
}

# ─────────────────────────────────────────────────────────────
# NADI PORUTHAM
# Vata, Pitta, Kapha — Same Nadi = 0 (worst), Different = 8 (best)
# ─────────────────────────────────────────────────────────────

NADI_TABLE = {
    ("Vata", "Vata"):    {"score": 0, "compatibility": "Nadi Dosha — Avoid"},
    ("Pitta", "Pitta"):  {"score": 0, "compatibility": "Nadi Dosha — Avoid"},
    ("Kapha", "Kapha"):  {"score": 0, "compatibility": "Nadi Dosha — Avoid"},
    ("Vata", "Pitta"):   {"score": 8, "compatibility": "Excellent"},
    ("Vata", "Kapha"):   {"score": 8, "compatibility": "Excellent"},
    ("Pitta", "Vata"):   {"score": 8, "compatibility": "Excellent"},
    ("Pitta", "Kapha"):  {"score": 8, "compatibility": "Excellent"},
    ("Kapha", "Vata"):   {"score": 8, "compatibility": "Excellent"},
    ("Kapha", "Pitta"):  {"score": 8, "compatibility": "Excellent"},
}

# ─────────────────────────────────────────────────────────────
# YONI PORUTHAM — Animal compatibility
# ─────────────────────────────────────────────────────────────

YONI_TABLE = {
    # (groom_yoni, bride_yoni): score (0-4)
    "friendly": [
        ("Horse", "Horse"), ("Elephant", "Elephant"),
        ("Sheep", "Sheep"), ("Snake", "Snake"),
        ("Dog", "Dog"),     ("Cat", "Cat"),
        ("Rat", "Rat"),     ("Bull", "Bull"),
        ("Buffalo", "Buffalo"), ("Tiger", "Tiger"),
        ("Deer", "Deer"),   ("Monkey", "Monkey"),
        ("Mongoose", "Mongoose"), ("Lion", "Lion"),
        ("Cow", "Cow"),
    ],
    "enemy": [
        ("Horse", "Buffalo"), ("Buffalo", "Horse"),
        ("Dog", "Deer"),      ("Deer", "Dog"),
        ("Rat", "Cat"),       ("Cat", "Rat"),
        ("Elephant", "Lion"), ("Lion", "Elephant"),
        ("Monkey", "Mongoose"), ("Mongoose", "Monkey"),
        ("Snake", "Mongoose"), ("Mongoose", "Snake"),
        ("Tiger", "Deer"),    ("Deer", "Tiger"),
        ("Sheep", "Monkey"),  ("Monkey", "Sheep"),
    ],
    "neutral_score": 2,
    "friendly_score": 4,
    "enemy_score": 0,
    "max_score": 4,
}

# ─────────────────────────────────────────────────────────────
# RAJJU PORUTHAM — Longevity / Marital harmony
# Stars are grouped into 5 Rajju categories
# Same Rajju = Dosha; Exception: Siro Rajju is worst
# ─────────────────────────────────────────────────────────────

RAJJU_GROUPS = {
    "Pada": [1, 2, 3, 28],       # Ashwini, Bharani, Krittika(p1), Revati(p4)
    "Kati": [4, 5, 6, 7, 26, 27],
    "Nabhi": [8, 9, 10, 11, 24, 25],
    "Kanta": [12, 13, 14, 15, 22, 23],
    "Siro": [16, 17, 18, 19, 20, 21],
}

# Map star_id → rajju
STAR_RAJJU = {}
for rajju, stars in RAJJU_GROUPS.items():
    for s in stars:
        STAR_RAJJU[s] = rajju

RAJJU_SCORES = {
    "different": {"score": 5, "compatibility": "Excellent — No Dosha"},
    "Pada":  {"score": 3, "compatibility": "Mild Dosha (Pada Rajju) — Acceptable"},
    "Kati":  {"score": 2, "compatibility": "Kati Rajju Dosha — Caution"},
    "Nabhi": {"score": 1, "compatibility": "Nabhi Rajju Dosha — Avoid"},
    "Kanta": {"score": 1, "compatibility": "Kanta Rajju Dosha — Avoid"},
    "Siro":  {"score": 0, "compatibility": "Siro Rajju Dosha — Strictly Avoid"},
}

# ─────────────────────────────────────────────────────────────
# VARNA PORUTHAM — Caste/Class compatibility (spiritual)
# Brahmin=4, Kshatriya=3, Vaishya=2, Shudra=1, Chandala=0
# Groom varna must be >= Bride varna
# ─────────────────────────────────────────────────────────────

VARNA_RANK = {
    "Brahmin": 4, "Kshatriya": 3, "Vaishya": 2, "Shudra": 1, "Chandala": 0
}

# ─────────────────────────────────────────────────────────────
# MAHENDRA PORUTHAM — Prosperity
# Count bride's star from groom's star; if result is 4,7,10,13,16,19,22,25 = Good
# ─────────────────────────────────────────────────────────────

MAHENDRA_GOOD = {4, 7, 10, 13, 16, 19, 22, 25}

# ─────────────────────────────────────────────────────────────
# STREE DEERGA PORUTHAM — Wife's well-being
# Count groom's star from bride's star; result must be > 7 (ideally >13)
# ─────────────────────────────────────────────────────────────

STREE_DEERGA_THRESHOLD = 7  # must be > this

# ─────────────────────────────────────────────────────────────
# VEDHA PORUTHAM — Obstacle / Affliction
# Certain star pairs cause Vedha dosha
# ─────────────────────────────────────────────────────────────

VEDHA_PAIRS = [
    (1, 18), (2, 16), (3, 14), (4, 12), (5, 20),
    (6, 17), (7, 11), (8, 23), (9, 22), (10, 21),
    (13, 27), (15, 24), (19, 25), (26, 26),
    # Reversed pairs
    (18, 1), (16, 2), (14, 3), (12, 4), (20, 5),
    (17, 6), (11, 7), (23, 8), (22, 9), (21, 10),
    (27, 13), (24, 15), (25, 19),
]

# ─────────────────────────────────────────────────────────────
# PLANETARY LORDS COMPATIBILITY
# ─────────────────────────────────────────────────────────────

PLANET_FRIENDS = {
    "Surya":  ["Chandra", "Kuja", "Guru"],
    "Chandra": ["Surya", "Budha"],
    "Kuja":   ["Surya", "Chandra", "Guru"],
    "Budha":  ["Surya", "Shukra"],
    "Guru":   ["Surya", "Chandra", "Kuja"],
    "Shukra": ["Budha", "Shani"],
    "Shani":  ["Budha", "Shukra"],
    "Rahu":   ["Shukra", "Shani"],
    "Ketu":   ["Kuja", "Shukra", "Shani"],
}

PLANET_ENEMIES = {
    "Surya":  ["Shukra", "Shani"],
    "Chandra": ["Kuja", "Ketu"],  # slight
    "Kuja":   ["Budha"],
    "Budha":  ["Chandra"],
    "Guru":   ["Budha", "Shukra", "Shani"],
    "Shukra": ["Surya", "Chandra"],
    "Shani":  ["Surya", "Chandra", "Kuja"],
    "Rahu":   ["Surya", "Chandra", "Kuja"],
    "Ketu":   ["Surya", "Chandra"],
}

# ─────────────────────────────────────────────────────────────
# 10 PORUTHAMS — Names, Max Scores, Weights
# ─────────────────────────────────────────────────────────────

PORUTHAMS = [
    {"id": 1,  "name": "Dina Porutham",      "tamil": "தின பொருத்தம்",    "max_score": 3,  "weight": 1.0, "critical": False, "category": "Health"},
    {"id": 2,  "name": "Gana Porutham",      "tamil": "கண பொருத்தம்",    "max_score": 6,  "weight": 1.5, "critical": True,  "category": "Temperament"},
    {"id": 3,  "name": "Mahendra Porutham",  "tamil": "மகேந்திர பொருத்தம்","max_score": 2, "weight": 0.8, "critical": False, "category": "Prosperity"},
    {"id": 4,  "name": "Stree Deerga",       "tamil": "ஸ்திரீ தீர்க்க பொருத்தம்","max_score": 3,"weight": 1.0,"critical": False,"category": "Longevity"},
    {"id": 5,  "name": "Yoni Porutham",      "tamil": "யோனி பொருத்தம்",  "max_score": 4,  "weight": 1.2, "critical": True,  "category": "Physical Harmony"},
    {"id": 6,  "name": "Rasi Porutham",      "tamil": "ராசி பொருத்தம்",  "max_score": 7,  "weight": 1.3, "critical": True,  "category": "Mental Harmony"},
    {"id": 7,  "name": "Rajju Porutham",     "tamil": "ரஜ்ஜு பொருத்தம்","max_score": 5,  "weight": 2.0, "critical": True,  "category": "Marital Bliss"},
    {"id": 8,  "name": "Vedha Porutham",     "tamil": "வேத பொருத்தம்",   "max_score": 2,  "weight": 1.0, "critical": False, "category": "Obstacles"},
    {"id": 9,  "name": "Varna Porutham",     "tamil": "வர்ண பொருத்தம்",  "max_score": 1,  "weight": 0.5, "critical": False, "category": "Spiritual"},
    {"id": 10, "name": "Nadi Porutham",      "tamil": "நாடி பொருத்தம்",  "max_score": 8,  "weight": 2.5, "critical": True,  "category": "Health & Lineage"},
]

# Total max raw score
TOTAL_MAX_SCORE = sum(p["max_score"] for p in PORUTHAMS)  # = 41

# ─────────────────────────────────────────────────────────────
# PADHAM (Quarter) DATA — Each Nakshatra has 4 Padhams
# Each Padham spans 3°20' = 200 arc-minutes
# Padhams fall in Navamsa Rasis cyclically from Mesha
# ─────────────────────────────────────────────────────────────

PADHAM_NAVAMSA = ["Mesha", "Vrishabha", "Mithuna", "Kataka",
                  "Simha", "Kanya", "Tula", "Vrischika",
                  "Dhanus", "Makara", "Kumbha", "Meena"]

def get_padham_navamsa(star_id: int, padham: int) -> str:
    """Return navamsa rasi for a given star and padham (1-4)."""
    idx = ((star_id - 1) * 4 + (padham - 1)) % 12
    return PADHAM_NAVAMSA[idx]

def get_nakshatra_by_name(name: str) -> dict:
    for n in NAKSHATRAS:
        if n["name"] == name:
            return n
    return None

def get_rasi_by_name(name: str) -> dict:
    for r in RASIS:
        if r["name"] == name:
            return r
    return None

def get_nakshatra_names() -> list:
    return [f"{n['name']} ({n['tamil']})" for n in NAKSHATRAS]

def get_rasi_names() -> list:
    return [f"{r['name']} ({r['tamil']})" for r in RASIS]
