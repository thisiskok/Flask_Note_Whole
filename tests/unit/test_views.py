import pytest
from website.views import views
from website.models import Note, User, SharedPermission
from flask import url_for
from flask_login import current_user, login_user
from website import db

@pytest.fixture
def test_note(app, test_user):
    """Create a test note fixture."""
    with app.app_context():
        note = Note(
            title="Test Note",
            description="Test Description",
            tag="test",
            user_id=test_user
        )
        db.session.add(note)
        db.session.commit()
        return note.id  # 返回笔记ID

def test_create_note(app, client, logged_in_client):
    """Test note creation functionality."""
    with app.app_context():
        # Test with unauthenticated user
        response = client.post('/', data={
            'title': 'Test Note',
            'description': 'Test Description',
            'tag': 'test'
        })
        assert response.status_code in [302, 401]  # Either redirect to login or unauthorized

        # Test with authenticated user
        response = logged_in_client.post('/', data={
            'title': 'Test Note',
            'description': 'Test Description',
            'tag': 'test'
        })
        assert response.status_code in [200, 302]  # Success or redirect

def test_delete_note(app, client, logged_in_client, test_note):
    """Test note deletion functionality."""
    with app.app_context():
        # Test with unauthenticated user
        response = client.post('/delete-note', json={
            'noteId': test_note
        })
        assert response.status_code in [302, 401]  # Either redirect to login or unauthorized

        # Test with authenticated user
        response = logged_in_client.post('/delete-note', json={
            'noteId': test_note
        })
        assert response.status_code in [200, 302]  # Success or redirect

def test_share_note(app, client, logged_in_client, test_note):
    """Test note sharing functionality."""
    with app.app_context():
        # Create a user to share with
        share_with_email = "share@test.com"

        # Test sharing note
        response = logged_in_client.post(f'/share-note/{test_note}', data={
            'shared_email': share_with_email,
            'permission_level': 'edit'
        })
        assert response.status_code in [200, 302]  # Success or redirect

def test_get_home_page(app, logged_in_client):
    """Test retrieving home page with notes."""
    with app.app_context():
        response = logged_in_client.get('/')
        assert response.status_code in [200, 302]  # Success or redirect
        if response.status_code == 200:
            assert b'Notes' in response.data 