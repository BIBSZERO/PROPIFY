import flet as ft
from typing import Optional, Callable, Any # 🚀 Any buraya eklendi

class CustomTextField(ft.TextField):
    def __init__(
        self,
        label: str,
        icon: ft.IconData,
        is_password: bool = False,
        is_numeric: bool = False,
        hint_text: str = "",
        expand: bool = False,
        multiline: bool = False,
        value: str = "",
        read_only: bool = False,
        # 🚀 'any' yerine 'Any' (Büyük harf) yapıyoruz
        on_change: Any = None 
    ):
        super().__init__(
            label=label,
            value=value,
            read_only=read_only,
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
            on_change=on_change, # Buraya paslıyoruz
        )
        
        if is_numeric:
            self.keyboard_type = ft.KeyboardType.NUMBER
            self.input_filter = ft.NumbersOnlyInputFilter()