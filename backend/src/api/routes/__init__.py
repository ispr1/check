"""
API Routes Package.

Registers all route modules.
"""

from .face import router as face_router
from .documents import router as documents_router

__all__ = [
    "face_router",
    "documents_router",
]
