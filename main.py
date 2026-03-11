import flet as ft

from typing import Optional

from src.views.login_view import LoginView
from src.views.dashboard_view import DashboardView
from src.views.password_reset_view import PasswordResetView
from src.views.add_property_view import AddPropertyView
from src.views.add_client_view import AddClientView

def main(page: ft.Page):
    page.title = "PROPIFY"
    page.window.width = 1200
    page.window.height = 800
    page.theme_mode = ft.ThemeMode.LIGHT

    page.data = {
        "user_id": "827164c3-ae15-44c7-a29c-e96b0c6ca905",
        "user_name": "Buse İbşiroğlu"
    }
    
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

        # 🚀 OTOMATİK GİRİŞ MANTIĞI:
        # Eğer rota ana sayfa (/) veya login ise doğrudan Dashboard'a git
        if current_route == "/" or current_route == "/login":
            page.route = "/dashboard" # Rotayı güncelle
            page.views.append(DashboardView(page))
        
        elif token:
            print(f"✅ Token yakalandı: {token[:10]}...")
            page.views.append(PasswordResetView(page, token=token))
            
        elif "/password-reset" in current_route:
            page.views.append(PasswordResetView(page))
            
        elif current_route == "/dashboard":
            page.views.append(DashboardView(page))

        elif current_route == "/add-client":
            page.views.append(AddClientView(page))
            
        elif current_route == "/add-property":
            page.views.append(AddPropertyView(page))
            
        else:
            # Diğer her durumda Login'e git (Güvenlik için)
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

