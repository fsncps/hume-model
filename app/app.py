# app/app.py
from textual.app import App
from .screen import SimScreen

class HumeSim(App):
    CSS_PATH = "main.css"
    BINDINGS = [("q", "quit", "Quit")]

    def on_mount(self) -> None:
        self.push_screen(SimScreen())

