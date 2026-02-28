import flet as ft
from src.models.properties import Property
from src.utils.formatters import Formatters

class PropertyCard(ft.Container):
    def __init__(self, property_obj: Property):
        super().__init__()
        
        # Kartın Temel Tasarımı
        self.padding = 15
        self.border_radius = 15
        self.bgcolor = ft.Colors.WHITE
        self.width = 280
        self.shadow = ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
        )

        # 📸 Resim Kontrolü
        # Modelindeki 'images' listesini kullanıyoruz
        image_url = (
            property_obj.images[0] 
            if property_obj.images and len(property_obj.images) > 0 
            else "https://via.placeholder.com/400x250?text=Resim+Yok"
        )

        self.content = ft.Column([
            # 1. Resim Alanı
            ft.Image(
                src=image_url,
                width=250,
                height=150,
                fit=ft.BoxFit.COVER,
                border_radius=10
            ),
            
            # 2. Başlık
            ft.Text(
                property_obj.title, 
                weight=ft.FontWeight.BOLD, 
                size=16, 
                no_wrap=True,
                overflow=ft.TextOverflow.ELLIPSIS
            ),
            
            # 3. Adres (Modelde 'address' olarak tanımlamıştık)
            ft.Row([
                ft.Icon(ft.Icons.LOCATION_ON, size=14, color=ft.Colors.GREY_600),
                ft.Text(property_obj.address if property_obj.address else "Konum Belirtilmedi", size=12, color=ft.Colors.GREY_600),
            ], spacing=5),
            
            # 4. Fiyat ve Tip (Modelde rooms yoktu, o yüzden mülk tipini koyuyoruz)
            ft.Row([
                ft.Text(
                    Formatters.format_money(property_obj.price),
                    color=ft.Colors.BLUE_700,
                    weight=ft.FontWeight.BOLD,
                    size=18
                ),
                # Mülk Tipi (Daire, Villa vb.)
                ft.Container(
                    content=ft.Text(
                        property_obj.property_type.value, 
                        size=10, 
                        color="white", 
                        weight=ft.FontWeight.BOLD
                    ),
                    bgcolor=ft.Colors.BLUE_700,
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=5
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], spacing=8)