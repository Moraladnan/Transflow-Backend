"""Config package initialization."""
from app.config.settings import settings
from app.config.appwrite import get_appwrite_client, get_account_service

__all__ = ["settings", "get_appwrite_client", "get_account_service"]
