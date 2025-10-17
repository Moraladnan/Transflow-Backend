#!/usr/bin/env python3
"""
Simple test script to verify API endpoints.
Note: Actual Appwrite integration requires valid credentials in .env file.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoints."""
    print("🔍 Testing health endpoints...")
    
    # Root endpoint
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ GET / -> {response.status_code}")
    print(f"   Response: {response.json()}\n")
    
    # Health endpoint
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ GET /health -> {response.status_code}")
    print(f"   Response: {response.json()}\n")

def test_validation():
    """Test Pydantic validation."""
    print("🔍 Testing data validation...")
    
    # Invalid email
    invalid_data = {
        "email": "not-an-email",
        "password": "123",
        "name": ""
    }
    response = requests.post(f"{BASE_URL}/auth/signup", json=invalid_data)
    print(f"❌ POST /auth/signup (invalid data) -> {response.status_code}")
    print(f"   Validation errors detected: {len(response.json()['detail'])} errors\n")

def test_signup():
    """Test signup endpoint."""
    print("🔍 Testing signup endpoint...")
    
    valid_data = {
        "email": "test@example.com",
        "password": "SecurePass123!",
        "name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/auth/signup", json=valid_data)
    print(f"📝 POST /auth/signup (valid data) -> {response.status_code}")
    print(f"   Note: Will fail without valid Appwrite credentials\n")

def test_signout():
    """Test signout endpoint."""
    print("🔍 Testing signout endpoint...")
    
    response = requests.post(f"{BASE_URL}/auth/signout")
    print(f"✅ POST /auth/signout -> {response.status_code}")
    print(f"   Response: {response.json()}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Transflow Backend API - Endpoint Test")
    print("=" * 60 + "\n")
    
    try:
        test_health()
        test_validation()
        test_signup()
        test_signout()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        print("\n📖 View API documentation at: http://localhost:8000/docs")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server.")
        print("   Please ensure the server is running: python run.py")
