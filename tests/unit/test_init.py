from website import create_app
from website.models import db
import os

def test_create_app(app):
    """Test app creation with test configuration."""
    assert app is not None
    assert app.config['TESTING'] is True
    assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']

def test_app_context(app):
    """Test application context and database initialization."""
    with app.app_context():
        assert db.engine is not None
        assert 'sqlite' in str(db.engine.url)

def test_blueprints_registered(app):
    """Test that all blueprints are registered."""
    assert 'auth' in app.blueprints
    assert 'views' in app.blueprints

def test_config_values(app):
    """Test configuration values."""
    assert app.config['SECRET_KEY'] is not None
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False 