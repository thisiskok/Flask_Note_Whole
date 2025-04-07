from website.models import User, Note, SharedPermission

def test_user_creation():
    """Test user creation."""
    user = User(
        email='test@example.com',
        first_name='Test',
        password='test123'
    )
    assert user.email == 'test@example.com'
    assert user.first_name == 'Test'
    assert user.password == 'test123'

def test_note_creation():
    """Test note creation."""
    note = Note(
        title='Test Note',
        description='This is a test note',
        tag='test',
        tag_color='#FF0000',
        user_id=1
    )
    assert note.title == 'Test Note'
    assert note.description == 'This is a test note'
    assert note.tag == 'test'
    assert note.tag_color == '#FF0000'
    assert note.user_id == 1

def test_shared_permission_creation():
    """Test shared permission creation."""
    permission = SharedPermission(
        note_id=1,
        email='shared@example.com',
        can_edit=True
    )
    assert permission.note_id == 1
    assert permission.email == 'shared@example.com'
    assert permission.can_edit is True 