import flet as ft
from src.utils.ui_helpers import UIHelpers
from src.utils.validators import Validators
from src.services.auth_service import auth_service

class LoginView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor=ft.Colors.GREY_50,
            padding=30
        )
        self.main_page = page

        # 1. ICON: 'name' parametresini kullanmıyoruz
        self.logo = ft.Icon(
            ft.Icons.REAL_ESTATE_AGENT_ROUNDED, 
            size=80, 
            color=ft.Colors.BLUE_700
        )
        
        self.title = ft.Text(
            "PROPIFY", 
            size=32, 
            weight=ft.FontWeight.BOLD, 
            color=ft.Colors.BLUE_900
        )

        self.email_input = ft.TextField(
            label="E-posta Adresi",
            hint_text="ornegin@mail.com",
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            width=350,
            border_radius=10,
        )

        self.password_input = ft.TextField(
            label="Şifre",
            prefix_icon=ft.Icons.LOCK_OUTLINED,
            password=True,
            can_reveal_password=True,
            width=350,
            border_radius=10,
        )

        # 2. BUTTON: 'text' parametresini sildik, metni doğrudan ilk sıraya koyduk
        self.login_button = ft.ElevatedButton(
            "Giriş Yap", 
            width=350,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE
            ),
            on_click=self.handle_login
        )

        self.controls = [
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[self.logo, self.title]
                    ),
                    ft.Container(height=10),
                    self.email_input,
                    self.password_input,
                    self.login_button,
                    ft.TextButton(
                        "Şifremi Unuttum", 
                        on_click=self.handle_forgot_password
                    )
                ]
            )
        ]

    def handle_login(self, e):
        email = self.email_input.value
        password = self.password_input.value

        if Validators.is_empty(email) or Validators.is_empty(password):
            UIHelpers.show_toast(self.main_page, "Lütfen tüm alanları doldurun!", False)
            return

        if not Validators.is_valid_email(email):
            UIHelpers.show_toast(self.main_page, "Geçerli bir e-posta adresi girin!", False)
            return

        loader = UIHelpers.loader_dialog(self.main_page, "Giriş yapılıyor...")
        
        try:
            session = auth_service.login(email, password)
            UIHelpers.close_dialog(self.main_page, loader)

            if session:
                UIHelpers.show_toast(self.main_page, "Giriş başarılı!", True)
                self.main_page.go("/dashboard")
            else:
                UIHelpers.show_toast(self.main_page, "E-posta veya şifre hatalı!", False)
        except Exception as err:
            UIHelpers.close_dialog(self.main_page, loader)
            UIHelpers.show_toast(self.main_page, f"Hata: {err}", False)
    
    def handle_forgot_password(self, e):
        email = self.email_input.value
        if not email or not Validators.is_valid_email(email):
            UIHelpers.show_toast(self.main_page, "Lütfen önce geçerli bir e-posta girin!", False)
            return
        success = auth_service.reset_password(email)
        if success:
            UIHelpers.show_toast(self.main_page, "Şifre sıfırlama maili gönderildi. Kutunuzu kontrol edin!", True)
        else:
            UIHelpers.show_toast(self.main_page, "Mail gönderilirken bir hata oluştu.", False)