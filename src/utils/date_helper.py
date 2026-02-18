from datetime import datetime, timedelta

class DateHelper:
    @staticmethod
    def to_supabase_format(date_obj: datetime) -> str:
        """Python datetime objesini Supabase ISO formatına çevirir."""
        return date_obj.isoformat()
    
    @staticmethod
    def get_readable_date(iso_string: str) -> str:
        """ISO tarihini '18 Şubat 2026' formatına çevirir."""
        try:
            if not iso_string:
                return "-"
            dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
            return dt.strftime("%d %B %Y")
        except Exception as e:
            print(f"❌ Tarih dönüştürme hatası: {e}")
            return str(iso_string)