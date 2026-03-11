import flet as ft
from src.components.top_bar import TopBar
from src.components.sidebar import SideBar
from src.components.custom_text_field import CustomTextField
from src.services.contact_service import contact_service
from src.models.contacts import Contact, ContactCategory
from src.utils.ui_helpers import UIHelpers

class AddClientView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/add-client", bgcolor="#F4F7F9", padding=0)
        self.main_page=page

        # Giriş Alanları
        self.name_input = CustomTextField(label="Ad Soyad", icon=ft.Icons.PERSON)
        self.phone_input = CustomTextField(label="Telefon Numarası", icon=ft.Icons.PHONE, is_numeric=True)
        self.email_input = CustomTextField(label="E-posta Adresi", icon=ft.Icons.EMAIL)
        self.notes_input = CustomTextField(label="Notlar", icon=ft.Icons.NOTES, multiline=True)

        self.controls = [
            ft.Row([
                SideBar(self.main_page),
                ft.Column([
                    TopBar(self.main_page),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("👤 Yeni Müşteri Kaydı", size=28, weight=ft.FontWeight.BOLD, color="#1A237E"),
                            ft.Divider(height=10),

                            self.name_input,
                            self.phone_input,
                            self.email_input,
                            self.notes_input,

                            ft.Row([
                                ft.ElevatedButton(
                                    "İptal",
                                    on_click=lambda _:self.main_page.go("/add-property"),
                                    bgcolor=ft.Colors.GREY_400, color=ft.Colors.WHITE
                                ),
                                ft.ElevatedButton(
                                    "Müşteriyi Kaydet",
                                    on_click=self.save_client,
                                    bgcolor="#1A237E", color=ft.Colors.WHITE,
                                    icon=ft.Icons.SAVE
                                ),
                            ], alignment=ft.MainAxisAlignment.END, spacing=10),
                        ], spacing=20, scroll=ft.ScrollMode.ADAPTIVE), padding=40, expand=True
                    )
                ], expand=True)
            ], expand=True)
        ]

    async def save_client(self, e):
        if not self.name_input.value:
            UIHelpers.show_toast(self.main_page, "İsim alanı boş bırakılamaz!", False)
            return
        new_contact = Contact(
            full_name=self.name_input.value,
            phone=self.phone_input.value,
            email=self.email_input.value,
            notes=self.notes_input.value,
            category=ContactCategory.MUSTERI
        )
        if contact_service.add(new_contact):
            UIHelpers.show_toast(self.main_page, "Müşteri başarıyla kaydedildi!", True)
        else:
            UIHelpers.show_toast(self.main_page, "Kayıt sırasında bir hata oluştu.", False)