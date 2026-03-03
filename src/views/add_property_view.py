import flet as ft
import uuid
from src.components.sidebar import SideBar
from src.components.top_bar import TopBar
from src.components.image_uploader import ImageUploader
from src.services.property_service import property_service
from src.models.properties import Property, PropertyType, PropertyStatus
from src.utils.ui_helpers import UIHelpers

class AddPropertyView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/add-property",
            bgcolor="#F4F7F9",
            padding=0
        )
        self.main_page = page
