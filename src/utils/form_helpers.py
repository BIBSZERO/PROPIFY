import flet as ft
from typing import Optional

class FormHelpers:
    """
    PROPIFY Form Bileşenleri Fabrikası.
    Tüm giriş alanlarının (input) aynı stilde olmasını sağlar.
    """
    @staticmethod
    def create_text_field(
        label: str,
        hint: str,
        icon: Optional[ft.IconData] = None,
        is_number: bool = False,
        multiline: bool = False
    ) -> ft.TextField:
        """Standart bir TextField döndürür."""
        return ft.TextField(
            label=label,
            hint_text=hint,
            prefix_icon=icon,
            border_color="#1A237E",
            border_radius=10,
            focused_bgcolor="#3F51B5",
            expand=True,
            multiline=multiline,
            min_lines=3 if multiline else 1,
            keyboard_type=ft.KeyboardType.NUMBER if is_number else ft.KeyboardType.TEXT
        )
    
    @staticmethod
    def create_dropdown(label: str, options:list[str], value: Optional[str] = None) -> ft.Dropdown:
        """Standart bir Dropdown (Açılır Menü) döndürür."""
        return ft.Dropdown(
            label=label,
            options=[ft.dropdown.Option(opt) for opt in options],
            value=value if value else (options[0] if options else None),
            border_color="#1A237E",
            border_radius=10,
            expand=True,
            focused_border_color="#3F51B5"
        )
    
    @staticmethod
    def section_title(text:str) -> ft.Text:
        """Form içindeki alt başlıklar için stilize metin."""
        return ft.Text(
            value=text,
            size=18,
            weight=ft.FontWeight.BOLD,
            color="#1A237E",
            margin=ft.margin.only(top=10)
        )