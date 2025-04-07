from website.utils import send_email
from unittest.mock import patch, MagicMock
import pytest

def test_send_email_single_recipient(app):
    """Test sending email to a single recipient."""
    with app.app_context():
        with patch('website.utils.EmailMessage') as mock_email:
            mock_instance = MagicMock()
            mock_email.return_value = mock_instance
            
            send_email(
                to="test@test.com",
                subject="Test Subject",
                body="Test Body"
            )
            
            mock_email.assert_called_once()
            mock_instance.send.assert_called_once()

def test_send_email_multiple_recipients(app):
    """Test sending email to multiple recipients."""
    with app.app_context():
        with patch('website.utils.EmailMessage') as mock_email:
            mock_instance = MagicMock()
            mock_email.return_value = mock_instance
            
            recipients = ["test1@test.com", "test2@test.com"]
            send_email(
                to=recipients,
                subject="Test Subject",
                body="Test Body"
            )
            
            mock_email.assert_called_once()
            mock_instance.send.assert_called_once()

def test_send_email_with_custom_sender(app):
    """Test sending email with a custom sender."""
    with app.app_context():
        with patch('website.utils.EmailMessage') as mock_email:
            mock_instance = MagicMock()
            mock_email.return_value = mock_instance
            
            send_email(
                to="test@test.com",
                subject="Test Subject",
                body="Test Body",
                from_email="sender@test.com"
            )
            
            mock_email.assert_called_once()
            mock_instance.send.assert_called_once() 