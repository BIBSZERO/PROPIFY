import flet as ft
from typing import Optional

from src.views.login_view import LoginView
from src.views.dashboard_view import DashboardView
from src.views.password_reset_view import PasswordResetView
from src.views.add_property_view import AddPropertyView
from src.views.add_client_view import AddClientView
from src.views.portfolio_view import PortfolioView
from src.views.property_detail_view import PropertyDetailView
from src.services.property_service import property_service

def main(page: ft.Page):
    page.title = "PROPIFY"
    page.window.width = 1200
    page.window.height = 800
    page.theme_mode = ft.ThemeMode.LIGHT

    page.data = {
        "user_id": "827164c3-ae15-44c7-a29c-e96b0c6ca905",
        "user_name": "Buse İbşiroğlu"
    }
    
    if not page.route:
        page.route = "/"

    def route_change(e):
        current_route = page.route
        print(f"🕵️ Gelen Rota: {current_route}")
        
        token = None
        try:
            token = page.query.get("token")
        except:
            pass
        
        page.views.clear()

        # 🚀 ROTASYON MANTIĞI:
        if current_route == "/" or current_route == "/login":
            page.views.append(DashboardView(page))
        
        elif token:
            print(f"✅ Token yakalandı: {token[:10]}...")
            page.views.append(PasswordResetView(page, token=token))
            
        elif "/password-reset" in current_route:
            page.views.append(PasswordResetView(page))
            
        elif current_route == "/dashboard":
            page.views.append(DashboardView(page))
        
        elif current_route == "/portfolio":
            page.views.append(PortfolioView(page))

        # 🏠 PORTFÖY DETAY ROTASI
        elif current_route.startswith("/property-detail/"):
            prop_id = current_route.split("/")[-1]
            all_props = property_service.get_all()
            selected_prop = next((p for p in all_props if p.id == prop_id), None)
            
            if selected_prop:
                page.views.append(PropertyDetailView(page, selected_prop))
            else:
                page.go("/portfolio")

        # ✍️ YENİ: DÜZENLEME MODU ROTASI
        elif current_route.startswith("/edit-property/"):
            # URL'den ID'yi alıyoruz
            prop_id = current_route.split("/")[-1]
            all_props = property_service.get_all()
            selected_prop = next((p for p in all_props if p.id == prop_id), None)
            
            if selected_prop:
                # 🚀 KRİTİK: AddPropertyView'ı 'edit_property' verisiyle çağırıyoruz
                page.views.append(AddPropertyView(page, edit_property=selected_prop))
            else:
                print(f"❌ Hata: {prop_id} ID'li mülk düzenleme için bulunamadı.")
                page.go("/portfolio")

        elif current_route == "/add-client":
            page.views.append(AddClientView(page))
            
        elif current_route == "/add-property":
            # Burası yeni (boş) ilan ekleme için
            page.views.append(AddPropertyView(page))
            
        else:
            page.views.append(LoginView(page))
        
        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change(None)

if __name__ == "__main__":
    ft.app(
        target=main, 
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER,
        port=8000
    )