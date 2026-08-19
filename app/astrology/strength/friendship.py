from typing import Dict, List, Set

# Natural Friendships (Naisargika Maitri)
# Format: {Planet: (Friends, Neutral, Enemies)}
NATURAL_FRIENDSHIP = {
    "Sun":     ({"Moon", "Mars", "Jupiter"}, {"Mercury"}, {"Venus", "Saturn"}),
    "Moon":    ({"Sun", "Mercury"}, {"Mars", "Jupiter", "Venus", "Saturn"}, set()),
    "Mars":    ({"Sun", "Moon", "Jupiter"}, {"Venus", "Saturn"}, {"Mercury"}),
    "Mercury": ({"Sun", "Venus"}, {"Mars", "Jupiter", "Saturn"}, {"Moon"}),
    "Jupiter": ({"Sun", "Moon", "Mars"}, {"Saturn"}, {"Mercury", "Venus"}),
    "Venus":   ({"Mercury", "Saturn"}, {"Mars", "Jupiter"}, {"Sun", "Moon"}),
    "Saturn":  ({"Mercury", "Venus"}, {"Jupiter"}, {"Sun", "Moon", "Mars"}),
}

def get_temporal_friendship(p1_house: int, p2_house: int) -> int:
    """
    Calculate Temporal Friendship (Tatkalika Maitri).
    Planets in 2nd, 3rd, 4th, 10th, 11th, 12th houses from a planet are friends.
    Returns: 1 for Friend, -1 for Enemy.
    """
    diff = (p2_house - p1_house + 12) % 12
    # Houses: 2, 3, 4, 10, 11, 12 (0-indexed: 1, 2, 3, 9, 10, 11)
    if diff in {1, 2, 3, 9, 10, 11}:
        return 1
    return -1

def get_compound_friendship(p1: str, p2: str, p1_house: int, p2_house: int) -> str:
    """
    Calculate Compound Friendship (Panchadha Maitri).
    Returns: Great Friend, Friend, Neutral, Enemy, Great Enemy.
    """
    if p1 not in NATURAL_FRIENDSHIP or p2 not in NATURAL_FRIENDSHIP:
        return "Neutral"

    friends, neutral, enemies = NATURAL_FRIENDSHIP[p1]

    natural_score = 0
    if p2 in friends: natural_score = 1
    elif p2 in enemies: natural_score = -1

    temporal_score = get_temporal_friendship(p1_house, p2_house)

    total = natural_score + temporal_score

    if total == 2: return "Great Friend"
    if total == 1: return "Friend"
    if total == 0: return "Neutral"
    if total == -1: return "Enemy"
    return "Great Enemy"
