import flet as ft
from src.components.sidebar import SideBar
from src.components.top_bar import TopBar
from src.components.stat_card import StatCard
from src.components.property_card import PropertyCard
from src.services.property_service import PropertyService

class DashboardView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/dashboard",
            bgcolor="#F4F7F9", # Ferah arka plan
            padding=0
        )
        self.main_page = page

        # VERİLERİ SERVİSTEN ÇEK
        self.properties = PropertyService.get_all()

        # Sidebar
        self.sidebar = SideBar(self.main_page)

        # İlan Gridi (İlanları yan yana dizer)
        self.property_grid = ft.Row(
            wrap=True,
            spacing=25,
            run_spacing=25,
            controls=[PropertyCard(p) for p in self.properties] if self.properties else[]
        )

        # Ana Sütun (Header + Stats + Grid)
        self.content_column = ft.Column([
            TopBar(self.main_page), # Dinamik isim çeken birleşen

            # İstatistikler
            ft.Container(
                content=ft.Row([
                    StatCard("Aktif Portföy", str(len(self.properties)), ft.Icons.HOME_ROUNDED, ft.Colors.BLUE),
                    StatCard("Görüntülenme", "1.2K", ft.Icons.AUTO_GRAPH, ft.Colors.GREEN),
                    StatCard("Talepler", "5", ft.Icons.CHAT_BUBBLE_OUTLINE, ft.Colors.ORANGE),
                ], spacing=20),
                padding=20
            ),

            #İlan Vitrini
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Son İlanlar", size=22, weight=ft.FontWeight.BOLD, color="#1A237E"),
                        ft.TextButton("Tümünü Gör", icon=ft.Icons.ARROW_FORWARD, on_click=lambda _: self.main_page.go("/all-properties")),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=10, color="transparent"),

                    # Sadece son 4 ilanı (en yeni eklenenleri) gösteren Row
                    ft.Row([
                        ft.Column([
                            ft.Row(
                                wrap=True,
                                spacing=25,
                                run_spacing=25,
                                # properties listesinin son 4 elemanını ters çevirerek alır
                                controls=[PropertyCard(p) for p in self.properties[:-5:-1]] if self.properties else [self.build_empty_state()]
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
                    ], alignment=ft.MainAxisAlignment.CENTER),     
                ]),
                padding=20,
                expand=True
            )
        ], expand=True, scroll=ft.ScrollMode.ADAPTIVE)

        self.controls = [
            ft.Row([
                self.sidebar,
                self.content_column
            ], expand=True, spacing=0)
        ]
    def build_empty_state(self):
        """İlan bulunmadığında gösterilecek alan"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ADD_BUSINESS_OUTLINED, size=60, color=ft.Colors.GREY_400),
                ft.Text("Henüz bir portföy eklenmemiş.", color=ft.Colors.GREY_600, size=16),
                ft.ElevatedButton(
                    "İlk İlanı Hemen Ekle",
                    icon=ft.Icons.ADD,
                    on_click=lambda _: self.main_page.go("/add-property"),
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor="#1A237E")
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=100,
            alignment=ft.Alignment.CENTER
        )