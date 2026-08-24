from typing import Dict

# Natural Relationships
# Friend: 1, Neutral: 0, Enemy: -1
NATURAL_RELATIONSHIPS = {
    "Sun": {"Moon": 1, "Mars": 1, "Jupiter": 1, "Mercury": 0, "Venus": -1, "Saturn": -1},
    "Moon": {"Sun": 1, "Mercury": 1, "Mars": 0, "Jupiter": 0, "Venus": 0, "Saturn": 0},
    "Mars": {"Sun": 1, "Moon": 1, "Jupiter": 1, "Venus": 0, "Saturn": 0, "Mercury": -1},
    "Mercury": {"Sun": 1, "Venus": 1, "Mars": 0, "Jupiter": 0, "Saturn": 0, "Moon": -1},
    "Jupiter": {"Sun": 1, "Moon": 1, "Mars": 1, "Saturn": 0, "Mercury": -1, "Venus": -1},
    "Venus": {"Mercury": 1, "Saturn": 1, "Mars": 0, "Jupiter": 0, "Sun": -1, "Moon": -1},
    "Saturn": {"Mercury": 1, "Venus": 1, "Jupiter": 0, "Sun": -1, "Moon": -1, "Mars": -1},
}

def get_natural_relationship(planet: str, other: str) -> str:
    """Return Friend, Neutral, or Enemy."""
    if planet == other: return "Owner"
    rel_map = NATURAL_RELATIONSHIPS.get(planet, {})
    val = rel_map.get(other, 0)
    if val == 1: return "Friend"
    if val == -1: return "Enemy"
    return "Neutral"

def get_temporary_relationship(p1_house: int, p2_house: int) -> int:
    """
    Planets in 2, 3, 4, 10, 11, 12 houses from each other are temporary friends.
    Returns 1 for Friend, -1 for Enemy.
    """
    diff = (p2_house - p1_house + 12) % 12
    # Houses 2, 3, 4, 10, 11, 12 (0-indexed house diff is 1, 2, 3, 9, 10, 11)
    if diff in [1, 2, 3, 9, 10, 11]:
        return 1
    return -1

def get_composite_relationship(planet: str, p1_house: int, other: str, p2_house: int) -> str:
    """
    Natural + Temporary = Composite
    Friend + Friend = Great Friend
    Friend + Enemy = Neutral
    Neutral + Friend = Friend
    Neutral + Enemy = Enemy
    Enemy + Friend = Neutral
    Enemy + Enemy = Great Enemy
    """
    if planet == other: return "Owner"

    n_val = NATURAL_RELATIONSHIPS.get(planet, {}).get(other, 0)
    t_val = get_temporary_relationship(p1_house, p2_house)

    comp = n_val + t_val
    if comp == 2: return "Great Friend"
    if comp == 1: return "Friend"
    if comp == 0: return "Neutral"
    if comp == -1: return "Enemy"
    if comp == -2: return "Great Enemy"
    return "Neutral"
