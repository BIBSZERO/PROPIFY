import flet as ft
from src.components.sidebar import SideBar
from src.components.top_bar import TopBar
from src.components.custom_text_field import CustomTextField
from src.services.property_service import property_service
from src.services.contact_service import contact_service
from src.models.properties import Property, PropertyType, PropertyStatus, RoomCount, BuildingAge, HeatingType, KitchenType, BalconyStatus, ElevatorStatus, ParkingStatus, FurnishedStatus, OccupationStatus, InSiteStatus 
from src.utils.ui_helpers import UIHelpers

class AddPropertyView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/add-property", bgcolor="#F0F2F5", padding=0)
        self.main_page = page

        # --- 1. FORM BİLEŞENLERİ ---
        self.title_input = CustomTextField(label="İlan Başlığı", icon=ft.Icons.TITLE, expand=True)
        self.listing_no_input = CustomTextField(label="İlan No (10 Hane)", icon=ft.Icons.NUMBERS)
        self.price_input = CustomTextField(label="Fiyat (TL)", icon=ft.Icons.MONETIZATION_ON_OUTLINED, is_numeric=True)
        
        self.m2_gross_input = CustomTextField(label="Brüt M2", icon=ft.Icons.SQUARE_FOOT, is_numeric=True)
        self.m2_net_input = CustomTextField(label="Net M2", icon=ft.Icons.SQUARE_FOOT, is_numeric=True)

        self.floor_level_input = CustomTextField(label="Bulunduğu Kat", icon=ft.Icons.LAYERS)
        self.total_floors_input = CustomTextField(label="Toplam Kat", icon=ft.Icons.BUSINESS, is_numeric=True)
        
        self.client_dropdown = ft.Dropdown(
            label="Mülk Sahibi",
            expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")

        self.type_dropdown = ft.Dropdown(
            label="Mülk Türü",
            options=[ft.dropdown.Option(key=t.name, text=t.value) for t in PropertyType],
            value=PropertyType.DAIRE.name,
            expand=True, border_radius=10, border_color="#1A237E", bgcolor="white"
        )

        self.status_dropdown = ft.Dropdown(
            label="İlan Durumu",
            options=[ft.dropdown.Option(key=s.name, text=s.value) for s in PropertyStatus],
            value=PropertyStatus.AKTIF.name,
            expand=True, border_radius=10, border_color="#1A237E", bgcolor="white"
        )

        self.room_count_dropdown = ft.Dropdown(
            label="Oda Sayısı",
            options=[ft.dropdown.Option(key=str(r.name), text=str(r.value)) for r in RoomCount],
            value="TWO_ONE",
            expand=True, border_radius=10, border_color="#1A237E", bgcolor="white"
        )

        self.building_age_dropdown = ft.Dropdown(
            label="Bina Yaşı",
            options=[ft.dropdown.Option(key=str(a.name), text=str(a.value)) for a in BuildingAge],
            value="ZERO",
            expand=True, border_radius=10, border_color="#1A237E", bgcolor="white"
        )

        self.heating_dropdown = ft.Dropdown(
            label="Isıtma Sistemi",
            options=[ft.dropdown.Option(key=h.name, text=h.value) for h in HeatingType],
            value=HeatingType.KOMBI_DOGALGAZ.name,
            expand=True,
            border_radius=10,
            border_color="#1A237E", 
            bgcolor="white"
        )

        self.bath_count_input = CustomTextField(
            label="Banyo Sayısı", 
            icon=ft.Icons.BATHTUB_OUTLINED, 
            is_numeric=True
        )

        self.kitchen_type_dropdown = ft.Dropdown(
            label="Mutfak Tipi",
            options=[ft.dropdown.Option(key=k.name, text=k.value) for k in KitchenType],
            value=KitchenType.KAPALI.name,
            expand=True, border_radius=10, border_color="#1A237E", bgcolor="white"
        )

        self.balcony_dropdown = ft.Dropdown(
            label="Balkon",
            options=[ft.dropdown.Option(key=b.name, text=b.value) for b in BalconyStatus],
            value=BalconyStatus.YOK.name,
            expand=True, border_radius=10, border_color="#1A237E", bgcolor="white"
        )

        self.elevator_dropdown = ft.Dropdown(
            label="Asansör",
            options=[ft.dropdown.Option(key=e.name, text=e.value) for e in ElevatorStatus],
            value=ElevatorStatus.YOK.name,
            expand=True, border_radius=10, border_color="#1A237E", bgcolor="white"
        )

        self.parking_dropdown = ft.Dropdown(
            label="Otopark Durumu",
            options=[ft.dropdown.Option(key=p.name, text=p.value) for p in ParkingStatus],
            value=ParkingStatus.YOK.name, # 🚀 Sayfa açıldığında "Yok" seçili gelir
            expand=True, 
            border_radius=10, 
            border_color="#1A237E", 
            bgcolor="white"
        )

        self.furnished_dropdown = ft.Dropdown(
            label="Eşya Durumu",
            options=[ft.dropdown.Option(key=f.name, text=f.value) for f in FurnishedStatus],
            value=FurnishedStatus.ESYASIZ.name,
            expand=True, border_radius=10, border_color="#1A237E", bgcolor="white"
        )

        self.occupation_dropdown = ft.Dropdown(
            label="Kullanım Durumu",
            options=[ft.dropdown.Option(key=o.name, text=o.value) for o in OccupationStatus],
            value=OccupationStatus.BOS.name,
            expand=True, border_radius=10, border_color="#1A237E", bgcolor="white"
        )

        self.in_site_dropdown = ft.Dropdown(
            label="Site İçerisinde",
            options=[ft.dropdown.Option(key=s.name, text=s.value) for s in InSiteStatus],
            value=InSiteStatus.HAYIR.name,
            expand=True, border_radius=10, border_color="#1A237E", bgcolor="white"
        )

        # --- 2. SAYFA TASARIMI ---
        # Formu Bölümlere Ayıran Yardımcı Fonksiyon
        def section_card(title: str, controls: list):
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color="#1A237E"),
                    ft.Divider(height=1, color="#EEEEEE"),
                    ft.Column(controls, spacing=15)
                ], spacing=10),
                padding=20,
                bgcolor="white",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, "black"))
            )

        self.controls = [
            ft.Row([
                SideBar(self.main_page),
                ft.Column([
                    TopBar(self.main_page),
                    ft.Container(
                        content=ft.Column([
                            # Üst Başlık ve Kaydet Butonu
                            ft.Row([
                                ft.Text("🏠 Yeni Mülk Ekle", size=28, weight=ft.FontWeight.BOLD, color="#1A237E"),
                                ft.ElevatedButton(
                                    "Portföye Kaydet",
                                    icon=ft.Icons.SAVE_ROUNDED,
                                    bgcolor="#1A237E", color="white",
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    on_click=lambda _: self.main_page.run_task(self.save_property)
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            
                            ft.Divider(height=20, color="transparent"),

                            # Ana Form Düzeni (Grid gibi)
                            ft.Row([
                                # Sol Kolon: Temel ve Teknik Bilgiler
                                ft.Column([
                                    section_card("Temel Bilgiler", [
                                        self.title_input,
                                        ft.Row([self.listing_no_input, self.price_input], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                                    ]),
                                    section_card("Mülk Detayları", [
                                        ft.Row([self.m2_gross_input, self.m2_net_input], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                        ft.Row([
                                            self.room_count_dropdown, 
                                            self.building_age_dropdown, 
                                            self.bath_count_input
                                        ], spacing=10)
                                    ]),
                                    section_card("Kat Bilgileri", [
                                        ft.Row([
                                            # Her birine expand=True vererek satırı 3 eşit parçaya böldük
                                            ft.Container(content=self.floor_level_input, expand=True),
                                            ft.Container(content=self.total_floors_input, expand=True),
                                            ft.Container(content=self.elevator_dropdown, expand=True),
                                        ], spacing=15) # Spacing'i biraz daraltarak yer kazandık
                                    ]),
                                    section_card("Donanım Bilgileri", [
                                        ft.Row([
                                            ft.Container(content=self.heating_dropdown, expand=True),
                                            ft.Container(content=self.kitchen_type_dropdown, expand=True),
                                        ], spacing=10),
                                        ft.Row([
                                            ft.Container(content=self.balcony_dropdown, expand=True),
                                            ft.Container(content=self.parking_dropdown, expand=True),
                                            ft.Container(content=self.furnished_dropdown, expand=True), # 🚀 Eşyalı durumu eklendi
                                        ], spacing=10)
                                    ]),

                                ], expand=2, spacing=20),

                                # Sağ Kolon: Durum ve Sahibi
                                ft.Column([
                                    section_card("Kategorizasyon", [
                                        ft.Row([
                                            ft.Container(content=self.type_dropdown, expand=True),
                                            ft.Container(content=self.status_dropdown, expand=True),
                                        ], spacing=10),
                                        ft.Row([
                                            ft.Container(content=self.occupation_dropdown, expand=True),
                                            ft.Container(content=self.in_site_dropdown, expand=True), # 🚀 Buraya eklendi
                                        ], spacing=10)
                                    ]),
                                    section_card("İletişim", [
                                        ft.Row([
                                            self.client_dropdown,
                                            ft.IconButton(
                                                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                                icon_color="#1A237E",
                                                on_click=lambda _: self.main_page.go("/add-client")
                                            ),
                                        ], spacing=5)
                                    ])
                                ], expand=1, spacing=20)
                            ], vertical_alignment=ft.CrossAxisAlignment.START, spacing=20)

                        ], scroll=ft.ScrollMode.HIDDEN, spacing=0),
                        padding=30, expand=True
                    )
                ], expand=True)
            ], expand=True)
        ]
        self.load_initial_data()

    def load_initial_data(self):
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
        if not self.title_input.value or not self.client_dropdown.value:
            UIHelpers.show_toast(self.main_page, "Lütfen gerekli alanları doldurun!", False)
            return

        listing_no = str(self.listing_no_input.value).strip()
        if len(listing_no) != 10:
            UIHelpers.show_toast(self.main_page, "İlan No tam 10 haneli olmalıdır!", False)
            return

        existing_properties = property_service.get_filtered("listing_no", listing_no)
        if len(existing_properties) > 0:
            UIHelpers.show_toast(self.main_page, "Bu İlan No zaten kullanımda!", False)
            return

        new_prop = Property(
            listing_no=listing_no,
            title=str(self.title_input.value),
            price=float(self.price_input.value or 0),
            m2_gross=int(self.m2_gross_input.value or 0),
            m2_net=int(self.m2_net_input.value or 0),
            floor_level=str(self.floor_level_input.value or ""),
            total_floors=int(self.total_floors_input.value or 0),
            room_count=RoomCount[self.room_count_dropdown.value],
            building_age=BuildingAge[self.building_age_dropdown.value],
            heating=HeatingType[self.heating_dropdown.value],
            kitchen_type=KitchenType[self.kitchen_type_dropdown.value],
            balcony=BalconyStatus[self.balcony_dropdown.value],
            elevator=ElevatorStatus[self.elevator_dropdown.value],
            bath_count=int(self.bath_count_input.value or 0),
            parking=ParkingStatus[self.parking_dropdown.value],
            furnished=FurnishedStatus[self.furnished_dropdown.value],
            occupation=OccupationStatus[self.occupation_dropdown.value],
            in_site=InSiteStatus[self.in_site_dropdown.value],
            owner_id=self.client_dropdown.value,
            property_type=PropertyType[self.type_dropdown.value],
            status=PropertyStatus[self.status_dropdown.value],
            images=[],
            address=""
        )
        
        if property_service.add(new_prop):
            UIHelpers.show_toast(self.main_page, "İlan başarıyla portföye eklendi! ✨", True)
            self.main_page.go("/dashboard")
        else:
            UIHelpers.show_toast(self.main_page, "Kayıt sırasında bir hata oluştu.", False)