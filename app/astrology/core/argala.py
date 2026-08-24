from typing import Dict, List, Any

# Primary Argala: 2, 4, 11
# Obstruction: 12, 10, 3 (respectively)
# Secondary Argala: 5. Obstruction: 9.

def calculate_full_argala(planets: Dict[str, Any], asc_rashi: int) -> Dict[int, Dict[str, List[str]]]:
    results = {}

    # Sign index for each house
    house_to_rashi = {h: (asc_rashi + h - 1) % 12 for h in range(1, 13)}

    for h in range(1, 13):
        h_rashi = house_to_rashi[h]

        argala = {"Primary": [], "Secondary": [], "Obstructing": []}

        # 2nd from house
        r2 = (h_rashi + 1) % 12
        argala["Primary"].extend([p for p, info in planets.items() if info.rashi == r2])

        # 12th from house (obstructs 2)
        r12 = (h_rashi + 11) % 12
        argala["Obstructing"].extend([p for p, info in planets.items() if info.rashi == r12])

        # 4th from house
        r4 = (h_rashi + 3) % 12
        argala["Primary"].extend([p for p, info in planets.items() if info.rashi == r4])

        # 10th from house (obstructs 4)
        r10 = (h_rashi + 9) % 12
        argala["Obstructing"].extend([p for p, info in planets.items() if info.rashi == r10])

        # 11th from house
        r11 = (h_rashi + 10) % 12
        argala["Primary"].extend([p for p, info in planets.items() if info.rashi == r11])

        # 3rd from house (obstructs 11)
        r3 = (h_rashi + 2) % 12
        argala["Obstructing"].extend([p for p, info in planets.items() if info.rashi == r3])

        # 5th from house (Secondary)
        r5 = (h_rashi + 4) % 12
        argala["Secondary"].extend([p for p, info in planets.items() if info.rashi == r5])

        # 9th from house (obstructs 5)
        r9 = (h_rashi + 8) % 12
        argala["Obstructing"].extend([p for p, info in planets.items() if info.rashi == r9])

        results[h] = argala

    return results
