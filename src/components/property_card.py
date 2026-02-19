import flet as ft
from typing import Optional
from src.utils.formatters import Formatters

class PropertyCard(ft.Container):
    def __init__(self, title: str, price: float, location: str, image_url: Optional[str] = None):
        super().__init__(
            content=ft.Column([
                ft.Image(
                    src=image_url if image_url else "no_image.png",
                    width=250, height=150, fit=ft.BoxFit.COVER, border_radius=10
                ),
                ft.Text(title, weight=ft.FontWeight.BOLD, size=16, no_wrap=True),
                ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON, size=14, color=ft.Colors.GREY_600),
                    ft.Text(location, size=12, color=ft.Colors.GREY_600),
                ]),
                ft.Text(
                    Formatters.format_money(price),
                    color=ft.Colors.BLUE_700,
                    weight=ft.FontWeight.BOLD,
                    size=18
                )
            ]),
            padding=15,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
            ),
            width=200
        )