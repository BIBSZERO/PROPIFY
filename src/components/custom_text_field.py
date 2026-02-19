import flet as ft

class CustomTextField(ft.TextField):
    def __init__(
        self,
        label: str,
        icon: ft.IconData,
        is_password: bool = False,
        hint_text: str = ""
    ):
        super().__init__(
            label=label,
            hint_text=hint_text,
            prefix_icon=icon,
            password=is_password,
            border_radius=12,
            border_color=ft.Colors.BLUE_700,
            focused_border_color=ft.Colors.ORANGE_700,
            bgcolor=ft.Colors.WHITE,
            text_size=14,
            height=60,
            cursor_color=ft.Colors.BLUE_700,
        )