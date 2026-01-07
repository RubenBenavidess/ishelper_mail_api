import pytest
from unittest.mock import Mock, patch, MagicMock
from controllers.mail_controller import MailController
from schemes.mail_scheme import Mail


class TestMailControllerInitialization:
    """Test cases for MailController initialization."""
    
    def test_mail_controller_initialization(self, mock_settings):
        """Test MailController initializes with MailService."""
        with patch('controllers.mail_controller.MailService') as mock_service:
            controller = MailController()
            
            # Verify MailService was instantiated
            mock_service.assert_called_once()
    
    def test_mail_controller_has_mail_service_instance(self, mock_settings):
        """Test that MailController has a MailService instance."""
        with patch('controllers.mail_controller.MailService'):
            controller = MailController()
            
            # Verify mail_service attribute exists
            assert hasattr(controller, 'mail_service')
            assert controller.mail_service is not None


class TestSendContactMail:
    """Test cases for MailController.send_contact_mail method."""
    
    @pytest.fixture
    def mail_object(self, valid_mail_data):
        """Fixture providing a Mail object."""
        return Mail(**valid_mail_data)
    
    def test_send_contact_mail_success(self, mock_settings, mock_mail_service, mail_object):
        """Test successful contact mail sending."""
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            
            controller = MailController()
            result = controller.send_contact_mail(mail_object)
            
            # Verify the result structure
            assert isinstance(result, dict)
            assert result['success'] is True
            assert 'message' in result
            assert result['email'] == "juan@example.com"
            assert result['sender_name'] == "Juan Pérez"
    
    def test_send_contact_mail_calls_service(self, mock_settings, mock_mail_service, mail_object):
        """Test that send_contact_mail calls MailService.send_mail."""
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            
            controller = MailController()
            controller.send_contact_mail(mail_object)
            
            # Verify send_mail was called with the mail object
            mock_mail_service.send_mail.assert_called_once_with(mail_object)
    
    def test_send_contact_mail_response_message(self, mock_settings, mock_mail_service, mail_object):
        """Test that response message is in Spanish."""
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            
            controller = MailController()
            result = controller.send_contact_mail(mail_object)
            
            # Verify message is in Spanish
            assert "Tu mensaje ha sido enviado exitosamente" in result['message']
            assert "Nos pondremos en contacto pronto" in result['message']
    
    def test_send_contact_mail_includes_sender_name(self, mock_settings, mock_mail_service, mail_object):
        """Test that response includes sender name."""
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            
            controller = MailController()
            result = controller.send_contact_mail(mail_object)
            
            # Verify sender name is correctly formatted
            assert result['sender_name'] == "Juan Pérez"
            assert result['sender_name'] == f"{mail_object.firstname} {mail_object.lastname}"
    
    def test_send_contact_mail_includes_email(self, mock_settings, mock_mail_service, mail_object):
        """Test that response includes sender email."""
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            
            controller = MailController()
            result = controller.send_contact_mail(mail_object)
            
            # Verify email is included
            assert result['email'] == mail_object.email
    
    def test_send_contact_mail_service_exception_propagates(self, mock_settings, mock_mail_service, mail_object):
        """Test that exceptions from MailService are propagated."""
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            mock_mail_service.send_mail.side_effect = ConnectionError("SMTP connection failed")
            
            controller = MailController()
            
            with pytest.raises(ConnectionError):
                controller.send_contact_mail(mail_object)
    
    def test_send_contact_mail_with_different_names(self, mock_settings, mock_mail_service):
        """Test send_contact_mail with different user names."""
        test_cases = [
            ("José", "García"),
            ("Jean-Pierre", "Dupont"),
            ("María", "López"),
            ("Patrick", "O'Brien")
        ]
        
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            
            for firstname, lastname in test_cases:
                mail_data = {
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": f"{firstname.lower()}@example.com",
                    "country_code": "1",
                    "phone": "1234567890",
                    "city": "Test City",
                    "country": "Test Country",
                    "contact_reason": "Test reason",
                    "requirement": "This is a test requirement message for testing purposes."
                }
                mail_object = Mail(**mail_data)
                controller = MailController()
                
                result = controller.send_contact_mail(mail_object)
                
                # Verify the response
                assert result['sender_name'] == f"{firstname} {lastname}"
                assert result['email'] == mail_object.email
    
    def test_send_contact_mail_response_structure(self, mock_settings, mock_mail_service, mail_object):
        """Test that response has correct structure with all required fields."""
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            
            controller = MailController()
            result = controller.send_contact_mail(mail_object)
            
            # Verify all required keys are present
            required_keys = ['success', 'message', 'email', 'sender_name']
            assert all(key in result for key in required_keys)
            
            # Verify value types
            assert isinstance(result['success'], bool)
            assert isinstance(result['message'], str)
            assert isinstance(result['email'], str)
            assert isinstance(result['sender_name'], str)
    
    def test_send_contact_mail_logging(self, mock_settings, mock_mail_service, mail_object):
        """Test that send_contact_mail logs appropriately."""
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            with patch('controllers.mail_controller.logger') as mock_logger:
                mock_service_class.return_value = mock_mail_service
                
                controller = MailController()
                controller.send_contact_mail(mail_object)
                
                # Verify logging calls were made
                assert mock_logger.info.called
    
    def test_send_contact_mail_always_returns_success_true(self, mock_settings, mock_mail_service, mail_object):
        """Test that successful send_contact_mail always returns success=True."""
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            
            # Test multiple times with different data
            for i in range(5):
                mail_data = {
                    "firstname": f"TestUser",
                    "lastname": f"LastName",
                    "email": f"user{i}@example.com",
                    "country_code": "1",
                    "phone": "1234567890",
                    "city": "Test City",
                    "country": "Test Country",
                    "contact_reason": "Test reason",
                    "requirement": "This is a test requirement for testing purposes."
                }
                mail_object = Mail(**mail_data)
                controller = MailController()
                
                result = controller.send_contact_mail(mail_object)
                assert result['success'] is True


class TestMailControllerErrorHandling:
    """Test cases for error handling in MailController."""
    
    def test_send_contact_mail_connection_error(self, mock_settings, mock_mail_service, valid_mail_data):
        """Test handling of connection errors from MailService."""
        mail_object = Mail(**valid_mail_data)
        
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            mock_mail_service.send_mail.side_effect = ConnectionError("SMTP server unreachable")
            
            controller = MailController()
            
            with pytest.raises(ConnectionError):
                controller.send_contact_mail(mail_object)
    
    def test_send_contact_mail_value_error(self, mock_settings, mock_mail_service, valid_mail_data):
        """Test handling of value errors from MailService."""
        mail_object = Mail(**valid_mail_data)
        
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            mock_mail_service.send_mail.side_effect = ValueError("Invalid email configuration")
            
            controller = MailController()
            
            with pytest.raises(ValueError):
                controller.send_contact_mail(mail_object)
    
    def test_send_contact_mail_generic_exception(self, mock_settings, mock_mail_service, valid_mail_data):
        """Test handling of generic exceptions from MailService."""
        mail_object = Mail(**valid_mail_data)
        
        with patch('controllers.mail_controller.MailService') as mock_service_class:
            mock_service_class.return_value = mock_mail_service
            mock_mail_service.send_mail.side_effect = Exception("Unexpected error")
            
            controller = MailController()
            
            with pytest.raises(Exception):
                controller.send_contact_mail(mail_object)
