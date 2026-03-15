import flet as ft

class CustomTextField(ft.TextField):
    def __init__(
        self,
        label: str,
        icon: ft.IconData,
        is_password: bool = False,
        is_numeric: bool = False,
        hint_text: str = "",
        expand: bool = False,
        multiline: bool = False
    ):
        super().__init__(
            label=label,
            hint_text=hint_text,
            prefix_icon=icon,
            password=is_password,
            can_reveal_password=is_password,
            border_radius=12,
            border_color=ft.Colors.BLUE_700,
            focused_border_color=ft.Colors.ORANGE_700,
            bgcolor=ft.Colors.WHITE,
            text_size=14,
            height=60 if not multiline else None,
            cursor_color=ft.Colors.BLUE_700,
            expand=expand,
            multiline=multiline,
        )
        
        # 🚀 Sayısal giriş (Fiyat, Aidat vb.) için geliştirme
        if is_numeric:
            self.keyboard_type = ft.KeyboardType.NUMBER
            self.input_filter = ft.NumbersOnlyInputFilter()