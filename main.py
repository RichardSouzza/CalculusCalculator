from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.utils import platform
from Screens.CalculatorScreen.calculator import CalculatorScreen
from Screens.CalculatorScreen.components.key import Key


class CalculusCalculator(MDApp):
    def build(self):
        self.title = "Calculus Calculator"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "LightBlue"
        self.load_all_kv_files("Screens")
        if platform in ["win", "linux", "macosx"]:
            Window.size = (400, 600)
        return CalculatorScreen()


if __name__ == "__main__":
    CalculusCalculator().run()