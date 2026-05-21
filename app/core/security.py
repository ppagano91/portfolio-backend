"""
Security utilities placeholder for future admin authentication.

When implementing admin auth, consider:
- JWT or session-based authentication
- Password hashing with passlib/bcrypt
- Role-based access for write endpoints
"""

from app.core.config import get_settings


def get_secret_key() -> str:
    return get_settings().secret_key
