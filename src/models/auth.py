from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class UserSession:
    user_id: str
    email: str
    access_token: str
    refresh_token: str
    expires_at: Optional[int] = None

    @staticmethod
    def from_supabase_session(session_data: Any):
        """Supabase'in kendi session objesini bizim modelimize çevirir."""
        return UserSession(
            user_id=session_data.user.id,
            email=session_data.user.email,
            access_token=session_data.access_token,
            refresh_token=session_data.refresh_token,
            expires_at=session_data.expires_at
        )