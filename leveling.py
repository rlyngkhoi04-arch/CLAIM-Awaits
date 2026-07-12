"""Leveling and rank system for CLAIM: Awaits"""

# EXP required to advance from the current level to the next
LEVEL_THRESHOLDS = {}
base_exp = 100
for lvl in range(1, 101):
    LEVEL_THRESHOLDS[lvl] = int(base_exp)
    base_exp = int(base_exp * 1.15) + 20

RANKS = [
    "Novice", "Trained", "Intermediate", "Advanced",
    "Expert", "Master", "Grandmaster", "Dominator"
]

def get_exp_for_level(level: int) -> int:
    """Get EXP needed to reach next level."""
    return LEVEL_THRESHOLDS.get(min(max(level, 1), 100), 999999)

def get_rank_from_level(level: int) -> str:
    """Get rank title from level."""
    if level >= 90:
        return "Dominator"
    elif level >= 80:
        return "Grandmaster"
    elif level >= 65:
        return "Master"
    elif level >= 50:
        return "Expert"
    elif level >= 35:
        return "Advanced"
    elif level >= 20:
        return "Intermediate"
    elif level >= 10:
        return "Trained"
    else:
        return "Novice"

def get_rank_index(rank: str) -> int:
    """Get numeric index of rank."""
    try:
        return RANKS.index(rank)
    except ValueError:
        return 0

def add_exp(player: dict, amount: int) -> list:
    """Add EXP to player and handle level-ups. Returns list of level-up messages."""
    messages = []

    if player.get("level", 1) >= 100:
        return messages

    player["exp"] = player.get("exp", 0) + max(0, int(amount))

    while player["level"] < 100 and player["exp"] >= player["exp_to_next"]:
        player["exp"] -= player["exp_to_next"]
        player["level"] += 1
        player["exp_to_next"] = get_exp_for_level(player["level"])
        player["skill_points"] = player.get("skill_points", 0) + 1

        stat_gains = {
            "Warrior": {"health": 10, "attack": 2, "defense": 2},
            "Mage": {"health": 5, "attack": 3, "defense": 1},
            "Rogue": {"health": 6, "attack": 2, "defense": 1},
            "Paladin": {"health": 12, "attack": 1, "defense": 3},
            "Berserker": {"health": 8, "attack": 3, "defense": 0},
            "Ranger": {"health": 7, "attack": 2, "defense": 1},
        }

        pclass = player.get("class", "Warrior")
        gains = stat_gains.get(pclass, stat_gains["Warrior"])

        player["max_health"] = player.get("max_health", 1) + gains["health"]
        player["health"] = player.get("health", 1) + gains["health"]
        player["attack"] = player.get("attack", 1) + gains["attack"]
        player["defense"] = player.get("defense", 0) + gains["defense"]

        if player["level"] % 5 == 0:
            player["critical_chance"] = min(50, player.get("critical_chance", 5) + 1)
            player["dodge_chance"] = min(40, player.get("dodge_chance", 5) + 1)

        if player["level"] % 3 == 0:
            player["escape_chance"] = min(80, player.get("escape_chance", 30) + 2)

        old_rank = get_rank_from_level(player["level"] - 1)
        new_rank = get_rank_from_level(player["level"])

        if old_rank != new_rank:
            messages.append(
                f"LEVEL UP! {player['name']} reached Level {player['level']}! "
                f"Rank: {new_rank} (+{gains['health']} HP, +{gains['attack']} ATK, +{gains['defense']} DEF) "
                f"+1 Skill Point!"
            )
        else:
            messages.append(
                f"Level Up! {player['name']} is now Level {player['level']}! "
                f"(+{gains['health']} HP, +{gains['attack']} ATK, +{gains['defense']} DEF) "
                f"+1 Skill Point!"
            )

    if player["level"] >= 100:
        player["level"] = 100
        player["exp"] = min(player["exp"], player["exp_to_next"])

    return messages

def get_level_progress(player: dict) -> dict:
    """Get level progress info."""
    exp = player.get("exp", 0)
    exp_to_next = max(1, player.get("exp_to_next", 100))
    percent = min(100, int((exp / exp_to_next) * 100))

    return {
        "level": player.get("level", 1),
        "rank": get_rank_from_level(player.get("level", 1)),
        "exp": exp,
        "exp_to_next": exp_to_next,
        "percent": percent,
        "skill_points": player.get("skill_points", 0),
    }