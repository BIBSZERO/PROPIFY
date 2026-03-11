import flet as ft
from src.components.sidebar import SideBar
from src.components.top_bar import TopBar
from src.components.custom_text_field import CustomTextField
from src.services.property_service import property_service
from src.services.contact_service import contact_service
from src.models.properties import Property, PropertyType, PropertyStatus
from src.utils.ui_helpers import UIHelpers

class AddPropertyView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/add-property", bgcolor="#F4F7F9", padding=0)
        self.main_page = page

        # --- 1. FORM BİLEŞENLERİ ---
        self.title_input = CustomTextField(label="İlan Başlığı", icon=ft.Icons.TITLE)
        self.listing_no_input = CustomTextField(label="İlan No", icon=ft.Icons.NUMBERS)
        self.price_input = CustomTextField(label="Fiyat (TL)", icon=ft.Icons.ATTACH_MONEY)
        self.price_input.input_filter = ft.NumbersOnlyInputFilter()
        
        # Müşteri Seçimi (Dropdown)
        self.client_dropdown = ft.Dropdown(
            label="Mülk Sahibi (Müşteri)",
            expand=True,
            border_radius=12,
            border_color="#1A237E",
        )

        # Mülk Türü
        self.type_dropdown = ft.Dropdown(
            label="Mülk Türü",
            options=[ft.dropdown.Option(key=t.name, text=t.value) for t in PropertyType],
            value=PropertyType.DAIRE.name,
            width=250,
            border_radius=12,
            border_color="#1A237E",
        )

        # Mülk Durumu Dropdown
        self.status_dropdown = ft.Dropdown(
            label="İlan Durumu",
            options=[ft.dropdown.Option(key=s.name, text=s.value) for s in PropertyStatus],
            value=PropertyStatus.AKTIF.name, # Varsayılan olarak Aktif seçili gelsin
            width=250,
            border_radius=12,
            border_color="#1A237E",
        )

        # --- 2. SAYFA TASARIMI ---
        self.controls = [
            ft.Row([
                SideBar(self.main_page),
                ft.Column([
                    TopBar(self.main_page),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🏠 Yeni Mülk Ekle", size=28, weight=ft.FontWeight.BOLD, color="#1A237E"),
                            ft.Divider(height=10),
                            
                            self.title_input,
                            self.listing_no_input,
                            
                            ft.Row([
                                self.client_dropdown,
                            ft.IconButton(
                                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                icon_color="#1A237E",
                                tooltip="Yeni Müşteri Ekle",
                                on_click=lambda _: self.main_page.go("/add-client")
                            ),
                            ], spacing=10),
                            
                            # Tür ve Durum Seçimi Yan Yana
                            ft.Row([
                                self.type_dropdown,
                                self.status_dropdown,
                            ], spacing=20),
                            
                            # Fiyat girişi (Uploader kaldırıldı, tek başına sütun olarak duruyor)
                            ft.Row([
                                ft.Column([self.price_input], width=300),
                            ], alignment=ft.MainAxisAlignment.START),
                            
                            ft.Divider(height=20),
                            
                            ft.ElevatedButton(
                                "Portföye Kaydet",
                                icon=ft.Icons.SAVE,
                                bgcolor="#1A237E", color="white",
                                width=250, height=50,
                                on_click=lambda _: self.main_page.run_task(self.save_property)
                            )
                        ], scroll=ft.ScrollMode.ADAPTIVE, spacing=15),
                        padding=40, expand=True
                    )
                ], expand=True)
            ], expand=True)
        ]
        
        # Verileri yükle
        self.load_initial_data()

    def load_initial_data(self):
        """Müşteri listesini yeniler."""
        try:
            contacts = contact_service.get_all()
            self.client_dropdown.options = [
                ft.dropdown.Option(key=str(c.id), text=str(c.full_name)) 
                for c in contacts
            ]
            self.main_page.update()
        except Exception as e:
            print(f"Yükleme hatası: {e}")

    async def save_property(self):
        """İlanı kaydeder."""
        # Validasyon: Başlık veya Müşteri boşsa uyarı ver
        if not self.title_input.value or not self.client_dropdown.value:
            UIHelpers.show_toast(self.main_page, "Lütfen ilan başlığını ve mülk sahibini seçin!", False)
            return

        # 🚀 Model oluşturma (images alanı boş liste olarak gönderiliyor)
        new_prop = Property(
            title=str(self.title_input.value),
            listing_no= str(self.listing_no_input.value),
            price=float(self.price_input.value or 0),
            owner_id=self.client_dropdown.value, # Müşteri ID'si
            images=[], # 📸 Şimdilik boş liste gönderiyoruz
            property_type=PropertyType.DAIRE,
            status=PropertyStatus.AKTIF,
            address=""
        )
        
        success = property_service.add(new_prop)
        
        if success:
            UIHelpers.show_toast(self.main_page, "İlan başarıyla eklendi! ✨", True)
            self.main_page.go("/dashboard")
        else:
            UIHelpers.show_toast(self.main_page, "Kayıt sırasında hata oluştu.", False)