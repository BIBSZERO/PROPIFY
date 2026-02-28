import flet as ft
from src.components.sidebar import SideBar
from src.components.top_bar import TopBar
from src.components.stat_card import StatCard

class DashboardView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/dashboard",
            bgcolor="#F4F7F9", # Ferah arka plan
            padding=0
        )
        self.main_page = page

        # 1. SOL MENÜ (Sidebar - Bileşenimiz)
        self.sidebar = SideBar(self.main_page)

        # 2. ANA İÇERİK ALANI (Header + Stats + Grid)
        self.content_column = ft.Column([
            # Üst Bar (Bileşenimiz)
            TopBar(self.main_page),
            
            # İstatistik Kartları (Bileşenlerimiz)
            ft.Container(
                content=ft.Row([
                    StatCard("Aktif Portföy", "12", ft.Icons.HOME_ROUNDED, ft.Colors.BLUE),
                    StatCard("Görüntülenme", "1.2K", ft.Icons.AUTO_GRAPH, ft.Colors.GREEN),
                    StatCard("Yeni Talepler", "5", ft.Icons.CHAT_BUBBLE_OUTLINE, ft.Colors.ORANGE),
                ], spacing=20),
                padding=ft.padding.only(left=20, right=20, bottom=10)
            ),

            # İlan Vitrini Alanı
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Son İlanlar", size=20, weight=ft.FontWeight.BOLD, color="#1A237E"),
                        ft.TextButton("Tümünü Gör", icon=ft.Icons.ARROW_FORWARD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                    # 🕵️ BURASI ÖNEMLİ: İlanlar eklendikçe burası dolacak. 
                    # Şimdilik Saatçiler Konağı için bir yer tutucu (placeholder) koyuyoruz.
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.ADD_BUSINESS_OUTLINED, size=50, color=ft.Colors.GREY_400),
                            ft.Text("Henüz ilan eklenmedi.", color=ft.Colors.GREY_600),
                            ft.ElevatedButton(
                                "İlk İlanı Oluştur", 
                                icon=ft.Icons.ADD,
                                on_click=lambda _: print("İlan ekleme sayfasına git")
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=50,
                        alignment=ft.Alignment.CENTER,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=15,
                        width=1000 # Genişliği ayarla
                    )
                ]),
                padding=20,
                expand=True
            )
        ], expand=True, spacing=0, scroll=ft.ScrollMode.ADAPTIVE)

        # 🛠️ Dashboard Kompozisyonu
        self.controls = [
            ft.Row([
                self.sidebar,        # Sol Menü
                self.content_column  # Sağ İçerik
            ], expand=True, spacing=0)
        ]