import flet as ft

class SideBar(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.main_page = page
        self.width = 250
        self.bgcolor = "#1A237E"
        self.border_radius = ft.border_radius.only(top_right=30)
        self.padding = ft.padding.only(top=40)

        self.content = ft.Column([
            ft.Text(" PROPIFY", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            self.nav_item(ft.Icons.DASHBOARD, "Genel Bakış", True, on_click=lambda _: self.page.go("/dashboard")),
            self.nav_item(ft.Icons.HOME_WORK, "Portföyler", True, on_click=lambda _: self.page.go("/portfolio")),
            self.nav_item(ft.Icons.PERSON, "Mülk Sahipleri", False),
            ft.Container(expand=True),
            self.nav_item(ft.Icons.ADD_CIRCLE, "Yeni Mülk Sahibi Ekle", True, on_click=lambda _: self.page.go("/add-client")),
            self.nav_item(ft.Icons.ADD_CIRCLE, "Yeni İlan Ekle", True, on_click=lambda _: self.page.go("/add-property")),
            self.nav_item(ft.Icons.PERSON, "Profil", False),
            ft.Container(expand=True),
            self.nav_item(ft.Icons.LOGOUT, "Çıkış", False, on_click=lambda _: self.page.go("/")),
            ft.Container(height=20),
        ], spacing=10, expand=True)
    
    def nav_item(self, icon, text, selected=False, on_click=None):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=ft.Colors.WHITE if selected else ft.Colors.WHITE_70),
                ft.Text(text, color=ft.Colors.WHITE if selected else ft.Colors.WHITE_70, weight=ft.FontWeight.W_500), 
            ], spacing=15),
            padding=ft.padding.symmetric(15,25),
            bgcolor=ft.Colors.WHITE_10 if selected else None,
            on_click=on_click,
            border_radius=ft.border_radius.only(top_right=20,bottom_right=20)
        )