"""Kullanıcı yanlış bir e-posta girdiğinde veya şifreyi boş bıraktığında 
veritabanına gidip hata almadan önce burada "vize kontrolü" yapacağız.
"""
import re

class Validators:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """E-posta formatını kontrol eder."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def strong_password(password: str) -> bool:
        """Şifrenin güvenlik standartlarına (min 6 karakter) uygunluğunu kontrol eder."""
        return len(password) >= 6
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Türkiye telefon formatına (5xx...) uygunluğu kontrol eder."""
        clean_phone = re.sub(r'\D', '', phone) # Sadece rakamları tut
        return len(clean_phone) == 10 and clean_phone.startswith('5')