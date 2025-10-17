"""
Appwrite client configuration and initialization.
"""
from appwrite.client import Client
from appwrite.services.account import Account
from app.config.settings import settings


def get_appwrite_client() -> Client:
    """
    Create and configure an Appwrite client instance.
    
    Returns:
        Client: Configured Appwrite client
    """
    client = Client()
    client.set_endpoint(settings.appwrite_endpoint)
    client.set_project(settings.appwrite_project_id)
    client.set_key(settings.appwrite_api_key)
    return client


def get_account_service(client: Client = None) -> Account:
    """
    Get Appwrite Account service instance.
    
    Args:
        client: Optional Appwrite client. If not provided, creates a new one.
    
    Returns:
        Account: Appwrite Account service
    """
    if client is None:
        client = get_appwrite_client()
    return Account(client)
