# Nakshatra attributes for Ashta-Kuta Matchmaking

NAKSHATRA_GANA = [
    "Deva",     # 1 Ashwini
    "Manushya", # 2 Bharani
    "Rakshasa", # 3 Krittika
    "Manushya", # 4 Rohini
    "Deva",     # 5 Mrigashira
    "Manushya", # 6 Ardra
    "Deva",     # 7 Punarvasu
    "Deva",     # 8 Pushya
    "Rakshasa", # 9 Ashlesha
    "Rakshasa", # 10 Magha
    "Manushya", # 11 Purva Phalguni
    "Manushya", # 12 Uttara Phalguni
    "Deva",     # 13 Hasta
    "Rakshasa", # 14 Chitra
    "Deva",     # 15 Swati
    "Rakshasa", # 16 Vishakha
    "Deva",     # 17 Anuradha
    "Rakshasa", # 18 Jyeshtha
    "Rakshasa", # 19 Mula
    "Manushya", # 20 Purva Ashadha
    "Manushya", # 21 Uttara Ashadha
    "Deva",     # 22 Shravana
    "Rakshasa", # 23 Dhanishtha
    "Rakshasa", # 24 Shatabhisha
    "Manushya", # 25 Purva Bhadrapada
    "Manushya", # 26 Uttara Bhadrapada
    "Deva"      # 27 Revati
]

NAKSHATRA_YONI = [
    "Horse",    # 1 Ashwini
    "Elephant", # 2 Bharani
    "Sheep",    # 3 Krittika
    "Serpent",  # 4 Rohini
    "Serpent",  # 5 Mrigashira
    "Dog",      # 6 Ardra
    "Cat",      # 7 Punarvasu
    "Sheep",    # 8 Pushya
    "Cat",      # 9 Ashlesha
    "Rat",      # 10 Magha
    "Rat",      # 11 Purva Phalguni
    "Cow",      # 12 Uttara Phalguni
    "Buffalo",  # 13 Hasta
    "Tiger",    # 14 Chitra
    "Buffalo",  # 15 Swati
    "Tiger",    # 16 Vishakha
    "Deer",     # 17 Anuradha
    "Deer",     # 18 Jyeshtha
    "Dog",      # 19 Mula
    "Monkey",   # 20 Purva Ashadha
    "Mongoose", # 21 Uttara Ashadha
    "Monkey",   # 22 Shravana
    "Lion",     # 23 Dhanishtha
    "Horse",    # 24 Shatabhisha
    "Lion",     # 25 Purva Bhadrapada
    "Cow",      # 26 Uttara Bhadrapada
    "Elephant"  # 27 Revati
]

# 0=Adi, 1=Madhya, 2=Antya
NAKSHATRA_NADI = [
    0, 1, 2, 2, 1, 0, 0, 1, 2, # 1-9
    2, 1, 0, 0, 1, 2, 1, 1, 0, # 10-18
    0, 1, 2, 2, 1, 0, 0, 1, 2  # 19-27
]

YONI_MATRI = {
    "Horse":    ["Horse", "Elephant", "Sheep", "Serpent", "Dog", "Cat", "Rat", "Cow", "Buffalo", "Tiger", "Deer", "Monkey", "Lion", "Mongoose"],
    # Yoni compatibility is complex, usually a table of 0-4 points.
}

# Simplified Yoni Table (0=Enemy, 1=Neutral, 2=Friendly, 3=Very Friendly, 4=Same)
YONI_SCORE_TABLE = {
    "Horse":    {"Horse": 4, "Elephant": 2, "Sheep": 2, "Serpent": 3, "Dog": 2, "Cat": 2, "Rat": 2, "Cow": 1, "Buffalo": 0, "Tiger": 1, "Deer": 3, "Monkey": 3, "Lion": 1, "Mongoose": 2},
    "Elephant": {"Horse": 2, "Elephant": 4, "Sheep": 3, "Serpent": 3, "Dog": 2, "Cat": 2, "Rat": 2, "Cow": 2, "Buffalo": 3, "Tiger": 1, "Deer": 2, "Monkey": 3, "Lion": 0, "Mongoose": 2},
    "Sheep":    {"Horse": 2, "Elephant": 3, "Sheep": 4, "Serpent": 2, "Dog": 1, "Cat": 2, "Rat": 1, "Cow": 3, "Buffalo": 3, "Tiger": 1, "Deer": 2, "Monkey": 0, "Lion": 1, "Mongoose": 2},
    "Serpent":  {"Horse": 3, "Elephant": 3, "Sheep": 2, "Serpent": 4, "Dog": 2, "Cat": 1, "Rat": 1, "Cow": 1, "Buffalo": 1, "Tiger": 2, "Deer": 2, "Monkey": 2, "Lion": 1, "Mongoose": 0},
    "Dog":      {"Horse": 2, "Elephant": 2, "Sheep": 1, "Serpent": 2, "Dog": 4, "Cat": 2, "Rat": 1, "Cow": 2, "Buffalo": 2, "Tiger": 1, "Deer": 0, "Monkey": 2, "Lion": 1, "Mongoose": 1},
    "Cat":      {"Horse": 2, "Elephant": 2, "Sheep": 2, "Serpent": 1, "Dog": 2, "Cat": 4, "Rat": 0, "Cow": 2, "Buffalo": 2, "Tiger": 2, "Deer": 3, "Monkey": 2, "Lion": 1, "Mongoose": 1},
    "Rat":      {"Horse": 2, "Elephant": 2, "Sheep": 1, "Serpent": 1, "Dog": 1, "Cat": 0, "Rat": 4, "Cow": 2, "Buffalo": 2, "Tiger": 2, "Deer": 2, "Monkey": 1, "Lion": 1, "Mongoose": 0},
    "Cow":      {"Horse": 1, "Elephant": 2, "Sheep": 3, "Serpent": 1, "Dog": 2, "Cat": 2, "Rat": 2, "Cow": 4, "Buffalo": 3, "Tiger": 0, "Deer": 3, "Monkey": 2, "Lion": 1, "Mongoose": 2},
    "Buffalo":  {"Horse": 0, "Elephant": 3, "Sheep": 3, "Serpent": 1, "Dog": 2, "Cat": 2, "Rat": 2, "Cow": 3, "Buffalo": 4, "Tiger": 1, "Deer": 2, "Monkey": 2, "Lion": 1, "Mongoose": 2},
    "Tiger":    {"Horse": 1, "Elephant": 1, "Sheep": 1, "Serpent": 2, "Dog": 1, "Cat": 2, "Rat": 2, "Cow": 0, "Buffalo": 1, "Tiger": 4, "Deer": 1, "Monkey": 1, "Lion": 2, "Mongoose": 1},
    "Deer":     {"Horse": 3, "Elephant": 2, "Sheep": 2, "Serpent": 2, "Dog": 0, "Cat": 3, "Rat": 2, "Cow": 3, "Buffalo": 2, "Tiger": 1, "Deer": 4, "Monkey": 2, "Lion": 1, "Mongoose": 2},
    "Monkey":   {"Horse": 3, "Elephant": 3, "Sheep": 0, "Serpent": 2, "Dog": 2, "Cat": 2, "Rat": 1, "Cow": 2, "Buffalo": 2, "Tiger": 1, "Deer": 2, "Monkey": 4, "Lion": 3, "Mongoose": 2},
    "Lion":     {"Horse": 1, "Elephant": 0, "Sheep": 1, "Serpent": 1, "Dog": 1, "Cat": 1, "Rat": 1, "Cow": 1, "Buffalo": 1, "Tiger": 2, "Deer": 1, "Monkey": 3, "Lion": 4, "Mongoose": 2},
    "Mongoose": {"Horse": 2, "Elephant": 2, "Sheep": 2, "Serpent": 0, "Dog": 1, "Cat": 1, "Rat": 0, "Cow": 2, "Buffalo": 2, "Tiger": 1, "Deer": 2, "Monkey": 2, "Lion": 2, "Mongoose": 4},
}

RASHI_VARNA = [
    0, # 0 Mesha (Kshatriya=1) -> mapping: 0=Brahmin, 1=Kshatriya, 2=Vaishya, 3=Shudra
    2, # 1 Vrishabha (Vaishya)
    3, # 2 Mithuna (Shudra)
    0, # 3 Karka (Brahmin)
    1, # 4 Simha (Kshatriya)
    2, # 5 Kanya (Vaishya)
    3, # 6 Tula (Shudra)
    0, # 7 Vrishchika (Brahmin)
    1, # 8 Dhanu (Kshatriya)
    2, # 9 Makara (Vaishya)
    3, # 10 Kumbha (Shudra)
    0, # 11 Meena (Brahmin)
]

RASHI_VASHYA = [
    "Chatushpad", # 0 Mesha
    "Chatushpad", # 1 Vrishabha
    "Manav",      # 2 Mithuna
    "Jalchar",    # 3 Karka
    "Chatushpad", # 4 Simha
    "Manav",      # 5 Kanya
    "Manav",      # 6 Tula
    "Keet",       # 7 Vrishchika
    "Manav",      # 8 Dhanu (1st half) -> Simplified
    "Jalchar",    # 9 Makara (2nd half) -> Simplified
    "Manav",      # 10 Kumbha
    "Jalchar",    # 11 Meena
]

# Graha Maitri (Friendship) Score Table
# 0=Sun, 1=Moon, 2=Mars, 3=Mercury, 4=Jupiter, 5=Venus, 6=Saturn
PLANET_FRIENDSHIP = [
    [5, 5, 5, 4, 5, 0, 0], # Sun
    [5, 5, 4, 5, 4, 3, 3], # Moon
    [5, 4, 5, 0, 5, 3, 3], # Mars
    [4, 1, 1, 5, 1, 5, 4], # Mercury
    [5, 4, 5, 0, 5, 0, 0], # Jupiter
    [0, 0, 3, 5, 3, 5, 5], # Venus
    [0, 0, 0, 5, 0, 5, 5], # Saturn
]

RASHI_LORDS = [0, 5, 3, 1, 0, 3, 5, 2, 4, 6, 6, 4]
