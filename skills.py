"""Skills system for CLAIM: Awaits - 3 skills per class"""

import random
from typing import List, Tuple

SKILLS = {
    "Warrior": [
        {
            "name": "Power Slash",
            "damage_multiplier": 1.5,
            "mana_cost": 10,
            "cooldown": 0,
            "description": "A powerful overhead slash that deals 150% damage.",
            "effect": "none",
        },
        {
            "name": "Shield Bash",
            "damage_multiplier": 1.2,
            "mana_cost": 15,
            "cooldown": 2,
            "description": "Bash the enemy with your shield. Deals 120% damage and stuns for 1 turn.",
            "effect": "stun",
            "stun_duration": 1,
        },
        {
            "name": "Berserker Rage",
            "damage_multiplier": 2.5,
            "mana_cost": 30,
            "cooldown": 5,
            "description": "Enter a battle frenzy. Deals 250% damage but take 20% recoil damage.",
            "effect": "recoil",
            "recoil_percent": 20,
        },
    ],
    "Mage": [
        {
            "name": "Fireball",
            "damage_multiplier": 1.7,
            "mana_cost": 12,
            "cooldown": 0,
            "description": "Hurl a ball of flame. Deals 170% damage with a chance to burn.",
            "effect": "burn",
            "burn_damage": 5,
            "burn_duration": 3,
        },
        {
            "name": "Frost Nova",
            "damage_multiplier": 1.4,
            "mana_cost": 18,
            "cooldown": 3,
            "description": "Freeze the area around you. Deals 140% damage and slows enemy attack.",
            "effect": "slow",
            "slow_percent": 30,
            "slow_duration": 2,
        },
        {
            "name": "Arcane Storm",
            "damage_multiplier": 3.0,
            "mana_cost": 35,
            "cooldown": 6,
            "description": "Unleash a storm of arcane energy. Deals 300% damage.",
            "effect": "aoe",
        },
    ],
    "Rogue": [
        {
            "name": "Shadow Strike",
            "damage_multiplier": 1.8,
            "mana_cost": 10,
            "cooldown": 0,
            "description": "Strike from the shadows. Deals 180% damage with high crit chance.",
            "effect": "crit_bonus",
            "crit_bonus": 20,
        },
        {
            "name": "Poison Blade",
            "damage_multiplier": 1.3,
            "mana_cost": 14,
            "cooldown": 2,
            "description": "Coat your blade in poison. Deals 130% damage and poisons for 4 turns.",
            "effect": "poison",
            "poison_damage": 8,
            "poison_duration": 4,
        },
        {
            "name": "Assassinate",
            "damage_multiplier": 4.0,
            "mana_cost": 40,
            "cooldown": 7,
            "description": "A devastating strike aimed at vital points. Deals 400% damage if target HP < 30%.",
            "effect": "execute",
            "execute_threshold": 0.30,
        },
    ],
    "Paladin": [
        {
            "name": "Holy Smite",
            "damage_multiplier": 1.6,
            "mana_cost": 12,
            "cooldown": 0,
            "description": "Strike with holy light. Deals 160% damage.",
            "effect": "holy",
            "holy_bonus": 10,
        },
        {
            "name": "Divine Shield",
            "damage_multiplier": 0.8,
            "mana_cost": 20,
            "cooldown": 4,
            "description": "Raise a shield of faith. Deals 80% damage and blocks next attack.",
            "effect": "block_next",
        },
        {
            "name": "Judgment",
            "damage_multiplier": 2.2,
            "mana_cost": 28,
            "cooldown": 5,
            "description": "Deliver divine judgment. Deals 220% damage and heals for 50% of damage dealt.",
            "effect": "life_steal",
            "life_steal_percent": 50,
        },
    ],
    "Berserker": [
        {
            "name": "Cleave",
            "damage_multiplier": 1.4,
            "mana_cost": 8,
            "cooldown": 0,
            "description": "A wide sweeping attack. Deals 140% damage.",
            "effect": "none",
        },
        {
            "name": "Blood Fury",
            "damage_multiplier": 2.0,
            "mana_cost": 20,
            "cooldown": 3,
            "description": "Sacrifice 15% max HP for immense power. Deals 200% damage.",
            "effect": "self_damage",
            "self_damage_percent": 15,
        },
        {
            "name": "World Shatter",
            "damage_multiplier": 3.5,
            "mana_cost": 45,
            "cooldown": 6,
            "description": "A devastating ground slam. Deals 350% damage and ignores 50% defense.",
            "effect": "armor_pierce",
            "pierce_percent": 50,
        },
    ],
    "Ranger": [
        {
            "name": "Piercing Shot",
            "damage_multiplier": 1.6,
            "mana_cost": 10,
            "cooldown": 0,
            "description": "A precise shot through weak points. Deals 160% damage.",
            "effect": "none",
        },
        {
            "name": "Volley",
            "damage_multiplier": 1.2,
            "mana_cost": 16,
            "cooldown": 3,
            "description": "Fire a hail of arrows. Deals 120% damage x3 hits.",
            "effect": "multi_hit",
            "hits": 3,
        },
        {
            "name": "Eagle Eye",
            "damage_multiplier": 2.8,
            "mana_cost": 30,
            "cooldown": 5,
            "description": "Focus completely. Next attacks have bonus critical chance.",
            "effect": "buff_crit",
            "crit_bonus": 25,
            "buff_duration": 3,
        },
    ],
}

class SkillSystem:
    """Manages player skills, cooldowns, and skill usage."""

    def __init__(self):
        self.cooldowns = {}

    def get_class_skills(self, player_class: str) -> List[dict]:
        """Get all skills for a class."""
        return SKILLS.get(player_class, [])

    def get_available_skills(self, player: dict) -> List[dict]:
        """Get skills that are off cooldown and affordable."""
        skills = self.get_class_skills(player.get("class", "Warrior"))
        available = []

        for skill in skills:
            name = skill["name"]
            mana_cost = skill.get("mana_cost", 0)
            current_cd = self.cooldowns.get(name, 0)
            current_mana = player.get("mana", 0)

            if current_cd <= 0 and current_mana >= mana_cost:
                available.append(skill)

        return available

    def use_skill(self, player: dict, target: dict, skill_index: int) -> Tuple[bool, str, dict]:
        """
        Use a skill on a target.
        Returns: (success, message, effect_data)
        """
        skills = self.get_class_skills(player.get("class", "Warrior"))

        if skill_index < 0 or skill_index >= len(skills):
            return False, "Invalid skill.", {}

        skill = skills[skill_index]
        name = skill["name"]
        mana_cost = skill.get("mana_cost", 0)

        if self.cooldowns.get(name, 0) > 0:
            return False, f"{name} is on cooldown for {self.cooldowns[name]} more turns.", {}

        player_mana = player.get("mana", 0)
        if player_mana < mana_cost:
            return False, f"Not enough mana. Need {mana_cost}, have {player_mana}.", {}

        player["mana"] = player_mana - mana_cost
        self.cooldowns[name] = skill.get("cooldown", 0)

        base_damage = player.get("attack", 1)
        multiplier = skill.get("damage_multiplier", 1.0)

        if skill.get("effect") == "execute":
            threshold = skill.get("execute_threshold", 0.30)
            target_hp_percent = target.get("health", 1) / max(1, target.get("max_health", 1))
            if target_hp_percent <= threshold:
                multiplier *= 1.5

        damage = int(base_damage * multiplier)

        crit_chance = player.get("critical_chance", 5)
        if "crit_bonus" in player.get("active_buffs", {}):
            crit_chance += player["active_buffs"]["crit_bonus"].get("value", 0)
        if skill.get("effect") == "crit_bonus":
            crit_chance += skill.get("crit_bonus", 0)

        is_crit = random.randint(1, 100) <= min(95, crit_chance)
        if is_crit:
            damage = int(damage * 1.5)

        if skill.get("effect") == "armor_pierce":
            pierce = skill.get("pierce_percent", 0) / 100
            target_def = target.get("defense", 0)
            effective_def = int(target_def * (1 - pierce))
            damage = max(1, damage - effective_def)
        else:
            damage = max(1, damage - target.get("defense", 0))

        target["health"] = max(0, int(target.get("health", 0)) - damage)

        effect_data = {
            "damage": damage,
            "is_critical": is_crit,
            "effect": skill.get("effect", "none"),
        }

        msg = f"{player.get('name', 'Player')} used {name}!"
        if is_crit:
            msg += " CRITICAL HIT!"
        msg += f" Dealt {damage} damage!"

        effect = skill.get("effect", "none")

        if effect == "recoil":
            recoil = int(damage * skill.get("recoil_percent", 20) / 100)
            player["health"] = max(1, player["health"] - recoil)
            msg += f" Took {recoil} recoil damage!"

        elif effect == "self_damage":
            self_dmg = int(player.get("max_health", 1) * skill.get("self_damage_percent", 15) / 100)
            player["health"] = max(1, player["health"] - self_dmg)
            msg += f" Sacrificed {self_dmg} HP!"

        elif effect == "life_steal":
            heal = int(damage * skill.get("life_steal_percent", 50) / 100)
            old_hp = player["health"]
            player["health"] = min(player.get("max_health", old_hp), player["health"] + heal)
            healed = player["health"] - old_hp
            msg += f" Healed {healed} HP!"

        elif effect == "stun":
            effect_data["stun_duration"] = skill.get("stun_duration", 1)
            msg += f" Enemy stunned for {effect_data['stun_duration']} turn(s)!"

        elif effect == "burn":
            effect_data["burn_damage"] = skill.get("burn_damage", 5)
            effect_data["burn_duration"] = skill.get("burn_duration", 3)
            msg += " Enemy is burning!"

        elif effect == "poison":
            effect_data["poison_damage"] = skill.get("poison_damage", 8)
            effect_data["poison_duration"] = skill.get("poison_duration", 4)
            msg += " Enemy is poisoned!"

        elif effect == "slow":
            effect_data["slow_percent"] = skill.get("slow_percent", 30)
            effect_data["slow_duration"] = skill.get("slow_duration", 2)
            msg += " Enemy slowed!"

        elif effect == "multi_hit":
            hits = skill.get("hits", 3)
            extra_damage = damage * (hits - 1)
            target["health"] = max(0, target["health"] - extra_damage)
            total_damage = damage * hits
            effect_data["damage"] = total_damage
            effect_data["hits"] = hits
            msg = f"{player.get('name', 'Player')} used {name}! {hits} hits for {total_damage} total damage!"

        elif effect == "block_next":
            player["block_next"] = True
            msg += " Next attack will be blocked!"

        elif effect == "buff_crit":
            player.setdefault("active_buffs", {})["crit_bonus"] = {
                "value": skill.get("crit_bonus", 25),
                "duration": skill.get("buff_duration", 3),
            }
            msg += f" Crit chance boosted for {skill.get('buff_duration', 3)} turns!"

        elif effect == "holy":
            holy_bonus = skill.get("holy_bonus", 0)
            if holy_bonus > 0:
                target["health"] = max(0, target["health"] - holy_bonus)
                effect_data["damage"] += holy_bonus
                msg += f" Holy power dealt an extra {holy_bonus} damage!"

        return True, msg, effect_data

    def tick_cooldowns(self) -> None:
        """Reduce all cooldowns by 1."""
        for name in list(self.cooldowns.keys()):
            self.cooldowns[name] = max(0, self.cooldowns[name] - 1)
            if self.cooldowns[name] <= 0:
                del self.cooldowns[name]

    def get_skill_info(self, player_class: str) -> List[dict]:
        """Get formatted skill info for display."""
        skills = self.get_class_skills(player_class)
        info = []

        for i, skill in enumerate(skills):
            info.append({
                "index": i,
                "name": skill["name"],
                "mana_cost": skill.get("mana_cost", 0),
                "cooldown": skill.get("cooldown", 0),
                "multiplier": skill.get("damage_multiplier", 1.0),
                "description": skill.get("description", ""),
                "effect": skill.get("effect", "none"),
                "on_cooldown": self.cooldowns.get(skill["name"], 0),
            })

        return info