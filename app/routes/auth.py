"""
Authentication routes for signup, signin, and signout.
"""
from fastapi import APIRouter, Response, HTTPException, status
from appwrite.exception import AppwriteException
from appwrite.id import ID
from app.models.auth import (
    SignupRequest,
    SigninRequest,
    AuthResponse,
    UserResponse,
    ErrorResponse
)
from app.config import get_appwrite_client, get_account_service, settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created successfully"},
        400: {"model": ErrorResponse, "description": "Bad request - validation error or user already exists"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Register a new user",
    description="Create a new user account with email, password, and name."
)
async def signup(user_data: SignupRequest, response: Response):
    """
    Register a new user account.
    
    Args:
        user_data: User signup information
        response: FastAPI response object for setting cookies
    
    Returns:
        AuthResponse with user data and success message
    
    Raises:
        HTTPException: If user creation fails
    """
    try:
        client = get_appwrite_client()
        account = get_account_service(client)
        
        # Create user account
        user = account.create(
            user_id=ID.unique(),
            email=user_data.email,
            password=user_data.password,
            name=user_data.name
        )
        
        # Create email session (signs in the user)
        session = account.create_email_password_session(
            email=user_data.email,
            password=user_data.password
        )
        
        # Set session cookie
        response.set_cookie(
            key=settings.session_cookie_name,
            value=session["secret"],
            max_age=settings.session_cookie_max_age,
            httponly=settings.session_cookie_httponly,
            secure=settings.session_cookie_secure,
            samesite=settings.session_cookie_samesite
        )
        
        # Prepare user response
        user_response = UserResponse(
            **user
        )
        
        return AuthResponse(
            message="User created and signed in successfully",
            user=user_response
        )
        
    except AppwriteException as e:
        # Handle Appwrite-specific errors
        error_message = str(e)
        if "user_already_exists" in error_message.lower() or "already exists" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {error_message}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post(
    "/signin",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User signed in successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized - invalid credentials"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Sign in a user",
    description="Authenticate a user with email and password, creating a session."
)
async def signin(credentials: SigninRequest, response: Response):
    """
    Sign in an existing user.
    
    Args:
        credentials: User login credentials
        response: FastAPI response object for setting cookies
    
    Returns:
        AuthResponse with user data and success message
    
    Raises:
        HTTPException: If authentication fails
    """
    try:
        client = get_appwrite_client()
        account = get_account_service(client)
        
        # Create email session
        session = account.create_email_password_session(
            email=credentials.email,
            password=credentials.password
        )
        
        # Set session cookie
        response.set_cookie(
            key=settings.session_cookie_name,
            value=session["secret"],
            max_age=settings.session_cookie_max_age,
            httponly=settings.session_cookie_httponly,
            secure=settings.session_cookie_secure,
            samesite=settings.session_cookie_samesite
        )
        
        # Get user data using the session
        client_with_session = get_appwrite_client()
        client_with_session.set_session(session["secret"])
        account_with_session = get_account_service(client_with_session)
        user = account_with_session.get()
        
        # Prepare user response
        user_response = UserResponse(
            **user
        )
        
        return AuthResponse(
            message="User signed in successfully",
            user=user_response
        )
        
    except AppwriteException as e:
        error_message = str(e)
        if "invalid credentials" in error_message.lower() or "unauthorized" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sign in: {error_message}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post(
    "/signout",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User signed out successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized - no active session"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Sign out a user",
    description="End the user's current session and clear the session cookie."
)
async def signout(response: Response):
    """
    Sign out the current user.
    
    Args:
        response: FastAPI response object for clearing cookies
    
    Returns:
        AuthResponse with success message
    
    Raises:
        HTTPException: If signout fails
    """
    try:
        # Note: In a real implementation, you would:
        # 1. Get the session token from the cookie
        # 2. Use it to authenticate with Appwrite
        # 3. Delete the session via Appwrite
        # For now, we'll just clear the cookie as a basic implementation
        
        # Clear session cookie
        response.delete_cookie(
            key=settings.session_cookie_name,
            httponly=settings.session_cookie_httponly,
            secure=settings.session_cookie_secure,
            samesite=settings.session_cookie_samesite
        )
        
        return AuthResponse(
            message="User signed out successfully",
            user=None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
