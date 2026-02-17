from typing import List, Optional, Dict, Any
from src.core.database import db
from src.models.appointments import Appointment, AppointmentStatus

class AppointmentService:
    """
    Randevu işlemlerini (Yer gösterme, Sözleşme vb.) yöneten servis katmanı.

    """
    @staticmethod
    def create(appointment: Appointment) -> bool:
        """Yeni bir randevu kaydı oluşturur."""
        response = db.insert_data("appointments", appointment.to_dict())
        return response is not None
    
    @staticmethod
    def get_all_detailed() -> List[Dict[str, Any]]:
        """
        Tüm randevuları; mülk başlığı, müşteri adı ve danışman adıyla birlikte getirir.
        Bu metod UI (Dashboard) tarafında listeleme yapmak için kritiktir.
        """
        # Join query: İlişkili tablolardan sadece ihtiyacımız olan sütunları çekiyoruz
        query = """
            *,
            properties(title),
            contacts(full_name),
            profiles(full_name)
        """
        response = db.get_joined_data("appointments", query)
        return response.data if response else []
    
    @staticmethod
    def get_by_agent(agent_id: str) -> List[Appointment]:
        """Sadece belirli bir danışmana (Agent) ait randevuları getirir."""
        response = db.get_filtered_data("appointments", "agent_id", agent_id)
        if response and response.data:
            return [Appointment.from_dict(item) for item in response.data]
        return []

    @staticmethod
    def update_status(appointment_id: str, status: AppointmentStatus, feedback: Optional[str] = None) -> bool:
        """
        Randevu durumunu (Tamamlandı, İptal vb.) ve varsa müşteri geri bildirimini günceller.
        """
        data: Dict[str, Any] = {"status": status.value}
        if feedback:
            data["feedback"] = feedback
            
        response = db.update_data("appointments", data, appointment_id)
        return response is not None

    @staticmethod
    def get_today_appointments() -> List[Dict[str, Any]]:
        """Bugünün randevularını hızlıca çekmek için (Dashboard özeti)."""
        # Bu kısım ileride tarih filtreleme ile geliştirilecek
        # Şimdilik genel listeyi çekip Python tarafında filtreleyebiliriz
        all_apps = AppointmentService.get_all_detailed()
        # Basit bir örnek: Tarih bugünle başlıyorsa filtrele (Gerçek projede SQL ile yapılmalı)
        return all_apps

# Singleton Nesnesi
appointment_service = AppointmentService()