"""Biome data and progression system for CLAIM: Awaits"""

from typing import List, Optional
import random
import copy

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
    """Get character rank based on level."""
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
    return "Novice"

def get_rank_index(rank: str) -> int:
    """Get numeric index of rank."""
    try:
        return RANKS.index(rank)
    except ValueError:
        return 0

BIOMES = {
    "Grasslands": {
        "description": "A peaceful plain where the journey begins. Soft grass stretches to the horizon.",
        "required_level": 1,
        "required_rank": "Novice",
        "required_bosses": [],
        "recommended_level": "1-10",
        "recommended_rank": "Novice - Trained",
        "danger_level": "Safe",
        "monsters": [
            {"name": "Slime", "health": 20, "attack": 5, "defense": 1, "exp": 20, "gold": 10, "level": 1},
            {"name": "Wild Rabbit", "health": 15, "attack": 4, "defense": 0, "exp": 15, "gold": 8, "level": 1},
            {"name": "Goblin Scout", "health": 25, "attack": 6, "defense": 2, "exp": 25, "gold": 12, "level": 2},
            {"name": "Stray Dog", "health": 22, "attack": 5, "defense": 1, "exp": 20, "gold": 10, "level": 2},
            {"name": "Field Bandit", "health": 30, "attack": 7, "defense": 2, "exp": 30, "gold": 15, "level": 3},
            {"name": "Horned Beetle", "health": 35, "attack": 6, "defense": 3, "exp": 28, "gold": 14, "level": 3},
            {"name": "Mud Crawler", "health": 28, "attack": 6, "defense": 2, "exp": 26, "gold": 13, "level": 3},
            {"name": "Grass Sprite", "health": 18, "attack": 7, "defense": 0, "exp": 24, "gold": 12, "level": 4},
            {"name": "Tiny Boar", "health": 32, "attack": 8, "defense": 2, "exp": 30, "gold": 16, "level": 4},
            {"name": "Broken Knight", "health": 40, "attack": 9, "defense": 4, "exp": 35, "gold": 18, "level": 5},
            {"name": "Rusty Drone", "health": 25, "attack": 7, "defense": 2, "exp": 28, "gold": 14, "level": 4},
            {"name": "Cursed Crow", "health": 20, "attack": 9, "defense": 1, "exp": 26, "gold": 13, "level": 5},
            {"name": "Lost Farmer Spirit", "health": 30, "attack": 8, "defense": 2, "exp": 32, "gold": 15, "level": 5},
            {"name": "Stone Rat", "health": 35, "attack": 7, "defense": 3, "exp": 30, "gold": 15, "level": 5},
            {"name": "Wind Imp", "health": 22, "attack": 10, "defense": 1, "exp": 34, "gold": 17, "level": 6},
        ],
        "loot": {
            "Small Potion": {"type": "consumable", "effect": "heal", "value": 25},
            "Herb": {"type": "consumable", "effect": "heal", "value": 10},
            "Old Coin": {"type": "material", "effect": "none", "value": 5},
            "Torn Cloth": {"type": "armor", "effect": "none", "value": 2},
            "Moss Clump": {"type": "consumable", "effect": "heal", "value": 5},
            "Honey Jar": {"type": "consumable", "effect": "heal", "value": 20},
        },
        "boss": {
            "name": "Troll King",
            "title": "Chieftain of the Mud Throne",
            "description": "A hulking brute who has crushed every challenger beneath his iron club.",
            "level": 8,
            "health": 200,
            "max_health": 200,
            "attack": 25,
            "defense": 8,
            "exp": 200,
            "gold": 150,
            "ability": {
                "name": "Ground Smash",
                "damage_multiplier": 1.5,
                "cooldown_turns": 3,
                "description": "A devastating overhead strike that deals 150% damage.",
            },
            "loot": [
                {"name": "Legendary Amulet", "drop_rate": 1.0},
                {"name": "Iron Sword", "drop_rate": 0.8},
                {"name": "Small Potion", "drop_rate": 1.0},
            ],
            "intro_text": "The ground trembles as the Troll King rises from his mud throne, club in hand.",
            "defeat_text": "The Troll King collapses with a thunderous roar. The Grasslands are free.",
        },
    },
    "Forest": {
        "description": "A dense woodland filled with lurking dangers. Sunlight barely pierces the canopy.",
        "required_level": 8,
        "required_rank": "Trained",
        "required_bosses": ["Grasslands"],
        "recommended_level": "8-20",
        "recommended_rank": "Trained - Intermediate",
        "danger_level": "Moderate",
        "monsters": [
            {"name": "Wolf", "health": 30, "attack": 8, "defense": 3, "exp": 30, "gold": 15, "level": 8},
            {"name": "Forest Spider", "health": 25, "attack": 9, "defense": 2, "exp": 28, "gold": 14, "level": 8},
            {"name": "Orc Warrior", "health": 45, "attack": 12, "defense": 5, "exp": 40, "gold": 20, "level": 10},
            {"name": "Treant Sapling", "health": 50, "attack": 10, "defense": 6, "exp": 45, "gold": 22, "level": 10},
            {"name": "Poison Snake", "health": 20, "attack": 11, "defense": 1, "exp": 30, "gold": 18, "level": 9},
            {"name": "Shadow Stalker", "health": 35, "attack": 13, "defense": 4, "exp": 50, "gold": 25, "level": 12},
            {"name": "Wood Bandit", "health": 38, "attack": 11, "defense": 4, "exp": 36, "gold": 18, "level": 11},
            {"name": "Thorn Beast", "health": 55, "attack": 12, "defense": 6, "exp": 48, "gold": 24, "level": 12},
            {"name": "Forest Spirit", "health": 40, "attack": 14, "defense": 3, "exp": 52, "gold": 26, "level": 13},
            {"name": "Moss Golem", "health": 60, "attack": 11, "defense": 7, "exp": 55, "gold": 28, "level": 14},
            {"name": "Venom Lizard", "health": 33, "attack": 13, "defense": 4, "exp": 42, "gold": 21, "level": 11},
            {"name": "Dark Elf Scout", "health": 37, "attack": 15, "defense": 4, "exp": 50, "gold": 25, "level": 13},
            {"name": "Rotting Stag", "health": 45, "attack": 12, "defense": 5, "exp": 47, "gold": 23, "level": 12},
            {"name": "Feral Druid", "health": 42, "attack": 14, "defense": 4, "exp": 53, "gold": 27, "level": 14},
            {"name": "Whispering Shade", "health": 38, "attack": 16, "defense": 3, "exp": 58, "gold": 30, "level": 15},
        ],
        "loot": {
            "Medium Potion": {"type": "consumable", "effect": "heal", "value": 50},
            "Forest Gem": {"type": "material", "effect": "none", "value": 25},
            "Spider Silk": {"type": "material", "effect": "none", "value": 15},
            "Enchanted Leaf": {"type": "consumable", "effect": "buff_attack", "value": 5, "duration": 3},
            "Bandage Roll": {"type": "consumable", "effect": "heal", "value": 15},
            "Strength Tonic": {"type": "consumable", "effect": "buff_attack", "value": 8, "duration": 5},
        },
        "boss": {
            "name": "Ancient Treant",
            "title": "Root of the Eternal Grove",
            "description": "A living tree older than kingdoms, its roots drink from veins of ancient magic.",
            "level": 18,
            "health": 250,
            "max_health": 250,
            "attack": 30,
            "defense": 12,
            "exp": 250,
            "gold": 200,
            "ability": {
                "name": "Root Slam",
                "damage_multiplier": 1.5,
                "cooldown_turns": 3,
                "description": "Smashes the ground with colossal roots, dealing 150% damage.",
            },
            "loot": [
                {"name": "Epic Staff", "drop_rate": 1.0},
                {"name": "Leather Armor", "drop_rate": 0.8},
                {"name": "Medium Potion", "drop_rate": 1.0},
            ],
            "intro_text": "Branches creak and leaves whisper as the Ancient Treant awakens from its slumber.",
            "defeat_text": "The Treant's bark crumbles to dust. Sunlight pierces the canopy once more.",
        },
    },
    "Mountains": {
        "description": "Treacherous peaks where only the strong survive. Thin air and thinner patience.",
        "required_level": 18,
        "required_rank": "Intermediate",
        "required_bosses": ["Forest"],
        "recommended_level": "18-30",
        "recommended_rank": "Intermediate - Advanced",
        "danger_level": "Dangerous",
        "monsters": [
            {"name": "Goblin Raider", "health": 40, "attack": 10, "defense": 4, "exp": 40, "gold": 20, "level": 18},
            {"name": "Stone Golem", "health": 70, "attack": 12, "defense": 10, "exp": 60, "gold": 30, "level": 20},
            {"name": "Mountain Wolf", "health": 50, "attack": 11, "defense": 5, "exp": 45, "gold": 22, "level": 19},
            {"name": "Ice Bat", "health": 30, "attack": 9, "defense": 2, "exp": 35, "gold": 18, "level": 18},
            {"name": "Rock Serpent", "health": 60, "attack": 14, "defense": 6, "exp": 70, "gold": 35, "level": 22},
            {"name": "Frost Giant Scout", "health": 80, "attack": 15, "defense": 8, "exp": 80, "gold": 40, "level": 24},
            {"name": "Cliff Harpy", "health": 45, "attack": 13, "defense": 4, "exp": 50, "gold": 25, "level": 20},
            {"name": "Avalanche Spirit", "health": 55, "attack": 16, "defense": 5, "exp": 65, "gold": 32, "level": 23},
            {"name": "Ironback Yak", "health": 75, "attack": 12, "defense": 9, "exp": 68, "gold": 34, "level": 24},
            {"name": "Crystal Spider", "health": 50, "attack": 15, "defense": 5, "exp": 60, "gold": 30, "level": 22},
            {"name": "Frozen Knight", "health": 85, "attack": 17, "defense": 10, "exp": 90, "gold": 45, "level": 26},
            {"name": "Blizzard Wraith", "health": 60, "attack": 18, "defense": 5, "exp": 85, "gold": 42, "level": 25},
            {"name": "Peak Guardian", "health": 90, "attack": 20, "defense": 12, "exp": 100, "gold": 50, "level": 28},
            {"name": "Snow Panther", "health": 55, "attack": 16, "defense": 6, "exp": 70, "gold": 35, "level": 24},
            {"name": "Storm Eagle", "health": 65, "attack": 19, "defense": 7, "exp": 95, "gold": 48, "level": 27},
        ],
        "loot": {
            "Large Potion": {"type": "consumable", "effect": "heal", "value": 100},
            "Mountain Ore": {"type": "material", "effect": "none", "value": 40},
            "Ice Crystal": {"type": "material", "effect": "none", "value": 35},
            "Ancient Relic": {"type": "material", "effect": "none", "value": 60},
            "Iron Skin Potion": {"type": "consumable", "effect": "buff_defense", "value": 6, "duration": 5},
            "Chainmail": {"type": "armor", "effect": "none", "value": 150},
        },
        "boss": {
            "name": "Dragon Lord",
            "title": "Warden of the Peaks",
            "description": "An ancient wyrm whose scales are harder than mountain stone.",
            "level": 30,
            "health": 300,
            "max_health": 300,
            "attack": 35,
            "defense": 15,
            "exp": 300,
            "gold": 300,
            "ability": {
                "name": "Dragonfire",
                "damage_multiplier": 2.0,
                "cooldown_turns": 4,
                "description": "Unleashes a torrent of dragonfire, dealing 200% damage.",
            },
            "loot": [
                {"name": "Dragon Slayer Sword", "drop_rate": 1.0},
                {"name": "Dragon Scale", "drop_rate": 1.0},
                {"name": "Large Potion", "drop_rate": 1.0},
            ],
            "intro_text": "Wings blot out the sun. The Dragon Lord descends from the highest peak.",
            "defeat_text": "The Dragon Lord crashes into the mountainside. Its hoard is yours.",
        },
    },
    "Desert": {
        "description": "A scorching wasteland where mirages deceive and the sun is merciless.",
        "required_level": 30,
        "required_rank": "Advanced",
        "required_bosses": ["Mountains"],
        "recommended_level": "30-45",
        "recommended_rank": "Advanced - Expert",
        "danger_level": "Very Dangerous",
        "monsters": [
            {"name": "Sand Bandit", "health": 45, "attack": 13, "defense": 5, "exp": 50, "gold": 25, "level": 30},
            {"name": "Scorpion", "health": 35, "attack": 15, "defense": 4, "exp": 48, "gold": 24, "level": 30},
            {"name": "Fire Lizard", "health": 50, "attack": 16, "defense": 6, "exp": 55, "gold": 28, "level": 32},
            {"name": "Dust Wraith", "health": 40, "attack": 18, "defense": 3, "exp": 60, "gold": 30, "level": 33},
            {"name": "Cactus Beast", "health": 65, "attack": 14, "defense": 8, "exp": 62, "gold": 31, "level": 34},
            {"name": "Sun Priest", "health": 55, "attack": 17, "defense": 5, "exp": 70, "gold": 35, "level": 35},
            {"name": "Desert Wolf", "health": 48, "attack": 15, "defense": 5, "exp": 58, "gold": 29, "level": 33},
            {"name": "Ancient Scarab", "health": 60, "attack": 14, "defense": 7, "exp": 65, "gold": 32, "level": 35},
            {"name": "Heat Elemental", "health": 70, "attack": 18, "defense": 6, "exp": 75, "gold": 38, "level": 37},
            {"name": "Mirage Assassin", "health": 45, "attack": 20, "defense": 4, "exp": 80, "gold": 40, "level": 38},
            {"name": "Sand Golem", "health": 85, "attack": 16, "defense": 10, "exp": 90, "gold": 45, "level": 40},
            {"name": "Blazing Hawk", "health": 50, "attack": 19, "defense": 5, "exp": 85, "gold": 42, "level": 39},
            {"name": "Nomad Raider", "health": 60, "attack": 17, "defense": 6, "exp": 72, "gold": 36, "level": 37},
            {"name": "Desert Spirit", "health": 55, "attack": 21, "defense": 5, "exp": 88, "gold": 44, "level": 40},
            {"name": "Molten Serpent", "health": 75, "attack": 22, "defense": 7, "exp": 95, "gold": 48, "level": 42},
        ],
        "loot": {
            "Heat Core": {"type": "material", "effect": "none", "value": 50},
            "Desert Relic": {"type": "material", "effect": "none", "value": 55},
            "Golden Sand": {"type": "material", "effect": "none", "value": 30},
            "Rare Gem": {"type": "accessory", "effect": "none", "value": 70},
            "Swiftness Elixir": {"type": "consumable", "effect": "buff_speed", "value": 10, "duration": 4},
            "Scale Mail": {"type": "armor", "effect": "none", "value": 200},
        },
        "boss": {
            "name": "Sun-Scorched Colossus",
            "title": "The Walking Furnace",
            "description": "A towering construct of sand and molten glass, animated by relentless heat.",
            "level": 45,
            "health": 340,
            "max_health": 340,
            "attack": 38,
            "defense": 18,
            "exp": 360,
            "gold": 360,
            "ability": {
                "name": "Solar Flare",
                "damage_multiplier": 2.0,
                "cooldown_turns": 4,
                "description": "Spews superheated sand, dealing 200% damage and ignoring 50% defense.",
            },
            "loot": [
                {"name": "Heat Core", "drop_rate": 1.0},
                {"name": "Desert Relic", "drop_rate": 0.8},
                {"name": "Rare Gem", "drop_rate": 0.5},
            ],
            "intro_text": "The dunes shift and rise. The Colossus awakens, sand pouring from its joints.",
            "defeat_text": "The Colossus crumbles into glass and dust. The desert falls silent.",
        },
    },
    "Ice Plains": {
        "description": "Frozen wastelands where the cold bites deeper than blades.",
        "required_level": 45,
        "required_rank": "Expert",
        "required_bosses": ["Desert"],
        "recommended_level": "45-60",
        "recommended_rank": "Expert - Master",
        "danger_level": "Deadly",
        "monsters": [
            {"name": "Ice Wolf", "health": 50, "attack": 15, "defense": 5, "exp": 60, "gold": 30, "level": 45},
            {"name": "Frost Spider", "health": 40, "attack": 14, "defense": 4, "exp": 55, "gold": 28, "level": 45},
            {"name": "Glacier Golem", "health": 90, "attack": 18, "defense": 12, "exp": 85, "gold": 42, "level": 48},
            {"name": "Frozen Spirit", "health": 60, "attack": 20, "defense": 5, "exp": 80, "gold": 40, "level": 47},
            {"name": "Snow Beast", "health": 70, "attack": 17, "defense": 7, "exp": 75, "gold": 38, "level": 47},
            {"name": "Ice Knight", "health": 85, "attack": 19, "defense": 10, "exp": 90, "gold": 45, "level": 50},
            {"name": "Blizzard Imp", "health": 45, "attack": 18, "defense": 4, "exp": 65, "gold": 32, "level": 48},
            {"name": "Frozen Harpy", "health": 55, "attack": 17, "defense": 5, "exp": 70, "gold": 35, "level": 49},
            {"name": "Polar Bear", "health": 100, "attack": 16, "defense": 12, "exp": 95, "gold": 48, "level": 52},
            {"name": "Ice Wraith", "health": 65, "attack": 21, "defense": 5, "exp": 88, "gold": 44, "level": 51},
            {"name": "Shard Beast", "health": 75, "attack": 20, "defense": 7, "exp": 92, "gold": 46, "level": 53},
            {"name": "Snow Assassin", "health": 60, "attack": 22, "defense": 5, "exp": 95, "gold": 48, "level": 54},
            {"name": "Frost Giant", "health": 110, "attack": 22, "defense": 14, "exp": 110, "gold": 55, "level": 56},
            {"name": "Avalanche Beast", "health": 95, "attack": 21, "defense": 10, "exp": 100, "gold": 50, "level": 55},
            {"name": "Ice Dragonling", "health": 105, "attack": 23, "defense": 11, "exp": 115, "gold": 58, "level": 58},
        ],
        "loot": {
            "Ice Core": {"type": "material", "effect": "none", "value": 55},
            "Frozen Relic": {"type": "material", "effect": "none", "value": 60},
            "Crystal Shard": {"type": "material", "effect": "none", "value": 45},
            "Ancient Ice": {"type": "consumable", "effect": "buff_defense", "value": 8, "duration": 5},
            "Frozen Plate": {"type": "armor", "effect": "none", "value": 450},
            "Focus Crystal": {"type": "consumable", "effect": "buff_critical", "value": 15, "duration": 5},
        },
        "boss": {
            "name": "Glacier Crown Regent",
            "title": "Sovereign of the Frozen Wastes",
            "description": "A knight encased in eternal ice, wielding a blade that freezes the very air.",
            "level": 60,
            "health": 370,
            "max_health": 370,
            "attack": 40,
            "defense": 20,
            "exp": 390,
            "gold": 390,
            "ability": {
                "name": "Absolute Zero",
                "damage_multiplier": 1.8,
                "cooldown_turns": 3,
                "description": "Shatters the ice beneath you with a titanic blow, dealing 180% damage.",
            },
            "loot": [
                {"name": "Ice Core", "drop_rate": 1.0},
                {"name": "Frozen Relic", "drop_rate": 0.8},
                {"name": "Ancient Ice", "drop_rate": 0.5},
            ],
            "intro_text": "The temperature plummets. The Regent emerges from the blizzard, blade drawn.",
            "defeat_text": "The Regent's armor shatters. The eternal winter begins to thaw.",
        },
    },
    "Swamp": {
        "description": "A toxic marsh where every step could be your last. The air itself is poison.",
        "required_level": 60,
        "required_rank": "Master",
        "required_bosses": ["Ice Plains"],
        "recommended_level": "60-80",
        "recommended_rank": "Master - Grandmaster",
        "danger_level": "Nightmare",
        "monsters": [
            {"name": "Swamp Slime", "health": 45, "attack": 12, "defense": 5, "exp": 50, "gold": 25, "level": 60},
            {"name": "Poison Frog", "health": 30, "attack": 16, "defense": 2, "exp": 48, "gold": 24, "level": 60},
            {"name": "Bog Beast", "health": 70, "attack": 14, "defense": 8, "exp": 65, "gold": 32, "level": 62},
            {"name": "Swamp Witch", "health": 60, "attack": 18, "defense": 5, "exp": 70, "gold": 35, "level": 63},
            {"name": "Toxic Serpent", "health": 50, "attack": 20, "defense": 4, "exp": 75, "gold": 38, "level": 64},
            {"name": "Rot Zombie", "health": 65, "attack": 15, "defense": 7, "exp": 68, "gold": 34, "level": 63},
            {"name": "Mud Golem", "health": 80, "attack": 13, "defense": 10, "exp": 72, "gold": 36, "level": 65},
            {"name": "Plague Rat", "health": 40, "attack": 17, "defense": 3, "exp": 55, "gold": 28, "level": 62},
            {"name": "Swamp Spirit", "health": 55, "attack": 19, "defense": 5, "exp": 78, "gold": 39, "level": 66},
            {"name": "Venom Spider", "health": 48, "attack": 21, "defense": 4, "exp": 80, "gold": 40, "level": 67},
            {"name": "Rotting Knight", "health": 75, "attack": 18, "defense": 9, "exp": 85, "gold": 42, "level": 68},
            {"name": "Toxic Elemental", "health": 90, "attack": 22, "defense": 6, "exp": 95, "gold": 48, "level": 70},
            {"name": "Swamp Hydra", "health": 110, "attack": 23, "defense": 11, "exp": 110, "gold": 55, "level": 73},
            {"name": "Plague Doctor", "health": 70, "attack": 20, "defense": 7, "exp": 88, "gold": 44, "level": 71},
            {"name": "Death Leech", "health": 60, "attack": 24, "defense": 4, "exp": 100, "gold": 50, "level": 74},
        ],
        "loot": {
            "Toxic Core": {"type": "material", "effect": "none", "value": 60},
            "Swamp Relic": {"type": "material", "effect": "none", "value": 65},
            "Venom Sac": {"type": "consumable", "effect": "poison_weapon", "value": 10, "duration": 4},
            "Dark Herb": {"type": "consumable", "effect": "heal", "value": 45},
            "Antidote Vial": {"type": "consumable", "effect": "cure_poison", "value": 25},
            "Shadow Weave": {"type": "armor", "effect": "none", "value": 500},
        },
        "boss": {
            "name": "Hydra of the Black Mire",
            "title": "The Many-Headed Plague",
            "description": "A serpent with heads that regenerate faster than they can be severed.",
            "level": 80,
            "health": 410,
            "max_health": 410,
            "attack": 42,
            "defense": 22,
            "exp": 430,
            "gold": 430,
            "ability": {
                "name": "Venom Storm",
                "damage_multiplier": 1.6,
                "cooldown_turns": 2,
                "description": "All heads strike simultaneously, dealing 160% damage and healing for 10%.",
            },
            "loot": [
                {"name": "Toxic Core", "drop_rate": 1.0},
                {"name": "Swamp Relic", "drop_rate": 0.8},
                {"name": "Venom Sac", "drop_rate": 0.5},
            ],
            "intro_text": "Bubbles rise from the black water. The Hydra's heads emerge, hissing in unison.",
            "defeat_text": "The Hydra's heads fall limp. The swamp's corruption begins to recede.",
        },
    },
    "Shadow Realm": {
        "description": "The final frontier. Reality bends here. Only the Dominator may enter.",
        "required_level": 80,
        "required_rank": "Grandmaster",
        "required_bosses": ["Swamp"],
        "recommended_level": "80-100",
        "recommended_rank": "Grandmaster - Dominator",
        "danger_level": "Apocalyptic",
        "monsters": [
            {"name": "Shadow Imp", "health": 50, "attack": 18, "defense": 5, "exp": 70, "gold": 35, "level": 80},
            {"name": "Dark Wraith", "health": 65, "attack": 22, "defense": 7, "exp": 85, "gold": 42, "level": 82},
            {"name": "Night Stalker", "health": 55, "attack": 24, "defense": 5, "exp": 90, "gold": 45, "level": 83},
            {"name": "Void Beast", "health": 90, "attack": 20, "defense": 10, "exp": 95, "gold": 48, "level": 85},
            {"name": "Abyss Knight", "health": 100, "attack": 23, "defense": 12, "exp": 110, "gold": 55, "level": 87},
            {"name": "Phantom Assassin", "health": 70, "attack": 26, "defense": 6, "exp": 105, "gold": 52, "level": 88},
            {"name": "Dark Sorcerer", "health": 80, "attack": 25, "defense": 8, "exp": 100, "gold": 50, "level": 87},
            {"name": "Shadow Dragonling", "health": 110, "attack": 24, "defense": 11, "exp": 115, "gold": 58, "level": 90},
            {"name": "Void Spider", "health": 60, "attack": 23, "defense": 6, "exp": 95, "gold": 48, "level": 88},
            {"name": "Nightmare Beast", "health": 120, "attack": 27, "defense": 13, "exp": 130, "gold": 65, "level": 92},
            {"name": "Dread Knight", "health": 130, "attack": 26, "defense": 15, "exp": 140, "gold": 70, "level": 94},
            {"name": "Soul Reaper", "health": 90, "attack": 28, "defense": 8, "exp": 150, "gold": 75, "level": 95},
            {"name": "Void Titan", "health": 150, "attack": 30, "defense": 16, "exp": 170, "gold": 85, "level": 97},
            {"name": "Abyssal Horror", "health": 140, "attack": 29, "defense": 14, "exp": 165, "gold": 82, "level": 96},
            {"name": "Eternal Shade", "health": 135, "attack": 31, "defense": 13, "exp": 180, "gold": 90, "level": 98},
        ],
        "loot": {
            "Void Core": {"type": "material", "effect": "none", "value": 80},
            "Shadow Relic": {"type": "material", "effect": "none", "value": 90},
            "Dark Crystal": {"type": "material", "effect": "none", "value": 75},
            "Soul Fragment": {"type": "consumable", "effect": "full_heal", "value": 0},
            "Berserker Brew": {"type": "consumable", "effect": "buff_attack", "value": 15, "duration": 3},
            "Void Shell": {"type": "armor", "effect": "none", "value": 3000},
        },
        "boss": {
            "name": "The Claim-Eater",
            "title": "Devourer of Realities",
            "description": "A being of pure void that consumes not just life, but the very concept of existence.",
            "level": 100,
            "health": 460,
            "max_health": 460,
            "attack": 45,
            "defense": 25,
            "exp": 520,
            "gold": 520,
            "ability": {
                "name": "Reality Tear",
                "damage_multiplier": 2.5,
                "cooldown_turns": 5,
                "description": "Unleashes the void itself, dealing 250% damage and reducing your defense by 5 for 3 turns.",
            },
            "loot": [
                {"name": "Void Core", "drop_rate": 1.0},
                {"name": "Shadow Relic", "drop_rate": 0.8},
                {"name": "Soul Fragment", "drop_rate": 0.5},
                {"name": "Crown of the Claimant", "drop_rate": 0.3},
            ],
            "intro_text": "Reality tears. The Claim-Eater steps through the rift. You forget your own name.",
            "defeat_text": "The Claim-Eater dissolves into nothingness. The Shadow Realm collapses. You have won.",
        },
    },
}

BIOME_ORDER = [
    "Grasslands",
    "Forest",
    "Mountains",
    "Desert",
    "Ice Plains",
    "Swamp",
    "Shadow Realm",
]

def get_available_biomes(player: dict) -> List[str]:
    """Return list of biomes the player can currently access."""
    available = []
    player_level = player.get("level", 1)
    player_rank = get_rank(player_level)
    player_rank_idx = get_rank_index(player_rank)
    bosses_defeated = player.get("bosses_defeated", [])

    for biome_name in BIOME_ORDER:
        biome = BIOMES[biome_name]

        meets_level = player_level >= biome["required_level"]
        meets_rank = player_rank_idx >= get_rank_index(biome["required_rank"])
        meets_bosses = all(boss in bosses_defeated for boss in biome["required_bosses"])

        if meets_level and meets_rank and meets_bosses:
            available.append(biome_name)

    return available

def get_biome_recommendation(player: dict, biome_name: str) -> dict:
    """Get travel recommendation for a biome."""
    biome = BIOMES.get(biome_name)
    if not biome:
        return {"can_enter": False, "reason": "Biome does not exist."}

    player_level = player.get("level", 1)
    player_rank = get_rank(player_level)
    player_rank_idx = get_rank_index(player_rank)
    bosses_defeated = player.get("bosses_defeated", [])

    meets_level = player_level >= biome["required_level"]
    meets_rank = player_rank_idx >= get_rank_index(biome["required_rank"])
    meets_bosses = all(boss in bosses_defeated for boss in biome["required_bosses"])

    if not meets_level:
        return {
            "can_enter": False,
            "reason": f"Requires Level {biome['required_level']}. You are Level {player_level}.",
            "recommendation": f"Train in easier areas until you reach Level {biome['required_level']}.",
        }

    if not meets_rank:
        return {
            "can_enter": False,
            "reason": f"Requires Rank: {biome['required_rank']}. You are {player_rank}.",
            "recommendation": "Complete more missions and defeat more monsters to increase your rank.",
        }

    if not meets_bosses:
        missing = [b for b in biome["required_bosses"] if b not in bosses_defeated]
        return {
            "can_enter": False,
            "reason": f"Defeat the guardian(s) of: {', '.join(missing)}",
            "recommendation": f"Challenge the boss of {missing[0]} to unlock this area.",
        }

    danger = biome["danger_level"]
    rec_level = biome["recommended_level"]
    rec_rank = biome["recommended_rank"]

    if player_level < biome["required_level"] + 3:
        assessment = "CAUTION: You are at the minimum level. Bring potions and be prepared!"
    elif player_level > biome["required_level"] + 10:
        assessment = "EASY: You are significantly overleveled. This will be a walk in the park."
    else:
        assessment = "MODERATE: You are appropriately leveled. Stay vigilant!"

    return {
        "can_enter": True,
        "danger_level": danger,
        "recommended_level": rec_level,
        "recommended_rank": rec_rank,
        "assessment": assessment,
        "reason": "You may enter this biome.",
    }
def get_random_monster(biome_name: str) -> Optional[dict]:
    """Get a random monster from a biome with fresh health."""
    biome = BIOMES.get(biome_name)
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

def get_random_loot(biome_name: str) -> Optional[dict]:
    """Get a random loot item data from a biome."""
    biome = BIOMES.get(biome_name)
    if not biome:
        return None

    loot_table = biome.get("loot", {})
    if not loot_table:
        return None

    item_name = random.choice(list(loot_table.keys()))
    return {"name": item_name, **loot_table[item_name]}

def get_boss(biome_name: str) -> Optional[dict]:
    """Get a copy of the boss for a biome, with fresh health."""
    biome = BIOMES.get(biome_name)
    if not biome:
        return None

    boss = biome.get("boss")
    if not boss:
        return None

    b = copy.deepcopy(boss)
    b["health"] = b["max_health"]
    b["dot_effects"] = []
    b["active_buffs"] = {}
    b["stunned"] = 0

    return b