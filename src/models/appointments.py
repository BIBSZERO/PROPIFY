from enum import Enum
from dataclasses import dataclass
from typing import Optional

class AppointmentType(Enum):
    YER_GOSTERME = "Yer Gösterme"
    SOZLESME = "Sözleşme"
    EXPERTIZ = "Expertiz"
    TOPLANTI = "Ofis Toplantısı"

class AppointmentStatus(Enum):
    BEKLEMEDE = "Beklemede"
    TAMAMLANDI = "Tamamlandı"
    IPTAL = "İptal Edildi"
    ERTELENDI = "Ertelendi"

@dataclass
class Appointment:
    id: Optional[str] = None
    date: str = ""
    appointment_type: AppointmentType = AppointmentType.YER_GOSTERME
    status: AppointmentStatus = AppointmentStatus.BEKLEMEDE
    property_id: str = ""
    contact_id: str = ""
    agent_id: str = ""
    notes: Optional[str] = None
    feedback: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        return Appointment(
            id=data.get("id"),
            date=data.get("date", ""),
            appointment_type=AppointmentType(data.get("type", "Yer Gösterme")),
            status=AppointmentStatus(data.get("status", "Beklemede")),
            property_id=data.get("property_id", ""),
            contact_id=data.get("contact_id", ""),
            agent_id=data.get("agent_id", ""),
            notes=data.get("notes"),
            feedback=data.get("feedback")
        )
    
    def to_dict(self):
            return {
                "date": self.date,
                "type": self.appointment_type.value,
                "status": self.status.value,
                "property_id": self.property_id,
                "contact_id": self.contact_id,
                "agent_id": self.agent_id,
                "notes": self.notes,
                "feedback": self.feedback
            }