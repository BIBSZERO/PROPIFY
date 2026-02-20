import flet as ft
from src.services.auth_service import auth_service
from src.components.custom_text_field import CustomTextField
from src.components.primary_button import PrimaryButton
from src.utils.ui_helpers import UIHelpers
from src.utils.validators import Validators

class LoginView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            padding=30,
            bgcolor=ft.Colors.GREY_50
        )
        self.main_page=page
        self.logo=ft.Icon(ft.Icons.REAL_ESTATE_AGENT_ROUNDED, size=80, color=ft.Colors.BLUE_700)
        self.title=ft.Text("PROPIFY", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
        self.subtitle=ft.Text("Emlak Yönetim Sistenine Hoşgeldin",size=14, color=ft.Colors.BLUE_GREY_900)

        self.email_input=CustomTextField(
            label="E-posta Adresi",
            icon=ft.Icons.EMAIL_OUTLINED,
            hint_text="ornek@mail.com"
        )
        self.password_input=CustomTextField(
            label="Şifre",
            icon=ft.Icons.LOCK_OUTLINE,
            is_password=True
        )
        self.login_button=PrimaryButton(
            text="Giriş Yap",
            on_click=self.handle_login
        )

    def handle_login(self, e):
        """Giriş butonuna basıldığında çalışan ana mantık."""
        email = self.email_input.value
        password = self.password_input.value

        # A. Basit Kontroller
        if not email or not password:
            UIHelpers.show_toast(self.page, "E-posta ve şifre boş bırakılamaz!", False)
            return
        
        if not Validators.is_valid_email(email):
            UIHelpers.show_toast(self.page, "Lütfen geçerli bir e-posta girin!", False)
            return
        
        # B. Giriş Süreci (Loader ile)
        loader = UIHelpers.loader_dialog(self.page, "Giriş yapılıyor...")

        try:
            session = auth_service.login(email, password)
            UIHelpers.close_dialog(self.page, loader)

            if session:
                UIHelpers.show_toast(self.page, "Giriş Başarılı! Hoşgeldin", True)
                self.page.go("/dashboard")
            else:
                UIHelpers.show_toast(self.page,"Hatalı e-posta veya şifre!", False)
                
        except Exception as err:
            UIHelpers.close_dialog(self.page, loader)
            UIHelpers.show_toast(self.page, f"Bağlantı Hatası: {err}", False)