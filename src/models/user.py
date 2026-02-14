from enum import Enum
from dataclasses import dataclass
from typing import Optional

class UserRole(Enum):
    ADMIN = "admin"
    AGENT = "agent"
    VIEWER = "viewer"

@dataclass
class User:
    id: str
    email: str
    full_name: str = ""
    phone: Optional[str] = None
    role: UserRole = UserRole.AGENT
    is_active: bool = True
