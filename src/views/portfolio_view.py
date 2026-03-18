import flet as ft
from src.components.sidebar import SideBar
from src.components.top_bar import TopBar
from src.components.property_list_item import PropertyListItem
from src.services.property_service import property_service # Küçük harf örneği kullanıyorsan buna dikkat
from src.utils.ui_helpers import UIHelpers

class PortfolioView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/portfolio",
            bgcolor="#F4F7F9",
            padding=0
        )
        self.main_page = page
        
        # 1. Verileri Çek
        try:
            # Sayfa her açıldığında verileri tazeleyelim
            self.all_properties = property_service.get_all()
        except Exception as e:
            print(f"🚀 Veri çekme hatası: {e}")
            self.all_properties = []

        # 2. Bileşenleri Başlat
        self.sidebar = SideBar(self.main_page)
        
        # 🔍 Arama Çubuğu
        self.search_field = ft.TextField(
            hint_text="İlan başlığına göre hızlı ara...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border_color="#E0E0E0",
            focused_border_color="#1A237E",
            on_change=self.filter_properties,
            expand=True
        )

        # 🏗️ Liste Sütunu
        self.property_list_column = ft.Column(
            controls=self.build_property_list(self.all_properties),
            spacing=10,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True
        )

        # 3. Sayfa Düzeni (Layout)
        self.content_column = ft.Column([
            TopBar(self.main_page),
            
            ft.Container(
                content=ft.Column([
                    # Başlık Bölümü
                    ft.Row([
                        ft.Column([
                            ft.Text("Mülk Portföyü", size=28, weight=ft.FontWeight.BOLD, color="#1A237E"),
                            ft.Text(f"Toplam {len(self.all_properties)} ilan kayıtlı", color=ft.Colors.GREY_600),
                        ]),
                        ft.ElevatedButton(
                            "Yeni İlan Ekle",
                            icon=ft.Icons.ADD,
                            style=ft.ButtonStyle(
                                color=ft.Colors.WHITE,
                                bgcolor="#1A237E",
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                            on_click=lambda _: self.main_page.go("/add-property")
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                    ft.Divider(height=30, color="transparent"),
                    
                    # Arama Satırı
                    ft.Row([
                        self.search_field,
                        ft.Container(
                            content=ft.IconButton(ft.Icons.TUNE, icon_color="#1A237E"),
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            border=ft.border.all(1, "#E0E0E0")
                        )
                    ], spacing=15),
                    
                    ft.Divider(height=20, color="transparent"),

                    # Liste Alanı
                    ft.Container(
                        content=self.property_list_column,
                        expand=True
                    )
                ]),
                padding=30,
                expand=True
            )
        ], expand=True)

        self.controls = [
            ft.Row([
                self.sidebar,
                self.content_column
            ], expand=True, spacing=0)
        ]

    def build_property_list(self, properties):
        """Mülk listesini oluşturur veya boş durum döner"""
        if not properties:
            return [self.build_empty_state()]
        
        return [PropertyListItem(p, self.on_property_click) for p in properties]

    def filter_properties(self, e):
        """Arama kutusuna yazıldığında listeyi anında günceller"""
        search_term = self.search_field.value.lower().strip()
        
        filtered_list = [
            p for p in self.all_properties 
            if search_term in p.title.lower()
        ]
        
        self.property_list_column.controls = self.build_property_list(filtered_list)
        self.update()

    def on_property_click(self, property_data):
        """
        🚀 KRİTİK GÜNCELLEME: 
        Doğrudan view append etmek yerine .go() kullanarak 
        URL'nin /property-detail/ID şeklinde güncellenmesini sağlar.
        """
        self.main_page.go(f"/property-detail/{property_data.id}")

    def build_empty_state(self):
        """Sonuç bulunamadığında gösterilecek alan"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.SEARCH_OFF_ROUNDED, size=80, color=ft.Colors.GREY_300),
                ft.Text("Aradığınız kriterlere uygun ilan bulunamadı.", color=ft.Colors.GREY_600),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=50,
            alignment=ft.Alignment.CENTER
        )