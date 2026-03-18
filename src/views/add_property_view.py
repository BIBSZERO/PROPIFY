import flet as ft
from typing import Optional, Any
from src.components.sidebar import SideBar
from src.components.top_bar import TopBar
from src.components.custom_text_field import CustomTextField
from src.services.property_service import property_service
from src.services.contact_service import contact_service
from src.models.properties import (
    Property, PropertyType, PropertyStatus, RoomCount, BuildingAge, 
    HeatingType, KitchenType, BalconyStatus, ElevatorStatus, 
    ParkingStatus, FurnishedStatus, OccupationStatus, InSiteStatus, TitleDeedStatus 
)
from src.utils.ui_helpers import UIHelpers

class AddPropertyView(ft.View):
    def __init__(self, page: ft.Page, edit_property: Optional[Property] = None):
        super().__init__(route="/add-property", bgcolor="#F0F2F5", padding=0)
        self.main_page = page
        self.p = edit_property
        self.edit_mode = edit_property is not None

        # --- 1. FORM BİLEŞENLERİ (Mypy Uyumlu ve Güvenli Veri Çekme) ---
        
        self.title_input = CustomTextField(
            label="İlan Başlığı", 
            icon=ft.Icons.TITLE, 
            expand=True,
            value=(self.p.title if self.p else "") if self.edit_mode else ""
        )
        
        self.listing_no_input = CustomTextField(
            label="İlan No (10 Hane)", 
            icon=ft.Icons.NUMBERS,
            value=(self.p.listing_no if self.p else "") if self.edit_mode else "",
            read_only=self.edit_mode 
        )
        
        self.price_input = CustomTextField(
            label="Fiyat (TL)", 
            icon=ft.Icons.MONETIZATION_ON_OUTLINED, 
            is_numeric=True,
            value=str(int(self.p.price)) if self.edit_mode and self.p else ""
        )
        
        self.m2_gross_input = CustomTextField(label="Brüt M2", icon=ft.Icons.SQUARE_FOOT, is_numeric=True, value=str(self.p.m2_gross) if self.edit_mode and self.p else "")
        self.m2_net_input = CustomTextField(label="Net M2", icon=ft.Icons.SQUARE_FOOT, is_numeric=True, value=str(self.p.m2_net) if self.edit_mode and self.p else "")
        self.floor_level_input = CustomTextField(label="Bulunduğu Kat", icon=ft.Icons.LAYERS, value=(self.p.floor_level if self.p else "") if self.edit_mode else "")
        self.total_floors_input = CustomTextField(label="Toplam Kat", icon=ft.Icons.BUSINESS, is_numeric=True, value=str(self.p.total_floors) if self.edit_mode and self.p else "")
        self.bath_count_input = CustomTextField(label="Banyo Sayısı", icon=ft.Icons.BATHTUB_OUTLINED, is_numeric=True, value=str(self.p.bath_count) if self.edit_mode and self.p else "")
        
        self.site_name_input = CustomTextField(
            label="Site Adı", 
            icon=ft.Icons.BUSINESS_OUTLINED, 
            value=(getattr(self.p, "site_name", "") or "") if self.edit_mode else ""
        )
        
        self.dues_input = CustomTextField(label="Aidat Tutarı (TL)", icon=ft.Icons.MONETIZATION_ON_OUTLINED, is_numeric=True, expand=True, value=str(int(self.p.dues)) if self.edit_mode and self.p else "")
        self.deposit_input = CustomTextField(label="Depozito Tutarı (TL)", icon=ft.Icons.SECURITY_OUTLINED, is_numeric=True, expand=True, value=str(int(self.p.deposit)) if self.edit_mode and self.p else "")

        # --- DROPDOWN BİLEŞENLERİ ---
        self.client_dropdown = ft.Dropdown(label="Mülk Sahibi", expand=True, border_radius=10, border_color="#1A237E", bgcolor="white", value=str(self.p.owner_id) if self.edit_mode and self.p else None)
        self.type_dropdown = ft.Dropdown(label="Mülk Türü", options=[ft.dropdown.Option(key=t.name, text=t.value) for t in PropertyType], value=self.p.property_type.name if self.edit_mode and self.p else PropertyType.DAIRE.name, expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.status_dropdown = ft.Dropdown(label="İlan Durumu", options=[ft.dropdown.Option(key=s.name, text=s.value) for s in PropertyStatus], value=self.p.status.name if self.edit_mode and self.p else PropertyStatus.AKTIF.name, expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.room_count_dropdown = ft.Dropdown(label="Oda Sayısı", options=[ft.dropdown.Option(key=str(r.name), text=str(r.value)) for r in RoomCount], value=self.p.room_count.name if self.edit_mode and self.p else "TWO_ONE", expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.building_age_dropdown = ft.Dropdown(label="Bina Yaşı", options=[ft.dropdown.Option(key=str(a.name), text=str(a.value)) for a in BuildingAge], value=self.p.building_age.name if self.edit_mode and self.p else "ZERO", expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.heating_dropdown = ft.Dropdown(label="Isıtma Sistemi", options=[ft.dropdown.Option(key=h.name, text=h.value) for h in HeatingType], value=self.p.heating.name if self.edit_mode and self.p else HeatingType.KOMBI_DOGALGAZ.name, expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.kitchen_type_dropdown = ft.Dropdown(label="Mutfak Tipi", options=[ft.dropdown.Option(key=k.name, text=k.value) for k in KitchenType], value=self.p.kitchen_type.name if self.edit_mode and self.p else KitchenType.KAPALI.name, expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.balcony_dropdown = ft.Dropdown(label="Balkon", options=[ft.dropdown.Option(key=b.name, text=b.value) for b in BalconyStatus], value=self.p.balcony.name if self.edit_mode and self.p else BalconyStatus.YOK.name, expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.elevator_dropdown = ft.Dropdown(label="Asansör", options=[ft.dropdown.Option(key=e.name, text=e.value) for e in ElevatorStatus], value=self.p.elevator.name if self.edit_mode and self.p else ElevatorStatus.YOK.name, expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.parking_dropdown = ft.Dropdown(label="Otopark Durumu", options=[ft.dropdown.Option(key=p.name, text=p.value) for p in ParkingStatus], value=self.p.parking.name if self.edit_mode and self.p else ParkingStatus.YOK.name, expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.furnished_dropdown = ft.Dropdown(label="Eşya Durumu", options=[ft.dropdown.Option(key=f.name, text=f.value) for f in FurnishedStatus], value=self.p.furnished.name if self.edit_mode and self.p else FurnishedStatus.ESYASIZ.name, expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.occupation_dropdown = ft.Dropdown(label="Kullanım Durumu", options=[ft.dropdown.Option(key=o.name, text=o.value) for o in OccupationStatus], value=self.p.occupation.name if self.edit_mode and self.p else OccupationStatus.BOS.name, expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.in_site_dropdown = ft.Dropdown(label="Site İçerisinde", options=[ft.dropdown.Option(key=s.name, text=s.value) for s in InSiteStatus], value=self.p.in_site.name if self.edit_mode and self.p else InSiteStatus.HAYIR.name, expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")
        self.title_deed_dropdown = ft.Dropdown(label="Tapu Durumu", options=[ft.dropdown.Option(key=t.name, text=t.value) for t in TitleDeedStatus], value=self.p.title_deed.name if self.edit_mode and self.p else TitleDeedStatus.KAT_MULKIYETI.name, expand=True, border_radius=10, border_color="#1A237E", bgcolor="white")

        # --- 2. SAYFA TASARIMI ---
        def section_card(title: str, controls: list):
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color="#1A237E"),
                    ft.Divider(height=1, color="#EEEEEE"),
                    ft.Column(controls, spacing=15)
                ], spacing=10),
                padding=20, bgcolor="white", border_radius=12,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, "black"))
            )

        self.controls = [
            ft.Row([
                SideBar(self.main_page),
                ft.Column([
                    TopBar(self.main_page),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("🏠 " + ("İlanı Düzenle" if self.edit_mode else "Yeni Mülk Ekle"), size=28, weight=ft.Fontweight.BOLD, color="#1A237E"),
                                ft.ElevatedButton(
                                    "GÜNCELLEMELERİ KAYDET" if self.edit_mode else "PORTFÖYE KAYDET",
                                    icon=ft.Icons.SAVE_ROUNDED, bgcolor="#1A237E", color="white",
                                    on_click=lambda _: self.main_page.run_task(self.save_property)
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(height=20, color="transparent"),
                            ft.Row([
                                ft.Column([
                                    section_card("Temel Bilgiler", [self.title_input, ft.Row([self.listing_no_input, self.price_input], expand=True)]),
                                    section_card("Mülk Detayları", [ft.Row([self.m2_gross_input, self.m2_net_input], expand=True), ft.Row([self.room_count_dropdown, self.building_age_dropdown, self.bath_count_input], spacing=10)]),
                                    section_card("Kat ve Donanım", [ft.Row([self.floor_level_input, self.total_floors_input, self.elevator_dropdown], expand=True), ft.Row([self.heating_dropdown, self.kitchen_type_dropdown], expand=True)]),
                                    section_card("Ekstra Özellikler", [ft.Row([self.balcony_dropdown, self.parking_dropdown, self.furnished_dropdown], expand=True)]),
                                    section_card("Konum ve Finans", [ft.Row([self.in_site_dropdown, self.site_name_input], expand=True), ft.Row([self.dues_input, self.deposit_input], expand=True)]),
                                ], expand=2, spacing=20),
                                ft.Column([
                                    section_card("Kategorizasyon", [self.type_dropdown, self.status_dropdown, self.occupation_dropdown, self.title_deed_dropdown]),
                                    section_card("İletişim", [ft.Row([self.client_dropdown, ft.IconButton(icon=ft.Icons.ADD_CIRCLE_OUTLINE, on_click=lambda _: self.main_page.go("/add-client"))])])
                                ], expand=1, spacing=20)
                            ], vertical_alignment=ft.CrossAxisAlignment.START)
                        ], scroll=ft.ScrollMode.ADAPTIVE),
                        padding=30, expand=True
                    )
                ], expand=True)
            ], expand=True)
        ]
        self.load_initial_data()

    def load_initial_data(self):
        try:
            contacts = contact_service.get_all()
            self.client_dropdown.options = [ft.dropdown.Option(key=str(c.id), text=f"{c.full_name} ({c.phone})") for c in contacts]
            self.main_page.update()
        except Exception as e:
            print(f"Yükleme hatası: {e}")

    async def save_property(self):
        if not self.title_input.value or not self.client_dropdown.value:
            UIHelpers.show_toast(self.main_page, "Lütfen gerekli alanları doldurun!", False)
            return

        loader = UIHelpers.loader_dialog(self.main_page, "Veriler kaydediliyor...")
        try:
            new_prop = Property(
                id=self.p.id if self.edit_mode and self.p else None,
                listing_no=str(self.listing_no_input.value).strip(),
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
                site_name=str(self.site_name_input.value or ""),
                dues=float(self.dues_input.value or 0),
                deposit=float(self.deposit_input.value or 0),
                title_deed=TitleDeedStatus[self.title_deed_dropdown.value],
                owner_id=self.client_dropdown.value,
                property_type=PropertyType[self.type_dropdown.value],
                status=PropertyStatus[self.status_dropdown.value],
                images=self.p.images if self.edit_mode and self.p else [],
                address=""
            )
            
            if self.edit_mode:
                success = property_service.update(new_prop)
                msg = "İlan başarıyla güncellendi! ✨"
            else:
                success = property_service.add(new_prop)
                msg = "İlan başarıyla portföye eklendi! ✨"

            UIHelpers.close_dialog(self.main_page, loader)
            if success:
                UIHelpers.show_toast(self.main_page, msg, True)
                self.main_page.go("/portfolio")
            else:
                UIHelpers.show_toast(self.main_page, "İşlem başarısız oldu.", False)

        except Exception as e:
            UIHelpers.close_dialog(self.main_page, loader)
            UIHelpers.show_toast(self.main_page, f"Hata: {e}", False)