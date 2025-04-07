import pytest
from website.models import User, Note, SharedPermission
from flask_login import current_user
from werkzeug.security import generate_password_hash

def test_complete_note_workflow(app, client):
    """Test the complete workflow: create note -> share -> delete"""
    with app.app_context():
        # Setup: Create and login user
        user = User(
            email='test@test.com',
            first_name='Test',
            password=generate_password_hash('password123')
        )
        app.db.session.add(user)
        app.db.session.commit()

        # Login
        client.post('/login', data={
            'email': 'test@test.com',
            'password': 'password123'
        })

        # 1. Create a note
        create_note_response = client.post('/', data={
            'title': 'Test Note',
            'description': 'Test Description',
            'tag': 'test'
        }, follow_redirects=True)
        assert b'Note added!' in create_note_response.data

        # Get the created note
        note = Note.query.filter_by(title='Test Note').first()
        assert note is not None

        # 2. Share the note
        share_response = client.post(f'/share-note/{note.id}', data={
            'shared_email': 'share@test.com',
            'permission_level': 'edit'
        }, follow_redirects=True)
        assert b'Shared with share@test.com!' in share_response.data

        # Verify sharing permission
        share_permission = SharedPermission.query.filter_by(
            note_id=note.id,
            email='share@test.com'
        ).first()
        assert share_permission is not None
        assert share_permission.can_edit is True

        # 3. Delete the note
        delete_response = client.post('/delete-note', json={
            'noteId': note.id
        })
        assert delete_response.status_code == 200

        # Verify note is deleted
        assert Note.query.get(note.id) is None

def test_shared_note_permissions(app, client):
    """Test shared note access and permissions"""
    with app.app_context():
        # Setup: Create users
        owner = User(
            email='owner@test.com',
            first_name='Owner',
            password=generate_password_hash('password123')
        )
        viewer = User(
            email='viewer@test.com',
            first_name='Viewer',
            password=generate_password_hash('password123')
        )
        app.db.session.add_all([owner, viewer])
        app.db.session.commit()

        # Login as owner
        client.post('/login', data={
            'email': 'owner@test.com',
            'password': 'password123'
        })

        # Create and share note
        client.post('/', data={
            'title': 'Shared Note',
            'description': 'This is a shared note',
            'tag': 'shared'
        })
        note = Note.query.filter_by(title='Shared Note').first()

        client.post(f'/share-note/{note.id}', data={
            'shared_email': 'viewer@test.com',
            'permission_level': 'view'
        })

        # Switch to viewer
        client.get('/logout')
        client.post('/login', data={
            'email': 'viewer@test.com',
            'password': 'password123'
        })

        # Test view-only permissions
        edit_response = client.post('/edit-note', data={
            'id': note.id,
            'title': 'Modified Title',
            'description': 'Modified Description',
            'tag': 'modified'
        })
        assert b'Note not found or unauthorized' in edit_response.data

        delete_response = client.post('/delete-note', json={
            'noteId': note.id
        })
        assert delete_response.status_code in [401, 403]

def test_note_operations_edge_cases(app, client):
    """Test edge cases for note operations"""
    with app.app_context():
        # Setup: Create and login user
        user = User(
            email='test@test.com',
            first_name='Test',
            password=generate_password_hash('password123')
        )
        app.db.session.add(user)
        app.db.session.commit()
        
        client.post('/login', data={
            'email': 'test@test.com',
            'password': 'password123'
        })

        # Test creating note with missing required fields
        response = client.post('/', data={
            'title': '',  # Missing title
            'description': 'Test Description'
        }, follow_redirects=True)
        assert b'Title and description are required!' in response.data

        # Test sharing note with invalid email
        note = Note(title='Test Note', description='Test', user_id=user.id)
        app.db.session.add(note)
        app.db.session.commit()

        share_response = client.post(f'/share-note/{note.id}', data={
            'shared_email': 'invalid-email',
            'permission_level': 'edit'
        }, follow_redirects=True)
        assert b'Invalid email format' in share_response.data or response.status_code != 200

        # Test operations on non-existent note
        delete_response = client.post('/delete-note', json={
            'noteId': 9999
        })
        assert delete_response.status_code in [404, 400] 