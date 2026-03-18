import flet as ft
from src.components.sidebar import SideBar
from src.components.top_bar import TopBar
from src.services.property_service import property_service # Küçük harfle servis örneği
from src.utils.ui_helpers import UIHelpers

class PropertyDetailView(ft.View):
    def __init__(self, page: ft.Page, property_data):
        super().__init__(
            route=f"/property-detail/{property_data.id}",
            bgcolor="#F4F7F9",
            padding=0
        )
        self.p = property_data
        self.main_page = page

        # --- Sayfa Ana Gövdesi ---
        self.content_column = ft.Column([
            TopBar(self.main_page),
            
            ft.Container(
                content=ft.Column([
                    # 1. Başlık ve Aksiyon Grubu
                    ft.Row([
                        ft.Column([
                            ft.Text(self.p.title, size=28, weight=ft.FontWeight.BOLD, color="#1A237E"),
                            ft.Row([
                                ft.Icon(ft.Icons.TAG, size=14, color=ft.Colors.GREY_500),
                                ft.Text(f"İlan No: {self.p.listing_no}", color=ft.Colors.GREY_500, size=13),
                            ]),
                        ], expand=True),
                        ft.Row([
                            ft.ElevatedButton(
                                "Düzenle",
                                icon=ft.Icons.EDIT_ROUNDED,
                                on_click=self.handle_edit,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor="#1A237E",
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                )
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_color=ft.Colors.RED_700,
                                tooltip="İlanı Sil",
                                on_click=self.confirm_delete # UIHelpers Onay Penceresini açar
                            ),
                        ])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    ft.Divider(height=30, color="transparent"),

                    # 2. Bilgi Kartları (Responsive Tasarım)
                    ft.ResponsiveRow([
                        self.create_info_section("💰 Finansal Detaylar", {
                            "Fiyat": f"{self.p.price:,.0f} TL",
                            "Aidat": f"{self.p.dues:,.0f} TL",
                            "Depozito": f"{self.p.deposit:,.0f} TL",
                            "Tapu Durumu": self.p.title_deed.value
                        }, col={"sm": 12, "md": 6}),
                        
                        self.create_info_section("🏠 Yapı Bilgileri", {
                            "Mülk Tipi": self.p.property_type.value,
                            "Oda Sayısı": self.p.room_count.value,
                            "Metrekare": f"{self.p.m2_net} m² / {self.p.m2_gross} m²",
                            "Isınma": self.p.heating.value,
                            "Bina Yaşı": self.p.building_age.value
                        }, col={"sm": 12, "md": 6}),

                        self.create_info_section("📍 Konum ve Ekstralar", {
                            "Site Adı": self.p.site_name if self.p.site_name else "Müstakil",
                            "Adres": self.p.address or "Kastamonu",
                            "Mutfak": self.p.kitchen_type.value,
                            "Eşya": self.p.furnished.value,
                            "Müşteri": self.p.owner_id or "Belirtilmemiş"
                        }, col={"sm": 12}),
                    ], spacing=20),

                ], scroll=ft.ScrollMode.ADAPTIVE),
                padding=30,
                expand=True
            )
        ], expand=True)

        self.controls = [
            ft.Row([
                SideBar(self.main_page),
                self.content_column
            ], expand=True, spacing=0)
        ]

    def create_info_section(self, title, data, col):
        """Şık bilgi kartları oluşturur."""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color="#1A237E"),
                ft.Divider(height=1, color="#EEEEEE"),
                *[ft.Row([
                    ft.Text(f"{k}:", color=ft.Colors.GREY_700),
                    ft.Text(v, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) for k, v in data.items()]
            ], spacing=12),
            bgcolor=ft.Colors.WHITE,
            padding=25,
            border_radius=15,
            border=ft.border.all(1, "#E8EAF6"),
            col=col
        )

    # --- AKSİYONLAR ---

    def confirm_delete(self, e):
        """UIHelpers kullanarak merkezi onay penceresini açar."""
        UIHelpers.show_confirm_dialog(
            page=self.main_page,
            title="⚠️ İlanı Sil",
            message=f"'{self.p.title}' başlıklı ilan kalıcı olarak silinecek. Emin misiniz?",
            on_confirm=self.actual_delete # Onay verilince çalışacak fonksiyon
        )

    def actual_delete(self):
        """Gerçek silme işlemini servis üzerinden yapar."""
        # UIHelpers Loader'ı başlat
        loader = UIHelpers.loader_dialog(self.main_page, "Veritabanından Siliniyor...")
        
        try:
            # Senin servisindeki delete metodunu çağırıyoruz
            success = property_service.delete(self.p.id)
            
            # Loader'ı kapat
            UIHelpers.close_dialog(self.main_page, loader)
            
            if success:
                UIHelpers.show_toast(self.main_page, "İlan başarıyla silindi.", is_success=True)
                self.main_page.go("/portfolio") # Listeye geri dön
            else:
                UIHelpers.show_toast(self.main_page, "Silme işlemi başarısız!", is_success=False)
                
        except Exception as err:
            UIHelpers.close_dialog(self.main_page, loader)
            UIHelpers.show_toast(self.main_page, f"Hata: {err}", is_success=False)

    def handle_edit(self, e):
        """
        Düzenleme butonuna basıldığında:
        1. Mevcut mülk verisini (self.p) paketler.
        2. main.py'daki '/edit-property/ID' rotasına gönderir.
        """
        UIHelpers.show_toast(self.main_page, "Düzenleme moduna geçiliyor...", is_success=True)
        
        # 🚀 KRİTİK SATIR:
        # Adresi değiştiriyoruz, main.py bunu yakalayıp AddPropertyView'ı 
        # düzenleme modunda açacak.
        self.main_page.go(f"/edit-property/{self.p.id}")