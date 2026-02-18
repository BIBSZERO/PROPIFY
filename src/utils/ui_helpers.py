import flet as ft
from typing import Optional, Callable

class UIHelpers:
    """
    PROPIFY Görsel Standartlar ve Yardımcı Araçlar.
    Uygulama genelinde tutarlı bir UI deneyimi sağlar.
    """
    @staticmethod
    def show_toast(page: ft.Page, text: str, is_success: bool = True):
        """Kullanıcıya hızlı geri bildirim veren SnackBar (Toast) mesajı."""
        try:
            snack = ft.SnackBar(
                content=ft.Text(text, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
                bgcolor=ft.Colors.GREEN_600 if is_success else ft.Colors.RED_ACCENT_700,
                behavior=ft.SnackBarBehavior.FLOATING,
                margin=ft.margin.all(20),
                duration=3000,
            )
            page.add(snack)
            snack.open = True
            page.update()
        except Exception as e:
            print(f"❌ Toast hatası: {e}")
    
if __name__ == "__main__":
    def test_main(page: ft.Page):
        page.title = "UIHelpers Test Alanı"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Başarılı mesaj testi
        success_btn = ft.ElevatedButton(
            "Başarı Mesajı Göster",
            on_click=lambda _:UIHelpers.show_toast(page, "İşlem başarıyla tamamlandı!!!", True),
        )

        # Hata mesajı testi
        error_btn = ft.ElevatedButton(
            "Hata Mesajı Göster",
            on_click=lambda _:UIHelpers.show_toast(page, "Bir şeyler ters gitti!", False),
        )

        page.add(
            ft.Text("UIHelpers SnackBar Testi", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([success_btn, error_btn], alignment=ft.MainAxisAlignment.CENTER)
        )

ft.app(target=test_main)

# Çalıştırma komutu : python -m src.utils.ui_helpers