import flet as ft
from src.core.database import db

class TopBar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.padding = 20

        user_display_name = self.get_user_display_name()

        self.content = ft.Row([
            ft.Column([
                ft.Text(f"Merhaba, {user_display_name} 👋", size=22, weight=ft.FontWeight.BOLD, color="#1A237E"),
                ft.Text("Propify Emlak Yönetim Paneli", size=14, color=ft.Colors.GREY_700),
            ], spacing=2),
            ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SEARCH, color=ft.Colors.GREY_500, size=20),
                        ft.Text("İlanlarda ara...", color=ft.Colors.GREY_500, size=14),
                    ]),
                    padding=ft.padding.symmetric(horizontal=15, vertical=8),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    width=250
                ),
                ft.IconButton(ft.Icons.NOTIFICATIONS_NONE_ROUNDED, icon_color="#1A237E"),
                ft.CircleAvatar(
                    content=ft.Text(user_display_name[0].upper()),
                    bgcolor=ft.Colors.ORANGE,
                    color=ft.Colors.WHITE
                )
            ], spacing=15)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def get_user_display_name(self):
        try:
            session = db.client.auth.get_session()
            if session:
                user = session.user
                full_name = user.user_metadata.get("full_name")
                if full_name:
                    return full_name
                return user.email.split("@")[0].capitalize()
            return "Kullanıcı"
    
        except Exception as e:
            print(f"User info error: {e}")
            return "Misafir"