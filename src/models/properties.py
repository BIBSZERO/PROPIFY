from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List

class PropertyType(Enum):
    DAIRE = "Daire"
    DUKKAN = "Dükkan"
    ARSA = "Arsa"
    VILLA = "Villa"

class PropertyStatus(Enum):
    AKTIF = "Aktif"
    PASIF = "Pasif"
    SATILDI = "Satıldı"
    KIRALANDI = "Kiralandı"

class RoomCount(Enum):
    STUDIO = "1+0"
    ONE_ONE = "1+1"
    TWO_ONE = "2+1"
    THREE_ONE = "3+1"
    FOUR_ONE = "4+1"
    FOUR_TWO = "4+2"
    FIVE_ONE = "5+1"
    OTHER = "Diğer"

class BuildingAge(Enum):
    ZERO = "0 (Yeni)"
    ONE_FIVE = "1-5 Yıl"
    SIX_TEN = "6-10 Yıl"
    ELEVEN_FIFTEEN = "11-15 Yıl"
    SIXTEEN_TWENTY = "16-20 Yıl"
    OVER_TWENTY = "21 ve Üzeri"

class HeatingType(Enum):
    YOK = "Yok"
    SOBA = "Soba"
    DOGALGAZ_SOBA = "Doğalgaz Sobası"
    KOMBI_DOGALGAZ = "Kombi (Doğalgaz)"
    MERKEZI = "Merkezi Sistem"
    MERKEZI_PAY = "Merkezi (Isı Pay Ölçer)"
    YERDEN_ISITMA = "Yerden Isıtma"
    KLIMA = "Klima"
    ISI_POMPASI = "Isı Pompası"

class KitchenType(Enum):
    KAPALI = "Kapalı Mutfak"
    AMERIKAN = "Amerikan Mutfak"

class BalconyStatus(Enum): # Balkon
    VAR = "Var"
    YOK = "Yok"

class ElevatorStatus(Enum): # Asansör
    VAR = "Var"
    YOK = "Yok"

class ParkingStatus(Enum):
    YOK = "Yok"
    KAPALI = "Kapalı"
    ACIK = "Açık"
    KAPALI_ACIK = "Kapalı + Açık"

class FurnishedStatus(Enum):
    ESYALI = "Eşyalı"
    ESYASIZ = "Eşyasız"

class OccupationStatus(Enum):
    BOS = "Boş"
    MULK_SAHIBI = "Mülk Sahibi"
    KIRACILI = "Kiracılı"

@dataclass
class Property:
    id: Optional[str] = None
    listing_no: str = ""
    title: str = ""
    property_type: PropertyType = PropertyType.DAIRE
    status: PropertyStatus = PropertyStatus.AKTIF
    price: float = 0.0
    m2_gross: int = 0
    m2_net: int = 0
    floor_level: str = ""
    total_floors: int = 0
    room_count: RoomCount = RoomCount.TWO_ONE
    building_age: BuildingAge = BuildingAge.ZERO
    heating: HeatingType = HeatingType.YOK
    kitchen_type: KitchenType = KitchenType.KAPALI
    balcony: BalconyStatus = BalconyStatus.VAR
    elevator: ElevatorStatus = ElevatorStatus.YOK
    parking: ParkingStatus = ParkingStatus.YOK
    furnished: FurnishedStatus = FurnishedStatus.ESYASIZ
    occupation: OccupationStatus = OccupationStatus.BOS
    bath_count: int = 0
    owner_id: Optional[str] = None
    address: Optional[str] = "" # 🚀 HATA DÜZELTME: Varsayılan değer ekledik (None yerine "")
    images: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict):
        # Enum dönüşümlerinde hata almamak için .get() ile gelen değeri kontrol ediyoruz
        b_age_val = data.get("building_age")
        r_count_val = data.get("room_count")
        heating_val = data.get("heating")
        kitchen_val = data.get("kitchen_type")
        balcony_val = data.get("balcony")
        elevator_val = data.get("elevator")
        parking_val = data.get("parking")
        furnished_val = data.get("furnished")
        occ_val = data.get("occupation")

        return Property(
            id=data.get("id"),
            listing_no=data.get("listing_no", ""),
            title=data.get("title", ""),
            # Supabase'deki anahtar isimlerinin to_dict ile uyumlu olduğundan emin ol (type vs property_type)
            property_type=PropertyType(data.get("type", "Daire")),
            status=PropertyStatus(data.get("status", "Aktif")),
            price=float(data.get("price", 0)),
            m2_gross=int(data.get("m2_gross", 0)),
            m2_net=int(data.get("m2_net", 0)),
            total_floors=int(data.get("total_floors") or 0),
            floor_level=str(data.get("floor_level") or ""),
            # 🚀 GÜVENLİ DÖNÜŞÜM: Eğer veritabanında geçersiz bir string varsa varsayılana döner
            building_age=next((x for x in BuildingAge if x.value == b_age_val), BuildingAge.ZERO),
            room_count=next((x for x in RoomCount if x.value == r_count_val), RoomCount.TWO_ONE),
            heating=next((h for h in HeatingType if h.value == heating_val), HeatingType.YOK),
            kitchen_type=next((k for k in KitchenType if k.value == kitchen_val), KitchenType.KAPALI),
            balcony=next((b for b in BalconyStatus if b.value == balcony_val), BalconyStatus.YOK),
            parking=next((p for p in ParkingStatus if p.value == parking_val), ParkingStatus.YOK),
            furnished=next((f for f in FurnishedStatus if f.value == furnished_val), FurnishedStatus.ESYASIZ),
            occupation=next((o for o in OccupationStatus if o.value == occ_val), OccupationStatus.BOS),
            elevator=next((e for e in ElevatorStatus if e.value == elevator_val), ElevatorStatus.YOK),
            bath_count=int(data.get("bath_count") or 0),
            owner_id=data.get("owner_id"),
            address=data.get("address", ""),
            images=data.get("images", [])
        )
    
    def to_dict(self):
        return {
            "listing_no": self.listing_no,
            "title": self.title,
            "type": self.property_type.value,
            "status": self.status.value,
            "price": self.price,
            "m2_gross": self.m2_gross,
            "m2_net": self.m2_net,
            "floor_level": self.floor_level,
            "total_floors": self.total_floors,
            "building_age": self.building_age.value,
            "heating": self.heating.value,
            "kitchen_type": self.kitchen_type.value,
            "balcony": self.balcony.value,
            "parking": self.parking.value,
            "furnished": self.furnished.value,
            "occupation": self.occupation.value,
            "elevator": self.elevator.value,
            "bath_count": self.bath_count,
            "room_count": self.room_count.value,
            "owner_id": self.owner_id,
            "address": self.address,
            "images": self.images
        }