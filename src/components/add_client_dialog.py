import flet as ft
from src.services.contact_service import contact_service
from src.models.contacts import Contact, ContactCategory
from src.utils.ui_helpers import UIHelpers
from src.components.custom_text_field import CustomTextField
from typing import Callable, Any

class AddClientDialog:
    def __init__(self, page: ft.Page, on_success: Callable):
        self.main_page = page
        self.on_success = on_success

        self.name_input = CustomTextField(
            label="Müşteri Ad Soyad",
            icon=ft.Icons.PERSON
        )
        self.phone_input = CustomTextField(
            label="Telefon Numarası",
            icon=ft.Icons.PHONE,
            is_numeric=True
        )

        self.dialog = ft.AlertDialog(
            title=ft.Text("👤 Yeni Mülk Sahibi Ekle", weight=ft.FontWeight.BOLD, color="#1A237E"),
            content=ft.Column([
                ft.Text("Müşteri bilgilerini eksiksiz giriniz.", size=12, italic=True),
                self.name_input,
                self.phone_input,
            ], tight=True, spacing=15),
            actions=[
                ft.TextButton("Vazgeç", on_click=self.close),
                ft.ElevatedButton(
                    "Kaydet",
                    on_click=self.save,
                    bgcolor="#1A237E",
                    color=ft.Colors.WHITE,
                    icon=ft.Icons.SAVE
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

    def show(self):
        self.main_page.dialog = self.dialog 
        self.dialog.open = True
        self.main_page.update()
    
    def close(self, e=None):
        self.dialog.open = False
        self.name_input.value = ""
        self.phone_input.value = ""
        self.main_page.update()

    async def save(self, e):
        name = self.name_input.value
        phone = self.phone_input.value

        if not name:
            UIHelpers.show_toast(self.main_page, "Lütfen isim giriniz!", False)
            return

        new_contact = Contact(
            full_name=name,
            phone=phone,
            category=ContactCategory.MULK_SAHIBI
        )

        if contact_service.add(new_contact):
            UIHelpers.show_toast(self.main_page, "Müşteri başarıyla eklendi! ✨", True)
            self.close()
            if self.on_success:
                self.on_success()
        else:
            UIHelpers.show_toast(self.main_page, "Kayıt sırasında bir hata oluştu.", False)