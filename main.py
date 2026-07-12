"""Kivy launcher for packaging CLAIM: Awaits as an Android APK."""

from __future__ import annotations

import builtins
import io
import os
import queue
import re
import sys
import threading
import traceback

from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.uix.textinput import TextInput

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


class KivyConsole(io.TextIOBase):
    """Redirect stdout/stderr into the Kivy console widget."""

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
    """Minimal mobile wrapper around the existing text-RPG."""

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
        self._reveal_event = None
        self._render_generation = 0
        self.current_prompt = ""
        self.current_biome = self.DEFAULT_BIOME
        self.pending_travel_biome = None
        self._loading_base_text = "Loading"
        self._loading_dots = 0
        self._loading_event = None

        root = ThemedFloatLayout(bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["bg"])
        self.root_container = root

        main_panel = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8))
        root.add_widget(main_panel)

        self.top_bar = ThemedBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            padding=(dp(12), dp(8)),
            size_hint_y=None,
            height=dp(54),
            bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["panel"],
        )

        self.status_label = Label(
            text="Starting game...",
            size_hint_x=0.68,
            halign="left",
            valign="middle",
        )
        self.status_label.bind(size=self._sync_label_text)
        self.top_bar.add_widget(self.status_label)

        self.biome_label = Label(
            text=self.DEFAULT_BIOME,
            size_hint_x=0.32,
            halign="right",
            valign="middle",
        )
        self.biome_label.bind(size=self._sync_label_text)
        self.top_bar.add_widget(self.biome_label)
        main_panel.add_widget(self.top_bar)

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
        main_panel.add_widget(self.console)

        self.controls_bar = ThemedBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(56),
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

        self.submit_button = Button(
            text="Submit",
            size_hint_x=None,
            width=dp(112),
            background_normal="",
            background_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["accent"],
            color=self.BIOME_THEMES[self.DEFAULT_BIOME]["button_text"],
        )
        self.submit_button.bind(on_release=lambda *_: self.submit_input())
        self.controls_bar.add_widget(self.submit_button)
        main_panel.add_widget(self.controls_bar)

        self.loading_overlay = ThemedFloatLayout(
            bg_color=[0.03, 0.04, 0.05, 0.68],
            opacity=0,
            disabled=True,
        )
        root.add_widget(self.loading_overlay)

        loading_card = ThemedBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=(dp(18), dp(18)),
            size_hint=(0.78, None),
            height=dp(150),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            bg_color=self.BIOME_THEMES[self.DEFAULT_BIOME]["panel"],
        )
        self.loading_overlay.add_widget(loading_card)

        self.loading_label = Label(
            text="Loading",
            font_size="22sp",
            halign="center",
            valign="middle",
        )
        self.loading_label.bind(size=self._sync_label_text)
        loading_card.add_widget(self.loading_label)

        self.loading_hint = Label(
            text="Preparing the next biome...",
            font_size="15sp",
            halign="center",
            valign="middle",
        )
        self.loading_hint.bind(size=self._sync_label_text)
        loading_card.add_widget(self.loading_hint)

        self.loading_progress = Widget(size_hint_y=None, height=dp(4))
        with self.loading_progress.canvas.before:
            self._loading_progress_color = Color(rgba=self.BIOME_THEMES[self.DEFAULT_BIOME]["accent"])
            self._loading_progress_rect = Rectangle(pos=self.loading_progress.pos, size=self.loading_progress.size)
        self.loading_progress.bind(pos=self._sync_loading_bar, size=self._sync_loading_bar)
        loading_card.add_widget(self.loading_progress)

        self.apply_biome_theme(self.DEFAULT_BIOME, animate=False)

        Clock.schedule_once(lambda *_: self.start_game(), 0)
        return root

    def _sync_label_text(self, instance: Label, _value: object) -> None:
        instance.text_size = instance.size

    def _sync_loading_bar(self, *_args) -> None:
        self._loading_progress_rect.pos = self.loading_progress.pos
        self._loading_progress_rect.size = self.loading_progress.size

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

    def submit_input(self) -> None:
        """Push the current input field value into the game's input queue."""
        value = self.input_box.text
        self.input_box.text = ""

        if (
            self.pending_travel_biome
            and "Proceed?" in self.current_prompt
            and value.strip().lower() == "y"
        ):
            self.show_loading(
                f"Traveling to {self.pending_travel_biome}",
                f"Entering {self.pending_travel_biome}...",
                self.pending_travel_biome,
            )

        if "Proceed?" in self.current_prompt and value.strip().lower() != "y":
            self.pending_travel_biome = None

        self._input_bridge.submit(value)

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
        self._pending_output += text

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
        travel_match = re.search(r"Traveling to ([A-Za-z ]+)\.\.\.", text)
        if travel_match:
            self.pending_travel_biome = travel_match.group(1).strip()

        arrived_match = re.search(r"Arrived at ([A-Za-z ]+)!", text)
        if arrived_match:
            biome_name = arrived_match.group(1).strip()
            self.pending_travel_biome = None
            self.apply_biome_theme(biome_name, animate=True)
            self.show_loading(f"Arrived at {biome_name}", "New biome discovered.", biome_name)
            Clock.schedule_once(lambda *_: self.hide_loading(), 0.9)

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
        if self._reveal_event is not None:
            self._reveal_event.cancel()
            self._reveal_event = None

        def _clear(_dt: float) -> None:
            self.console.text = ""

        Clock.schedule_once(_clear, 0)

    def set_prompt(self, prompt: str) -> None:
        """Show the current input prompt above the console."""
        self.current_prompt = prompt

        def _set(_dt: float) -> None:
            self.status_label.text = prompt or "Waiting for input"

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
        self.loading_label.color = theme["text"]
        self.loading_hint.color = theme["accent"]
        self.console.foreground_color = theme["text"]
        self.console.background_color = theme["console"]
        self.console.cursor_color = theme["accent"]
        self.input_box.foreground_color = theme["text"]
        self.input_box.background_color = theme["input"]
        self.input_box.cursor_color = theme["accent"]
        self.input_box.hint_text_color = [theme["text"][0], theme["text"][1], theme["text"][2], 0.55]
        self.submit_button.background_color = theme["accent"]
        self.submit_button.color = theme["button_text"]
        self._loading_progress_color.rgba = theme["accent"]

        if animate:
            Animation.cancel_all(self.root_container, "bg_color")
            Animation.cancel_all(self.top_bar, "bg_color")
            Animation.cancel_all(self.controls_bar, "bg_color")
            Animation(bg_color=theme["bg"], d=0.35, t="out_quad").start(self.root_container)
            Animation(bg_color=theme["panel"], d=0.30, t="out_quad").start(self.top_bar)
            Animation(bg_color=theme["panel"], d=0.30, t="out_quad").start(self.controls_bar)
        else:
            self.root_container.bg_color = theme["bg"]
            self.top_bar.bg_color = theme["panel"]
            self.controls_bar.bg_color = theme["panel"]

    def show_loading(self, title: str, hint: str, biome_name: str | None = None) -> None:
        """Show a short fullscreen loading overlay."""
        self._loading_base_text = title
        self._loading_dots = 0
        self.loading_label.text = title
        self.loading_hint.text = hint
        self.loading_overlay.disabled = False
        self.loading_overlay.opacity = 0
        self.input_box.disabled = True
        self.submit_button.disabled = True

        if biome_name:
            theme = self.BIOME_THEMES.get(biome_name, self.BIOME_THEMES[self.DEFAULT_BIOME])
            self.loading_hint.color = theme["accent"]
            self._loading_progress_color.rgba = theme["accent"]

        Animation.cancel_all(self.loading_overlay)
        Animation(opacity=1, d=0.22, t="out_quad").start(self.loading_overlay)

        if self._loading_event is None:
            self._loading_event = Clock.schedule_interval(self._animate_loading_text, 0.35)

    def hide_loading(self) -> None:
        """Hide the loading overlay and restore input controls."""

        def _finish(*_args) -> None:
            self.loading_overlay.disabled = True
            self.input_box.disabled = False
            self.submit_button.disabled = False
            self.input_box.focus = True

        if self._loading_event is not None:
            self._loading_event.cancel()
            self._loading_event = None

        Animation.cancel_all(self.loading_overlay)
        anim = Animation(opacity=0, d=0.20, t="out_quad")
        anim.bind(on_complete=_finish)
        anim.start(self.loading_overlay)

    def _animate_loading_text(self, _dt: float) -> bool:
        self._loading_dots = (self._loading_dots + 1) % 4
        dots = "." * self._loading_dots
        self.loading_label.text = f"{self._loading_base_text}{dots}"
        return True

    def on_stop(self) -> None:
        """Restore standard I/O when the app closes."""
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr
        builtins.input = self._original_input


if __name__ == "__main__":
    ClaimAwaitsMobileApp().run()
