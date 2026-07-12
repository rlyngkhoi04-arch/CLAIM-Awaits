"""Prepare the Android build folder for Kivy/Buildozer packaging."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
ANDROID_DIR = ROOT_DIR / "android_build"

FILE_MAP = {
    "mobile_launcher.py": "main.py",
    "claim_game.py": "claim_game.py",
    "biomes.py": "biomes.py",
    "combat.py": "combat.py",
    "items.py": "items.py",
    "leveling.py": "leveling.py",
    "save_system.py": "save_system.py",
    "shop.py": "shop.py",
    "skills.py": "skills.py",
}

ASSET_FILES = {
    "app_icon.png",
    "splash_screen.png",
    "Combat_sound.mp3",
    "MainMenu_sound.mp3",
    "Travel_sound.mp3",
    "river-adventurer.txt",
}

ASSET_GLOBS = ("*.ttf", "*.otf")


def sync_game_files() -> None:
    """Copy the Android launcher plus the game sources into the Android build folder."""
    ANDROID_DIR.mkdir(exist_ok=True)

    for source_name, target_name in FILE_MAP.items():
        source_path = ROOT_DIR / source_name
        target_path = ANDROID_DIR / target_name

        if not source_path.exists():
            raise FileNotFoundError(f"Missing source file: {source_path}")

        shutil.copy2(source_path, target_path)
        print(f"Synced {source_name} -> android_build/{target_name}")

    for asset_name in sorted(ASSET_FILES):
        source_path = ROOT_DIR / asset_name
        if not source_path.exists():
            continue
        target_path = ANDROID_DIR / asset_name
        shutil.copy2(source_path, target_path)
        print(f"Synced {asset_name} -> android_build/{asset_name}")

    for pattern in ASSET_GLOBS:
        for source_path in sorted(ROOT_DIR.glob(pattern)):
            if not source_path.is_file():
                continue
            target_path = ANDROID_DIR / source_path.name
            shutil.copy2(source_path, target_path)
            print(f"Synced {source_path.name} -> android_build/{source_path.name}")


if __name__ == "__main__":
    sync_game_files()
    print("Android build sources are ready.")
