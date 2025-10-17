# Transflow Backend - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Application                       │
│                    (Browser, Mobile App, etc.)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS
                             │ (CORS Enabled)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              CORS Middleware Layer                      │   │
│  │  - Allow specified origins                              │   │
│  │  - Handle credentials (cookies)                         │   │
│  └──────────────────┬─────────────────────────────────────┘   │
│                     │                                           │
│  ┌──────────────────▼─────────────────────────────────────┐   │
│  │              Route Handlers                             │   │
│  │                                                          │   │
│  │  POST /auth/signup    - User Registration               │   │
│  │  POST /auth/signin    - User Authentication             │   │
│  │  POST /auth/signout   - Session Termination             │   │
│  │  GET  /               - Health Check                     │   │
│  │  GET  /health         - Health Status                    │   │
│  └──────────────────┬─────────────────────────────────────┘   │
│                     │                                           │
│  ┌──────────────────▼─────────────────────────────────────┐   │
│  │           Pydantic Models (Validation)                  │   │
│  │                                                          │   │
│  │  - SignupRequest     (email, password, name)            │   │
│  │  - SigninRequest     (email, password)                  │   │
│  │  - UserResponse      (user data structure)              │   │
│  │  - AuthResponse      (API responses)                    │   │
│  │  - ErrorResponse     (error handling)                   │   │
│  └──────────────────┬─────────────────────────────────────┘   │
│                     │                                           │
│  ┌──────────────────▼─────────────────────────────────────┐   │
│  │              Appwrite Client                            │   │
│  │                                                          │   │
│  │  - Account Service                                       │   │
│  │  - Session Management                                    │   │
│  │  - User CRUD Operations                                  │   │
│  └──────────────────┬─────────────────────────────────────┘   │
│                     │                                           │
└─────────────────────┼───────────────────────────────────────────┘
                      │
                      │ REST API
                      │ (HTTPS)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Appwrite BaaS Platform                        │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              User Management Service                    │   │
│  │                                                          │   │
│  │  - User Registration                                     │   │
│  │  - Authentication                                        │   │
│  │  - Session Management                                    │   │
│  │  - Email Verification                                    │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                  Database                               │   │
│  │                                                          │   │
│  │  - User Data                                             │   │
│  │  - Session Tokens                                        │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow

### 1. User Signup Flow

```
Client                   FastAPI                Appwrite
  │                        │                       │
  ├─ POST /auth/signup ───>│                       │
  │  {email, password,     │                       │
  │   name}                │                       │
  │                        │                       │
  │                        ├─ Validate Input       │
  │                        │  (Pydantic)           │
  │                        │                       │
  │                        ├─ Create Account ─────>│
  │                        │                       │
  │                        │                       ├─ Store User
  │                        │                       │
  │                        │<─ User Created ───────┤
  │                        │                       │
  │                        ├─ Create Session ─────>│
  │                        │                       │
  │                        │                       ├─ Generate Token
  │                        │                       │
  │                        │<─ Session Token ──────┤
  │                        │                       │
  │                        ├─ Set Cookie           │
  │                        │  (HTTP-only)          │
  │                        │                       │
  │<─ 201 Created ─────────┤                       │
     {message, user}       │                       │
     Set-Cookie: session   │                       │
```

### 2. User Signin Flow

```
Client                   FastAPI                Appwrite
  │                        │                       │
  ├─ POST /auth/signin ───>│                       │
  │  {email, password}     │                       │
  │                        │                       │
  │                        ├─ Validate Input       │
  │                        │  (Pydantic)           │
  │                        │                       │
  │                        ├─ Authenticate ───────>│
  │                        │                       │
  │                        │                       ├─ Verify Credentials
  │                        │                       │
  │                        │<─ Session Token ──────┤
  │                        │                       │
  │                        ├─ Get User Data ──────>│
  │                        │                       │
  │                        │<─ User Info ──────────┤
  │                        │                       │
  │                        ├─ Set Cookie           │
  │                        │  (HTTP-only)          │
  │                        │                       │
  │<─ 200 OK ──────────────┤                       │
     {message, user}       │                       │
     Set-Cookie: session   │                       │
```

### 3. User Signout Flow

```
Client                   FastAPI                Appwrite
  │                        │                       │
  ├─ POST /auth/signout ──>│                       │
  │  Cookie: session       │                       │
  │                        │                       │
  │                        ├─ Delete Session ─────>│
  │                        │  (optional)           │
  │                        │                       │
  │                        ├─ Clear Cookie         │
  │                        │                       │
  │<─ 200 OK ──────────────┤                       │
     {message}             │                       │
     Clear Cookie          │                       │
```

## Security Features

### 1. HTTP Cookie Configuration
- **HTTP-only**: Prevents JavaScript access (XSS protection)
- **Secure**: HTTPS-only in production
- **SameSite**: CSRF protection (lax/strict)
- **Max-Age**: Session expiration (7 days default)

### 2. CORS Protection
- Whitelist allowed origins
- Credentials support (cookies)
- Specific HTTP methods allowed
- Custom headers configuration

### 3. Data Validation
- Email format validation (EmailStr)
- Password minimum length (8 chars)
- Required field enforcement
- Type checking (Pydantic)

### 4. Error Handling
- Proper HTTP status codes
- No sensitive data exposure
- User-friendly error messages
- Appwrite exception handling

## Configuration

### Environment Variables
```env
APPWRITE_ENDPOINT        - Appwrite API endpoint
APPWRITE_PROJECT_ID      - Project identifier
APPWRITE_API_KEY         - Server API key

API_HOST                 - Server host (0.0.0.0)
API_PORT                 - Server port (8000)
CORS_ORIGINS             - Allowed origins (CSV)

SESSION_COOKIE_NAME      - Cookie name
SESSION_COOKIE_MAX_AGE   - Cookie lifetime (seconds)
SESSION_COOKIE_SECURE    - HTTPS only flag
SESSION_COOKIE_HTTPONLY  - HTTP-only flag
SESSION_COOKIE_SAMESITE  - SameSite policy
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | FastAPI 0.119.0 | Async API framework |
| ASGI Server | Uvicorn 0.37.0 | Production server |
| Validation | Pydantic 2.12.2 | Data validation |
| BaaS | Appwrite 13.4.1 | User management |
| Config | python-dotenv | Environment vars |
| Email | email-validator | Email validation |

## API Documentation

Interactive documentation is automatically generated:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`
