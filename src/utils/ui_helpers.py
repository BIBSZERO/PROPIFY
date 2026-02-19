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
        try:
            if dialog:
                dialog.open = False
                page.update()
        except Exception as e:
            print(f"❌ Dialog kapatma hatası: {e}")
    
    @staticmethod
    def create_stat_card(title: str, value: str, icon: ft.IconData, color: str = ft.Colors.BLUE_700) -> ft.Container:
        """Dashboard üzerindeki özet bilgi kartları (İlan Sayısı, Randevular vb.)."""
        return ft.Container(
            content=ft.Column([
                ft.ListTile(
                    leading=ft.Icon(icon, color=color, size=35),
                    title=ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800),
                    subtitle=ft.Text(title, size=14, color=ft.Colors.BLUE_GREY_400)
                )
            ]),
            width=220,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=15,
            shadow=ft.BoxShadow(
                blur_radius=15, 
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 5)
            )
        )
