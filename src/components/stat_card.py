import flet as ft

class StatCard(ft.Container):
    def __init__(self, title, value, icon, color):
        super().__init__()
        self.expand = True
        self.bgcolor = ft.Colors.WHITE
        self.padding = 20
        self.border_radius = 15
        self.shadow = ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK_12)

        self.content = ft.Row([
            ft.Container(
                content=ft.Icon(icon, color=color, size=30),
                bgcolor=f"{color}10", # İkonun renginden çok açık bir arka plan
                padding=10,
                border_radius=10
            ),
            ft.Column([
                ft.Text(value, size=22, weight=ft.FontWeight.BOLD, color="#1A237E"),
                ft.Text(title, color=ft.Colors.GREEN_700,size=14)
            ], spacing=2, alignment=ft.MainAxisAlignment.CENTER)
        ], spacing=15)