"""Enhanced Kivy launcher for packaging CLAIM: Awaits as an Android APK."""

from __future__ import annotations

import builtins
import io
import os
import queue
import re
import sys
import threading
import traceback

from kivy.animation import Animation
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

import claim_game
import save_system


class ThemedFloatLayout(FloatLayout):
    """Float layout with an animatable background color."""

    bg_color = ListProperty([0.09, 0.11, 0.10, 1.0])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        with self.canvas.before:
            self._bg_instruction = Color(rgba=self.bg_color)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_canvas, size=self._update_canvas, bg_color=self._update_color)

    def _update_canvas(self, *_args) -> None:
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def _update_color(self, *_args) -> None:
        self._bg_instruction.rgba = self.bg_color


class ThemedBoxLayout(BoxLayout):
    """Box layout with an animatable background color."""

    bg_color = ListProperty([0.12, 0.15, 0.13, 0.94])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        with self.canvas.before:
            self._bg_instruction = Color(rgba=self.bg_color)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_canvas, size=self._update_canvas, bg_color=self._update_color)

    def _update_canvas(self, *_args) -> None:
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def _update_color(self, *_args) -> None:
        self._bg_instruction.rgba = self.bg_color


class ThemedButton(Button):
    """Button with custom background color and text wrapping."""

    bg_color = ListProperty([0.35, 0.65, 0.40, 1.0])
    text_rgba = ListProperty([0.08, 0.10, 0.08, 1.0])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.halign = "center"
        self.valign = "middle"
        with self.canvas.before:
            self._bg_instruction = Color(rgba=self.bg_color)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            bg_color=self._update_color,
            text_rgba=self._update_text_color,
        )
        self.bind(size=self._sync_text_size)
        self._sync_text_size()
        self._update_text_color()

    def _update_canvas(self, *_args) -> None:
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def _update_color(self, *_args) -> None:
        self._bg_instruction.rgba = self.bg_color

    def _update_text_color(self, *_args) -> None:
        self.color = self.text_rgba

    def _sync_text_size(self, *_args) -> None:
        self.text_size = (max(0, self.width - dp(12)), None)


class KivyConsole(io.TextIOBase):
    """Redirect stdout and stderr into the Kivy console widget."""

    def __init__(self, app: "ClaimAwaitsMobileApp") -> None:
        self.app = app

    def write(self, data: str) -> int:
        if data:
            self.app.append_output(data)
        return len(data)

    def flush(self) -> None:
        return None


class InputBridge:
    """Bridge blocking input() calls to the Kivy UI."""

    def __init__(self, app: "ClaimAwaitsMobileApp") -> None:
        self.app = app
        self.input_queue: "queue.Queue[str]" = queue.Queue()

    def submit(self, value: str) -> None:
        self.input_queue.put(value)

    def input(self, prompt: str = "") -> str:
        if prompt:
            self.app.set_prompt(prompt)
            self.app.append_output(prompt)
        value = self.input_queue.get()
        self.app.append_output(f"{value}\n")
        self.app.set_prompt("")
        return value


class ClaimAwaitsMobileApp(App):
    """Mobile-first wrapper around the existing text-RPG."""

    SOUND_SETTINGS = {
        "menu": {"file": "MainMenu_sound.mp3", "volume": 0.28, "loop": True},
        "travel": {"file": "Travel_sound.mp3", "volume": 0.36, "loop": True},
        "combat": {"file": "Combat_sound.mp3", "volume": 0.42, "loop": True},
    }
    FONT_PATTERNS = (
        "River Adventurer*.ttf",
        "River Adventurer*.otf",
        "river*.ttf",
        "river*.otf",
        "*.ttf",
        "*.otf",
    )
    TITLE_FALLBACK_FONT = None

    BIOME_THEMES = {
        "Grasslands": {
            "bg": [0.73, 0.85, 0.62, 1.0],
            "panel": [0.15, 0.24, 0.16, 0.94],
            "console": [0.08, 0.14, 0.09, 0.94],
            "input": [0.12, 0.19, 0.12, 0.98],
            "accent": [0.63, 0.88, 0.47, 1.0],
            "text": [0.94, 0.98, 0.93, 1.0],
            "button_text": [0.12, 0.16, 0.11, 1.0],
        },
        "Forest": {
            "bg": [0.18, 0.33, 0.22, 1.0],
            "panel": [0.07, 0.16, 0.10, 0.95],
            "console": [0.05, 0.11, 0.07, 0.95],
            "input": [0.08, 0.15, 0.10, 0.98],
            "accent": [0.38, 0.73, 0.44, 1.0],
            "text": [0.92, 0.97, 0.93, 1.0],
            "button_text": [0.08, 0.12, 0.08, 1.0],
        },
        "Mountains": {
            "bg": [0.40, 0.43, 0.47, 1.0],
            "panel": [0.15, 0.18, 0.22, 0.95],
            "console": [0.09, 0.11, 0.14, 0.95],
            "input": [0.13, 0.15, 0.19, 0.98],
            "accent": [0.74, 0.78, 0.82, 1.0],
            "text": [0.95, 0.97, 0.99, 1.0],
            "button_text": [0.11, 0.13, 0.16, 1.0],
        },
        "Desert": {
            "bg": [0.83, 0.73, 0.46, 1.0],
            "panel": [0.28, 0.22, 0.12, 0.95],
            "console": [0.18, 0.14, 0.07, 0.95],
            "input": [0.22, 0.17, 0.09, 0.98],
            "accent": [0.95, 0.83, 0.42, 1.0],
            "text": [0.99, 0.96, 0.90, 1.0],
            "button_text": [0.18, 0.13, 0.05, 1.0],
        },
        "Ice Plains": {
            "bg": [0.71, 0.82, 0.91, 1.0],
            "panel": [0.17, 0.24, 0.31, 0.95],
            "console": [0.10, 0.16, 0.22, 0.95],
            "input": [0.13, 0.20, 0.27, 0.98],
            "accent": [0.80, 0.92, 1.00, 1.0],
            "text": [0.95, 0.98, 1.00, 1.0],
            "button_text": [0.10, 0.16, 0.21, 1.0],
        },
        "Swamp": {
            "bg": [0.33, 0.41, 0.24, 1.0],
            "panel": [0.13, 0.16, 0.09, 0.95],
            "console": [0.08, 0.10, 0.06, 0.95],
            "input": [0.11, 0.14, 0.08, 0.98],
            "accent": [0.67, 0.78, 0.42, 1.0],
            "text": [0.94, 0.97, 0.90, 1.0],
            "button_text": [0.12, 0.15, 0.08, 1.0],
        },
        "Shadow Realm": {
            "bg": [0.17, 0.09, 0.22, 1.0],
            "panel": [0.08, 0.04, 0.11, 0.95],
            "console": [0.05, 0.03, 0.08, 0.96],
            "input": [0.08, 0.05, 0.12, 0.98],
            "accent": [0.74, 0.42, 0.98, 1.0],
            "text": [0.97, 0.92, 1.00, 1.0],
            "button_text": [0.11, 0.06, 0.15, 1.0],
        },
    }
    DEFAULT_BIOME = "Grasslands"

    def build(self) -> BoxLayout:
        self.title = "CLAIM: Awaits"
        Window.softinput_mode = "below_target"

        self._input_bridge = InputBridge(self)
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._original_input = builtins.input
        self._output_queue: "queue.Queue[tuple[int, str]]" = queue.Queue()
        self._pending_output = ""
        self._screen_buffer = ""
        self._reveal_event = None
        self._render_generation = 0
        self._loading_event = None
        self._loading_auto_hide = None
        self._loading_base_text = "Loading"
        self._loading_dots = 0
        self._loading_reason = ""
        self._last_scene_key = ""
        self.current_prompt = ""
        self.current_biome = self.DEFAULT_BIOME
        self.pending_travel_biome = None
        self.asset_dir = os.path.dirname(os.path.abspath(__file__))
        self.custom_font_name = self._detect_font_path()
        self.sounds: dict[str, object] = {}
        self.current_sound_key: str | None = None
        self.start_overlay_visible = True
        self.start_overlay_event = None
        self.app_icon_path = self._optional_asset_path("app_icon.png")
        self.splash_image_path = self._optional_asset_path("splash_screen.png")

        root = ThemedFloatLayout(bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["bg"])
        self.root_container = root

        main_panel = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8))
        root.add_widget(main_panel)

        self.top_bar = ThemedBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            padding=(dp(12), dp(8)),
            size_hint_y=None,
            height=dp(52),
            bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["panel"],
        )

        self.status_label = Label(text="Starting game...", size_hint_x=0.68, halign="left", valign="middle")
        self.status_label.bind(size=self._sync_label_text)
        self.top_bar.add_widget(self.status_label)

        self.biome_label = Label(text=self.DEFAULT_BIOME, size_hint_x=0.32, halign="right", valign="middle")
        self.biome_label.bind(size=self._sync_label_text)
        self.top_bar.add_widget(self.biome_label)
        main_panel.add_widget(self.top_bar)

        self.banner_card = ThemedBoxLayout(
            orientation="vertical",
            spacing=dp(4),
            padding=(dp(14), dp(12)),
            size_hint_y=None,
            height=dp(118),
            bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["panel"],
        )
        self.banner_header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(42),
            spacing=dp(10),
        )
        if self.app_icon_path:
            self.banner_icon = Image(
                source=self.app_icon_path,
                size_hint=(None, None),
                size=(dp(36), dp(36)),
                allow_stretch=True,
                keep_ratio=True,
            )
        else:
            self.banner_icon = Widget(size_hint=(None, None), size=(0, 0))
        self.banner_header.add_widget(self.banner_icon)
        self.banner_title = Label(text="CLAIM: Awaits", font_size="24sp", halign="left", valign="middle")
        self.banner_title.bind(size=self._sync_label_text)
        self.banner_header.add_widget(self.banner_title)
        self.banner_subtitle = Label(
            text="Biome header banners, cards, and smoother transitions now drive the mobile shell.",
            font_size="14sp",
            halign="left",
            valign="middle",
        )
        self.banner_subtitle.bind(size=self._sync_label_text)
        self.prompt_hint = Label(
            text="Tap a button or type a choice below.",
            font_size="13sp",
            halign="left",
            valign="middle",
        )
        self.prompt_hint.bind(size=self._sync_label_text)
        self.banner_card.add_widget(self.banner_header)
        self.banner_card.add_widget(self.banner_subtitle)
        self.banner_card.add_widget(self.prompt_hint)
        main_panel.add_widget(self.banner_card)

        self.travel_panel = ThemedBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=(dp(12), dp(12)),
            size_hint_y=None,
            height=0,
            opacity=0,
            disabled=True,
            bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["panel"],
        )
        self.travel_title = Label(text="Travel Routes", size_hint_y=None, height=dp(24), halign="left", valign="middle")
        self.travel_title.bind(size=self._sync_label_text)
        self.travel_panel.add_widget(self.travel_title)
        self.travel_scroll = ScrollView(do_scroll_x=False, bar_width=dp(4))
        self.travel_grid = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        self.travel_grid.bind(minimum_height=self.travel_grid.setter("height"))
        self.travel_scroll.add_widget(self.travel_grid)
        self.travel_panel.add_widget(self.travel_scroll)
        main_panel.add_widget(self.travel_panel)

        self.console_card = ThemedBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=(dp(10), dp(10)),
            bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["panel"],
        )
        console_header = Label(
            text="Adventure Feed",
            size_hint_y=None,
            height=dp(24),
            font_size="14sp",
            halign="left",
            valign="middle",
        )
        console_header.bind(size=self._sync_label_text)
        self.console_card.add_widget(console_header)

        self.console = TextInput(
            text="",
            readonly=True,
            multiline=True,
            size_hint=(1, 1),
            font_size="15sp",
            background_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["console"],
            foreground_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["text"],
            cursor_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["accent"],
        )
        self.console_card.add_widget(self.console)
        main_panel.add_widget(self.console_card)

        self.action_panel = ThemedBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=(dp(12), dp(12)),
            size_hint_y=None,
            height=dp(170),
            bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["panel"],
        )
        self.action_title = Label(text="Action Buttons", size_hint_y=None, height=dp(24), halign="left", valign="middle")
        self.action_title.bind(size=self._sync_label_text)
        self.action_panel.add_widget(self.action_title)
        self.action_scroll = ScrollView(do_scroll_x=False, bar_width=dp(4))
        self.action_grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=None)
        self.action_grid.bind(minimum_height=self.action_grid.setter("height"))
        self.action_scroll.add_widget(self.action_grid)
        self.action_panel.add_widget(self.action_scroll)
        main_panel.add_widget(self.action_panel)

        self.controls_bar = ThemedBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(58),
            spacing=dp(8),
            padding=(dp(8), dp(8)),
            bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["panel"],
        )
        self.input_box = TextInput(
            multiline=False,
            hint_text="Type your choice here, then tap Submit",
            background_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["input"],
            foreground_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["text"],
            cursor_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["accent"],
            hint_text_color=[0.88, 0.94, 0.88, 0.55],
        )
        self.input_box.bind(on_text_validate=lambda *_: self.submit_input())
        self.controls_bar.add_widget(self.input_box)

        self.submit_button = ThemedButton(text="Submit", size_hint_x=None, width=dp(120))
        self.submit_button.bind(on_release=lambda *_: self.submit_input())
        self.controls_bar.add_widget(self.submit_button)
        main_panel.add_widget(self.controls_bar)

        self.loading_overlay = ThemedFloatLayout(bg_color=[0.03, 0.04, 0.05, 0.70], opacity=0, disabled=True)
        root.add_widget(self.loading_overlay)

        loading_card = ThemedBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=(dp(18), dp(18)),
            size_hint=(0.82, None),
            height=dp(170),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["panel"],
        )
        self.loading_overlay.add_widget(loading_card)

        self.loading_label = Label(text="Loading", font_size="22sp", halign="center", valign="middle")
        self.loading_label.bind(size=self._sync_label_text)
        loading_card.add_widget(self.loading_label)

        self.loading_hint = Label(text="Preparing the next transition...", font_size="15sp", halign="center", valign="middle")
        self.loading_hint.bind(size=self._sync_label_text)
        loading_card.add_widget(self.loading_hint)

        self.loading_progress = Widget(size_hint_y=None, height=dp(4))
        with self.loading_progress.canvas.before:
            self._loading_progress_color = Color(rgba=self.BIOME_THEMES[self.DEFAULT_BIOME]["accent"])
            self._loading_progress_rect = Rectangle(pos=self.loading_progress.pos, size=self.loading_progress.size)
        self.loading_progress.bind(pos=self._sync_loading_bar, size=self._sync_loading_bar)
        loading_card.add_widget(self.loading_progress)

        self.start_overlay = ThemedFloatLayout(
            bg_color=[0.02, 0.03, 0.04, 0.96],
            opacity=1,
            disabled=False,
        )
        root.add_widget(self.start_overlay)

        start_card = ThemedBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=(dp(18), dp(18)),
            size_hint=(0.86, None),
            height=dp(380),
            pos_hint={"center_x": 0.5, "center_y": 0.53},
            bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["panel"],
        )
        self.start_overlay.add_widget(start_card)

        if self.splash_image_path:
            self.start_splash = Image(
                source=self.splash_image_path,
                size_hint=(1, None),
                height=dp(180),
                allow_stretch=True,
                keep_ratio=True,
            )
            start_card.add_widget(self.start_splash)

        branding_row = BoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(64),
        )
        if self.app_icon_path:
            self.start_icon = Image(
                source=self.app_icon_path,
                size_hint=(None, None),
                size=(dp(56), dp(56)),
                allow_stretch=True,
                keep_ratio=True,
            )
            branding_row.add_widget(self.start_icon)

        start_texts = BoxLayout(orientation="vertical", spacing=dp(4))
        self.start_title = Label(text="CLAIM: Awaits", font_size="28sp", halign="left", valign="middle")
        self.start_title.bind(size=self._sync_label_text)
        self.start_subtitle = Label(
            text="A polished mobile shell with themed biomes, cards, and scene-based audio.",
            font_size="14sp",
            halign="left",
            valign="middle",
        )
        self.start_subtitle.bind(size=self._sync_label_text)
        start_texts.add_widget(self.start_title)
        start_texts.add_widget(self.start_subtitle)
        branding_row.add_widget(start_texts)
        start_card.add_widget(branding_row)

        self.start_hint = Label(
            text="Loading your adventure...",
            font_size="14sp",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(32),
        )
        self.start_hint.bind(size=self._sync_label_text)
        start_card.add_widget(self.start_hint)

        self.start_button = ThemedButton(
            text="Enter Realm",
            size_hint=(1, None),
            height=dp(52),
            font_size="16sp",
        )
        self.start_button.bind(on_release=lambda *_: self.dismiss_start_overlay())
        start_card.add_widget(self.start_button)

        self._apply_custom_fonts()
        self._load_audio_assets()
        self.apply_biome_theme(self.DEFAULT_BIOME, animate=False)
        self._refresh_scene_ui()
        self.show_loading(
            "Opening CLAIM",
            "Preparing banners, route cards, and battle transitions...",
            self.DEFAULT_BIOME,
            reason="startup",
        )
        Clock.schedule_once(lambda *_: self.start_game(), 0)
        return root

    def _sync_label_text(self, instance: Label, _value: object = None) -> None:
        instance.text_size = instance.size

    def _sync_loading_bar(self, *_args) -> None:
        self._loading_progress_rect.pos = self.loading_progress.pos
        self._loading_progress_rect.size = self.loading_progress.size

    def _optional_asset_path(self, filename: str) -> str | None:
        """Return the packaged asset path when it exists."""
        candidate = os.path.join(self.asset_dir, filename)
        if os.path.isfile(candidate):
            return candidate
        return None

    def _detect_font_path(self) -> str | None:
        """Return the first available custom font path from the packaged assets."""
        for pattern in self.FONT_PATTERNS:
            for entry in sorted(os.listdir(self.asset_dir)):
                if not re.fullmatch(pattern.replace(".", r"\.").replace("*", ".*"), entry, flags=re.IGNORECASE):
                    continue
                candidate = os.path.join(self.asset_dir, entry)
                if os.path.isfile(candidate):
                    return candidate
        return None

    def _apply_font_to_widget(self, widget: object) -> None:
        """Apply the custom font to a widget when the actual font file exists."""
        if hasattr(widget, "font_name"):
            if self.custom_font_name:
                widget.font_name = self.custom_font_name
            elif self.TITLE_FALLBACK_FONT:
                widget.font_name = self.TITLE_FALLBACK_FONT

    def _apply_custom_fonts(self) -> None:
        """Use decorative font for branding and keep body text readable."""
        title_widgets = (
            self.banner_title,
            self.start_title,
            self.start_button,
            self.loading_label,
        )
        body_widgets = (
            self.status_label,
            self.biome_label,
            self.banner_subtitle,
            self.prompt_hint,
            self.travel_title,
            self.console,
            self.action_title,
            self.input_box,
            self.submit_button,
            self.loading_hint,
            self.start_subtitle,
            self.start_hint,
        )
        for widget in title_widgets:
            self._apply_font_to_widget(widget)
        if self.custom_font_name:
            for widget in body_widgets:
                if hasattr(widget, "font_name"):
                    widget.font_name = self.custom_font_name

    def _sound_volume(self, sound_key: str) -> float:
        """Return the tuned volume for a given scene soundtrack."""
        return float(self.SOUND_SETTINGS.get(sound_key, {}).get("volume", 0.35))

    def _load_audio_assets(self) -> None:
        """Load optional menu, travel, and combat sounds from packaged assets."""
        for sound_key, settings in self.SOUND_SETTINGS.items():
            filename = settings["file"]
            asset_path = os.path.join(self.asset_dir, filename)
            if not os.path.exists(asset_path):
                continue
            sound = SoundLoader.load(asset_path)
            if sound is None:
                continue
            try:
                sound.volume = self._sound_volume(sound_key)
                sound.loop = bool(settings.get("loop", True))
            except Exception:
                pass
            self.sounds[sound_key] = sound

    def _play_scene_sound(self, sound_key: str | None) -> None:
        """Switch background audio for the current major screen."""
        if sound_key == self.current_sound_key:
            return

        if self.current_sound_key and self.current_sound_key in self.sounds:
            try:
                self.sounds[self.current_sound_key].stop()
            except Exception:
                pass

        self.current_sound_key = sound_key
        if not sound_key or sound_key not in self.sounds:
            return

        try:
            self.sounds[sound_key].seek(0)
        except Exception:
            pass

        try:
            self.sounds[sound_key].play()
        except Exception:
            return

    def dismiss_start_overlay(self) -> None:
        """Hide the branded splash start screen once the app is ready."""
        if not self.start_overlay_visible:
            return
        self.start_overlay_visible = False
        if self.start_overlay_event is not None:
            self.start_overlay_event.cancel()
            self.start_overlay_event = None
        self.start_overlay.disabled = True
        Animation.cancel_all(self.start_overlay)
        Animation(opacity=0, d=0.35, t="out_quad").start(self.start_overlay)

    def start_game(self) -> None:
        """Patch console I/O and start the existing game on a worker thread."""
        self.configure_runtime()
        game_thread = threading.Thread(target=self.run_game, daemon=True)
        game_thread.start()

    def configure_runtime(self) -> None:
        """Redirect saves and console I/O for mobile execution."""
        save_system.SAVE_DIR = os.path.join(self.user_data_dir, "saves")
        os.makedirs(save_system.SAVE_DIR, exist_ok=True)

        console = KivyConsole(self)
        sys.stdout = console
        sys.stderr = console
        builtins.input = self._input_bridge.input
        claim_game.clear_screen = self.clear_output

    def run_game(self) -> None:
        """Run the original text game and capture any crash output."""
        try:
            self.set_status("Game running")
            claim_game.main()
            self.set_status("Game finished")
            self.append_output("\nGame session ended. Close the app or relaunch it to play again.\n")
        except Exception:
            self.set_status("Game crashed")
            self.append_output("\nA runtime error occurred:\n")
            self.append_output(traceback.format_exc())

    def submit_input(self, value: str | None = None) -> None:
        """Push the current input field value into the game's input queue."""
        submitted = self.input_box.text if value is None else value
        self.input_box.text = ""
        self._prepare_loading_for_input(submitted)

        if (
            self.pending_travel_biome
            and "Proceed?" in self.current_prompt
            and submitted.strip().lower() == "y"
        ):
            self.show_loading(
                f"Traveling to {self.pending_travel_biome}",
                f"Entering {self.pending_travel_biome}...",
                self.pending_travel_biome,
                reason="travel_confirmed",
            )

        if "Proceed?" in self.current_prompt and submitted.strip().lower() != "y":
            self.pending_travel_biome = None

        self._input_bridge.submit(submitted)

    def _prepare_loading_for_input(self, value: str) -> None:
        """Add light transitions for major app actions without blocking gameplay logic."""
        choice = value.strip().lower()
        screen_text = self._current_screen_text()
        biome = self.current_biome

        if not choice and "Press Enter to continue..." in self.current_prompt:
            self.show_loading(
                "Continuing adventure",
                "Turning the next page of the story...",
                biome,
                reason="continue",
                auto_hide_after=0.55,
            )
            return

        if "[MAIN MENU]" in screen_text and "Explore" in screen_text:
            menu_loading = {
                "1": ("Exploring biome", "Searching the area for events...", "explore"),
                "2": ("Encountering monsters", "Tracking movement in the biome...", "monster"),
                "3": ("Approaching boss", "The air grows heavier ahead...", "boss"),
                "4": ("Opening inventory", "Sorting gear and consumables...", "submenu"),
                "5": ("Opening skills", "Preparing combat techniques...", "submenu"),
                "6": ("Reviewing stats", "Gathering your latest battle record...", "submenu"),
                "7": ("Travel planning", "Drawing up routes and warnings...", "submenu"),
                "8": ("Opening shop", "Welcoming you to town services...", "submenu"),
                "9": ("Opening property panel", "Reviewing homes, farms, and taxes...", "submenu"),
                "10": ("Opening mission board", "Collecting fresh contracts...", "submenu"),
                "11": ("Saving journey", "Writing your progress to the archive...", "save"),
                "12": ("Leaving camp", "Preparing your farewell...", "submenu"),
            }
            if choice in menu_loading:
                title, hint, reason = menu_loading[choice]
                self.show_loading(title, hint, biome, reason=reason, auto_hide_after=0.75)
                return

        if "[1] New Game" in screen_text and "[2] Load Game" in screen_text:
            launch_loading = {
                "1": ("Forging new claimant", "Preparing class choices and a fresh save...", "startup"),
                "2": ("Opening save archives", "Searching existing heroes...", "startup"),
                "3": ("Opening delete menu", "Loading the archive ledger...", "startup"),
                "4": ("Closing game", "Ending the current session...", "startup"),
            }
            if choice in launch_loading:
                title, hint, reason = launch_loading[choice]
                self.show_loading(title, hint, biome, reason=reason, auto_hide_after=0.70)
                return

        if "[TRAVEL]" in screen_text and re.fullmatch(r"\d+", choice or " "):
            self.show_loading(
                "Checking route",
                "Comparing danger and rank recommendations...",
                biome,
                reason="travel_preview",
                auto_hide_after=0.80,
            )
            return

        if "(y/n)" in self.current_prompt.lower() and choice in {"y", "n"}:
            self.show_loading(
                "Applying choice",
                "Transitioning to the next game state...",
                biome,
                reason="choice",
                auto_hide_after=0.55,
            )

    def append_output(self, text: str) -> None:
        """Append text to the console from any thread."""
        self._output_queue.put((self._render_generation, text))
        Clock.schedule_once(self._consume_output_queue, 0)

    def _consume_output_queue(self, _dt: float) -> None:
        chunks = []
        while not self._output_queue.empty():
            generation, text = self._output_queue.get_nowait()
            if generation == self._render_generation:
                chunks.append(text)

        if not chunks:
            return

        text = "".join(chunks)
        self._handle_visual_triggers(text)
        self._screen_buffer += text
        self._pending_output += text
        self._refresh_scene_ui()

        if self._reveal_event is None:
            self._reveal_event = Clock.schedule_interval(self._reveal_text_tick, 1 / 60)

    def _reveal_text_tick(self, _dt: float) -> bool:
        if not self._pending_output:
            self._reveal_event = None
            return False

        if self._pending_output.startswith("\n"):
            chunk_size = 1
        elif len(self._pending_output) > 220:
            chunk_size = 18
        elif len(self._pending_output) > 100:
            chunk_size = 10
        else:
            chunk_size = 4

        chunk = self._pending_output[:chunk_size]
        self._pending_output = self._pending_output[chunk_size:]
        self.console.text += chunk
        self.console.cursor = (0, max(0, len(self.console.text.splitlines()) - 1))
        self.console.scroll_y = 0
        return True

    def _handle_visual_triggers(self, text: str) -> None:
        """React to important story transitions emitted by the text game."""
        travel_match = re.search(r"Traveling to ([A-Za-z ]+)\.\.\.", text)
        if travel_match:
            self.pending_travel_biome = travel_match.group(1).strip()

        arrived_match = re.search(r"Arrived at ([A-Za-z ]+)!", text)
        if arrived_match:
            biome_name = arrived_match.group(1).strip()
            self.pending_travel_biome = None
            self.apply_biome_theme(biome_name, animate=True)
            self.show_loading(
                f"Arrived at {biome_name}",
                "New biome banner, travel cards, and actions are ready.",
                biome_name,
                reason="arrival",
                auto_hide_after=0.95,
            )

        combat_match = re.search(r"COMBAT: ([^\n]+)", text)
        if combat_match:
            self.show_loading(
                f"Enemy spotted: {combat_match.group(1).strip()}",
                "Preparing combat actions and battle cards...",
                self.current_biome,
                reason="monster",
                auto_hide_after=0.85,
            )

        boss_match = re.search(r"BOSS FIGHT: ([^\n]+)", text)
        if boss_match:
            self.show_loading(
                f"Boss fight: {boss_match.group(1).strip()}",
                "Bracing for a major encounter...",
                self.current_biome,
                reason="boss",
                auto_hide_after=0.95,
            )

        location_matches = re.findall(r"Location: ([A-Za-z ]+)", text)
        if location_matches:
            self.apply_biome_theme(location_matches[-1].strip(), animate=True)

        if "Travel cancelled." in text or "You are already here!" in text:
            self.pending_travel_biome = None
            self.hide_loading()

    def clear_output(self, *_args: object, **_kwargs: object) -> None:
        """Clear the console when the game requests a screen refresh."""
        self._render_generation += 1
        self._pending_output = ""
        self._screen_buffer = ""
        if self._reveal_event is not None:
            self._reveal_event.cancel()
            self._reveal_event = None

        def _clear(_dt: float) -> None:
            self.console.text = ""
            self._animate_context_cards()
            self._refresh_scene_ui()

        Clock.schedule_once(_clear, 0)

    def set_prompt(self, prompt: str) -> None:
        """Show the current input prompt above the console."""
        self.current_prompt = prompt

        def _set(_dt: float) -> None:
            self.status_label.text = prompt or "Waiting for input"
            self.prompt_hint.text = prompt or "Tap a button or type a choice below."
            self._refresh_scene_ui()
            if prompt and self._loading_reason == "startup":
                self.hide_loading()

        Clock.schedule_once(_set, 0)

    def set_status(self, status: str) -> None:
        """Show a short status message."""

        def _set(_dt: float) -> None:
            self.status_label.text = status

        Clock.schedule_once(_set, 0)

    def apply_biome_theme(self, biome_name: str, animate: bool = True) -> None:
        """Apply color theme based on the active biome."""
        theme = self.BIOME_THEMES.get(biome_name, self.BIOME_THEMES[self.DEFAULT_BIOME])
        self.current_biome = biome_name

        self.biome_label.text = biome_name
        self.status_label.color = theme["text"]
        self.biome_label.color = theme["accent"]
        self.banner_title.color = theme["text"]
        self.banner_subtitle.color = theme["accent"]
        self.prompt_hint.color = [theme["text"][0], theme["text"][1], theme["text"][2], 0.88]
        self.travel_title.color = theme["accent"]
        self.action_title.color = theme["accent"]
        self.loading_label.color = theme["text"]
        self.loading_hint.color = theme["accent"]
        self.console.foreground_color = theme["text"]
        self.console.background_color = theme["console"]
        self.console.cursor_color = theme["accent"]
        self.input_box.foreground_color = theme["text"]
        self.input_box.background_color = theme["input"]
        self.input_box.cursor_color = theme["accent"]
        self.input_box.hint_text_color = [theme["text"][0], theme["text"][1], theme["text"][2], 0.55]
        self._loading_progress_color.rgba = theme["accent"]

        for widget in (self.top_bar, self.banner_card, self.console_card, self.action_panel, self.travel_panel, self.controls_bar):
            if animate:
                Animation.cancel_all(widget, "bg_color")
                Animation(bg_color=theme["panel"], d=0.28, t="out_quad").start(widget)
            else:
                widget.bg_color = theme["panel"]

        if animate:
            Animation.cancel_all(self.root_container, "bg_color")
            Animation(bg_color=theme["bg"], d=0.35, t="out_quad").start(self.root_container)
        else:
            self.root_container.bg_color = theme["bg"]

        self._apply_button_palette(self.submit_button, "submit")
        for widget in self.action_grid.children:
            if isinstance(widget, ThemedButton):
                self._apply_button_palette(widget, getattr(widget, "semantic_name", "default"))
        for widget in self.travel_grid.children:
            if isinstance(widget, ThemedButton):
                self._apply_button_palette(widget, "travel")

    def show_loading(
        self,
        title: str,
        hint: str,
        biome_name: str | None = None,
        *,
        reason: str,
        auto_hide_after: float | None = None,
    ) -> None:
        """Show a short fullscreen loading overlay."""
        self._loading_reason = reason
        self._loading_base_text = title
        self._loading_dots = 0
        self.loading_label.text = title
        self.loading_hint.text = hint
        self.loading_overlay.disabled = False
        self.loading_overlay.opacity = 0
        self.input_box.disabled = True
        self.submit_button.disabled = True

        if self._loading_auto_hide is not None:
            self._loading_auto_hide.cancel()
            self._loading_auto_hide = None

        if biome_name:
            theme = self.BIOME_THEMES.get(biome_name, self.BIOME_THEMES[self.DEFAULT_BIOME])
            self.loading_hint.color = theme["accent"]
            self._loading_progress_color.rgba = theme["accent"]

        Animation.cancel_all(self.loading_overlay)
        Animation(opacity=1, d=0.18, t="out_quad").start(self.loading_overlay)

        if self._loading_event is None:
            self._loading_event = Clock.schedule_interval(self._animate_loading_text, 0.35)

        if auto_hide_after is not None:
            self._loading_auto_hide = Clock.schedule_once(lambda *_: self.hide_loading(), auto_hide_after)

    def hide_loading(self) -> None:
        """Hide the loading overlay and restore input controls."""

        def _finish(*_args) -> None:
            self.loading_overlay.disabled = True
            self.input_box.disabled = False
            self.submit_button.disabled = False
            self.input_box.focus = True
            self._loading_reason = ""

        if self._loading_auto_hide is not None:
            self._loading_auto_hide.cancel()
            self._loading_auto_hide = None

        if self._loading_event is not None:
            self._loading_event.cancel()
            self._loading_event = None

        Animation.cancel_all(self.loading_overlay)
        anim = Animation(opacity=0, d=0.18, t="out_quad")
        anim.bind(on_complete=_finish)
        anim.start(self.loading_overlay)

    def _animate_loading_text(self, _dt: float) -> bool:
        self._loading_dots = (self._loading_dots + 1) % 4
        dots = "." * self._loading_dots
        self.loading_label.text = f"{self._loading_base_text}{dots}"
        return True

    def _refresh_scene_ui(self) -> None:
        """Refresh banners, travel cards, and action buttons from console text."""
        screen_text = self._current_screen_text()
        scene = self._derive_scene_info(screen_text, self.current_prompt)
        self._play_scene_sound(self._scene_sound_key(scene["key"]))

        self.banner_title.text = scene["title"]
        self.banner_subtitle.text = scene["subtitle"]
        if self.current_prompt:
            self.prompt_hint.text = self.current_prompt

        if scene["key"] != self._last_scene_key:
            self._last_scene_key = scene["key"]
            self._animate_context_cards()

        actions = self._extract_menu_options(screen_text, self.current_prompt)
        destinations = self._extract_travel_destinations(screen_text)
        if destinations and "Select destination" in self.current_prompt:
            actions = [action for action in actions if action["key"].lower() == "b"]

        self._render_action_buttons(actions)
        self._render_travel_destinations(destinations)

    def _derive_scene_info(self, screen_text: str, prompt: str) -> dict[str, str]:
        """Create banner title and subtitle from the current text screen."""
        if match := re.search(r"COMBAT: ([^\n]+)", screen_text):
            return {
                "key": f"combat:{match.group(1).strip()}",
                "title": f"{match.group(1).strip()}",
                "subtitle": "Combat banner active. Attack, skills, items, and escape buttons are color coded.",
            }

        if match := re.search(r"BOSS FIGHT: ([^\n]+)", screen_text):
            return {
                "key": f"boss:{match.group(1).strip()}",
                "title": f"{match.group(1).strip()}",
                "subtitle": "Boss encounter active. The battle card layout is primed for major actions.",
            }

        if "[TRAVEL]" in screen_text:
            return {
                "key": "travel",
                "title": f"{self.current_biome} Route Board",
                "subtitle": "A better travel screen is active below with destination cards and danger hints.",
            }

        if "[SHOP & INN]" in screen_text:
            return {
                "key": "shop",
                "title": "Shop and Inn",
                "subtitle": "Town services are grouped into card-style actions for faster touch navigation.",
            }

        if "[HOUSING & PROPERTY]" in screen_text:
            return {
                "key": "housing",
                "title": "Housing and Property",
                "subtitle": "Property management now appears under the mobile card panel with smoother transitions.",
            }

        if "[MISSIONS]" in screen_text:
            return {
                "key": "missions",
                "title": "Mission Board",
                "subtitle": "Contracts, rewards, and acceptance actions are now easier to tap and review.",
            }

        if "[SKILLS]" in screen_text:
            return {
                "key": "skills",
                "title": "Skillbook",
                "subtitle": "Class techniques and combat skills are framed by the active biome banner.",
            }

        if "[INVENTORY]" in screen_text:
            return {
                "key": "inventory",
                "title": "Inventory",
                "subtitle": "Equipment, consumables, and quick actions sit inside card style mobile panels.",
            }

        if "NEW GAME" in screen_text:
            return {
                "key": "new_game",
                "title": "Create a New Claimant",
                "subtitle": "Choose a name, pick a class, and begin the journey with guided action buttons.",
            }

        if "LOAD GAME" in screen_text:
            return {
                "key": "load_game",
                "title": "Load Save",
                "subtitle": "Continue a saved hero from the archive with one-tap selections.",
            }

        if "DELETE SAVE" in screen_text:
            return {
                "key": "delete_save",
                "title": "Delete Save",
                "subtitle": "Archive cleanup now uses clearer confirm actions and smoother feedback.",
            }

        if "[MAIN MENU]" in screen_text and "Explore" in screen_text:
            return {
                "key": f"game_menu:{self.current_biome}",
                "title": f"{self.current_biome} Command Deck",
                "subtitle": "Biome header banners, quick actions, and transitions are active for the main field menu.",
            }

        if "[1] New Game" in screen_text and "[2] Load Game" in screen_text:
            return {
                "key": "title_menu",
                "title": "CLAIM: Awaits",
                "subtitle": "Open the game, load a save, or start a new run with mobile-first transition screens.",
            }

        if match := re.search(r"Location: ([A-Za-z ]+)", screen_text):
            return {
                "key": f"location:{match.group(1).strip()}",
                "title": match.group(1).strip(),
                "subtitle": "The active biome theme updates this banner and the surrounding card panels.",
            }

        fallback = prompt or "Tap a button or type a choice below."
        return {
            "key": "default",
            "title": "CLAIM: Awaits",
            "subtitle": fallback,
        }

    def _extract_menu_options(self, screen_text: str, prompt: str) -> list[dict[str, str]]:
        """Create quick action buttons from bracketed menu text and prompts."""
        options: list[dict[str, str]] = []
        seen_keys: set[str] = set()

        if "Press Enter to continue..." in prompt:
            return [{"key": "", "label": "Continue", "semantic": "continue"}]

        if "(y/n)" in prompt.lower():
            return [
                {"key": "y", "label": "Yes", "semantic": "confirm"},
                {"key": "n", "label": "No", "semantic": "cancel"},
            ]

        for line in screen_text.splitlines():
            match = re.match(r"\s*\[([0-9]+|[A-Za-z])\]\s+(.+)", line)
            if not match:
                continue
            key, label = match.groups()
            key = key.strip()
            clean_label = label.replace("<- YOU ARE HERE", "").strip()
            if key.lower() in seen_keys:
                continue
            seen_keys.add(key.lower())
            options.append(
                {
                    "key": key,
                    "label": clean_label,
                    "semantic": self._semantic_name(clean_label),
                }
            )

        if "0 to cancel" in prompt and "0" not in seen_keys:
            options.append({"key": "0", "label": "Cancel", "semantic": "cancel"})

        return options[:12]

    def _extract_travel_destinations(self, screen_text: str) -> list[dict[str, str]]:
        """Build richer travel destination cards from the travel screen text."""
        if "[TRAVEL]" not in screen_text or "Available destinations:" not in screen_text:
            return []

        destinations: list[dict[str, str]] = []
        lines = screen_text.splitlines()
        for index, line in enumerate(lines):
            match = re.match(r"\s*\[(\d+)\]\s+(.+?)\s+\[([^\]]+)\](.*)", line)
            if not match:
                continue
            key, biome_name, danger, tail = match.groups()
            info_line = ""
            if index + 1 < len(lines):
                next_line = lines[index + 1].strip()
                if next_line.startswith("Rec. Level:"):
                    info_line = next_line
            card_text = f"{biome_name}\nDanger: {danger}"
            if info_line:
                card_text = f"{card_text}\n{info_line}"
            if "YOU ARE HERE" in tail:
                card_text = f"{card_text}\nCurrent location"
            destinations.append({"key": key, "label": card_text})

        return destinations

    def _render_action_buttons(self, actions: list[dict[str, str]]) -> None:
        """Render the current quick action grid."""
        self.action_grid.clear_widgets()
        self.action_grid.cols = 1 if len(actions) <= 1 else 2

        if not actions:
            placeholder = Label(
                text="No quick actions detected yet. The text input remains available below.",
                halign="center",
                valign="middle",
                size_hint_y=None,
                height=dp(62),
            )
            placeholder.bind(size=self._sync_label_text)
            placeholder.color = self.BIOME_THEMES[self.current_biome]["text"]
            self.action_grid.add_widget(placeholder)
            self.action_grid.height = dp(62)
            return

        row_count = (len(actions) + self.action_grid.cols - 1) // self.action_grid.cols
        self.action_grid.height = row_count * dp(62)
        for action in actions:
            button = self._make_action_button(
                action["label"],
                action["semantic"],
                lambda _instance, key=action["key"]: self.submit_input(key),
                height=dp(54),
            )
            self.action_grid.add_widget(button)

    def _render_travel_destinations(self, destinations: list[dict[str, str]]) -> None:
        """Render a dedicated travel card area when the travel screen is active."""
        self.travel_grid.clear_widgets()

        if not destinations:
            self.travel_panel.disabled = True
            Animation.cancel_all(self.travel_panel)
            self.travel_panel.height = 0
            self.travel_panel.opacity = 0
            return

        self.travel_panel.disabled = False
        visible_height = min(dp(300), dp(68) + len(destinations) * dp(88))
        self.travel_grid.height = len(destinations) * dp(84)

        for destination in destinations:
            button = self._make_action_button(
                destination["label"],
                "travel",
                lambda _instance, key=destination["key"]: self.submit_input(key),
                height=dp(76),
            )
            button.font_size = "13sp"
            self.travel_grid.add_widget(button)

        Animation.cancel_all(self.travel_panel)
        self.travel_panel.opacity = 0.0
        self.travel_panel.height = visible_height
        Animation(opacity=1, d=0.20, t="out_quad").start(self.travel_panel)

    def _make_action_button(self, text: str, semantic: str, callback, *, height: float) -> ThemedButton:
        """Create a themed action button."""
        button = ThemedButton(text=text, size_hint_y=None, height=height, font_size="14sp")
        self._apply_font_to_widget(button)
        button.semantic_name = semantic
        self._apply_button_palette(button, semantic)
        button.bind(on_release=callback)
        return button

    def _apply_button_palette(self, button: ThemedButton, semantic: str) -> None:
        """Apply semantic button colors while respecting the biome accent for defaults."""
        theme = self.BIOME_THEMES.get(self.current_biome, self.BIOME_THEMES[self.DEFAULT_BIOME])
        palette = {
            "attack": ([0.82, 0.27, 0.24, 1.0], [0.99, 0.97, 0.96, 1.0]),
            "skill": ([0.45, 0.34, 0.82, 1.0], [0.96, 0.94, 1.0, 1.0]),
            "inventory": ([0.22, 0.57, 0.69, 1.0], [0.93, 0.98, 1.0, 1.0]),
            "travel": ([0.21, 0.46, 0.80, 1.0], [0.95, 0.98, 1.0, 1.0]),
            "shop": ([0.86, 0.56, 0.18, 1.0], [0.15, 0.09, 0.04, 1.0]),
            "boss": ([0.56, 0.18, 0.26, 1.0], [0.99, 0.94, 0.95, 1.0]),
            "save": ([0.17, 0.61, 0.33, 1.0], [0.95, 0.98, 0.95, 1.0]),
            "confirm": ([0.20, 0.66, 0.38, 1.0], [0.96, 0.99, 0.96, 1.0]),
            "cancel": ([0.42, 0.45, 0.50, 1.0], [0.96, 0.97, 0.98, 1.0]),
            "continue": ([0.29, 0.61, 0.84, 1.0], [0.96, 0.98, 1.0, 1.0]),
            "submit": (theme["accent"], theme["button_text"]),
            "default": (theme["accent"], theme["button_text"]),
        }
        button.bg_color, button.text_rgba = palette.get(semantic, palette["default"])

    def _semantic_name(self, label: str) -> str:
        """Map action labels to semantic button styles."""
        label_lower = label.lower()
        if "attack" in label_lower:
            return "attack"
        if "skills" in label_lower or "skill" in label_lower:
            return "skill"
        if "inventory" in label_lower or "item" in label_lower or "equip" in label_lower:
            return "inventory"
        if "travel" in label_lower or "destination" in label_lower:
            return "travel"
        if "shop" in label_lower or "buy" in label_lower or "sell" in label_lower or "inn" in label_lower:
            return "shop"
        if "boss" in label_lower:
            return "boss"
        if "save" in label_lower:
            return "save"
        if "quit" in label_lower or "exit" in label_lower or "back" in label_lower:
            return "cancel"
        return "default"

    def _animate_context_cards(self) -> None:
        """Apply lightweight transitions whenever the visible screen changes."""
        for widget in (self.banner_card, self.console_card, self.action_panel):
            Animation.cancel_all(widget)
            widget.opacity = 0.86
            Animation(opacity=1, d=0.18, t="out_quad").start(widget)

    def _scene_sound_key(self, scene_key: str) -> str | None:
        """Map the current scene to one of the uploaded sound themes."""
        if scene_key.startswith("combat:") or scene_key.startswith("boss:"):
            return "combat"
        if scene_key == "travel":
            return "travel"
        if scene_key in {
            "title_menu",
            "new_game",
            "load_game",
            "delete_save",
            "shop",
            "housing",
            "missions",
            "skills",
            "inventory",
        } or scene_key.startswith("game_menu:"):
            return "menu"
        return self.current_sound_key

    def _current_screen_text(self) -> str:
        """Return the latest visible screen contents."""
        return f"{self._screen_buffer}{self._pending_output}"

    def on_stop(self) -> None:
        """Restore standard I/O when the app closes."""
        for sound in self.sounds.values():
            try:
                sound.stop()
            except Exception:
                pass
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr
        builtins.input = self._original_input


if __name__ == "__main__":
    ClaimAwaitsMobileApp().run()
