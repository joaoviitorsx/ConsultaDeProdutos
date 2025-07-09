light_theme = {
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
}

dark_theme = {
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
}

current_theme = light_theme

def set_theme(mode: str):
    global current_theme
    current_theme = dark_theme if mode == "dark" else light_theme

CARD_RADIUS = 12
CARD_ELEVATION = 8
FONT_FAMILY = "Segoe UI"
BORDER_RADIUS_INPUT = 8
