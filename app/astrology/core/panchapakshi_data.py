from typing import Dict, List, Any

# Activities in order: 0=Eating, 1=Walking, 2=Ruling, 3=Sleeping, 4=Dying
# Weekday order: 0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri, 6=Sat

# Segment 1 to 5 for each Day/Bird
ACTIVITIES_TABLE_DAY = {
    "Vulture": {
        0: [0, 1, 2, 3, 4], # Sun
        1: [1, 2, 3, 4, 0], # Mon
        2: [2, 3, 4, 0, 1], # Tue
        3: [3, 4, 0, 1, 2], # Wed
        4: [4, 0, 1, 2, 3], # Thu
        5: [0, 1, 2, 3, 4], # Fri
        6: [1, 2, 3, 4, 0]  # Sat
    },
    "Owl": {
        0: [1, 2, 3, 4, 0],
        1: [2, 3, 4, 0, 1],
        2: [3, 4, 0, 1, 2],
        3: [4, 0, 1, 2, 3],
        4: [0, 1, 2, 3, 4],
        5: [1, 2, 3, 4, 0],
        6: [2, 3, 4, 0, 1]
    },
    "Crow": {
        0: [2, 3, 4, 0, 1],
        1: [3, 4, 0, 1, 2],
        2: [4, 0, 1, 2, 3],
        3: [0, 1, 2, 3, 4],
        4: [1, 2, 3, 4, 0],
        5: [2, 3, 4, 0, 1],
        6: [3, 4, 0, 1, 2]
    },
    "Cock": {
        0: [3, 4, 0, 1, 2],
        1: [4, 0, 1, 2, 3],
        2: [0, 1, 2, 3, 4],
        3: [1, 2, 3, 4, 0],
        4: [2, 3, 4, 0, 1],
        5: [3, 4, 0, 1, 2],
        6: [4, 0, 1, 2, 3]
    },
    "Peacock": {
        0: [4, 0, 1, 2, 3],
        1: [0, 1, 2, 3, 4],
        2: [1, 2, 3, 4, 0],
        3: [2, 3, 4, 0, 1],
        4: [3, 4, 0, 1, 2],
        5: [4, 0, 1, 2, 3],
        6: [0, 1, 2, 3, 4]
    }
}

ACTIVITY_NAMES = ["Eating", "Walking", "Ruling", "Sleeping", "Dying"]

def get_segment_activity(bird: str, weekday: int, segment: int) -> str:
    """
    weekday: 0=Sun, 6=Sat
    segment: 0-4
    """
    if bird not in ACTIVITIES_TABLE_DAY: return "Unknown"
    act_list = ACTIVITIES_TABLE_DAY[bird].get(weekday, [])
    if not act_list: return "Unknown"

    act_idx = act_list[segment]
    return ACTIVITY_NAMES[act_idx]
