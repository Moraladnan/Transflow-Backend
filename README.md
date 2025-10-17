# Transflow-Backend

A RESTful Authentication API built with **FastAPI** and **Python 3.12+**, integrating with **Appwrite** (Backend-as-a-Service) for secure user management and session handling.

## Features

- ✅ **RESTful API** with standard endpoints
- 🔐 **Secure Authentication** (Signup, Signin, Signout)
- 🍪 **HTTP Cookie-based Sessions** for secure session management
- 🛡️ **CORS Configuration** for security
- 📝 **Pydantic Models** for data validation
- 🚀 **FastAPI** with automatic OpenAPI documentation
- ⚡ **Uvicorn** ASGI server for production-ready deployment
- 🔌 **Appwrite Integration** for user management

## Tech Stack

- **FastAPI** 0.115.0 - Modern, fast web framework
- **Uvicorn** 0.31.0 - Lightning-fast ASGI server
- **Pydantic** 2.9.2 - Data validation using Python type annotations
- **Appwrite** 5.1.1 - Backend-as-a-Service for user management
- **Python** 3.12+

## Project Structure

```
Transflow-Backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application setup
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py      # Configuration settings
│   │   └── appwrite.py      # Appwrite client setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── auth.py          # Pydantic models for auth
│   └── routes/
│       ├── __init__.py
│       └── auth.py          # Authentication endpoints
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.12 or higher
- Appwrite account and project ([Sign up here](https://appwrite.io/))

### 1. Clone the Repository

```bash
git clone https://github.com/Moraladnan/Transflow-Backend.git
cd Transflow-Backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and update with your Appwrite credentials:

```bash
cp .env.example .env
```

Edit `.env` and configure:

```env
# Appwrite Configuration
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id_here
APPWRITE_API_KEY=your_api_key_here

# Application Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Session Configuration
SESSION_COOKIE_NAME=transflow_session
SESSION_COOKIE_MAX_AGE=604800
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=lax
```

**Getting Appwrite Credentials:**
1. Create an account at [Appwrite Cloud](https://cloud.appwrite.io/)
2. Create a new project
3. Copy the **Project ID** from project settings
4. Generate an **API Key** with `users.read` and `users.write` scopes

### 5. Run the Application

```bash
python run.py
```

Or use Uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### Health Check

- **GET** `/` - Root endpoint with API information
- **GET** `/health` - Health check endpoint

### Authentication

#### 1. Sign Up (Register)

**POST** `/auth/signup`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "message": "User created and signed in successfully",
  "user": {
    "$id": "5f7d8e9a0b1c2d3e4f5g6h7i",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerification": false
  }
}
```

#### 2. Sign In (Login)

**POST** `/auth/signin`

Authenticate an existing user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "message": "User signed in successfully",
  "user": {
    "$id": "5f7d8e9a0b1c2d3e4f5g6h7i",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerification": false
  }
}
```

#### 3. Sign Out (Logout)

**POST** `/auth/signout`

End the current user session.

**Response (200 OK):**
```json
{
  "message": "User signed out successfully",
  "user": null
}
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Security Features

### CORS (Cross-Origin Resource Sharing)

CORS is configured to allow requests from specified origins (configured in `.env`):
- Supports credentials (cookies)
- Configurable allowed origins
- Supports all standard HTTP methods

### Session Management

- Sessions are stored as **HTTP-only cookies** (not accessible via JavaScript)
- Configurable cookie settings (secure, SameSite, max age)
- Session tokens managed by Appwrite

### Data Validation

- All request data validated using **Pydantic models**
- Email validation using `EmailStr`
- Password minimum length enforcement
- Automatic error responses for invalid data

## Error Handling

The API provides clear error messages:

- **400 Bad Request**: Validation errors or user already exists
- **401 Unauthorized**: Invalid credentials
- **500 Internal Server Error**: Server-side errors

Example error response:
```json
{
  "detail": "A user with this email already exists"
}
```

## Development

### Running in Development Mode

```bash
python run.py
```

This enables auto-reload on code changes.

### Testing Endpoints

You can test the API using:

1. **Swagger UI**: http://localhost:8000/docs (interactive)
2. **cURL**:
   ```bash
   # Sign Up
   curl -X POST http://localhost:8000/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"SecurePass123!","name":"Test User"}'
   
   # Sign In
   curl -X POST http://localhost:8000/auth/signin \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"SecurePass123!"}'
   
   # Sign Out
   curl -X POST http://localhost:8000/auth/signout
   ```

3. **Postman** or any API client

## Production Deployment

For production deployment:

1. Set `SESSION_COOKIE_SECURE=True` in `.env`
2. Use a production-grade server (Uvicorn with Gunicorn)
3. Set up HTTPS/TLS
4. Configure appropriate CORS origins
5. Use environment variables for secrets

```bash
# Production run with Gunicorn + Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on GitHub.