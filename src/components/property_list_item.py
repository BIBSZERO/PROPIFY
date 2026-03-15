import flet as ft

class PropertyListItem(ft.Container):
    def __init__(self, property_data, on_click_action):
        super().__init__()
        self.p = property_data
        self.on_click_action = on_click_action
        
        # --- Konteynır Temel Tasarımı ---
        self.bgcolor = ft.Colors.WHITE
        self.border_radius = 12
        self.padding = 15
        self.margin = ft.margin.only(bottom=10)
        self.border = ft.border.all(1, "#E0E0E0")
        
        # Tıklama ve Hover Ayarları
        self.on_click = lambda _: self.on_click_action(self.p)
        self.mouse_cursor = ft.MouseCursor.CLICK
        self.on_hover = self.handle_hover  # Hata veren hover_style yerine bu fonksiyonu kullanıyoruz

        # --- İçerik Düzeni ---
        self.content = ft.Row([
            # 1. Sol Bölüm: Mülk Tipi İkonu
            ft.Container(
                content=ft.Icon(
                    self.get_icon_by_type(self.p.property_type.value), 
                    color="#1A237E", 
                    size=28
                ),
                width=52,
                height=52,
                bgcolor="#F0F2F8",
                border_radius=10,
            ),
            
            # 2. Orta Bölüm: Başlık ve Alt Bilgiler
            ft.Column([
                ft.Text(
                    self.p.title, 
                    weight=ft.FontWeight.BOLD, 
                    size=16, 
                    color="#1A237E",
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=14, color=ft.Colors.GREY_500),
                    ft.Text(f"{self.p.address or 'Kastamonu'}", size=12, color=ft.Colors.GREY_600),
                    ft.Text(" • ", color=ft.Colors.GREY_400),
                    ft.Text(f"{self.p.room_count.value if hasattr(self.p.room_count, 'value') else self.p.room_count}", size=12, color=ft.Colors.GREY_700),
                    ft.Text(" • ", color=ft.Colors.GREY_400),
                    ft.Text(f"{self.p.m2_net} m² Net", size=12, color=ft.Colors.GREY_700),
                ], spacing=4),
            ], expand=True, spacing=4),
            
            # 3. Sağ Bölüm: Fiyat ve Durum Rozeti
            ft.Column([
                ft.Text(
                    f"{self.p.price:,.0f} TL", 
                    weight=ft.FontWeight.BOLD, 
                    size=16, 
                    color=ft.Colors.BLUE_800
                ),
                ft.Container(
                    content=ft.Text(
                        self.p.status.value, 
                        size=10, 
                        color=ft.Colors.WHITE, 
                        weight=ft.FontWeight.BOLD
                    ),
                    bgcolor=self.get_status_color(self.p.status.value),
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    border_radius=6,
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=4)
            
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)

    def handle_hover(self, e):
        """Mouse üzerine gelince arka plan rengini yumuşak bir şekilde değiştirir"""
        self.bgcolor = "#F0F4FF" if e.data == "true" else ft.Colors.WHITE
        self.update()

    def get_icon_by_type(self, p_type):
        """Mülk tipine göre ilgili ikonu döner"""
        icons = {
            "Daire": ft.Icons.APARTMENT_ROUNDED,
            "Villa": ft.Icons.VILLA_ROUNDED,
            "Dükkan": ft.Icons.STOREFRONT_ROUNDED,
            "Arsa": ft.Icons.LANDSCAPE_ROUNDED
        }
        return icons.get(p_type, ft.Icons.HOME_ROUNDED)

    def get_status_color(self, status):
        """İlan durumuna göre renk döner"""
        colors = {
            "Aktif": ft.Colors.GREEN_700,
            "Pasif": ft.Colors.GREY_600,
            "Satıldı": ft.Colors.RED_700,
            "Kiralandı": ft.Colors.ORANGE_700
        }
        return colors.get(status, ft.Colors.BLUE_GREY_400)