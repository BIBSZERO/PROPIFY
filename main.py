import flet as ft

from typing import Optional

from src.views.login_view import LoginView
from src.views.dashboard_view import DashboardView
from src.views.password_reset_view import PasswordResetView

def main(page: ft.Page):
    page.title = "PROPIFY"
    page.window.width = 1200
    page.window.height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 1. HATA ÖNLEME: Varsayılan rotayı belirleyelim
    if not page.route:
        page.route = "/"

    def route_change(e):
        current_route = page.route
        print(f"🕵️ Gelen Rota: {current_route}")
        
        # 💡 %100 GARANTİ MANTIK:
        # Metodları veya iterable özelliğini sorgulamak yerine 
        # doğrudan değeri çekmeyi deniyoruz.
        token = None
        try:
            # Query nesnesinden token'ı en sade haliyle istiyoruz
            token = page.query.get("token")
        except:
            pass
        
        page.views.clear()

        if token:
            print(f"✅ Token yakalandı: {token[:10]}...")
            page.views.append(PasswordResetView(page, token=token))
        elif "/password-reset" in current_route:
            page.views.append(PasswordResetView(page))
        elif current_route == "/dashboard":
            page.views.append(DashboardView(page))
        else:
            page.views.append(LoginView(page))
        
        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    # 2. KRİTİK: Olayları bağla
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # 3. ZORLA TETİKLE: Sayfa ilk açıldığında route_change'i manuel çağır
    route_change(None)

if __name__ == "__main__":
    # view=ft.AppView.WEB_BROWSER ekleyerek tarayıcıda açılmasını sağlıyoruz
    ft.app(
            target=main, 
            assets_dir="assets",
            view=ft.AppView.WEB_BROWSER,
            port=8000 # Tarayıcıda açar
        )

