"""Save and load system for CLAIM: Awaits"""

import json
import os
from typing import Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "saves")

CLASS_BASE_STATS = {
    "Warrior": {"health": 120, "attack": 12, "defense": 8},
    "Mage": {"health": 80, "attack": 18, "defense": 3},
    "Rogue": {"health": 90, "attack": 14, "defense": 5},
    "Paladin": {"health": 130, "attack": 10, "defense": 10},
    "Berserker": {"health": 110, "attack": 20, "defense": 2},
    "Ranger": {"health": 95, "attack": 15, "defense": 6},
}

RANKS = [
    "Novice", "Trained", "Intermediate", "Advanced",
    "Expert", "Master", "Grandmaster", "Dominator"
]

def get_rank(level: int) -> str:
    """Get character rank based on level (1-100)."""
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

def new_player(name: str, player_class: str) -> dict:
    """Create a new player with all required fields."""
    name = str(name).strip() if name else "Claimant"
    player_class = str(player_class).strip() if player_class else "Warrior"

    if player_class not in CLASS_BASE_STATS:
        player_class = "Warrior"

    stats = CLASS_BASE_STATS[player_class]

    base_mana = {
        "Warrior": 40,
        "Mage": 100,
        "Rogue": 60,
        "Paladin": 70,
        "Berserker": 35,
        "Ranger": 65,
    }.get(player_class, 50)

    return {
        "name": name or "Claimant",
        "class": player_class,
        "level": 1,
        "exp": 0,
        "exp_to_next": 100,
        "health": stats["health"],
        "max_health": stats["health"],
        "mana": base_mana,
        "max_mana": base_mana,
        "attack": stats["attack"],
        "defense": stats["defense"],
        "gold": 50,
        "inventory": [],
        "equipment": {},
        "location": "Grasslands",
        "skill_points": 0,
        "bosses_defeated": [],
        "completed_missions": [],
        "active_missions": [],
        "active_buffs": {},
        "dot_effects": [],
        "critical_chance": 5,
        "dodge_chance": 5,
        "escape_chance": 30,
        "house": None,
        "farm": None,
        "servants": [],
        "tax_due": 0,
        "tax_paid_total": 0,
        "play_time": 0,
        "monsters_killed": 0,
        "items_found": 0,
    }

def load_game(save_name: str) -> Optional[dict]:
    """Load player data from a JSON save file."""
    safe_name = str(save_name).strip().replace(" ", "_")
    save_path = os.path.join(SAVE_DIR, f"{safe_name}.json")

    if not os.path.exists(save_path):
        return None

    try:
        with open(save_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError, IOError, ValueError):
        return None

    if not isinstance(data, dict):
        return None

    player = data

    defaults = {
        "name": "Claimant",
        "class": "Warrior",
        "level": 1,
        "exp": 0,
        "exp_to_next": 100,
        "health": 1,
        "max_health": 1,
        "mana": 50,
        "max_mana": 50,
        "attack": 1,
        "defense": 0,
        "gold": 0,
        "inventory": [],
        "equipment": {},
        "location": "Grasslands",
        "skill_points": 0,
        "bosses_defeated": [],
        "completed_missions": [],
        "active_missions": [],
        "active_buffs": {},
        "dot_effects": [],
        "critical_chance": 5,
        "dodge_chance": 5,
        "escape_chance": 30,
        "house": None,
        "farm": None,
        "servants": [],
        "tax_due": 0,
        "tax_paid_total": 0,
        "play_time": 0,
        "monsters_killed": 0,
        "items_found": 0,
    }

    for key, default_val in defaults.items():
        player.setdefault(key, default_val)

    if player["class"] not in CLASS_BASE_STATS:
        player["class"] = "Warrior"

    try:
        player["level"] = max(1, min(100, int(player.get("level", 1))))
        player["exp"] = max(0, int(player.get("exp", 0)))
        player["exp_to_next"] = max(1, int(player.get("exp_to_next", 100)))
        player["max_health"] = max(1, int(player.get("max_health", 1)))
        player["health"] = max(0, min(int(player.get("health", 1)), player["max_health"]))
        player["mana"] = max(0, int(player.get("mana", 50)))
        player["max_mana"] = max(1, int(player.get("max_mana", 50)))
        player["mana"] = min(player["mana"], player["max_mana"])
        player["attack"] = max(0, int(player.get("attack", 1)))
        player["defense"] = max(0, int(player.get("defense", 0)))
        player["gold"] = max(0, int(player.get("gold", 0)))
        player["skill_points"] = max(0, int(player.get("skill_points", 0)))
        player["critical_chance"] = max(0, min(100, int(player.get("critical_chance", 5))))
        player["dodge_chance"] = max(0, min(100, int(player.get("dodge_chance", 5))))
        player["escape_chance"] = max(0, min(100, int(player.get("escape_chance", 30))))
        player["tax_due"] = max(0, int(player.get("tax_due", 0)))
        player["tax_paid_total"] = max(0, int(player.get("tax_paid_total", 0)))
        player["play_time"] = max(0, int(player.get("play_time", 0)))
        player["monsters_killed"] = max(0, int(player.get("monsters_killed", 0)))
        player["items_found"] = max(0, int(player.get("items_found", 0)))
    except (TypeError, ValueError):
        return None

    if not isinstance(player.get("inventory"), list):
        player["inventory"] = []
    if not isinstance(player.get("bosses_defeated"), list):
        player["bosses_defeated"] = []
    if not isinstance(player.get("completed_missions"), list):
        player["completed_missions"] = []
    if not isinstance(player.get("active_missions"), list):
        player["active_missions"] = []
    if not isinstance(player.get("equipment"), dict):
        player["equipment"] = {}
    if not isinstance(player.get("active_buffs"), dict):
        player["active_buffs"] = {}
    if not isinstance(player.get("dot_effects"), list):
        player["dot_effects"] = []
    if not isinstance(player.get("servants"), list):
        player["servants"] = []

    return player

def save_game(player: dict, save_name: str) -> bool:
    """Save player data to a JSON file."""
    safe_name = str(save_name).strip().replace(" ", "_")
    if not safe_name:
        safe_name = "save"

    save_path = os.path.join(SAVE_DIR, f"{safe_name}.json")

    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(player, f, indent=2, ensure_ascii=False)
        return True
    except (OSError, IOError, TypeError, ValueError):
        return False

def list_saves() -> list:
    """List all available save files."""
    if not os.path.exists(SAVE_DIR):
        return []

    try:
        saves = []
        for filename in os.listdir(SAVE_DIR):
            if filename.endswith(".json"):
                saves.append(filename[:-5])
        return sorted(saves)
    except OSError:
        return []

def delete_save(save_name: str) -> bool:
    """Delete a save file."""
    safe_name = str(save_name).strip().replace(" ", "_")
    save_path = os.path.join(SAVE_DIR, f"{safe_name}.json")

    if os.path.exists(save_path):
        try:
            os.remove(save_path)
            return True
        except OSError:
            return False
    return False