import pytest
from website import create_app, db
from website.models import User, Note
from flask_login import login_user
import os
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='function')
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'MAIL_SUPPRESS_SEND': True,  # 禁用邮件发送
        'LOGIN_DISABLED': False,
        'SECRET_KEY': 'test_secret_key',
        'SERVER_NAME': None,  # 移除 SERVER_NAME 配置
        'SESSION_TYPE': 'filesystem',
        'SESSION_COOKIE_SECURE': False,
        'SESSION_COOKIE_HTTPONLY': True,
        'PRESERVE_CONTEXT_ON_EXCEPTION': False
    })
    
    # 创建应用上下文
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """A test runner for the app."""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def test_user(app):
    """Create a test user for authentication tests."""
    with app.app_context():
        # 创建测试用户
        user = User(
            email='test@example.com',
            first_name='Test',
            password=generate_password_hash('test123', method='pbkdf2:sha256')
        )
        db.session.add(user)
        db.session.commit()
        return user 