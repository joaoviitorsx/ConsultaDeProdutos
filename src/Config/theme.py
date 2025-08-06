import flet as ft

_LIGHT_THEME = {
    "MODE": "light",
    "PRIMARY_COLOR": "#2563EB", 
    "PRIMARY_HOVER": "#1D4ED8",
    "BACKGROUND": "#F9FAFB",
    "CARD": "#F3F4F6",
    "CARD_DARK": "#2d2d2d",
    "BORDER": "#404040",
    "ON_PRIMARY": "#FFFFFF",
    "TEXT": "#1F2937",
    "TEXT_SECONDARY": "#6B7280",
    "ERROR": "#EF4444",
    "BACKGROUNDSCREEN": "#C2C2C2",
    "BLACK": "#000000",
    "INPUT_BG": "#FFFFFF",
    "HOVER": "#7A9FEE",
}

_DARK_THEME = {
    "MODE": "dark",
    "PRIMARY_COLOR": "#3B82F6",
    "PRIMARY_HOVER": "#2563EB",
    "BACKGROUND": "#111827",
    "CARD": "#1F2937",
    "CARD_DARK": "#2d2d2d",
    "BORDER": "#404040",
    "ON_PRIMARY": "#FFFFFF",
    "TEXT": "#F9FAFB",
    "TEXT_SECONDARY": "#9CA3AF",
    "ERROR": "#F87171",
    "BACKGROUNDSCREEN": "#151A27",
    "BLACK": "#FFFFFF",
    "INPUT_BG": "#23272F",
}

STYLE = {
    "CARD_RADIUS": 12,
    "CARD_ELEVATION": 8,
    "BORDER_RADIUS_INPUT": 8,
    "FONT_FAMILY": "Segoe UI"
}

__current_theme = _LIGHT_THEME

def set_theme(mode: str):
    global __current_theme
    if mode.lower() == "dark":
        __current_theme = _DARK_THEME
    else:
        __current_theme = _LIGHT_THEME

def get_theme() -> dict:
    return __current_theme

def apply_theme(page: ft.Page):
    th = get_theme()
    page.theme_mode = ft.ThemeMode.LIGHT if th["MODE"] == "light" else ft.ThemeMode.DARK
    page.bgcolor = th["BACKGROUNDSCREEN"]
    page.window_bgcolor = th["BACKGROUNDSCREEN"]
    return th
