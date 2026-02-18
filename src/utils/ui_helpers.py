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

    @staticmethod
    def loader_dialog(page: ft.Page, message: str = "Lütfen Bekleyin..."):
        """Veri işlenirken ekranı kilitleyen yükleme ekranı."""
        try:
            dialog = ft.AlertDialog(
                modal=True,
                content=ft.Column(
                    [
                        ft.ProgressRing(width=40, height=40, stroke_width=4, color=ft.Colors.BLUE_700),
                        ft.Text(message, size=16, weight=ft.FontWeight.W_400)
                    ],
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            )
            page.add(dialog)
            dialog.open = True
            return dialog
        
        except Exception as e:
            print(f"❌ Loader hatası: {e}")
            return None
        
    @staticmethod
    def close_dialog(page: ft.Page, dialog: ft.AlertDialog):
        """Spesifik bir diyalog penceresini güvenli bir şekilde kapatır."""
       
    
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "PROPIFY UI Test"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        page.add(
            ft.Text("UIHelpers Test Ekranı", size=25, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton(
                "Başarılı Toast", 
                on_click=lambda _: UIHelpers.show_toast(page, "İşlem Tamam!", True)
            ),
            ft.ElevatedButton(
                "Hatalı Toast", 
                on_click=lambda _: UIHelpers.show_toast(page, "Hata Oluştu!", False)
            ),
            ft.ElevatedButton(
                "Yükleme Ekranını Aç (2 sn)", 
                on_click=lambda _: test_loader(page)
            )
        )

    def test_loader(page):
        import time
        loader = UIHelpers.loader_dialog(page, "Veriler çekiliyor...")
        time.sleep(2) # Test için bekletme
        UIHelpers.close_dialog(page, loader)

ft.app(target=main)

# Çalıştırma komutu : python -m src.utils.ui_helpers