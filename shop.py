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

    return True, f"Unequipped {item['display_name']}."
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
"""Shop, Inn, Housing, and Farming system for CLAIM: Awaits"""

import random
from typing import List, Tuple


# =========================================================
# SHOP ITEMS
# =========================================================

SHOP_INVENTORY = {
    "consumables": [
        {"name": "Small Potion", "price": 25, "stock": 99},
        {"name": "Medium Potion", "price": 60, "stock": 50},
        {"name": "Large Potion", "price": 120, "stock": 25},
        {"name": "Herb", "price": 15, "stock": 99},
        {"name": "Dark Herb", "price": 50, "stock": 30},
        {"name": "Bandage Roll", "price": 20, "stock": 50},
        {"name": "Antidote Vial", "price": 40, "stock": 20},
        {"name": "Strength Tonic", "price": 80, "stock": 15},
        {"name": "Iron Skin Potion", "price": 80, "stock": 15},
        {"name": "Regeneration Salve", "price": 100, "stock": 10},
        {"name": "Phoenix Feather", "price": 800, "stock": 1},
        {"name": "Ambrosia", "price": 500, "stock": 2},
    ],
    "weapons": [
        {"name": "Iron Sword", "price": 100, "stock": 5},
        {"name": "Steel Blade", "price": 250, "stock": 3},
        {"name": "Knight Greatsword", "price": 500, "stock": 2},
        {"name": "Wooden Staff", "price": 90, "stock": 5},
        {"name": "Epic Staff", "price": 600, "stock": 2},
        {"name": "Twin Daggers", "price": 120, "stock": 5},
        {"name": "Shadow Knife", "price": 350, "stock": 3},
        {"name": "Holy Hammer", "price": 180, "stock": 4},
        {"name": "Blessed Sword", "price": 400, "stock": 2},
        {"name": "Battle Axe", "price": 200, "stock": 4},
        {"name": "Hunter Bow", "price": 140, "stock": 5},
        {"name": "Longbow", "price": 350, "stock": 3},
    ],
    "armor": [
        {"name": "Leather Armor", "price": 80, "stock": 5},
        {"name": "Studded Leather", "price": 160, "stock": 4},
        {"name": "Chainmail", "price": 300, "stock": 3},
        {"name": "Knight Armor", "price": 400, "stock": 2},
        {"name": "Scale Mail", "price": 350, "stock": 3},
    ],
    "accessories": [
        {"name": "Copper Ring", "price": 30, "stock": 10},
        {"name": "Silver Locket", "price": 60, "stock": 8},
        {"name": "Ring of Vitality", "price": 350, "stock": 3},
        {"name": "Ring of Power", "price": 400, "stock": 3},
        {"name": "Ring of Protection", "price": 380, "stock": 3},
        {"name": "Lucky Coin", "price": 300, "stock": 2},
    ],
}

# =========================================================
# INNS
# =========================================================

INNS = {
    "Grasslands": {
        "name": "The Restful Meadow",
        "rest_cost": 15,
        "meal_cost": 10,
        "heal_percent": 50,
        "description": "A cozy inn at the edge of the grasslands. Smells of fresh bread.",
    },
    "Forest": {
        "name": "Whispering Woods Tavern",
        "rest_cost": 25,
        "meal_cost": 15,
        "heal_percent": 60,
        "description": "Built into a hollow tree. The beds are mossy but surprisingly comfortable.",
    },
    "Mountains": {
        "name": "Stone Hearth Lodge",
        "rest_cost": 40,
        "meal_cost": 25,
        "heal_percent": 70,
        "description": "Carved into the mountainside. Warm fires and hot stew await.",
    },
    "Desert": {
        "name": "Oasis Rest",
        "rest_cost": 50,
        "meal_cost": 30,
        "heal_percent": 70,
        "description": "A miracle in the sands. Cool water and shade from the relentless sun.",
    },
    "Ice Plains": {
        "name": "Frozen Hearth Inn",
        "rest_cost": 60,
        "meal_cost": 35,
        "heal_percent": 80,
        "description": "Heated by magical flames. The warmest place for miles around.",
    },
    "Swamp": {
        "name": "Mudskipper's Rest",
        "rest_cost": 45,
        "meal_cost": 20,
        "heal_percent": 65,
        "description": "Built on stilts above the bog. Don't ask what's in the stew.",
    },
    "Shadow Realm": {
        "name": "The Last Light",
        "rest_cost": 100,
        "meal_cost": 50,
        "heal_percent": 100,
        "description": "A beacon of hope in eternal darkness. The beds are surprisingly soft.",
    },
}

# =========================================================
# HOUSING
# =========================================================

HOUSES = {
    "hut": {
        "name": "Humble Hut",
        "buy_price": 500,
        "rent_price": 20,
        "tax_rate": 5,
        "storage_bonus": 10,
        "rest_heal": 30,
        "description": "A small wooden hut. Leaks when it rains, but it's yours.",
    },
    "cottage": {
        "name": "Cozy Cottage",
        "buy_price": 1500,
        "rent_price": 50,
        "tax_rate": 10,
        "storage_bonus": 20,
        "rest_heal": 50,
        "description": "A charming stone cottage with a thatched roof. Home sweet home.",
    },
    "manor": {
        "name": "Noble Manor",
        "buy_price": 5000,
        "rent_price": 150,
        "tax_rate": 20,
        "storage_bonus": 40,
        "rest_heal": 80,
        "description": "A grand estate befitting a hero of the realm.",
    },
    "castle": {
        "name": "Claimant's Castle",
        "buy_price": 20000,
        "rent_price": 500,
        "tax_rate": 50,
        "storage_bonus": 100,
        "rest_heal": 100,
        "description": "A fortress of your own. The kingdom itself acknowledges your claim.",
    },
}

# =========================================================
# FARMS
# =========================================================

FARMS = {
    "small_plot": {
        "name": "Small Garden Plot",
        "buy_price": 300,
        "rent_price": 15,
        "tax_rate": 3,
        "yield_amount": 2,
        "yield_items": ["Herb", "Honey Jar", "Moss Clump"],
        "growth_time": 3,
        "description": "A tiny patch of fertile soil. Good for herbs and small crops.",
    },
    "farm": {
        "name": "Family Farm",
        "buy_price": 1200,
        "rent_price": 40,
        "tax_rate": 8,
        "yield_amount": 5,
        "yield_items": ["Herb", "Dark Herb", "Honey Jar", "Bandage Roll"],
        "growth_time": 5,
        "description": "A proper farm with room for various crops. Hard work, good harvest.",
    },
    "estate": {
        "name": "Vast Estate",
        "buy_price": 8000,
        "rent_price": 200,
        "tax_rate": 25,
        "yield_amount": 12,
        "yield_items": ["Herb", "Dark Herb", "Honey Jar", "Bandage Roll", "Antidote Vial", "Strength Tonic"],
        "growth_time": 7,
        "description": "Rolling fields as far as the eye can see. A farming empire.",
    },
}

# =========================================================
# SERVANTS
# =========================================================

SERVANTS = {
    "apprentice": {
        "name": "Apprentice",
        "hire_cost": 100,
        "weekly_wage": 10,
        "tax_rate": 2,
        "benefit": "inventory_sort",
        "description": "A young helper who organizes your inventory for you.",
    },
    "cook": {
        "name": "Personal Cook",
        "hire_cost": 300,
        "weekly_wage": 25,
        "tax_rate": 5,
        "benefit": "daily_meal",
        "description": "Prepares a free meal every day. Restores 20 HP.",
    },
    "guard": {
        "name": "House Guard",
        "hire_cost": 500,
        "weekly_wage": 40,
        "tax_rate": 8,
        "benefit": "defense_bonus",
        "defense_bonus": 3,
        "description": "A trained guard who watches your home. +3 Defense while resting.",
    },
    "healer": {
        "name": "Court Healer",
        "hire_cost": 800,
        "weekly_wage": 60,
        "tax_rate": 12,
        "benefit": "daily_heal",
        "heal_amount": 50,
        "description": "A skilled healer who tends your wounds. Heals 50 HP daily.",
    },
    "steward": {
        "name": "Estate Steward",
        "hire_cost": 1500,
        "weekly_wage": 100,
        "tax_rate": 15,
        "benefit": "auto_collect",
        "description": "Manages your farm and collects taxes. Auto-harvests crops.",
    },
}


# =========================================================
# SHOP FUNCTIONS
# =========================================================

def get_shop_items(category: str) -> List[dict]:
    """Get items in a shop category."""
    return SHOP_INVENTORY.get(category, [])

def buy_item(player: dict, category: str, item_index: int, items_module) -> Tuple[bool, str]:
    """Buy an item from the shop."""
    items = get_shop_items(category)

    if item_index < 0 or item_index >= len(items):
        return False, "Invalid item selection."

    shop_item = items[item_index]

    if shop_item["stock"] <= 0:
        return False, "Out of stock!"

    if player["gold"] < shop_item["price"]:
        return False, f"Not enough gold! Need {shop_item['price']}, have {player['gold']}."

    success, msg = items_module.add_item(player, shop_item["name"], biome_tier=0)
    if not success:
        return False, msg

    player["gold"] -= shop_item["price"]
    shop_item["stock"] -= 1

    return True, f"Bought {shop_item['name']} for {shop_item['price']} gold! {msg}"

def sell_to_shop(player: dict, item_index: int) -> Tuple[bool, str]:
    """Sell an item from inventory."""
    from items import remove_item

    success, item, msg = remove_item(player, item_index)
    if not success:
        return False, msg

    sell_value = int(item.get("value", 0) * 0.6)
    player["gold"] += sell_value

    return True, f"Sold {item['display_name']} for {sell_value} gold."

# =========================================================
# INN FUNCTIONS
# =========================================================

def rest_at_inn(player: dict, biome_name: str) -> Tuple[bool, str]:
    """Rest at an inn."""
    inn = INNS.get(biome_name)
    if not inn:
        return False, "No inn in this biome."

    if player["gold"] < inn["rest_cost"]:
        return False, f"Not enough gold! Rest costs {inn['rest_cost']} gold."

    player["gold"] -= inn["rest_cost"]

    heal_amount = int(player["max_health"] * inn["heal_percent"] / 100)
    old_hp = player["health"]
    player["health"] = min(player["max_health"], player["health"] + heal_amount)
    healed = player["health"] - old_hp

    player["dot_effects"] = []
    player["active_buffs"] = {}

    if "max_mana" in player:
        player["mana"] = player.get("max_mana", player.get("mana", 0))

    return True, (
        f"Rested at {inn['name']}. (-{inn['rest_cost']} gold) "
        f"Healed {healed} HP! Mana restored. All debuffs cleared."
    )

def buy_meal(player: dict, biome_name: str) -> Tuple[bool, str]:
    """Buy a meal at an inn."""
    inn = INNS.get(biome_name)
    if not inn:
        return False, "No inn in this biome."

    if player["gold"] < inn["meal_cost"]:
        return False, f"Not enough gold! Meal costs {inn['meal_cost']} gold."

    player["gold"] -= inn["meal_cost"]

    heal_amount = 25
    old_hp = player["health"]
    player["health"] = min(player["max_health"], player["health"] + heal_amount)
    healed = player["health"] - old_hp

    player.setdefault("active_buffs", {})["attack"] = {
        "value": 2,
        "duration": 3,
    }

    return True, (
        f"Enjoyed a hearty meal at {inn['name']}. (-{inn['meal_cost']} gold) "
        f"Healed {healed} HP! Attack +2 for 3 turns."
    )

# =========================================================
# HOUSING FUNCTIONS
# =========================================================

def buy_house(player: dict, house_type: str) -> Tuple[bool, str]:
    """Buy a house."""
    house = HOUSES.get(house_type)
    if not house:
        return False, "Invalid house type."

    if player.get("house"):
        return False, "You already own a house! Sell it first."

    if player["gold"] < house["buy_price"]:
        return False, f"Not enough gold! Costs {house['buy_price']} gold."

    player["gold"] -= house["buy_price"]
    player["house"] = {
        "type": house_type,
        "name": house["name"],
        "tax_rate": house["tax_rate"],
        "rest_heal": house["rest_heal"],
        "storage_bonus": house["storage_bonus"],
        "rented": False,
    }

    return True, f"Bought {house['name']}! Welcome home, {player['name']}!"

def rent_house(player: dict, house_type: str) -> Tuple[bool, str]:
    """Rent a house."""
    house = HOUSES.get(house_type)
    if not house:
        return False, "Invalid house type."

    if player.get("house"):
        return False, "You already have housing!"

    if player["gold"] < house["rent_price"]:
        return False, f"Not enough gold! Rent is {house['rent_price']} gold."

    player["gold"] -= house["rent_price"]
    player["house"] = {
        "type": house_type,
        "name": house["name"],
        "tax_rate": house["tax_rate"],
        "rest_heal": house["rest_heal"],
        "storage_bonus": house["storage_bonus"],
        "rented": True,
        "rent_due": 7,
    }

    return True, f"Rented {house['name']} for {house['rent_price']} gold/week!"

def rest_at_home(player: dict) -> Tuple[bool, str]:
    """Rest at home."""
    house = player.get("house")
    if not house:
        return False, "You don't have a house!"

    heal_amount = int(player["max_health"] * house["rest_heal"] / 100)
    old_hp = player["health"]
    player["health"] = min(player["max_health"], player["health"] + heal_amount)
    healed = player["health"] - old_hp

    player["dot_effects"] = []
    player["active_buffs"] = {}

    if "max_mana" in player:
        player["mana"] = player.get("max_mana", player.get("mana", 0))

    return True, (
        f"Rested at {house['name']}. Healed {healed} HP! "
        f"Mana restored. All debuffs cleared. Sweet dreams!"
    )

# =========================================================
# FARM FUNCTIONS
# =========================================================

def buy_farm(player: dict, farm_type: str) -> Tuple[bool, str]:
    """Buy a farm."""
    farm = FARMS.get(farm_type)
    if not farm:
        return False, "Invalid farm type."

    if player.get("farm"):
        return False, "You already own a farm!"

    if player["gold"] < farm["buy_price"]:
        return False, f"Not enough gold! Costs {farm['buy_price']} gold."

    player["gold"] -= farm["buy_price"]
    player["farm"] = {
        "type": farm_type,
        "name": farm["name"],
        "tax_rate": farm["tax_rate"],
        "yield_amount": farm["yield_amount"],
        "yield_items": farm["yield_items"],
        "growth_time": farm["growth_time"],
        "days_grown": 0,
        "rented": False,
    }

    return True, f"Bought {farm['name']}! Plant your first seeds!"

def rent_farm(player: dict, farm_type: str) -> Tuple[bool, str]:
    """Rent a farm."""
    farm = FARMS.get(farm_type)
    if not farm:
        return False, "Invalid farm type."

    if player.get("farm"):
        return False, "You already have a farm!"

    if player["gold"] < farm["rent_price"]:
        return False, f"Not enough gold! Rent is {farm['rent_price']} gold."

    player["gold"] -= farm["rent_price"]
    player["farm"] = {
        "type": farm_type,
        "name": farm["name"],
        "tax_rate": farm["tax_rate"],
        "yield_amount": farm["yield_amount"],
        "yield_items": farm["yield_items"],
        "growth_time": farm["growth_time"],
        "days_grown": 0,
        "rented": True,
        "rent_due": 7,
    }

    return True, f"Rented {farm['name']} for {farm['rent_price']} gold/week!"

def harvest_farm(player: dict, items_module) -> Tuple[bool, str]:
    """Harvest crops from farm."""
    farm = player.get("farm")
    if not farm:
        return False, "You don't have a farm!"

    if farm["days_grown"] < farm["growth_time"]:
        remaining = farm["growth_time"] - farm["days_grown"]
        return False, f"Crops not ready! {remaining} day(s) remaining."

    farm["days_grown"] = 0
    harvested = []

    for _ in range(farm["yield_amount"]):
        item_name = random.choice(farm["yield_items"])
        items_module.add_item(player, item_name)
        harvested.append(item_name)

    from collections import Counter
    counts = Counter(harvested)
    harvest_msg = ", ".join([f"{count}x {item}" for item, count in counts.items()])

    return True, f"Harvested from {farm['name']}: {harvest_msg}!"

def advance_farm_day(player: dict) -> None:
    """Advance farm growth by one day."""
    farm = player.get("farm")
    if farm:
        farm["days_grown"] = min(farm["growth_time"], farm["days_grown"] + 1)


# =========================================================
# SERVANT FUNCTIONS
# =========================================================

def hire_servant(player: dict, servant_type: str) -> Tuple[bool, str]:
    """Hire a servant."""
    servant = SERVANTS.get(servant_type)
    if not servant:
        return False, "Invalid servant type."

    servants = player.setdefault("servants", [])

    for s in servants:
        if s["type"] == servant_type:
            return False, f"You already have a {servant['name']}!"

    if player["gold"] < servant["hire_cost"]:
        return False, f"Not enough gold! Hire cost is {servant['hire_cost']} gold."

    player["gold"] -= servant["hire_cost"]
    servants.append({
        "type": servant_type,
        "name": servant["name"],
        "weekly_wage": servant["weekly_wage"],
        "tax_rate": servant["tax_rate"],
        "benefit": servant["benefit"],
    })

    return True, f"Hired {servant['name']}! Weekly wage: {servant['weekly_wage']} gold."

def fire_servant(player: dict, servant_type: str) -> Tuple[bool, str]:
    """Fire a servant."""
    servants = player.get("servants", [])

    for i, s in enumerate(servants):
        if s["type"] == servant_type:
            fired = servants.pop(i)
            return True, f"Fired {fired['name']}. They pack their bags and leave."

    return False, "You don't have that servant."

# =========================================================
# TAX FUNCTIONS
# =========================================================

def calculate_weekly_tax(player: dict) -> int:
    """Calculate total weekly tax."""
    total_tax = 0

    house = player.get("house")
    if house:
        total_tax += house["tax_rate"]

    farm = player.get("farm")
    if farm:
        total_tax += farm["tax_rate"]

    for servant in player.get("servants", []):
        total_tax += servant.get("tax_rate", 0)

    return total_tax

def pay_taxes(player: dict) -> Tuple[bool, str]:
    """Pay taxes."""
    current_tax = calculate_weekly_tax(player)
    total_due = current_tax + player.get("tax_due", 0)

    if total_due <= 0:
        return True, "No taxes due."

    if player["gold"] < total_due:
        player["tax_due"] = total_due
        return False, (
            f"Cannot pay {total_due} gold in taxes! Tax debt remains {player['tax_due']}. "
            f"The kingdom is displeased..."
        )

    player["gold"] -= total_due
    player["tax_paid_total"] = player.get("tax_paid_total", 0) + total_due
    player["tax_due"] = 0

    return True, f"Paid {total_due} gold in taxes to the kingdom. Long live the Crown!"

def get_property_summary(player: dict) -> dict:
    """Get summary of all player properties and weekly costs."""
    house = player.get("house")
    farm = player.get("farm")
    servants = player.get("servants", [])

    weekly_cost = 0

    if house and house.get("rented"):
        house_data = HOUSES.get(house["type"], {})
        weekly_cost += house_data.get("rent_price", 0)

    if farm and farm.get("rented"):
        farm_data = FARMS.get(farm["type"], {})
        weekly_cost += farm_data.get("rent_price", 0)

    for s in servants:
        weekly_cost += s.get("weekly_wage", 0)

    tax = calculate_weekly_tax(player)

    return {
        "house": house["name"] if house else None,
        "farm": farm["name"] if farm else None,
        "servant_count": len(servants),
        "servant_names": [s["name"] for s in servants],
        "weekly_rent": weekly_cost,
        "weekly_tax": tax,
        "total_weekly": weekly_cost + tax,
        "tax_due": player.get("tax_due", 0),
        "tax_paid_total": player.get("tax_paid_total", 0),
    }
