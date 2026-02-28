import flet as ft
from src.utils.ui_helpers import UIHelpers
from src.services.auth_service import auth_service

class DashboardView(ft.View):
    def __init__(self, page:ft.Page):
        super().__init__(
            route="/dashboard",
            padding=0,
            bgcolor=ft.Colors.GREY_50
        )