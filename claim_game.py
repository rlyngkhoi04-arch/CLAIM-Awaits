
"""
CLAIM: Awaits
A text-based RPG for Android and PC
"""

import os
import random

from save_system import new_player, load_game, save_game, list_saves, delete_save, get_rank
from biomes import BIOMES, BIOME_ORDER, get_available_biomes, get_biome_recommendation, get_random_monster, get_boss
from leveling import add_exp, get_level_progress, get_exp_for_level
from skills import SkillSystem, SKILLS
from combat import (
    calculate_damage, check_dodge, check_escape, enemy_attack,
    player_basic_attack, process_dot_effects, tick_buffs,
    apply_dot, combat_victory, create_combat_enemy, generate_loot_message
)
from items import (
    add_item, remove_item, sell_item, use_item, get_inventory_summary,
    equip_item, unequip_item, recalculate_stats, give_random_loot,
    update_mission_progress, get_available_missions, accept_mission,
    get_mission_summary, ITEMS, MAX_INVENTORY_SIZE
)
from shop import (
    get_shop_items, buy_item, sell_to_shop,
    rest_at_inn, buy_meal, rest_at_home,
    buy_house, rent_house, buy_farm, rent_farm,
    harvest_farm, advance_farm_day,
    hire_servant, fire_servant,
    pay_taxes, calculate_weekly_tax, get_property_summary,
    INNS, HOUSES, FARMS, SERVANTS
)


# =========================================================
# GAME CONSTANTS
# =========================================================

GAME_TITLE = """
   _____ _       _    __  __
  / ____| |     | |  |  \\/  |   /\\
 | |    | | __ _| | _| \\  / |  /  \\
 | |    | |/ _` | |/ / |\\/| | / /\\ \\
 | |____| | (_| |   <| |  | |/ ____ \\
  \\_____|_|\\__,_|_|\\_\\_|  |_/_/    \\_\\

        A W A I T S
"""


# =========================================================
# UTILITY FUNCTIONS
# =========================================================

def clear_screen():
    """Clear the terminal screen safely on PC and Pydroid."""
    try:
        if os.name == "nt":
            os.system("cls")
        elif os.environ.get("TERM"):
            os.system("clear")
        else:
            print("\n" * 40)
    except Exception:
        print("\n" * 40)


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)


def print_divider():
    """Print a divider line."""
    print("-" * 50)


def get_input(prompt="> "):
    """Get user input safely."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def press_enter():
    """Wait for user to press enter."""
    try:
        input("\nPress Enter to continue...")
    except (EOFError, KeyboardInterrupt):
        pass


def display_player_stats(player):
    """Display player stats in a nice format."""
    rank = get_rank(player["level"])

    print_header(f"{player['name']} - {rank} {player['class']}")
    print(f"  Level: {player['level']} / 100")
    print(f"  EXP: {player['exp']} / {player['exp_to_next']} ({get_level_progress(player)['percent']}%)")
    print(f"  HP: {player['health']} / {player['max_health']}")
    print(f"  Mana: {player.get('mana', 0)} / {player.get('max_mana', 0)}")
    print(f"  Attack: {player['attack']}")
    print(f"  Defense: {player['defense']}")
    print(f"  Crit Chance: {player['critical_chance']}%")
    print(f"  Dodge Chance: {player['dodge_chance']}%")
    print(f"  Escape Chance: {player['escape_chance']}%")
    print(f"  Gold: {player['gold']}")
    print(f"  Skill Points: {player['skill_points']}")
    print(f"  Location: {player['location']}")
    print(f"  Monsters Killed: {player.get('monsters_killed', 0)}")
    print(f"  Items Found: {player.get('items_found', 0)}")

    equipment = player.get("equipment", {})
    print("\n  [EQUIPPED]")
    for slot in ["weapon", "armor", "accessory"]:
        item = equipment.get(slot)
        if item:
            print(f"    {slot.title()}: {item['display_name']}")
        else:
            print(f"    {slot.title()}: None")

    buffs = player.get("active_buffs", {})
    if buffs:
        print("\n  [ACTIVE BUFFS]")
        for name, buff in buffs.items():
            print(f"    {name.replace('_', ' ').title()}: +{buff['value']} ({buff['duration']} turns)")

    print_divider()


def display_inventory(player):
    """Display inventory in categories."""
    summary = get_inventory_summary(player)

    print_header("INVENTORY")
    print(f"  Items: {len(player['inventory'])} / {MAX_INVENTORY_SIZE}")
    print_divider()

    for category, items in summary.items():
        if items:
            print(f"\n  [{category.upper()}]")
            for item in items:
                print(f"    [{item['index'] + 1}] {item['display_name']} ({item['value']}g)")

    if not player["inventory"]:
        print("\n  Your inventory is empty.")

    print_divider()


def display_missions(player):
    """Display active and available missions."""
    print_header("MISSIONS")

    active = get_mission_summary(player)
    if active:
        print("\n  [ACTIVE]")
        for m in active:
            bar = "█" * (m["percent"] // 10) + "░" * (10 - m["percent"] // 10)
            print(f"    {m['title']}: {bar} {m['percent']}% ({m['progress']}/{m['amount']})")
    else:
        print("\n  No active missions.")

    available = get_available_missions(player)
    if available:
        print("\n  [AVAILABLE]")
        for i, m in enumerate(available[:5]):
            print(f"    [{i}] {m['title']} [{m['difficulty']}]")
            print(f"      {m['description']}")
            print(f"      Reward: {m['reward_gold']}g, {m['reward_exp']} EXP, {m['reward_item']}")
    else:
        print("\n  No available missions.")

    print_divider()


# =========================================================
# COMBAT SYSTEM
# =========================================================

def combat_encounter(player, biome_name):
    """Handle a combat encounter."""
    enemy = create_combat_enemy(biome_name, BIOMES)
    if not enemy:
        print("No enemies here...")
        return

    skill_system = SkillSystem()
    turn = 0

    print_header(f"COMBAT: {enemy['name']}")
    print(f"  Enemy HP: {enemy['health']} | ATK: {enemy['attack']} | DEF: {enemy['defense']}")
    print_divider()

    while player["health"] > 0 and enemy["health"] > 0:
        turn += 1
        print(f"\n--- Turn {turn} ---")
        print(f"Your HP: {player['health']}/{player['max_health']}")
        print(f"Your Mana: {player.get('mana', 0)}/{player.get('max_mana', 0)}")
        print(f"Enemy HP: {enemy['health']}/{enemy['max_health']}")

        print("\n[Actions]")
        print("  [1] Attack")
        print("  [2] Skills")
        print("  [3] Use Item")
        print("  [4] Escape")

        choice = get_input("Choose action: ")

        if choice == "1":
            dmg, crit, dodged, msg = player_basic_attack(player, enemy)
            print(f"\n{msg}")

        elif choice == "2":
            skills = skill_system.get_skill_info(player["class"])
            if not skills:
                print("No skills available!")
                continue

            print("\n[Skills]")
            for s in skills:
                cd_msg = f" [CD: {s['on_cooldown']}]" if s["on_cooldown"] > 0 else ""
                print(f"  [{s['index'] + 1}] {s['name']} | Mana: {s['mana_cost']} | x{s['multiplier']}{cd_msg}")

            skill_choice = get_input("Choose skill (or 0 to cancel): ")
            if skill_choice == "0":
                continue

            try:
                idx = int(skill_choice) - 1
                success, msg, effect = skill_system.use_skill(player, enemy, idx)
                print(f"\n{msg}")

                if effect.get("stun_duration"):
                    enemy["stunned"] = effect["stun_duration"]
                if effect.get("burn_damage"):
                    apply_dot(enemy, "burn", effect["burn_damage"], effect["burn_duration"])
                if effect.get("poison_damage"):
                    apply_dot(enemy, "poison", effect["poison_damage"], effect["poison_duration"])
                if effect.get("slow_percent"):
                    enemy.setdefault("active_buffs", {})["slow"] = {
                        "value": effect["slow_percent"],
                        "duration": effect["slow_duration"],
                    }

            except (ValueError, IndexError):
                print("Invalid skill!")
                continue

        elif choice == "3":
            display_inventory(player)
            item_choice = get_input("Use item number (0 to cancel): ")
            if item_choice == "0":
                continue
            try:
                idx = int(item_choice) - 1
                success, msg = use_item(player, idx)
                print(f"\n{msg}")
            except ValueError:
                print("Invalid item!")
            continue

        elif choice == "4":
            if check_escape(player, enemy):
                print("\nYou escaped successfully!")
                return
            else:
                print("\nEscape failed!")

        else:
            print("Invalid choice!")
            continue

        if enemy["health"] <= 0:
            print(f"\n*** {enemy['name']} DEFEATED! ***")

            msgs = combat_victory(player, enemy, BIOMES, __import__("items"))
            for msg in msgs:
                print(f"  {msg}")

            press_enter()
            return

        if enemy.get("stunned", 0) > 0:
            enemy["stunned"] -= 1
            print(f"\n{enemy['name']} is stunned! ({enemy['stunned']} turns left)")
        else:
            dmg, crit, dodged, msg = enemy_attack(enemy, player)
            print(f"\n{msg}")

        dot_msgs = process_dot_effects(player)
        for m in dot_msgs:
            print(f"  {m}")

        dot_msgs = process_dot_effects(enemy)
        for m in dot_msgs:
            print(f"  {m}")

        buff_msgs = tick_buffs(player)
        for m in buff_msgs:
            print(f"  {m}")

        buff_msgs = tick_buffs(enemy)
        for m in buff_msgs:
            print(f"  {m}")

        skill_system.tick_cooldowns()

        if player["health"] <= 0:
            print(f"\n*** YOU HAVE FALLEN ***")
            print(f"The {enemy['name']} stands victorious...")
            player["health"] = 1
            print("You barely crawl away with your life.")
            press_enter()
            return

    press_enter()


def boss_fight(player, biome_name):
    """Handle a boss fight."""
    boss = get_boss(biome_name)
    if not boss:
        print("No boss in this biome!")
        return

    if biome_name in player.get("bosses_defeated", []):
        print(f"You have already defeated {boss['name']}!")
        return

    print_header(f"BOSS FIGHT: {boss['name']}")
    print(f'  "{boss["title"]}"')
    print(f"  {boss['description']}")
    print_divider()
    print(f"  HP: {boss['health']} | ATK: {boss['attack']} | DEF: {boss['defense']}")
    print(f"\n{boss['intro_text']}")
    print_divider()

    confirm = get_input("Challenge the boss? (y/n): ").lower()
    if confirm != "y":
        print("You retreat... for now.")
        return

    skill_system = SkillSystem()
    turn = 0

    while player["health"] > 0 and boss["health"] > 0:
        turn += 1
        print(f"\n--- Turn {turn} ---")
        print(f"Your HP: {player['health']}/{player['max_health']}")
        print(f"Your Mana: {player.get('mana', 0)}/{player.get('max_mana', 0)}")
        print(f"{boss['name']} HP: {boss['health']}/{boss['max_health']}")

        print("\n[Actions]")
        print("  [1] Attack")
        print("  [2] Skills")
        print("  [3] Use Item")

        choice = get_input("Choose action: ")

        if choice == "1":
            dmg, crit, dodged, msg = player_basic_attack(player, boss)
            print(f"\n{msg}")

        elif choice == "2":
            skills = skill_system.get_skill_info(player["class"])
            print("\n[Skills]")
            for s in skills:
                cd_msg = f" [CD: {s['on_cooldown']}]" if s["on_cooldown"] > 0 else ""
                print(f"  [{s['index'] + 1}] {s['name']} | Mana: {s['mana_cost']} | x{s['multiplier']}{cd_msg}")

            skill_choice = get_input("Choose skill (or 0 to cancel): ")
            if skill_choice == "0":
                continue
            try:
                idx = int(skill_choice) - 1
                success, msg, effect = skill_system.use_skill(player, boss, idx)
                print(f"\n{msg}")

                if effect.get("stun_duration"):
                    boss["stunned"] = effect["stun_duration"]
                if effect.get("burn_damage"):
                    apply_dot(boss, "burn", effect["burn_damage"], effect["burn_duration"])
                if effect.get("poison_damage"):
                    apply_dot(boss, "poison", effect["poison_damage"], effect["poison_duration"])
                if effect.get("slow_percent"):
                    boss.setdefault("active_buffs", {})["slow"] = {
                        "value": effect["slow_percent"],
                        "duration": effect["slow_duration"],
                    }

            except (ValueError, IndexError):
                print("Invalid skill!")
                continue

        elif choice == "3":
            display_inventory(player)
            item_choice = get_input("Use item number (0 to cancel): ")
            if item_choice == "0":
                continue
            try:
                idx = int(item_choice) - 1
                success, msg = use_item(player, idx)
                print(f"\n{msg}")
            except ValueError:
                print("Invalid item!")
            continue

        else:
            print("Invalid choice!")
            continue

        if boss["health"] <= 0:
            print(f"\n*** {boss['name']} DEFEATED! ***")
            print(f"\n{boss['defeat_text']}")

            player.setdefault("bosses_defeated", []).append(biome_name)

            exp_gained = boss["exp"]
            level_msgs = add_exp(player, exp_gained)
            for msg in level_msgs:
                print(f"  {msg}")
            print(f"  Gained {exp_gained} EXP!")

            player["gold"] += boss["gold"]
            print(f"  Found {boss['gold']} Gold!")

            for loot_item in boss.get("loot", []):
                if random.random() <= loot_item.get("drop_rate", 1.0):
                    add_item(player, loot_item["name"])
                    print(f"  Dropped: {loot_item['name']}!")

            print("\n*** NEW AREA UNLOCKED! ***")
            press_enter()
            return

        if boss.get("stunned", 0) > 0:
            boss["stunned"] -= 1
            print(f"\n{boss['name']} is stunned!")
        else:
            ability = boss.get("ability", {})
            if ability and random.randint(1, 100) <= 30:
                mult = ability.get("damage_multiplier", 1.5)
                dmg = max(1, int(boss["attack"] * mult) - player["defense"])
                player["health"] = max(0, player["health"] - dmg)
                print(f"\n{boss['name']} uses {ability['name']}!")
                print(f"  Dealt {dmg} damage! {ability['description']}")
            else:
                dmg, crit, dodged, msg = enemy_attack(boss, player)
                print(f"\n{msg}")

        dot_msgs = process_dot_effects(player)
        for m in dot_msgs:
            print(f"  {m}")

        dot_msgs = process_dot_effects(boss)
        for m in dot_msgs:
            print(f"  {m}")

        buff_msgs = tick_buffs(player)
        for m in buff_msgs:
            print(f"  {m}")

        buff_msgs = tick_buffs(boss)
        for m in buff_msgs:
            print(f"  {m}")

        skill_system.tick_cooldowns()

        if player["health"] <= 0:
            print(f"\n*** DEFEATED BY {boss['name'].upper()} ***")
            player["health"] = 1
            print("You retreat, battered but alive. Train harder and try again!")
            press_enter()
            return

    press_enter()


# =========================================================
# MAIN MENU
# =========================================================

def main_menu():
    """Display main menu."""
    clear_screen()
    print(GAME_TITLE)
    print("\n[1] New Game")
    print("[2] Load Game")
    print("[3] Delete Save")
    print("[4] Exit")

    choice = get_input("\nSelect: ")
    return choice


def new_game():
    """Create a new game."""
    clear_screen()
    print_header("NEW GAME")

    name = get_input("Enter your name: ")
    if not name:
        name = "Claimant"

    print("\nChoose your class:")
    classes = ["Warrior", "Mage", "Rogue", "Paladin", "Berserker", "Ranger"]
    for i, cls in enumerate(classes):
        stats = {
            "Warrior": "High HP/DEF, balanced ATK",
            "Mage": "Low HP, highest ATK",
            "Rogue": "Medium stats, high crit",
            "Paladin": "Highest HP/DEF, low ATK",
            "Berserker": "High HP/ATK, no DEF",
            "Ranger": "Balanced, good crit",
        }
        print(f"  [{i}] {cls} - {stats[cls]}")

    cls_choice = get_input("Select class: ")
    try:
        player_class = classes[int(cls_choice)]
    except (ValueError, IndexError):
        player_class = "Warrior"

    player = new_player(name, player_class)
    recalculate_stats(player)

    print(f"\nWelcome, {player['name']} the {player['class']}!")
    print("Your journey begins in the Grasslands...")
    press_enter()

    return player


def load_game_menu():
    """Load an existing game."""
    clear_screen()
    print_header("LOAD GAME")

    saves = list_saves()
    if not saves:
        print("No save files found!")
        press_enter()
        return None

    print("Available saves:")
    for i, save in enumerate(saves):
        print(f"  [{i}] {save}")

    choice = get_input("\nSelect save (or 'b' to go back): ")
    if choice.lower() == "b":
        return None

    try:
        save_name = saves[int(choice)]
        player = load_game(save_name)
        if player:
            player["exp_to_next"] = get_exp_for_level(player["level"])
            recalculate_stats(player)
            print(f"\nLoaded {player['name']} the {player['class']}!")
            press_enter()
            return player
        else:
            print("Failed to load save!")
            press_enter()
            return None
    except (ValueError, IndexError):
        print("Invalid selection!")
        press_enter()
        return None


def delete_save_menu():
    """Delete a save file."""
    clear_screen()
    print_header("DELETE SAVE")

    saves = list_saves()
    if not saves:
        print("No save files found!")
        press_enter()
        return

    print("Available saves:")
    for i, save in enumerate(saves):
        print(f"  [{i}] {save}")

    choice = get_input("\nSelect save to delete (or 'b' to go back): ")
    if choice.lower() == "b":
        return

    try:
        save_name = saves[int(choice)]
        confirm = get_input(f"Are you sure you want to delete '{save_name}'? (y/n): ").lower()
        if confirm == "y":
            if delete_save(save_name):
                print("Save deleted!")
            else:
                print("Failed to delete save!")
        else:
            print("Cancelled.")
    except (ValueError, IndexError):
        print("Invalid selection!")

    press_enter()


  # =========================================================
# GAME LOOP
# =========================================================

def game_loop(player):
    """Main game loop."""
    save_name = player["name"].replace(" ", "_").lower()

    while True:
        clear_screen()

        rank = get_rank(player["level"])
        print(f"\n[{rank}] {player['name']} | Lv.{player['level']} | HP: {player['health']}/{player['max_health']} | Mana: {player.get('mana', 0)}/{player.get('max_mana', 0)} | Gold: {player['gold']}")
        print(f"Location: {player['location']}")
        print_divider()

        print("\n[MAIN MENU]")
        print("  [1] Explore")
        print("  [2] Fight Monster")
        print("  [3] Challenge Boss")
        print("  [4] Inventory")
        print("  [5] Skills")
        print("  [6] Stats")
        print("  [7] Travel")
        print("  [8] Shop & Inn")
        print("  [9] Housing & Farm")
        print("  [10] Missions")
        print("  [11] Save Game")
        print("  [12] Quit")

        choice = get_input("\nSelect: ")

        if choice == "1":
            events = [
                "You wander through the area, finding nothing of interest.",
                "You discover some old ruins. Nothing valuable remains.",
                "A merchant passes by, nodding in greeting.",
                "You find a small shrine and leave an offering.",
                "The wind carries whispers of distant battles.",
            ]
            print(f"\n{random.choice(events)}")
            advance_farm_day(player)
            press_enter()

        elif choice == "2":
            combat_encounter(player, player["location"])

        elif choice == "3":
            boss_fight(player, player["location"])

        elif choice == "4":
            inventory_menu(player)

        elif choice == "5":
            skills_menu(player)

        elif choice == "6":
            display_player_stats(player)
            press_enter()

        elif choice == "7":
            travel_menu(player)

        elif choice == "8":
            shop_inn_menu(player)

        elif choice == "9":
            housing_menu(player)

        elif choice == "10":
            missions_menu(player)

        elif choice == "11":
            if save_game(player, save_name):
                print("\nGame saved successfully!")
            else:
                print("\nFailed to save game!")
            press_enter()

        elif choice == "12":
            confirm = get_input("Save before quitting? (y/n): ").lower()
            if confirm == "y":
                save_game(player, save_name)
            print("\nUntil next time, Claimant...")
            break

        else:
            print("\nInvalid choice!")
            press_enter()


def inventory_menu(player):
    """Inventory submenu."""
    while True:
        clear_screen()
        display_inventory(player)

        print("\n[Inventory Actions]")
        print("  [1] Use/Equip Item")
        print("  [2] Sell Item")
        print("  [3] Unequip")
        print("  [4] Back")

        choice = get_input("Select: ")

        if choice == "1":
            idx = get_input("Item number: ")
            try:
                success, msg = use_item(player, int(idx) - 1)
                print(f"\n{msg}")
            except ValueError:
                print("Invalid number!")
            press_enter()

        elif choice == "2":
            idx = get_input("Item number: ")
            try:
                success, msg = sell_item(player, int(idx) - 1)
                print(f"\n{msg}")
            except ValueError:
                print("Invalid number!")
            press_enter()

        elif choice == "3":
            print("\nSlots: weapon, armor, accessory")
            slot = get_input("Slot to unequip: ").lower()
            success, msg = unequip_item(player, slot)
            print(f"\n{msg}")
            press_enter()

        elif choice == "4":
            break

        else:
            print("Invalid choice!")
            press_enter()


def skills_menu(player):
    """Skills submenu."""
    clear_screen()
    print_header("SKILLS")

    skills = SKILLS.get(player["class"], [])
    for i, skill in enumerate(skills):
        damage_mult = skill.get("damage_multiplier", skill.get("multiplier", 1))
        print(f"\n  [{i}] {skill['name']}")
        print(f"      Mana Cost: {skill['mana_cost']} | Damage: x{damage_mult}")
        print(f"      Cooldown: {skill['cooldown']} turns")
        print(f"      Effect: {skill.get('effect', 'None')}")
        print(f"      {skill['description']}")

    print_divider()
    press_enter()


def travel_menu(player):
    """Travel submenu."""
    while True:
        clear_screen()
        print_header("TRAVEL")

        available = get_available_biomes(player)

        print("\nAvailable destinations:")
        for i, biome in enumerate(available):
            rec = BIOMES[biome]
            current = " <- YOU ARE HERE" if biome == player["location"] else ""
            print(f"  [{i}] {biome} [{rec['danger_level']}]{current}")
            print(f"      Rec. Level: {rec['recommended_level']} | Rec. Rank: {rec['recommended_rank']}")

        print("\n  [b] Back")

        choice = get_input("\nSelect destination: ")
        if choice.lower() == "b":
            break

        try:
            idx = int(choice)
            if 0 <= idx < len(available):
                biome_name = available[idx]

                if biome_name == player["location"]:
                    print("You are already here!")
                    press_enter()
                    continue

                rec = get_biome_recommendation(player, biome_name)
                print(f"\nTraveling to {biome_name}...")
                print(f"Danger: {rec.get('danger_level', 'Unknown')}")
                print(f"Assessment: {rec.get('assessment', '')}")

                confirm = get_input("\nProceed? (y/n): ").lower()
                if confirm == "y":
                    player["location"] = biome_name
                    print(f"\nArrived at {biome_name}!")
                    print(BIOMES[biome_name]["description"])
                else:
                    print("Travel cancelled.")

                press_enter()
        except ValueError:
            print("Invalid selection!")
            press_enter()


def shop_inn_menu(player):
    """Shop and Inn submenu."""
    while True:
        clear_screen()
        print_header("SHOP & INN")
        print(f"Gold: {player['gold']}")
        print_divider()

        print("\n[1] Buy Items")
        print("[2] Sell Items")
        print("[3] Rest at Inn")
        print("[4] Buy Meal")
        print("[5] Back")

        choice = get_input("\nSelect: ")

        if choice == "1":
            shop_buy_menu(player)

        elif choice == "2":
            display_inventory(player)
            idx = get_input("Sell item number (or 'b' to cancel): ")
            if idx.lower() == "b":
                continue
            try:
                success, msg = sell_to_shop(player, int(idx) - 1)
                print(f"\n{msg}")
            except ValueError:
                print("Invalid number!")
            press_enter()

        elif choice == "3":
            success, msg = rest_at_inn(player, player["location"])
            print(f"\n{msg}")
            press_enter()

        elif choice == "4":
            success, msg = buy_meal(player, player["location"])
            print(f"\n{msg}")
            press_enter()

        elif choice == "5":
            break

        else:
            print("Invalid choice!")
            press_enter()


def shop_buy_menu(player):
    """Shop buying submenu."""
    categories = {
        "1": ("consumables", "Consumables"),
        "2": ("weapons", "Weapons"),
        "3": ("armor", "Armor"),
        "4": ("accessories", "Accessories"),
    }

    while True:
        clear_screen()
        print_header("SHOP - BUY")
        print(f"Gold: {player['gold']}")
        print_divider()

        print("\nCategories:")
        print("  [1] Consumables")
        print("  [2] Weapons")
        print("  [3] Armor")
        print("  [4] Accessories")
        print("  [5] Back")

        choice = get_input("\nSelect category: ")

        if choice == "5":
            break

        if choice not in categories:
            print("Invalid category!")
            press_enter()
            continue

        cat_key, cat_name = categories[choice]
        from shop import SHOP_INVENTORY
        items = SHOP_INVENTORY.get(cat_key, [])

        if not items:
            print("No items in this category!")
            press_enter()
            continue

        print(f"\n[{cat_name}]")
        for i, item in enumerate(items):
            print(f"  [{i}] {item['name']} - {item['price']}g (Stock: {item['stock']})")

        item_choice = get_input("\nBuy item (number, or 'b' to cancel): ")
        if item_choice.lower() == "b":
            continue

        try:
            idx = int(item_choice)
            success, msg = buy_item(player, cat_key, idx, __import__("items"))
            print(f"\n{msg}")
        except ValueError:
            print("Invalid number!")

        press_enter()


def housing_menu(player):
    """Housing and farm submenu."""
    while True:
        clear_screen()
        print_header("HOUSING & PROPERTY")

        house = player.get("house")
        farm = player.get("farm")
        servants = player.get("servants", [])

        print("\n[Current Properties]")
        if house:
            print(f"  House: {house['name']} ({'Rented' if house.get('rented') else 'Owned'})")
        else:
            print("  House: None")

        if farm:
            print(f"  Farm: {farm['name']} (Growth: {farm['days_grown']}/{farm['growth_time']})")
        else:
            print("  Farm: None")

        if servants:
            print(f"  Servants: {', '.join(s['name'] for s in servants)}")
        else:
            print("  Servants: None")

        tax = calculate_weekly_tax(player)
        print(f"\n  Weekly Tax: {tax} gold")
        print(f"  Tax Debt: {player.get('tax_due', 0)} gold")

        print_divider()
        print("\n[1] Buy House")
        print("[2] Rent House")
        print("[3] Buy Farm")
        print("[4] Rent Farm")
        print("[5] Hire Servant")
        print("[6] Rest at Home")
        print("[7] Harvest Farm")
        print("[8] Pay Taxes")
        print("[9] Back")

        choice = get_input("\nSelect: ")

        if choice == "1":
            print("\n[Houses for Sale]")
            for key, h in HOUSES.items():
                print(f"  [{key}] {h['name']} - {h['buy_price']}g")
                print(f"      Tax: {h['tax_rate']}/week | Rest Heal: {h['rest_heal']}%")

            h_choice = get_input("Select house (or 'b' to cancel): ")
            if h_choice.lower() != "b":
                success, msg = buy_house(player, h_choice)
                print(f"\n{msg}")
                press_enter()

        elif choice == "2":
            print("\n[Houses for Rent]")
            for key, h in HOUSES.items():
                print(f"  [{key}] {h['name']} - {h['rent_price']}g/week")

            h_choice = get_input("Select house (or 'b' to cancel): ")
            if h_choice.lower() != "b":
                success, msg = rent_house(player, h_choice)
                print(f"\n{msg}")
                press_enter()

        elif choice == "3":
            print("\n[Farms for Sale]")
            for key, f in FARMS.items():
                print(f"  [{key}] {f['name']} - {f['buy_price']}g")

            f_choice = get_input("Select farm (or 'b' to cancel): ")
            if f_choice.lower() != "b":
                success, msg = buy_farm(player, f_choice)
                print(f"\n{msg}")
                press_enter()

        elif choice == "4":
            print("\n[Farms for Rent]")
            for key, f in FARMS.items():
                print(f"  [{key}] {f['name']} - {f['rent_price']}g/week")

            f_choice = get_input("Select farm (or 'b' to cancel): ")
            if f_choice.lower() != "b":
                success, msg = rent_farm(player, f_choice)
                print(f"\n{msg}")
                press_enter()

        elif choice == "5":
            print("\n[Servants for Hire]")
            for key, s in SERVANTS.items():
                print(f"  [{key}] {s['name']} - Hire: {s['hire_cost']}g | Wage: {s['weekly_wage']}g/week")

            s_choice = get_input("Select servant (or 'b' to cancel): ")
            if s_choice.lower() != "b":
                success, msg = hire_servant(player, s_choice)
                print(f"\n{msg}")
                press_enter()

        elif choice == "6":
            success, msg = rest_at_home(player)
            print(f"\n{msg}")
            press_enter()

        elif choice == "7":
            success, msg = harvest_farm(player, __import__("items"))
            print(f"\n{msg}")
            press_enter()

        elif choice == "8":
            success, msg = pay_taxes(player)
            print(f"\n{msg}")
            press_enter()

        elif choice == "9":
            break

        else:
            print("Invalid choice!")
            press_enter()


def missions_menu(player):
    """Missions submenu."""
    while True:
        clear_screen()
        display_missions(player)

        print("\n[1] Accept Mission")
        print("[2] Back")

        choice = get_input("Select: ")

        if choice == "1":
            available = get_available_missions(player)
            if available:
                idx = get_input("Accept mission number: ")
                try:
                    mission = available[int(idx)]
                    success, msg = accept_mission(player, mission["id"])
                    print(f"\n{msg}")
                except (ValueError, IndexError):
                    print("Invalid selection!")
                press_enter()
            else:
                print("No missions available!")
                press_enter()

        elif choice == "2":
            break

        else:
            print("Invalid choice!")
            press_enter()


# =========================================================
# ENTRY POINT
# =========================================================

def main():
    """Main entry point."""
    while True:
        choice = main_menu()

        if choice == "1":
            player = new_game()
            if player:
                game_loop(player)

        elif choice == "2":
            player = load_game_menu()
            if player:
                game_loop(player)

        elif choice == "3":
            delete_save_menu()

        elif choice == "4":
            print("\nFarewell, Claimant...")
            break

        else:
            print("\nInvalid choice!")
            press_enter()


if __name__ == "__main__":
    main()
