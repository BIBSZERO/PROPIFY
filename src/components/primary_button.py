import flet as ft
from typing import Optional # Bu satırı eklemeyi unutma!

class PrimaryButton(ft.ElevatedButton):
    def __init__(
        self, 
        text: str, 
        on_click, 
        icon: Optional[ft.IconData] = None # 'Optional' ekledik
    ):
        super().__init__()
        
        self.text = text
        self.icon = icon
        self.on_click = on_click
        
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            color=ft.Colors.WHITE,
            bgcolor={
                ft.ControlState.DEFAULT: ft.Colors.BLUE_700,
                ft.ControlState.HOVERED: ft.Colors.BLUE_900,
            },
        )
        self.width = 300
        self.height = 50