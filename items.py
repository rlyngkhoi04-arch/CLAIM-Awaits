import random
from typing import Optional, List, Tuple

# =========================================================
# ITEM RANKS
# =========================================================

ITEM_RANKS = {
    "Common": {
        "multiplier": 1.0,
        "value_multiplier": 1.0,
        "color": "White",
    },
    "Enhanced": {
        "multiplier": 1.25,
        "value_multiplier": 1.4,
        "color": "Green",
    },
    "Rare": {
        "multiplier": 1.5,
        "value_multiplier": 2.0,
        "color": "Blue",
    },
    "Epic": {
        "multiplier": 2.0,
        "value_multiplier": 3.5,
        "color": "Purple",
    },
    "Legend": {
        "multiplier": 3.0,
        "value_multiplier": 6.0,
        "color": "Gold",
    },
    "Dominant": {
        "multiplier": 5.0,
        "value_multiplier": 12.0,
        "color": "Red",
    },
}

# =========================================================
# CONSUMABLES
# =========================================================

CONSUMABLES = {
    "Small Potion": {
        "type": "consumable",
        "heal": 30,
        "value": 15,
        "description": "A basic healing potion. Tastes like cherries... mostly.",
    },
    "Medium Potion": {
        "type": "consumable",
        "heal": 60,
        "value": 35,
        "description": "A stronger healing brew. The label says 'Drink responsibly'.",
    },
    "Large Potion": {
        "type": "consumable",
        "heal": 120,
        "value": 70,
        "description": "Restores a significant amount of health. Glows faintly blue.",
    },
    "Elixir of Vitality": {
        "type": "consumable",
        "heal": 250,
        "value": 150,
        "description": "A legendary healing draught. One sip and you feel reborn.",
    },
    "Herb": {
        "type": "consumable",
        "heal": 15,
        "value": 8,
        "description": "A common medicinal herb. Crushed and applied to wounds.",
    },
    "Dark Herb": {
        "type": "consumable",
        "heal": 45,
        "value": 30,
        "description": "A rare herb from shadowed forests. Smells of midnight rain.",
    },
    "Moss Clump": {
        "type": "consumable",
        "heal": 10,
        "value": 5,
        "description": "Damp moss with minor curative properties. Better than nothing.",
    },
    "Honey Jar": {
        "type": "consumable",
        "heal": 35,
        "value": 20,
        "description": "Sweet golden honey. Soothes wounds and spirits alike.",
    },
    "Bandage Roll": {
        "type": "consumable",
        "heal": 20,
        "value": 12,
        "description": "Clean linen bandages. Stops bleeding and prevents infection.",
    },
    "Antidote Vial": {
        "type": "consumable",
        "heal": 25,
        "cure_poison": True,
        "value": 25,
        "description": "A clear liquid that neutralizes most common toxins.",
    },
    "Strength Tonic": {
        "type": "consumable",
        "buff_attack": 8,
        "duration": 5,
        "value": 40,
        "description": "A fiery red drink that makes your muscles feel like iron.",
    },
    "Iron Skin Potion": {
        "type": "consumable",
        "buff_defense": 6,
        "duration": 5,
        "value": 40,
        "description": "Your skin hardens like stone. Useful in a pinch.",
    },
    "Swiftness Elixir": {
        "type": "consumable",
        "buff_speed": 10,
        "duration": 4,
        "value": 35,
        "description": "Everything seems to slow down around you.",
    },
    "Berserker Brew": {
        "type": "consumable",
        "buff_attack": 15,
        "buff_defense": -5,
        "duration": 3,
        "value": 50,
        "description": "Trade defense for raw power. The rage is intoxicating.",
    },
    "Focus Crystal": {
        "type": "consumable",
        "buff_critical": 15,
        "duration": 5,
        "value": 45,
        "description": "A crystalline shard that sharpens your aim and reflexes.",
    },
    "Regeneration Salve": {
        "type": "consumable",
        "regen_per_turn": 15,
        "duration": 5,
        "value": 55,
        "description": "Gradually restores health over several turns.",
    },
    "Mana Crystal": {
        "type": "consumable",
        "buff_magic": 25,
        "duration": 1,
        "value": 48,
        "description": "Pulsing with arcane energy. Mages swear by these.",
    },
    "Phoenix Feather": {
        "type": "consumable",
        "revive": True,
        "heal": 50,
        "value": 500,
        "description": "A feather from a mythical bird. Burns away death itself.",
    },
    "Ambrosia": {
        "type": "consumable",
        "full_heal": True,
        "cure_all": True,
        "value": 300,
        "description": "Food of the gods. Restores body and soul completely.",
    },
    "Dragon Blood": {
        "type": "consumable",
        "buff_attack": 10,
        "buff_defense": 10,
        "buff_max_health": 30,
        "duration": 8,
        "value": 200,
        "description": "Thick, warm, and terrifyingly powerful. Handle with care.",
    },
}

# =========================================================
# WEAPONS
# =========================================================

WARRIOR_WEAPONS = {
    "Rusty Blade": {"class": "Warrior", "type": "weapon", "attack": 3, "value": 15, "description": "Better than fists, barely. Found in a ditch."},
    "Iron Sword": {"class": "Warrior", "type": "weapon", "attack": 5, "value": 50, "description": "A standard-issue iron sword. Reliable and sturdy."},
    "Steel Blade": {"class": "Warrior", "type": "weapon", "attack": 10, "value": 120, "description": "Forged from quality steel. A soldier's trusted companion."},
    "Knight Greatsword": {"class": "Warrior", "type": "weapon", "attack": 18, "critical_chance": 5, "value": 250, "description": "A massive blade wielded by knights of old. Heavy but devastating."},
    "Bastard Sword": {"class": "Warrior", "type": "weapon", "attack": 14, "defense": 2, "value": 180, "description": "Versatile and balanced. Can be wielded with one or two hands."},
    "War Hammer": {"class": "Warrior", "type": "weapon", "attack": 16, "armor_pierce": 5, "value": 220, "description": "Crushes armor and bone alike. Favored against heavily armored foes."},
    "Flamebrand": {"class": "Warrior", "type": "weapon", "attack": 22, "fire_damage": 8, "value": 400, "description": "A blade that burns with eternal flame. Leaves scorch marks on everything."},
    "Dragon Slayer Sword": {"class": "Warrior", "type": "weapon", "attack": 25, "critical_chance": 10, "dragon_bonus": 15, "value": 800, "description": "Forged to pierce dragon scales. Glows when beasts are near."},
    "Excalibur's Echo": {"class": "Warrior", "type": "weapon", "attack": 35, "critical_chance": 12, "defense": 5, "holy_damage": 10, "value": 1500, "description": "A replica of the legendary blade. Even a shadow of its power is immense."},
    "World Breaker": {"class": "Warrior", "type": "weapon", "attack": 50, "critical_chance": 15, "armor_pierce": 10, "value": 3000, "description": "Said to have shattered a mountain in a single swing. You believe it."},
}

MAGE_WEAPONS = {
    "Twig Wand": {"class": "Mage", "type": "weapon", "attack": 2, "value": 10, "description": "Literally a twig. At least it has a crystal taped to it."},
    "Wooden Staff": {"class": "Mage", "type": "weapon", "attack": 6, "value": 45, "description": "A simple wooden staff topped with a quartz crystal."},
    "Apprentice Rod": {"class": "Mage", "type": "weapon", "attack": 9, "mana_regen": 2, "value": 80, "description": "Given to magic academy graduates. Standard issue."},
    "Epic Staff": {"class": "Mage", "type": "weapon", "attack": 18, "critical_chance": 8, "value": 450, "description": "A staff of ancient design. Channels magic with frightening efficiency."},
    "Arcane Wand": {"class": "Mage", "type": "weapon", "attack": 22, "critical_chance": 10, "value": 600, "description": "A slender wand that hums with contained magical energy."},
    "Frost Staff": {"class": "Mage", "type": "weapon", "attack": 20, "ice_damage": 10, "value": 550, "description": "Touching it makes your breath visible. Permafrost core inside."},
    "Void Scepter": {"class": "Mage", "type": "weapon", "attack": 28, "critical_chance": 15, "void_damage": 12, "value": 900, "description": "Stares back at you when you look into its gem. Unsettling."},
    "Staff of the Archmage": {"class": "Mage", "type": "weapon", "attack": 35, "critical_chance": 18, "mana_regen": 5, "value": 1600, "description": "Once wielded by the Archmage Theron. Power leaks from every crack."},
    "Starcaller": {"class": "Mage", "type": "weapon", "attack": 45, "critical_chance": 20, "cosmic_damage": 15, "value": 3200, "description": "Forged from a fallen star. Its magic feels... alien."},
}

ROGUE_WEAPONS = {
    "Rusty Dagger": {"class": "Rogue", "type": "weapon", "attack": 4, "value": 18, "description": "Tetanus included at no extra charge."},
    "Twin Daggers": {"class": "Rogue", "type": "weapon", "attack": 8, "critical_chance": 5, "value": 60, "description": "A matched pair of lightweight daggers. Swift and deadly."},
    "Shadow Knife": {"class": "Rogue", "type": "weapon", "attack": 14, "critical_chance": 10, "value": 180, "description": "Absorbs light around its edge. Hard to see, harder to dodge."},
    "Silent Fang": {"class": "Rogue", "type": "weapon", "attack": 20, "critical_chance": 15, "value": 450, "description": "Makes no sound when drawn. Victims never hear it coming."},
    "Venom Shiv": {"class": "Rogue", "type": "weapon", "attack": 16, "critical_chance": 12, "poison_damage": 6, "value": 320, "description": "Coated in a fast-acting toxin. One scratch is enough."},
    "Phantom Blade": {"class": "Rogue", "type": "weapon", "attack": 24, "critical_chance": 18, "dodge_bonus": 5, "value": 650, "description": "Partially phased out of reality. Slips through armor like mist."},
    "Assassin's Promise": {"class": "Rogue", "type": "weapon", "attack": 32, "critical_chance": 25, "critical_damage": 1.5, "value": 1400, "description": "A blade that has ended kings. The edge whispers names of its victims."},
    "Night's Edge": {"class": "Rogue", "type": "weapon", "attack": 42, "critical_chance": 30, "stealth_bonus": 10, "value": 2800, "description": "Forged in absolute darkness. Exists only to end lives silently."},
}

PALADIN_WEAPONS = {
    "Wooden Mallet": {"class": "Paladin", "type": "weapon", "attack": 4, "value": 20, "description": "A humble wooden mallet. Better than nothing."},
    "Holy Hammer": {"class": "Paladin", "type": "weapon", "attack": 9, "defense": 2, "value": 90, "description": "Blessed by the Order of the Dawn. Glows faintly at night."},
    "Blessed Sword": {"class": "Paladin", "type": "weapon", "attack": 15, "defense": 4, "value": 220, "description": "A blade sanctified in holy water. Purity radiates from it."},
    "Guardian Mace": {"class": "Paladin", "type": "weapon", "attack": 20, "defense": 6, "value": 500, "description": "Heavy and protective. Wielded by temple guardians for centuries."},
    "Crusader's Flail": {"class": "Paladin", "type": "weapon", "attack": 18, "defense": 3, "holy_damage": 5, "value": 380, "description": "A spiked ball on a chain. Devastating against undead."},
    "Aegis Blade": {"class": "Paladin", "type": "weapon", "attack": 22, "defense": 8, "block_chance": 10, "value": 700, "description": "Sword and shield in one. The blade is as broad as a tower shield."},
    "Dawnbringer": {"class": "Paladin", "type": "weapon", "attack": 28, "defense": 10, "holy_damage": 12, "heal_on_hit": 5, "value": 1300, "description": "Each strike brings light. Each kill, redemption."},
    "Divine Judgment": {"class": "Paladin", "type": "weapon", "attack": 38, "defense": 12, "holy_damage": 18, "heal_on_hit": 10, "value": 2600, "description": "The gods themselves forged this weapon. It judges all who face it."},
}

BERSERKER_WEAPONS = {
    "Broken Axe": {"class": "Berserker", "type": "weapon", "attack": 6, "value": 25, "description": "The head is loose but it still cuts. Sort of."},
    "Battle Axe": {"class": "Berserker", "type": "weapon", "attack": 12, "value": 100, "description": "A solid iron battle axe. Standard issue for raiding parties."},
    "Rage Cleaver": {"class": "Berserker", "type": "weapon", "attack": 20, "critical_chance": 8, "value": 300, "description": "The more you swing, the sharper it gets. Or so the smith claimed."},
    "Blood Splitter": {"class": "Berserker", "type": "weapon", "attack": 28, "critical_chance": 15, "value": 700, "description": "Said to thirst for blood. The edge never dulls after a kill."},
    "Fury's Edge": {"class": "Berserker", "type": "weapon", "attack": 24, "critical_chance": 12, "rage_bonus": 5, "value": 500, "description": "Gains power as its wielder takes damage. Dangerous symbiosis."},
    "Skull Crusher": {"class": "Berserker", "type": "weapon", "attack": 32, "critical_chance": 10, "stun_chance": 15, "value": 850, "description": "A massive two-handed hammer. One hit can shatter a helm."},
    "Berserker's Heart": {"class": "Berserker", "type": "weapon", "attack": 40, "critical_chance": 20, "rage_bonus": 10, "life_steal": 5, "value": 1700, "description": "Pulses with the heartbeat of its first owner. Still beating."},
    "World Ender": {"class": "Berserker", "type": "weapon", "attack": 55, "critical_chance": 25, "armor_pierce": 15, "value": 3500, "description": "A weapon of apocalypse. Its name is not hyperbole."},
}

RANGER_WEAPONS = {
    "Crude Bow": {"class": "Ranger", "type": "weapon", "attack": 5, "value": 22, "description": "A roughly carved bow. The string is... questionable."},
    "Hunter Bow": {"class": "Ranger", "type": "weapon", "attack": 8, "critical_chance": 4, "value": 70, "description": "A reliable hunting bow. Accurate at medium range."},
    "Longbow": {"class": "Ranger", "type": "weapon", "attack": 15, "critical_chance": 8, "value": 200, "description": "A tall yew longbow. Requires strength to draw fully."},
    "Windpiercer": {"class": "Ranger", "type": "weapon", "attack": 24, "critical_chance": 12, "value": 550, "description": "Arrows fired from this bow cut through wind like it's not there."},
    "Venom Bow": {"class": "Ranger", "type": "weapon", "attack": 20, "critical_chance": 10, "poison_damage": 5, "value": 420, "description": "Coated in serpent venom. Wounds fester and weaken the target."},
    "Eagle Eye": {"class": "Ranger", "type": "weapon", "attack": 28, "critical_chance": 18, "accuracy_bonus": 10, "value": 750, "description": "Grants the vision of an eagle. No target is too far or too small."},
    "Stormcaller Bow": {"class": "Ranger", "type": "weapon", "attack": 35, "critical_chance": 15, "lightning_damage": 10, "value": 1450, "description": "Arrows crackle with electricity. Thunder follows each shot."},
    "Apex Predator": {"class": "Ranger", "type": "weapon", "attack": 45, "critical_chance": 22, "critical_damage": 1.5, "value": 2900, "description": "The ultimate hunting weapon. Prey cannot hide, cannot run, cannot survive."},
}

# =========================================================
# ARMOR
# =========================================================

ARMOR = {
    "Tattered Rags": {"type": "armor", "defense": 1, "value": 5, "description": "Barely qualifies as clothing. Better than naked, barely."},
    "Torn Cloth": {"type": "armor", "defense": 1, "value": 5, "description": "Ripped and stained, but still wearable."},
    "Leather Armor": {"type": "armor", "defense": 4, "value": 40, "description": "Hardened leather plates. Light and flexible protection."},
    "Studded Leather": {"type": "armor", "defense": 6, "value": 80, "description": "Leather reinforced with iron studs. A step up from basic."},
    "Chainmail": {"type": "armor", "defense": 8, "value": 150, "description": "Interlocking metal rings. Good against slashing attacks."},
    "Knight Armor": {"type": "armor", "defense": 10, "value": 180, "description": "Full plate armor of a knight. Heavy but protective."},
    "Scale Mail": {"type": "armor", "defense": 9, "fire_resist": 5, "value": 200, "description": "Overlapping metal scales. Inspired by dragon hide."},
    "Frozen Plate": {"type": "armor", "defense": 16, "health": 25, "ice_resist": 10, "value": 450, "description": "Armor forged from enchanted ice. Never melts, never cracks."},
    "Shadow Weave": {"type": "armor", "defense": 12, "dodge_bonus": 8, "value": 500, "description": "Armor woven from shadow itself. Harder to hit than to see."},
    "Dragon Scale Armor": {"type": "armor", "defense": 20, "health": 40, "fire_resist": 15, "value": 900, "description": "Crafted from the scales of a fallen dragon. Nearly impenetrable."},
    "Aegis of the Fallen": {"type": "armor", "defense": 25, "health": 60, "all_resist": 10, "value": 1600, "description": "Worn by a hero who saved the world once. It remembers."},
    "Void Shell": {"type": "armor", "defense": 30, "health": 50, "void_resist": 20, "value": 3000, "description": "Armor from beyond reality. Damage seems to disappear into it."},
}

# =========================================================
# ACCESSORIES
# =========================================================

ACCESSORIES = {
    "Copper Ring": {"type": "accessory", "attack": 1, "value": 15, "description": "A simple copper band. Slightly tarnished."},
    "Silver Locket": {"type": "accessory", "health": 10, "value": 30, "description": "Contains a faded portrait. Whose, no one knows."},
    "Rare Gem": {"type": "accessory", "attack": 5, "value": 220, "description": "A gemstone of exceptional clarity. Pulsing with inner light."},
    "Frozen Relic": {"type": "accessory", "defense": 8, "health": 25, "value": 350, "description": "An artifact from the frozen north. Cold to the touch."},
    "Shadow Relic": {"type": "accessory", "attack": 8, "critical_chance": 8, "value": 700, "description": "Absorbs light around it. Grants power at a price."},
    "Desert Relic": {"type": "accessory", "attack": 6, "defense": 4, "value": 300, "description": "An ancient token from a lost civilization of the sands."},
    "Swamp Relic": {"type": "accessory", "health": 40, "critical_chance": 6, "value": 400, "description": "A charm made of bog iron. Smells faintly of decay."},
    "Legendary Amulet": {"type": "accessory", "health": 50, "critical_chance": 5, "value": 600, "description": "An amulet of legendary power. Warm against the skin."},
    "Ring of Vitality": {"type": "accessory", "health": 30, "regen": 3, "value": 280, "description": "Slowly mends wounds while worn. A traveler's best friend."},
    "Ring of Power": {"type": "accessory", "attack": 10, "critical_chance": 5, "value": 350, "description": "Amplifies the wearer's strength. Handle with caution."},
    "Ring of Protection": {"type": "accessory", "defense": 8, "block_chance": 5, "value": 320, "description": "Creates a faint barrier around the wearer. Subtle but effective."},
    "Cloak of Shadows": {"type": "accessory", "dodge_bonus": 10, "stealth_bonus": 15, "value": 600, "description": "Makes the wearer harder to see. Fades into darkness."},
    "Crown of the Claimant": {"type": "accessory", "attack": 15, "defense": 10, "health": 30, "critical_chance": 10, "value": 2500, "description": "Worn by those who would rule. Grants authority and power."},
}

# =========================================================
# MATERIALS
# =========================================================

MATERIALS = {
    "Old Coin": {"type": "material", "value": 12, "description": "An ancient coin with unreadable markings. Collectors might want it."},
    "Spider Silk": {"type": "material", "value": 25, "description": "Stronger than steel thread. Prized by weavers and alchemists."},
    "Mountain Ore": {"type": "material", "value": 45, "description": "Raw ore from deep within the mountains. Unrefined but valuable."},
    "Ice Crystal": {"type": "material", "value": 60, "description": "A crystal that never melts. Used in frost enchantments."},
    "Void Core": {"type": "material", "value": 150, "description": "A fragment of pure void. Staring into it is... unwise."},
    "Soul Fragment": {"type": "material", "value": 180, "description": "A shard of captured soul energy. Handle with extreme care."},
    "Heat Core": {"type": "material", "value": 80, "description": "A burning ember that never cools. Warm to the touch, painfully so."},
    "Golden Sand": {"type": "material", "value": 35, "description": "Sand that glitters like gold. Some say it actually is gold, cursed."},
    "Ancient Ice": {"type": "material", "value": 70, "description": "Ice from the first winter. Older than recorded history."},
    "Venom Sac": {"type": "material", "value": 55, "description": "A preserved venom gland. Useful for alchemy and assassination."},
    "Toxic Core": {"type": "material", "value": 90, "description": "A condensed ball of pure toxin. Do not drop. Do not breathe near it."},
    "Enchanted Leaf": {"type": "material", "value": 40, "description": "A leaf that glows with faint magic. Never wilts, never browns."},
    "Forest Gem": {"type": "material", "value": 30, "description": "A gemstone grown from tree sap. Unique to the ancient forests."},
    "Dragon Scale": {"type": "material", "value": 200, "description": "A single scale from a dragon's hide. Worth a small fortune."},
    "Demon Horn": {"type": "material", "value": 250, "description": "The twisted horn of a demon. Still warm. Still... listening?"},
    "Star Metal": {"type": "material", "value": 400, "description": "Metal that fell from the sky. Forged only in the hottest fires."},
    "Phoenix Ash": {"type": "material", "value": 350, "description": "Ash left behind by a phoenix rebirth. Contains life itself."},
    "Ectoplasm": {"type": "material", "value": 45, "description": "Residue from a ghostly encounter. Slimy and faintly glowing."},
    "Werewolf Fang": {"type": "material", "value": 120, "description": "A fang from a slain werewolf. Still sharp. Still dangerous."},
    "Basilisk Eye": {"type": "material", "value": 280, "description": "The eye of a basilisk. Don't look directly at it."},
}

# =========================================================
# MISCELLANEOUS / SPECIAL
# =========================================================

MISCELLANEOUS = {
    "Map Fragment": {"type": "misc", "value": 50, "description": "A torn piece of an old map. Shows something important... maybe."},
    "Ancient Key": {"type": "misc", "value": 100, "description": "An ornate key of unknown origin. It must open something."},
    "Mysterious Scroll": {"type": "misc", "value": 80, "description": "A scroll covered in unreadable script. Magic hums from it."},
    "Compass of Truth": {"type": "misc", "value": 200, "description": "Points not north, but toward what you seek most."},
    "Music Box": {"type": "misc", "value": 60, "description": "Plays a haunting melody. No one knows the tune's origin."},
    "Family Portrait": {"type": "misc", "value": 5, "description": "A faded painting of a family. Someone must miss them."},
    "Lucky Coin": {"type": "misc", "luck_bonus": 5, "value": 150, "description": "A coin with two heads. Cheating fate has never been easier."},
    "Crystal Ball": {"type": "misc", "value": 300, "description": "Shows glimpses of possible futures. Mostly confusing ones."},
    "Cursed Doll": {"type": "misc", "value": 10, "description": "A creepy doll that moves when you're not looking. Probably."},
    "Hero's Journal": {"type": "misc", "value": 75, "description": "The final entries of a fallen hero. Their story lives on."},
    "Bottle of Stardust": {"type": "misc", "value": 180, "description": "Actual stardust in a bottle. Shimmers with distant galaxies."},
    "Whispering Skull": {"type": "misc", "value": 120, "description": "A skull that whispers secrets. Mostly useless ones."},
}

# =========================================================
# BOUNTY ITEMS
# =========================================================

BOUNTY_ITEMS = {
    "Goblin Ear": {"type": "bounty", "value": 15, "description": "Proof of a slain goblin. Bounty collectors pay per ear.", "source": "Goblin"},
    "Wolf Pelt": {"type": "bounty", "value": 25, "description": "A thick wolf pelt. Fur traders pay well for quality pelts.", "source": "Wolf"},
    "Spider Venom Sac": {"type": "bounty", "value": 30, "description": "A venom gland from a giant spider. Alchemists need these.", "source": "Forest Spider"},
    "Orc Trophy": {"type": "bounty", "value": 40, "description": "A crude necklace taken from an orc warrior. Proof of valor.", "source": "Orc Warrior"},
    "Golem Core": {"type": "bounty", "value": 60, "description": "The animating core of a stone golem. Still faintly warm.", "source": "Stone Golem"},
    "Dragon Tooth": {"type": "bounty", "value": 150, "description": "A tooth from a dragon. One of the ultimate trophies.", "source": "Dragon Lord"},
    "Bandit Mask": {"type": "bounty", "value": 20, "description": "A mask taken from a defeated bandit. Proof for the authorities.", "source": "Bandit"},
    "Slime Gel": {"type": "bounty", "value": 8, "description": "A blob of congealed slime. Surprisingly valuable to alchemists.", "source": "Slime"},
    "Wraith Essence": {"type": "bounty", "value": 80, "description": "A captured fragment of wraith essence. Glows with ghostly light.", "source": "Wraith"},
    "Hydra Head": {"type": "bounty", "value": 200, "description": "A severed hydra head. Don't worry, the rest is dead too... right?", "source": "Hydra"},
    "Demon Horn": {"type": "bounty", "value": 250, "description": "Proof of a slain demon. The church pays handsomely.", "source": "Demon"},
    "Shadow Fragment": {"type": "bounty", "value": 100, "description": "A piece of solidified shadow. Proof of realm-touched kills.", "source": "Shadow Creature"},
}
# =========================================================
# COMBINE ALL ITEMS
# =========================================================

ITEMS = {}
ITEMS.update(CONSUMABLES)
ITEMS.update(WARRIOR_WEAPONS)
ITEMS.update(MAGE_WEAPONS)
ITEMS.update(ROGUE_WEAPONS)
ITEMS.update(PALADIN_WEAPONS)
ITEMS.update(BERSERKER_WEAPONS)
ITEMS.update(RANGER_WEAPONS)
ITEMS.update(ARMOR)
ITEMS.update(ACCESSORIES)
ITEMS.update(MATERIALS)
ITEMS.update(MISCELLANEOUS)
ITEMS.update(BOUNTY_ITEMS)

# =========================================================
# MISSIONS
# =========================================================

MISSIONS = {
    "slime_hunter": {
        "title": "Slime Infestation",
        "description": "The grasslands are overrun with slimes. Clear them out!",
        "type": "hunt",
        "target": "Slime",
        "amount": 5,
        "reward_gold": 100,
        "reward_exp": 150,
        "reward_item": "Small Potion",
        "difficulty": "Easy",
        "biome": "Grasslands",
    },
    "goblin_threat": {
        "title": "Goblin Menace",
        "description": "Goblin scouts have been spotted near the village. Deal with them.",
        "type": "hunt",
        "target": "Goblin Scout",
        "amount": 3,
        "reward_gold": 150,
        "reward_exp": 200,
        "reward_item": "Iron Sword",
        "difficulty": "Easy",
        "biome": "Grasslands",
    },
    "wolf_problem": {
        "title": "Wolves at the Door",
        "description": "Wolves are attacking travelers in the forest. Thin their numbers.",
        "type": "hunt",
        "target": "Wolf",
        "amount": 4,
        "reward_gold": 200,
        "reward_exp": 250,
        "reward_item": "Leather Armor",
        "difficulty": "Easy",
        "biome": "Forest",
    },
    "spider_nest": {
        "title": "Spider Nest",
        "description": "A giant spider nest threatens the forest path. Destroy it.",
        "type": "hunt",
        "target": "Forest Spider",
        "amount": 6,
        "reward_gold": 250,
        "reward_exp": 300,
        "reward_item": "Medium Potion",
        "difficulty": "Medium",
        "biome": "Forest",
    },
    "orc_invasion": {
        "title": "Orc Invasion",
        "description": "Orc warriors are massing for an attack. Strike first.",
        "type": "hunt",
        "target": "Orc Warrior",
        "amount": 5,
        "reward_gold": 400,
        "reward_exp": 500,
        "reward_item": "Steel Blade",
        "difficulty": "Medium",
        "biome": "Forest",
 },
    "golem_slayer": {
        "title": "Golem Slayer",
        "description": "Stone golems are blocking mountain passes. Clear the way.",
        "type": "hunt",
        "target": "Stone Golem",
        "amount": 3,
        "reward_gold": 500,
        "reward_exp": 600,
        "reward_item": "Knight Armor",
        "difficulty": "Hard",
        "biome": "Mountains",
    },
    "frost_giant": {
        "title": "Frost Giant Threat",
        "description": "A frost giant scout has been seen. Take it down before more come.",
        "type": "hunt",
        "target": "Frost Giant Scout",
        "amount": 2,
        "reward_gold": 600,
        "reward_exp": 700,
        "reward_item": "Frozen Plate",
        "difficulty": "Hard",
        "biome": "Mountains",
    },
    "desert_bandits": {
        "title": "Desert Bandits",
        "description": "Sand bandits are raiding caravans. Bring them to justice.",
        "type": "hunt",
        "target": "Sand Bandit",
        "amount": 5,
        "reward_gold": 450,
        "reward_exp": 550,
        "reward_item": "Rare Gem",
        "difficulty": "Medium",
        "biome": "Desert",
    },
    "scorpion_king": {
        "title": "Scorpion King",
        "description": "A giant scorpion terrorizes the dunes. End its reign.",
        "type": "hunt",
        "target": "Scorpion",
        "amount": 8,
        "reward_gold": 550,
        "reward_exp": 650,
        "reward_item": "Venom Shiv",
        "difficulty": "Hard",
        "biome": "Desert",
    },
    "ice_wolves": {
        "title": "Ice Wolf Pack",
        "description": "A pack of ice wolves preys on the frozen plains. Protect the settlers.",
        "type": "hunt",
        "target": "Ice Wolf",
        "amount": 6,
        "reward_gold": 600,
        "reward_exp": 750,
        "reward_item": "Ice Crystal",
        "difficulty": "Hard",
        "biome": "Ice Plains",
    },
    "frozen_knight": {
        "title": "The Frozen Knight",
        "description": "A cursed knight wanders the ice. Put him to rest.",
        "type": "hunt",
        "target": "Ice Knight",
        "amount": 3,
        "reward_gold": 700,
        "reward_exp": 850,
        "reward_item": "Frozen Relic",
        "difficulty": "Very Hard",
        "biome": "Ice Plains",
},
    "frozen_knight": {
        "title": "The Frozen Knight",
        "description": "A cursed knight wanders the ice. Put him to rest.",
        "type": "hunt",
        "target": "Ice Knight",
        "amount": 3,
        "reward_gold": 700,
        "reward_exp": 850,
        "reward_item": "Frozen Relic",
        "difficulty": "Very Hard",
        "biome": "Ice Plains",
    },
    "swamp_cleansing": {
        "title": "Swamp Cleansing",
        "description": "The swamp's corruption spreads. Destroy the source creatures.",
        "type": "hunt",
        "target": "Swamp Slime",
        "amount": 8,
        "reward_gold": 500,
        "reward_exp": 600,
        "reward_item": "Antidote Vial",
        "difficulty": "Medium",
        "biome": "Swamp",
    },
    "plague_doctor": {
        "title": "The Plague Doctor",
        "description": "A mad doctor experiments on the living. Stop him.",
        "type": "hunt",
        "target": "Plague Doctor",
        "amount": 2,
        "reward_gold": 800,
        "reward_exp": 900,
        "reward_item": "Swamp Relic",
        "difficulty": "Very Hard",
        "biome": "Swamp",
    },
    "shadow_hunter": {
        "title": "Shadow Hunter",
        "description": "Shadow creatures leak into our world. Hunt them back.",
        "type": "hunt",
        "target": "Shadow Imp",
        "amount": 10,
        "reward_gold": 700,
        "reward_exp": 800,
        "reward_item": "Shadow Relic",
        "difficulty": "Hard",
        "biome": "Shadow Realm",
    },
    "void_titan": {
        "title": "Titan of the Void",
        "description": "A void titan threatens reality itself. This is the final test.",
        "type": "hunt",
        "target": "Void Titan",
        "amount": 1,
        "reward_gold": 2000,
        "reward_exp": 2500,
        "reward_item": "Void Core",
        "difficulty": "Legendary",
        "biome": "Shadow Realm",
    },
    "herb_gathering": {
        "title": "Herb Gathering",
        "description": "The village healer needs herbs. Collect them from the grasslands.",
        "type": "collect",
        "target": "Herb",
        "amount": 10,
        "reward_gold": 80,
        "reward_exp": 100,
        "reward_item": "Small Potion",
        "difficulty": "Easy",
        "biome": "Grasslands",
    },
    "spider_silk": {
        "title": "Silk for the Weavers",
        "description": "The weavers guild needs quality spider silk.",
        "type": "collect",
        "target": "Spider Silk",
        "amount": 5,
        "reward_gold": 200,
        "reward_exp": 250,
        "reward_item": "Medium Potion",
        "difficulty": "Medium",
        "biome": "Forest",
},
    "ore_delivery": {
        "title": "Ore Delivery",
        "description": "The blacksmiths need mountain ore for their forges.",
        "type": "collect",
        "target": "Mountain Ore",
        "amount": 8,
        "reward_gold": 350,
        "reward_exp": 400,
        "reward_item": "Steel Blade",
        "difficulty": "Medium",
        "biome": "Mountains",
    },
    "troll_king_bounty": {
        "title": "Bounty: Troll King",
        "description": "The Troll King must fall. The grasslands will be safe again.",
        "type": "boss",
        "target": "Troll King",
        "amount": 1,
        "reward_gold": 500,
        "reward_exp": 600,
        "reward_item": "Legendary Amulet",
        "difficulty": "Hard",
        "biome": "Grasslands",
    },
    "treant_bounty": {
        "title": "Bounty: Ancient Treant",
        "description": "The Ancient Treant has awakened. End its rampage.",
        "type": "boss",
        "target": "Ancient Treant",
        "amount": 1,
        "reward_gold": 700,
        "reward_exp": 800,
        "reward_item": "Epic Staff",
        "difficulty": "Hard",
        "biome": "Forest",
    },
    "dragon_bounty": {
        "title": "Bounty: Dragon Lord",
        "description": "Slay the Dragon Lord and claim its hoard.",
        "type": "boss",
        "target": "Dragon Lord",
        "amount": 1,
        "reward_gold": 1500,
        "reward_exp": 1500,
        "reward_item": "Dragon Slayer Sword",
        "difficulty": "Very Hard",
        "biome": "Mountains",
    },
    "claim_eater_bounty": {
        "title": "The Final Claim",
        "description": "Defeat the Claim-Eater and save reality itself.",
        "type": "boss",
        "target": "The Claim-Eater",
        "amount": 1,
        "reward_gold": 5000,
        "reward_exp": 5000,
        "reward_item": "Crown of the Claimant",
        "difficulty": "Legendary",
        "biome": "Shadow Realm",
    },
}

# =========================================================
# RANK GENERATION
# =========================================================

def generate_rank(biome_tier: int = 0, luck_bonus: int = 0) -> str:
    """Generate an item rank. Higher biome tier and luck increase better rank odds."""
    roll = random.randint(1, 100)
    tier_bonus = biome_tier * 3 + luck_bonus

    if roll <= max(5, 40 - tier_bonus):
        return "Common"
    elif roll <= max(15, 65 - tier_bonus * 2):
        return "Enhanced"
    elif roll <= max(30, 82 - tier_bonus * 2):
        return "Rare"
    elif roll <= max(50, 93 - tier_bonus):
        return "Epic"
    elif roll <= max(80, 99 - tier_bonus):
        return "Legend"
    return "Dominant"

def create_ranked_item(item_name: str, biome_tier: int = 0, luck_bonus: int = 0) -> Optional[dict]:
    """Create a ranked version of an item."""
    if item_name not in ITEMS:
        return None

    base_item = ITEMS[item_name].copy()
    rank = generate_rank(biome_tier, luck_bonus)
    rank_data = ITEM_RANKS[rank]
    multiplier = rank_data["multiplier"]

    for stat in [
        "attack", "defense", "health", "heal", "critical_chance",
        "fire_damage", "ice_damage", "poison_damage", "void_damage",
        "lightning_damage", "holy_damage", "cosmic_damage",
        "armor_pierce", "life_steal", "regen", "regen_per_turn",
        "dodge_bonus", "stealth_bonus", "block_chance", "accuracy_bonus",
        "luck_bonus", "buff_attack", "buff_defense", "buff_speed",
        "buff_critical", "buff_magic", "buff_max_health"
    ]:
        if stat in base_item and isinstance(base_item[stat], (int, float)):
            base_item[stat] = int(base_item[stat] * multiplier)

    base_item["value"] = int(base_item.get("value", 0) * rank_data["value_multiplier"])
    base_item["rank"] = rank
    base_item["color"] = rank_data["color"]
    base_item["display_name"] = f"{rank} {item_name}"
    base_item["original_name"] = item_name

    return base_item

# =========================================================
# EQUIPMENT
# =========================================================

EQUIPMENT_SLOTS = ["weapon", "armor", "accessory"]

def get_equipped(player: dict, slot: str) -> Optional[dict]:
    """Get equipped item from slot."""
    return player.get("equipment", {}).get(slot)

def equip_item(player: dict, item: dict) -> Tuple[bool, str]:
    """Equip an item."""
    item_type = item.get("type")
    item_class = item.get("class")
    player_class = player.get("class")

    if item_type not in EQUIPMENT_SLOTS:
        return False, "This item cannot be equipped."

    if item_class and item_class != player_class:
        return False, f"Requires {item_class} class. You are a {player_class}."

    equipment = player.setdefault("equipment", {})
    old_item = equipment.get(item_type)
    equipment[item_type] = item.copy()

    recalculate_stats(player)

    if old_item:
        player.setdefault("inventory", []).append(old_item)
        return True, f"Equipped {item['display_name']}. {old_item['display_name']} returned to inventory."

    return True, f"Equipped {item['display_name']}."

def unequip_item(player: dict, slot: str) -> Tuple[bool, str]:
    """Unequip item from slot."""
    equipment = player.get("equipment", {})

    if slot not in equipment or equipment[slot] is None:
        return False, f"No item equipped in {slot} slot."

    item = equipment.pop(slot)
    player.setdefault("inventory", []).append(item)
    recalculate_stats(player)

def recalculate_stats(player: dict) -> None:
    """Recalculate player stats from class, level, and equipment."""
    try:
        from biomes import CLASS_BASE_STATS
    except ImportError:
        CLASS_BASE_STATS = {
            "Warrior": {"health": 120, "attack": 12, "defense": 8},
            "Mage": {"health": 80, "attack": 18, "defense": 3},
            "Rogue": {"health": 90, "attack": 14, "defense": 5},
            "Paladin": {"health": 130, "attack": 10, "defense": 10},
            "Berserker": {"health": 110, "attack": 20, "defense": 2},
            "Ranger": {"health": 95, "attack": 15, "defense": 6},
        }

    player_class = player.get("class", "Warrior")
    base_stats = CLASS_BASE_STATS.get(player_class, CLASS_BASE_STATS["Warrior"])
    level = max(1, int(player.get("level", 1)))

    bonus_per_level = {
        "Warrior": {"health": 10, "attack": 2, "defense": 2},
        "Mage": {"health": 5, "attack": 3, "defense": 1},
        "Rogue": {"health": 6, "attack": 2, "defense": 1},
        "Paladin": {"health": 12, "attack": 1, "defense": 3},
        "Berserker": {"health": 8, "attack": 3, "defense": 0},
        "Ranger": {"health": 7, "attack": 2, "defense": 1},
    }
    level_bonus = bonus_per_level.get(player_class, bonus_per_level["Warrior"])

    current_health = player.get("health", base_stats["health"])

    player["max_health"] = base_stats["health"] + (level - 1) * level_bonus["health"]
    player["attack"] = base_stats["attack"] + (level - 1) * level_bonus["attack"]
    player["defense"] = base_stats["defense"] + (level - 1) * level_bonus["defense"]

    player["critical_chance"] = min(50, 5 + (level // 5))
    player["dodge_chance"] = min(40, 5 + (level // 5))
    player["escape_chance"] = min(80, 30 + 2 * (level // 3))

    base_mana_map = {
        "Warrior": 40,
        "Mage": 100,
        "Rogue": 60,
        "Paladin": 70,
        "Berserker": 35,
        "Ranger": 65,
    }
    player["max_mana"] = max(player.get("max_mana", 0), base_mana_map.get(player_class, 50))

    equipment = player.get("equipment", {})
    for item in equipment.values():
        if not item:
            continue
        for stat in ["attack", "defense", "health", "critical_chance", "dodge_bonus"]:
            if stat in item:
                if stat == "health":
                    player["max_health"] += item[stat]
                elif stat == "dodge_bonus":
                    player["dodge_chance"] += item[stat]
                else:
                    player[stat] = player.get(stat, 0) + item[stat]

    player["health"] = min(current_health, player["max_health"])
    player["mana"] = min(player.get("mana", player["max_mana"]), player["max_mana"])


# =========================================================
# INVENTORY MANAGEMENT
# =========================================================

MAX_INVENTORY_SIZE = 50

def add_item(player: dict, item_name: str, biome_tier: int = 0, luck_bonus: int = 0) -> Tuple[bool, str]:
    """Add item to inventory."""
    inventory = player.setdefault("inventory", [])

    if len(inventory) >= MAX_INVENTORY_SIZE:
        return False, "Inventory is full! Cannot carry more items."

    ranked_item = create_ranked_item(item_name, biome_tier, luck_bonus)
    if not ranked_item:
        return False, f"Unknown item: {item_name}"

    inventory.append(ranked_item)
    player["items_found"] = player.get("items_found", 0) + 1

    return True, f"Obtained: {ranked_item['display_name']}"

def remove_item(player: dict, index: int) -> Tuple[bool, Optional[dict], str]:
    """Remove item by inventory index."""
    inventory = player.get("inventory", [])

    if not (0 <= index < len(inventory)):
        return False, None, "Invalid item index."

    item = inventory.pop(index)
    return True, item, f"Removed {item['display_name']}."

def sell_item(player: dict, index: int) -> Tuple[bool, str]:
    """Sell item directly from inventory."""
    success, item, msg = remove_item(player, index)
    if not success:
        return False, msg

    value = item.get("value", 0)
    player["gold"] = player.get("gold", 0) + value
    return True, f"Sold {item['display_name']} for {value} gold."
def use_item(player: dict, index: int) -> Tuple[bool, str]:
    """Use or equip inventory item."""
    inventory = player.get("inventory", [])

    if not (0 <= index < len(inventory)):
        return False, "Invalid item index."

    item = inventory[index]
    item_type = item.get("type")

    if item_type == "consumable":
        messages = []

        if item.get("revive") and player.get("health", 0) <= 0:
            heal_amount = item.get("heal", 50)
            player["health"] = min(heal_amount, player["max_health"])
            inventory.pop(index)
            return True, f"You were revived with {player['health']} HP!"

        if item.get("full_heal"):
            old_health = player["health"]
            player["health"] = player["max_health"]
            healed = player["health"] - old_health
            messages.append(f"Fully restored! Healed {healed} HP.")
        elif item.get("heal", 0) > 0:
            old_health = player["health"]
            player["health"] = min(player["health"] + item["heal"], player["max_health"])
            healed = player["health"] - old_health
            messages.append(f"Restored {healed} HP!")

        if item.get("cure_poison") or item.get("cure_all"):
            dots = player.get("dot_effects", [])
            before = len(dots)
            if item.get("cure_all"):
                player["dot_effects"] = []
            else:
                player["dot_effects"] = [d for d in dots if d.get("type") != "poison"]
            removed = before - len(player.get("dot_effects", []))
            if removed > 0:
                messages.append("Negative effects cured!")

        active_buffs = player.setdefault("active_buffs", {})

        if "buff_attack" in item:
            active_buffs["attack"] = {"value": item["buff_attack"], "duration": item.get("duration", 3)}
            messages.append(f"Attack +{item['buff_attack']} for {item.get('duration', 3)} turns.")

        if "buff_defense" in item:
            active_buffs["defense"] = {"value": item["buff_defense"], "duration": item.get("duration", 3)}
            messages.append(f"Defense +{item['buff_defense']} for {item.get('duration', 3)} turns.")

        if "buff_speed" in item:
            active_buffs["speed"] = {"value": item["buff_speed"], "duration": item.get("duration", 3)}
            messages.append(f"Speed +{item['buff_speed']} for {item.get('duration', 3)} turns.")

        if "buff_critical" in item:
            active_buffs["crit_bonus"] = {"value": item["buff_critical"], "duration": item.get("duration", 3)}
            messages.append(f"Critical chance +{item['buff_critical']} for {item.get('duration', 3)} turns.")

        if "buff_max_health" in item:
            active_buffs["max_health"] = {"value": item["buff_max_health"], "duration": item.get("duration", 3)}
            player["max_health"] += item["buff_max_health"]
            player["health"] = min(player["max_health"], player["health"] + item["buff_max_health"])
            messages.append(f"Max health +{item['buff_max_health']} for {item.get('duration', 3)} turns.")

        if "buff_magic" in item:
            old_mana = player.get("mana", 0)
            player["mana"] = min(player.get("max_mana", old_mana), old_mana + item["buff_magic"])
            restored = player["mana"] - old_mana
            if restored > 0:
                messages.append(f"Restored {restored} Mana.")

        if "regen_per_turn" in item:
            player.setdefault("dot_effects", []).append({
                "type": "regen",
                "heal": item["regen_per_turn"],
                "duration": item.get("duration", 5),
            })
            messages.append(f"Regeneration active: {item['regen_per_turn']} HP/turn for {item.get('duration', 5)} turns.")

        if not messages:
            return False, "This consumable has no effect."

        inventory.pop(index)
        return True, " ".join(messages)

    if item_type in EQUIPMENT_SLOTS:
        success, msg = equip_item(player, item)
        if success:
            inventory.pop(index)
        return success, msg

    if item_type in ("material", "bounty", "misc"):
        return False, f"{item_type.capitalize()} items cannot be used directly. Sell them for gold."

    return False, "Unknown item type."
def get_inventory_summary(player: dict) -> dict:
    """Get categorized inventory summary."""
    inventory = player.get("inventory", [])
    summary = {
        "consumable": [],
        "weapon": [],
        "armor": [],
        "accessory": [],
        "material": [],
        "misc": [],
        "bounty": [],
    }

    for i, item in enumerate(inventory):
        item_type = item.get("type", "unknown")
        entry = {
            "index": i,
            "display_name": item.get("display_name", item.get("original_name", "Unknown")),
            "value": item.get("value", 0),
            "description": item.get("description", ""),
        }
        if item_type in summary:
            summary[item_type].append(entry)
        else:
            summary.setdefault("other", []).append(entry)

    return summary


# =========================================================
# LOOT
# =========================================================

def give_random_loot(player: dict, biome_name: str, biomes: dict) -> Tuple[bool, str]:
    """Give random loot from biome loot table."""
    biome = biomes.get(biome_name)
    if not biome:
        return False, f"Unknown biome: {biome_name}"

    loot_table = biome.get("loot", {})
    if not loot_table:
        return False, "No loot available in this biome."

    biome_order = ["Grasslands", "Forest", "Mountains", "Desert", "Ice Plains", "Swamp", "Shadow Realm"]
    biome_tier = biome_order.index(biome_name) if biome_name in biome_order else 0
    item_name = random.choice(list(loot_table.keys()))

    return add_item(player, item_name, biome_tier)

def give_loot_from_pool(player: dict, loot_pool: list, biome_tier: int = 0) -> Tuple[bool, str]:
    """Give loot from custom loot pool."""
    if not loot_pool:
        return False, "No loot in pool."

    item_data = random.choice(loot_pool)
    if isinstance(item_data, str):
        return add_item(player, item_data, biome_tier)
    if isinstance(item_data, dict):
        item_name = item_data.get("name")
        if not item_name:
            return False, "Invalid loot data."
        return add_item(player, item_name, biome_tier)
    return False, "Unknown loot format."

# =========================================================
# MISSIONS
# =========================================================

def get_available_missions(player: dict) -> List[dict]:
    """Get missions available to player."""
    from biomes import get_available_biomes

    available_biomes = get_available_biomes(player)
    player_level = player.get("level", 1)
    completed_missions = player.get("completed_missions", [])
    active_missions = player.get("active_missions", [])
    active_ids = {m.get("id") for m in active_missions if "id" in m}

    diff_levels = {
        "Easy": 1,
        "Medium": 5,
        "Hard": 10,
        "Very Hard": 15,
        "Legendary": 25,
    }

    available = []
    for mission_id, mission in MISSIONS.items():
        if mission_id in completed_missions:
            continue
        if mission_id in active_ids:
            continue
        if mission["biome"] not in available_biomes:
            continue

        req_level = diff_levels.get(mission["difficulty"], 1)
        if player_level >= req_level:
            available.append({"id": mission_id, **mission})

    return available

def accept_mission(player: dict, mission_id: str) -> Tuple[bool, str]:
    """Accept a mission."""
    if mission_id not in MISSIONS:
        return False, "Mission not found."

    active_missions = player.setdefault("active_missions", [])
    for m in active_missions:
        if m.get("id") == mission_id:
            return False, "You already have this mission active."

    mission = MISSIONS[mission_id].copy()
    mission["id"] = mission_id
    mission["progress"] = 0
    active_missions.append(mission)

    return True, f"Accepted mission: {mission['title']}"
def update_mission_progress(player: dict, target_name: str, amount: int = 1) -> List[str]:
    """Update mission progress and return reward messages."""
    active_missions = player.get("active_missions", [])
    completed_missions = player.setdefault("completed_missions", [])
    messages = []

    for mission in active_missions[:]:
        if mission["target"] == target_name:
            mission["progress"] += amount

            if mission["progress"] >= mission["amount"]:
                active_missions.remove(mission)
                completed_missions.append(mission["id"])

                player["gold"] = player.get("gold", 0) + mission["reward_gold"]

                from leveling import add_exp
                level_msgs = add_exp(player, mission["reward_exp"])

                if mission.get("reward_item"):
                    success, item_msg = add_item(player, mission["reward_item"])
                    if success:
                        messages.append(item_msg)

                messages.append(
                    f"Mission Complete: {mission['title']}! "
                    f"+{mission['reward_gold']} Gold, +{mission['reward_exp']} EXP"
                )
                messages.extend(level_msgs)

    return messages

def get_mission_summary(player: dict) -> List[dict]:
    """Get summary of active missions."""
    active = player.get("active_missions", [])
    return [
        {
            "id": m["id"],
            "title": m["title"],
            "progress": m["progress"],
            "amount": m["amount"],
            "target": m["target"],
            "percent": int((m["progress"] / m["amount"]) * 100),
        }
        for m in active
    ]
