import pytest
from flask import url_for

def test_create_note(logged_in_client):
    """Test note creation."""
    response = logged_in_client.post('/', data={
        'title': 'New Test Note',
        'description': 'This is a new test note',
        'tag': 'test'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'New Test Note' in response.data
    assert b'Note added!' in response.data

def test_edit_note(logged_in_client, test_note):
    """Test note editing."""
    response = logged_in_client.post('/edit-note', data={
        'id': test_note.id,
        'title': 'Updated Note',
        'description': 'This is an updated note',
        'tag': 'updated'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Updated Note' in response.data
    assert b'Note updated!' in response.data

def test_delete_note(logged_in_client, test_note):
    """Test note deletion."""
    response = logged_in_client.post('/delete-note', 
        json={'noteId': test_note.id},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Test Note' not in response.data

def test_share_note(logged_in_client, test_note):
    """Test note sharing."""
    response = logged_in_client.post(f'/share-note/{test_note.id}', data={
        'shared_email': 'shared@example.com',
        'permission_level': 'edit'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Shared with shared@example.com!' in response.data

def test_filter_notes(logged_in_client, test_note):
    """Test note filtering."""
    response = logged_in_client.get('/?tag=test')
    assert response.status_code == 200
    assert b'Test Note' in response.data 