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
    
        