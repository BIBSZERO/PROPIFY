import flet as ft
from src.components.sidebar import SideBar
from src.components.top_bar import TopBar
from src.services.property_service import PropertyService
from src.utils.ui_helpers import UIHelpers

class PropertyDetailView(ft.View):
    def __init__(self, page:ft.Page, property_data):
        super().__init__(
            route=f"/property-detail/{property_data.id}",
            bgcolor="#F4F7F9",
            padding=0
        )
        self.p = property_data
        self.main_page = page

        self.content_column = ft.Column([
            TopBar(self.main_page),

            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(self.p.title, size=28, weight=ft.FontWeight.BOLD, color="#1A237E"),
                            ft.Row([
                                ft.Icon(ft.Icons.NUMBERS, size=14, color=ft.Colors.GREY_500),
                                ft.Text(f"İlan No: {self.p.listing_no}", color=ft.Colors.GREY_500, size=13),
                            ]),
                        ], expand=True)
                    ])
                ])
            )
        ])

        self.controls = [
            ft.Row([
                SideBar(self.main_page),
                self.content_column
            ], expand=True, spacing=0)
        ]