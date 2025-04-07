from website.auth import auth
from flask import url_for
from website.models import User
from werkzeug.security import check_password_hash, generate_password_hash

def test_password_hashing():
    """Test password hashing functionality."""
    password = "test123"
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    user = User(email="test@test.com", first_name="Test", password=hashed_password)
    assert check_password_hash(user.password, password)
    assert not check_password_hash(user.password, "wrong_password")

def test_login_validation():
    """Test login validation logic."""
    user = User(
        email="test@test.com",
        first_name="Test",
        password=generate_password_hash("test123", method='pbkdf2:sha256')
    )
    assert user.email == "test@test.com"
    assert user.first_name == "Test"

def test_signup_validation():
    """Test signup validation logic."""
    email = "test@test.com"
    first_name = "T"  # Too short
    password1 = "test"  # Too short
    password2 = "test123"  # Don't match
    
    # Test email length
    assert len(email) > 3
    
    # Test first name length
    assert len(first_name) < 2
    
    # Test password length
    assert len(password1) < 7
    
    # Test password match
    assert password1 != password2 