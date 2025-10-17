"""
Pydantic models for authentication requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Request model for user signup."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="User password (min 8 characters)")
    name: str = Field(..., min_length=1, max_length=128, description="User's full name")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "SecurePass123!",
                    "name": "John Doe"
                }
            ]
        }
    }


class SigninRequest(BaseModel):
    """Request model for user signin."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "SecurePass123!"
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """Response model for user data."""
    
    id: str = Field(..., alias="$id", description="User ID")
    email: str = Field(..., description="User email address")
    name: str = Field(..., description="User's full name")
    email_verification: bool = Field(..., alias="emailVerification", description="Email verification status")
    
    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "$id": "5f7d8e9a0b1c2d3e4f5g6h7i",
                    "email": "user@example.com",
                    "name": "John Doe",
                    "emailVerification": False
                }
            ]
        }
    }


class AuthResponse(BaseModel):
    """Response model for authentication operations."""
    
    message: str = Field(..., description="Response message")
    user: UserResponse | None = Field(None, description="User data (for signup and signin)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "User signed in successfully",
                    "user": {
                        "$id": "5f7d8e9a0b1c2d3e4f5g6h7i",
                        "email": "user@example.com",
                        "name": "John Doe",
                        "emailVerification": False
                    }
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Response model for errors."""
    
    detail: str = Field(..., description="Error message")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "detail": "Invalid credentials"
                }
            ]
        }
    }
