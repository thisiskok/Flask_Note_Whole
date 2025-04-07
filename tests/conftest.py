import pytest
from website import create_app, db
from website.models import User, Note, SharedPermission
from flask_login import login_user
import os
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'MAIL_DEFAULT_SENDER': 'test@example.com',
        'LOGIN_DISABLED': False
    })
    
    # Create tables and context
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def test_user(app):
    """Create a test user."""
    with app.app_context():
        user = User(
            email="test@test.com",
            first_name="Test",
            password=generate_password_hash("password123", method='pbkdf2:sha256')
        )
        db.session.add(user)
        db.session.commit()
        return user.id  # 返回用户ID

@pytest.fixture
def test_note(app, test_user):
    """Create a test note."""
    with app.app_context():
        note = Note(
            title='Test Note',
            description='This is a test note',
            tag='test',
            tag_color='#FF0000',
            user_id=test_user
        )
        db.session.add(note)
        db.session.commit()
        return note.id  # 返回笔记ID

@pytest.fixture
def logged_in_client(app, client, test_user):
    """A test client with logged in user."""
    with app.app_context():
        user = User.query.get(test_user)
        # 确保用户存在
        if not user:
            user = User(
                email="test@test.com",
                first_name="Test",
                password=generate_password_hash("password123", method='pbkdf2:sha256')
            )
            db.session.add(user)
            db.session.commit()
        
        # 登录用户
        with client.session_transaction() as session:
            session['_user_id'] = str(user.id)
            session['_fresh'] = True
        
        # 执行实际的登录
        with client:
            login_user(user)
            client.get('/')  # 发送一个请求来确保登录状态
        
        return client 