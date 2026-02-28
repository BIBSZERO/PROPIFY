import flet as ft
from src.core.database import db

class PasswordResetView(ft.View):
    def __init__(self, page: ft.Page, token=None):
        super().__init__(
            route="/password-reset",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            padding=30
        )
        self.main_page = page
        self.recovery_token = token # main.py'dan gelen token

        self.new_password = ft.TextField(
            label="Yeni Şifre", 
            password=True, 
            can_reveal_password=True, 
            width=350
        )
        self.confirm_password = ft.TextField(
            label="Şifreyi Onayla", 
            password=True, 
            can_reveal_password=True, 
            width=350
        )

        self.controls = [
            ft.Icon(ft.Icons.LOCK_RESET, size=60, color="orange"),
            ft.Text("Yeni Şifrenizi Belirleyin", size=25, weight=ft.FontWeight.BOLD),
            self.new_password,
            self.confirm_password,
            ft.ElevatedButton(
                "Şifreyi Güncelle ve Giriş Yap", 
                on_click=self.handle_password_update, 
                width=350,
                height=50
            )
        ]

    def handle_password_update(self, e):
        new_pass = self.new_password.value
        
        if new_pass != self.confirm_password.value:
            self.main_page.snack_bar = ft.SnackBar(ft.Text("Şifreler uyuşmuyor!"))
            self.main_page.snack_bar.open = True
            self.main_page.update()
            return

        try:
            if self.recovery_token:
                # 💡 EN GARANTİ DOĞRULAMA YÖNTEMİ
                verify_response = db.client.auth.verify_otp({
                    "token_hash": self.recovery_token,
                    "type": "recovery" # Şablonda '&type=recovery' eklemiştik, burada da eşleşmeli
                })
                
                if verify_response.user:
                    # 2. Oturum doğrulandı, şimdi şifreyi güncelle
                    response = db.client.auth.update_user({"password": new_pass})
                    
                    if response.user:
                        self.main_page.snack_bar = ft.SnackBar(
                            ft.Text("Şifre başarıyla yenilendi! ✅", color="white"), 
                            bgcolor="green"
                        )
                        self.main_page.snack_bar.open = True
                        self.main_page.update()
                        self.main_page.go("/") 
                        return
            
            raise Exception("Token doğrulanamadı veya süresi dolmuş.")

        except Exception as err:
            print(f"❌ Güncelleme Hatası: {err}")
            self.main_page.snack_bar = ft.SnackBar(ft.Text(f"Hata: {err}"))
            self.main_page.snack_bar.open = True
            self.main_page.update()