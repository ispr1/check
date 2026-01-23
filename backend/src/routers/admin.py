from fastapi import APIRouter, Depends
from ..models import User
from ..dependencies import require_roles

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/health")
async def admin_health_check(admin_user: User = Depends(require_roles("admin"))):
    """
    Admin-only health check endpoint.

    Requires admin role. Returns server status and admin info.
    """
    return {
        "status": "healthy",
        "message": "Admin access granted",
        "admin": {
            "id": admin_user.id,
            "email": admin_user.email,
            "role": admin_user.role,
        },
    }
