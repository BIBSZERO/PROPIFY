from typing import Optional
from src.core.database import db
from src.models.auth import UserSession

class AuthService:
    """
    PROPIFY Kimlik Doğrulama Servisi.
    Kullanıcı giriş, kayıt ve oturum kapatma işlemlerini yönetir.
    """
    def login(self, email:str, password: str) -> Optional[UserSession]:
        """
        E-posta ve şifre ile sisteme giriş yapar.
        Başarılıysa UserSession döner, başarısızsa None döner.
        """
        try:
            response = db.get_auth().sign_in_with_password({
                'email': email,
                'password': password
            })
            if response.session:
                print(f"✅ Giriş başarılı: {email}")
                return UserSession.from_supabase_session(response.session)
            return None
        
        except Exception as e:
            print(f"❌ Giriş hatası: {e}")
            return None
    
    def reset_password(self, email: str) -> bool:
        try:
            db.get_auth().reset_password_for_email(email)
            print(f"📧 Şifre sıfırlama maili gönderildi: {email}")
            return True
        except Exception as e:
            print(f"❌ Şifre sıfırlama hatası: {e}")
            return False
    
    def update_password(self, new_password: str) -> bool:
        try:
            db.get_auth().update_user({"password": new_password})
            print("✅ Şifre başarıyla güncellendi.")
            return True
        except Exception as e:
            print(f"❌ Şifre güncelleme hatası: {e}")
            return False
        
    def register(self, email: str, password: str) -> Optional[str]:
        """
        Sisteme yeni bir kullanıcı kaydeder ve benzersiz ID'sini (UUID) döndürür.
        """
        try:
            response = db.get_auth().sign_up({
                'email': email,
                'password': password
            })
            if response.user:
                print(f"✅ Yeni kullanıcı kaydedildi: {email}")
                return response.user.id
            
            return None
        
        except Exception as e:
            print(f"❌ Kayıt hatası: {e}")
            return None
    
    def logout(self) -> bool:
        """
        Mevcut oturumu güvenli bir şekilde kapatır.
        """
        try:
            db.get_auth().sign_out()
            print("👋 Oturum kapatıldı.")
            return True
        except Exception as e:
            print(f"❌ Çıkış hatası: {e}")
            return False

# Proje genelinde kullanılacak tekil servis nesnesi
auth_service = AuthService()