import flet as ft
import uuid
from typing import Any
from src.core.database import db

class ImageUploader(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        
        # Mypy için tip tanımlaması
        self.uploaded_urls: list[str] = [] 

        # 🕵️ Mypy'ın "on_result yok" demesini engellemek için lambda kullanıyoruz
        # Bu yöntem, parametreyi çalışma anında (runtime) bağlar
        self.file_picker = ft.FilePicker(
            on_upload=lambda e: self.on_file_result(e)
        )
        self.main_page.overlay.append(self.file_picker)

        # Önizleme alanı
        self.preview_row = ft.Row(wrap=True, spacing=10)

        # Tasarım
        self.content = ft.Column([
            ft.Text("Mülk Fotoğrafları", size=16, weight=ft.FontWeight.BOLD, color="#1A237E"),
            ft.ElevatedButton(
                "Fotoğraf Seç ve Yükle",
                icon=ft.Icons.ADD_A_PHOTO_ROUNDED,
                on_click=lambda _: self.file_picker.pick_files(
                    allow_multiple=True,
                    file_type=ft.FilePickerFileType.IMAGE
                ),
                style=ft.ButtonStyle(color="white", bgcolor="#1A237E")
            ),
            ft.Container(
                content=self.preview_row,
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                # 💡 min_height hatasını height kullanarak çözdük
                height=150, 
            )
        ], spacing=10)

    # 💡 Tipini Any yaparak Mypy'ın 'files' özelliği yok demesini engelliyoruz
    def on_file_result(self, e: Any) -> None:
        """Dosya seçimi bittiğinde tetiklenen fonksiyon."""
        
        # Seçilen dosyaların varlığını kontrol et
        if not hasattr(e, "files") or e.files is None:
            return

        for file in e.files:
            # Path kontrolü
            if not file.path:
                continue

            # Benzersiz isim oluşturma
            file_ext = file.name.split(".")[-1]
            unique_name = f"{uuid.uuid4()}.{file_ext}"

            try:
                # 🚀 SUPABASE STORAGE'A YÜKLE
                with open(file.path, "rb") as f:
                    db.client.storage.from_("property_images").upload(
                        path=unique_name,
                        file=f
                    )
                
                # Public URL'i al
                public_url = db.client.storage.from_("property_images").get_public_url(unique_name)
                self.uploaded_urls.append(public_url)
                
                # Arayüze önizleme ekle
                self.add_preview(public_url, unique_name)

            except Exception as err:
                print(f"❌ Yükleme hatası ({file.name}): {err}")

        self.update()

    def add_preview(self, url: str, filename: str) -> None:
        """Küçük bir önizleme kartı ve silme butonu oluşturur."""
        
        # 💡 DÜZELTME: preview_card'ın bir ft.Stack olduğunu Mypy'a fısıldıyoruz
        preview_card: ft.Stack = ft.Stack([
            ft.Image(
                src=url,
                width=100,
                height=100,
                fit=ft.ImageFit.COVER,
                border_radius=10
            ),
            ft.IconButton(
                icon=ft.Icons.CANCEL,
                icon_color="red",
                bgcolor="white",
                top=0,
                right=0,
                on_click=lambda _: self.remove_image(url, filename, preview_card)
            )
        ])
        
        self.preview_row.controls.append(preview_card)
        self.update()

    def remove_image(self, url: str, filename: str, control: ft.Control) -> None:
        """Resmi hem arayüzden hem de Storage'dan siler."""
        try:
            db.client.storage.from_("property_images").remove([filename])
            self.uploaded_urls.remove(url)
            self.preview_row.controls.remove(control)
            self.update()
        except Exception as err:
            print(f"❌ Silme hatası: {err}")

    def get_urls(self) -> list[str]:
        """Model için URL listesini döndürür."""
        return self.uploaded_urls