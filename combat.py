"""Combat system for CLAIM: Awaits"""

import random
from typing import List, Tuple, Optional

def calculate_damage(attacker: dict, defender: dict, is_skill: bool = False,
                     skill_multiplier: float = 1.0) -> Tuple[int, bool]:
    """Calculate damage from attacker to defender. Returns (damage, is_critical)."""
    base_attack = attacker.get("attack", 1)

    buffs = attacker.get("active_buffs", {})
    if "attack" in buffs:
        base_attack += buffs["attack"]["value"]

    damage = int(base_attack * skill_multiplier)

    crit_chance = attacker.get("critical_chance", 5)
    if "crit_bonus" in buffs:
        crit_chance += buffs["crit_bonus"]["value"]

    is_crit = random.randint(1, 100) <= min(95, crit_chance)

    if is_crit:
        damage = int(damage * 1.5)

    defense = defender.get("defense", 0)
    if "defense" in defender.get("active_buffs", {}):
        defense += defender["active_buffs"]["defense"]["value"]

    damage = max(1, damage - defense)

    return damage, is_crit

def check_dodge(defender: dict) -> bool:
    """Check if defender dodges the attack."""
    dodge_chance = defender.get("dodge_chance", 5)
    if "speed" in defender.get("active_buffs", {}):
        dodge_chance += defender["active_buffs"]["speed"]["value"] // 2

    return random.randint(1, 100) <= min(75, dodge_chance)

def check_escape(player: dict, enemy: dict) -> bool:
    """Check if player successfully escapes combat."""
    base_escape = player.get("escape_chance", 30)

    enemy_level_factor = enemy.get("level", 1) / max(1, player.get("level", 1))
    if enemy_level_factor > 1.5:
        base_escape = int(base_escape * 0.6)
    elif enemy_level_factor > 1.0:
        base_escape = int(base_escape * 0.8)

    return random.randint(1, 100) <= min(95, base_escape)

def process_dot_effects(entity: dict) -> List[str]:
    """Process damage-over-time effects. Returns list of messages."""
    messages = []
    dots = entity.get("dot_effects", [])

    for dot in dots[:]:
        dot["duration"] -= 1

        if dot["type"] == "burn":
            damage = dot.get("damage", 5)
            entity["health"] = max(0, entity["health"] - damage)
            messages.append(f"{entity.get('name', 'Target')} burns for {damage} damage!")

        elif dot["type"] == "poison":
            damage = dot.get("damage", 8)
            entity["health"] = max(0, entity["health"] - damage)
            messages.append(f"{entity.get('name', 'Target')} takes {damage} poison damage!")

        elif dot["type"] == "regen":
            heal = dot.get("heal", 10)
            old_hp = entity["health"]
            entity["health"] = min(entity["max_health"], entity["health"] + heal)
            healed = entity["health"] - old_hp
            messages.append(f"{entity.get('name', 'Target')} regenerates {healed} HP!")

        if dot["duration"] <= 0:
            dots.remove(dot)
            messages.append(f"{dot['type'].capitalize()} effect wore off.")

    return messages

def apply_dot(target: dict, dot_type: str, damage: int, duration: int) -> None:
    """Apply a damage-over-time effect to target."""
    target.setdefault("dot_effects", []).append({
        "type": dot_type,
        "damage": damage,
        "duration": duration,
    })

def tick_buffs(entity: dict) -> List[str]:
    """Reduce buff durations. Returns list of expired buff messages."""
    messages = []
    buffs = entity.get("active_buffs", {})

    for buff_name in list(buffs.keys()):
        buffs[buff_name]["duration"] -= 1

        if buff_name == "max_health" and buffs[buff_name]["duration"] <= 0:
            entity["max_health"] = max(1, entity["max_health"] - buffs[buff_name]["value"])
            entity["health"] = min(entity["health"], entity["max_health"])

        if buffs[buff_name]["duration"] <= 0:
            del buffs[buff_name]
            messages.append(f"{buff_name.replace('_', ' ').title()} buff wore off.")

    return messages

def enemy_attack(enemy: dict, player: dict) -> Tuple[int, bool, bool, str]:
    """
    Enemy attacks player.
    Returns: (damage_dealt, is_critical, player_dodged, message)
    """
    if player.get("block_next", False):
        player["block_next"] = False
        return 0, False, False, f"{player['name']} blocked {enemy['name']}'s attack!"

    if check_dodge(player):
        return 0, False, True, f"{player['name']} dodged {enemy['name']}'s attack!"

    damage, is_crit = calculate_damage(enemy, player)

    slow_data = enemy.get("active_buffs", {}).get("slow")
    if slow_data:
        slow_percent = max(0, min(90, int(slow_data.get("value", 0))))
        damage = max(1, int(damage * (100 - slow_percent) / 100))

    player["health"] = max(0, player["health"] - damage)

    msg = f"{enemy['name']} attacks!"
    if is_crit:
        msg += " CRITICAL HIT!"
    msg += f" Dealt {damage} damage!"

    if slow_data:
        msg += " Its attack is weakened by slow!"

    return damage, is_crit, False, msg

def player_basic_attack(player: dict, enemy: dict) -> Tuple[int, bool, bool, str]:
    """
    Player basic attacks enemy.
    Returns: (damage_dealt, is_critical, enemy_dodged, message)
    """
    if check_dodge(enemy):
        return 0, False, True, f"{enemy['name']} dodged {player['name']}'s attack!"

    damage, is_crit = calculate_damage(player, enemy)
    enemy["health"] = max(0, enemy["health"] - damage)

    msg = f"{player['name']} attacks!"
    if is_crit:
        msg += " CRITICAL HIT!"
    msg += f" Dealt {damage} damage!"

    equipment = player.get("equipment", {})
    for item in equipment.values():
        if item and "life_steal" in item:
            steal = int(damage * item["life_steal"] / 100)
            if steal > 0:
                old_hp = player["health"]
                player["health"] = min(player["max_health"], player["health"] + steal)
                healed = player["health"] - old_hp
                msg += f" Stole {healed} HP!"
                break

    return damage, is_crit, False, msg

def generate_loot_message(item_name: str, rank: str, color: str) -> str:
    """Generate an exciting loot drop message."""
    messages = {
        "Common": [
            f"You found a {item_name}! Not bad.",
            f"A {item_name} lies on the ground.",
            f"Picked up a {item_name}.",
        ],
        "Enhanced": [
            f"Nice! A {item_name} dropped!",
            f"Lucky find - a {item_name}!",
            f"This {item_name} looks well-made!",
        ],
        "Rare": [
            f"Excellent! A rare {item_name} appeared!",
            f"The {item_name} glows with rare power!",
            f"Fortune smiles! A {item_name}!",
        ],
        "Epic": [
            f"INCREDIBLE! An epic {item_name} drops!",
            f"The ground trembles as a {item_name} appears!",
            f"LEGENDARY FIND! ...Wait, it's just Epic. Still amazing!",
        ],
        "Legend": [
            f"THE GODS BLESS YOU! A LEGENDARY {item_name.upper()}!",
            f"Reality itself bends around this {item_name}!",
            f"You feel the weight of destiny in this {item_name}!",
        ],
        "Dominant": [
            f"IMPOSSIBLE! A DOMINANT {item_name.upper()} HAS MANIFESTED!",
            f"THE VERY FABRIC OF EXISTENCE SHATTERS! A DOMINANT {item_name.upper()}!",
            f"ALL HAIL THE CLAIMANT! A DOMINANT {item_name.upper()} IS YOURS!",
            f"THE REALM TREMBLES BEFORE YOUR LUCK! DOMINANT {item_name.upper()}!",
        ],
    }

    return random.choice(messages.get(rank, [f"Found {item_name}."]))

def combat_victory(player: dict, enemy: dict, biomes: dict, items_module) -> List[str]:
    """Handle post-combat rewards. Returns list of messages."""
    messages = []

    exp_gained = enemy.get("exp", 10)
    from leveling import add_exp
    level_msgs = add_exp(player, exp_gained)
    messages.extend(level_msgs)
    messages.append(f"Gained {exp_gained} EXP!")

    gold_gained = enemy.get("gold", 5)
    player["gold"] += gold_gained
    messages.append(f"Found {gold_gained} Gold!")

    biome_name = player.get("location", "Grasslands")
    success, loot_msg = items_module.give_random_loot(player, biome_name, biomes)
    if success:
        messages.append(loot_msg)

    bounty_chance = random.randint(1, 100)
    if bounty_chance <= 30:
        bounty_items = [
            "Goblin Ear", "Wolf Pelt", "Slime Gel", "Spider Venom Sac",
            "Orc Trophy", "Bandit Mask", "Wraith Essence", "Shadow Fragment"
        ]
        bounty = random.choice(bounty_items)
        items_module.add_item(player, bounty)
        messages.append(f"Bounty item: {bounty}!")

    from items import update_mission_progress
    mission_msgs = update_mission_progress(player, enemy.get("name", "Unknown"))
    messages.extend(mission_msgs)

    player["monsters_killed"] = player.get("monsters_killed", 0) + 1

    return messages

def create_combat_enemy(biome_name: str, biomes: dict) -> Optional[dict]:
    """Create a fresh enemy instance for combat."""
    biome = biomes.get(biome_name)
    if not biome:
        return None

    monsters = biome.get("monsters", [])
    if not monsters:
        return None

    enemy = random.choice(monsters).copy()
    enemy["max_health"] = enemy["health"]
    enemy["dot_effects"] = []
    enemy["active_buffs"] = {}
    enemy["stunned"] = 0

    return enemy