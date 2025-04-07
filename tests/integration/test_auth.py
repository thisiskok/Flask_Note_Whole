import pytest
from website.models import User
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from bs4 import BeautifulSoup
from flask import session
from flask_login import current_user

def get_flashed_messages(response):
    """Extract flashed messages from response HTML."""
    soup = BeautifulSoup(response.data, 'html.parser')
    messages = []
    alerts = soup.find_all('div', class_=lambda x: x and ('alert' in x))
    for alert in alerts:
        [button.decompose() for button in alert.find_all('button')]
        message = alert.get_text(strip=True)
        if message:
            messages.append(message)
    return messages

def test_login_page(client):
    """Test login page access."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_signup_page(client):
    """Test signup page access."""
    response = client.get('/sign-up')
    assert response.status_code == 200
    assert b'Sign Up' in response.data

def test_user_creation(test_app):
    """Test user creation in database."""
    with test_app.app_context():
        # 创建用户
        user = User(
            email='test2@example.com',  # 使用不同的邮箱避免冲突
            first_name='Test2',
            password=generate_password_hash('test123')
        )
        db.session.add(user)
        db.session.commit()

        # 验证用户
        saved_user = User.query.filter_by(email='test2@example.com').first()
        assert saved_user is not None
        assert saved_user.first_name == 'Test2'
        assert check_password_hash(saved_user.password, 'test123')

def test_login_process(client, test_user):
    """Test the login process."""
    with client.session_transaction() as sess:
        sess['_fresh'] = True
    
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'test123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Logged in successfully!' in response.data

def test_invalid_login(client):
    """Test login with invalid credentials."""
    response = client.post('/login', data={
        'email': 'wrong@example.com',
        'password': 'wrongpass'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Email does not exist' in response.data

def test_signup_process(app, client):
    """Test the signup process."""
    response = client.post('/sign-up', data={
        'email': 'new@example.com',
        'firstName': 'New',
        'password1': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Account created!' in response.data
    
    with app.app_context():
        user = User.query.filter_by(email='new@example.com').first()
        assert user is not None
        assert user.first_name == 'New'

def test_signup_validation(client):
    """Test signup validation."""
    response = client.post('/sign-up', data={
        'email': 'inv',
        'firstName': 'Test',
        'password1': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Email must be greater than 3 characters' in response.data

def test_logout(client, test_user):
    """Test logout process."""
    # 先登录
    with client.session_transaction() as sess:
        sess['_fresh'] = True
    
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'test123'
    }, follow_redirects=True)
    
    # 然后登出
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data 