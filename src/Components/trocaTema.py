import flet as ft
from flet import Animation, AnimationCurve
from src.Config import theme

def ThemeToggle(page: ft.Page, on_theme_changed=None):
    def is_dark():
        return page.theme_mode == ft.ThemeMode.DARK

    current_mode = is_dark()

    sun_icon = ft.Container(
        width=20,
        height=20,
        content=ft.Icon(
            name="wb_sunny",
            color="#FFF8E1",
            size=16
        ),
        bgcolor="#FFB300",
        border_radius=50,
        opacity=0.0 if current_mode else 1.0,
        scale=ft.Scale(0.5 if current_mode else 1.0),
        animate_opacity=Animation(400, AnimationCurve.EASE_IN_OUT),
        animate_scale=Animation(400, AnimationCurve.EASE_OUT_BACK),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color="#FFB30040",
            offset=ft.Offset(0, 2)
        )
    )

    moon_icon = ft.Container(
        width=20,
        height=20,
        content=ft.Icon(
            name="nightlight_round",
            color="#E8EAF6",
            size=14
        ),
        bgcolor="#3F51B5",
        border_radius=50,
        opacity=1.0 if current_mode else 0.0,
        scale=ft.Scale(1.0 if current_mode else 0.5),
        animate_opacity=Animation(400, AnimationCurve.EASE_IN_OUT),
        animate_scale=Animation(400, AnimationCurve.EASE_OUT_BACK),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color="#3F51B540",
            offset=ft.Offset(0, 2)
        )
    )

    track = ft.Container(
        width=54,
        height=28,
        bgcolor=theme.current_theme["CARD"],
        border_radius=28,
        border=ft.border.all(
            width=2,
            color="#FFB300" if not current_mode else "#3F51B5"
        ),
        animate=Animation(400, AnimationCurve.EASE_IN_OUT),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=12,
            color="#00000015",
            offset=ft.Offset(0, 4)
        )
    )

    slider_icon = ft.Container(
        width=24,
        height=24,
        left=2 if not current_mode else 28,
        top=2,
        content=ft.Stack([
            sun_icon,
            moon_icon
        ]),
        animate_position=Animation(500, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
    )

    glow_effect = ft.Container(
        width=54,
        height=28,
        bgcolor=f"{'#FFB30015' if not current_mode else '#3F51B515'}",
        border_radius=28,
        animate=Animation(400, AnimationCurve.EASE_IN_OUT),
    )

    toggle_stack = ft.Stack([
        glow_effect,
        track,
        slider_icon
    ])

    toggle_container = ft.Container(
        width=58,
        height=32,
        content=toggle_stack,
        padding=2,
        border_radius=32,
        bgcolor="transparent",
        animate=Animation(300, AnimationCurve.EASE_IN_OUT),
        tooltip="Alternar tema",
        ink=True,  # Efeito ripple
        on_hover=lambda e: on_hover(e),
    )

    def on_hover(e):
        if e.data == "true":
            toggle_container.scale = 1.05
            track.shadow = ft.BoxShadow(
                spread_radius=2,
                blur_radius=16,
                color="#00000025",
                offset=ft.Offset(0, 6)
            )
        else:
            # Mouse leave
            toggle_container.scale = 1.0
            track.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color="#00000015",
                offset=ft.Offset(0, 4)
            )
        page.update()

    def alternar_tema(e):
        novo_modo = "light" if is_dark() else "dark"
        theme.set_theme(novo_modo)
        page.theme_mode = ft.ThemeMode.LIGHT if novo_modo == "light" else ft.ThemeMode.DARK

        is_dark_mode = is_dark()

        track.bgcolor = theme.current_theme["CARD"]
        track.border = ft.border.all(
            width=2,
            color="#3F51B5" if is_dark_mode else "#FFB300"
        )

        glow_effect.bgcolor = f"{'#3F51B515' if is_dark_mode else '#FFB30015'}"

        slider_icon.left = 28 if is_dark_mode else 2

        sun_icon.opacity = 0.0 if is_dark_mode else 1.0
        sun_icon.scale = 0.8 if is_dark_mode else 1.0

        moon_icon.opacity = 1.0 if is_dark_mode else 0.0
        moon_icon.scale = 1.0 if is_dark_mode else 0.8

        def bounce():
            import time
            time.sleep(0.1)
            toggle_container.scale = 1.1
            page.update()
            time.sleep(0.1)
            toggle_container.scale = 1.0
            page.update()

        import threading
        threading.Thread(target=bounce).start()

        if on_theme_changed:
            on_theme_changed(novo_modo)

        page.update()

    toggle_container.on_click = alternar_tema
    return toggle_container