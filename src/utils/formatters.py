import re
class Formatters:
    @staticmethod
    def format_money(amount: float) -> str:
        """Rakamı TL formatına çevirir (Örn: 1.250.000 TL)."""
        try:
            return f"{amount:,.0f}".replace(",", ".").replace(".","-").replace("-",".").replace("-",",") + " TL"
        except (ValueError, TypeError):
            return "0 TL"
    
    @staticmethod
    def format_phone_display(phone: str) -> str:
        """Numarayı okunabilir yapar: (543) 159 06 37."""
        p = re.sub(r'\D', '', phone)
        if len(p) == 10:
            return f"({p[:3]}) {p[3:6]} {p[6:8]} {p[8:]}"
        return phone
        