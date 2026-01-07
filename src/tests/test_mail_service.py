import pytest
import smtplib
from unittest.mock import Mock, patch, MagicMock, call
from services.mail_service import MailService
from schemes.mail_scheme import Mail


class TestMailServiceInitialization:
    """Test cases for MailService initialization."""
    
    def test_mail_service_initialization(self, mock_settings):
        """Test MailService initializes with correct settings."""
        service = MailService()
        
        assert service.server_hostname == "127.0.0.1"
        assert service.server_port == 465
        assert service.user_email == "XXXX"
        assert service.user_password == "XXXX"
    
    def test_mail_service_loads_settings_from_environment(self, mock_settings):
        """Test that MailService loads settings from environment."""
        service = MailService()
        
        # Verify settings are loaded
        assert service.server_hostname is not None
        assert service.server_port is not None
        assert service.user_email is not None
        assert service.user_password is not None


class TestMailServiceSendMail:
    """Test cases for MailService.send_mail method."""
    
    @pytest.fixture
    def mail_object(self, valid_mail_data):
        """Fixture providing a Mail object."""
        return Mail(**valid_mail_data)
    
    def test_send_mail_successfully(self, mock_settings, mock_smtp_connection, mail_object):
        """Test successful email sending."""
        service = MailService()
        
        # Execute
        service.send_mail(mail_object)
        
        # Verify SMTP methods were called
        mock_smtp_connection.ehlo.assert_called()
        mock_smtp_connection.starttls.assert_called()
        mock_smtp_connection.login.assert_called_once_with("XXXX", "XXXX")
        mock_smtp_connection.send_message.assert_called_once()
    
    def test_send_mail_constructs_correct_message(self, mock_settings, mock_smtp_connection, mail_object):
        """Test that send_mail constructs the email message correctly."""
        service = MailService()
        
        service.send_mail(mail_object)
        
        # Get the message that was sent
        sent_message = mock_smtp_connection.send_message.call_args[0][0]
        
        # Verify message properties
        assert sent_message['Subject'] == "Nuevo contacto de Juan Pérez"
        assert sent_message['From'] == "XXXX"
        assert sent_message['To'] == "XXXX"
    
    def test_send_mail_message_contains_contact_data(self, mock_settings, mock_smtp_connection, mail_object):
        """Test that email body contains all contact information."""
        service = MailService()
        
        service.send_mail(mail_object)
        
        # Get the message content
        sent_message = mock_smtp_connection.send_message.call_args[0][0]
        message_body = sent_message.get_content()
        
        # Verify contact information is in the message
        assert "Juan" in message_body
        assert "Pérez" in message_body
        assert "juan@example.com" in message_body
        assert "593" in message_body
        assert "987654321" in message_body
        assert "Quito" in message_body
        assert "Ecuador" in message_body
    
    def test_send_mail_with_special_characters(self, mock_settings, mock_smtp_connection):
        """Test email sending with special characters in data."""
        mail_data = {
            "firstname": "José",
            "lastname": "García",
            "email": "jose@example.com",
            "country_code": "34",
            "phone": "912345678",
            "city": "Madrid",
            "country": "España",
            "contact_reason": "¿Consulta?",
            "requirement": "Me gustaría conocer más. ¡Muchas gracias!"
        }
        mail_object = Mail(**mail_data)
        service = MailService()
        
        service.send_mail(mail_object)
        
        # Verify the message was sent successfully with special characters
        mock_smtp_connection.send_message.assert_called_once()
        sent_message = mock_smtp_connection.send_message.call_args[0][0]
        assert "José" in sent_message.get_content()
    
    def test_send_mail_smtp_authentication_error(self, mock_settings, mail_object):
        """Test handling of SMTP authentication error."""
        with patch('services.mail_service.smtplib.SMTP_SSL') as mock_smtp:
            mock_smtp.return_value.__enter__.return_value.login.side_effect = smtplib.SMTPAuthenticationError(
                535, "Authentication failed"
            )
            
            service = MailService()
            
            with pytest.raises(ConnectionError) as exc_info:
                service.send_mail(mail_object)
            
            assert "Invalid email credentials" in str(exc_info.value)
    
    def test_send_mail_smtp_exception(self, mock_settings, mail_object):
        """Test handling of general SMTP exception."""
        with patch('services.mail_service.smtplib.SMTP_SSL') as mock_smtp:
            mock_smtp.return_value.__enter__.return_value.login.side_effect = smtplib.SMTPException(
                "Connection error"
            )
            
            service = MailService()
            
            with pytest.raises(ConnectionError) as exc_info:
                service.send_mail(mail_object)
            
            assert "Error during connecting to the server" in str(exc_info.value)
    
    def test_send_mail_unexpected_error(self, mock_settings, mail_object):
        """Test handling of unexpected error during email sending."""
        with patch('services.mail_service.smtplib.SMTP_SSL') as mock_smtp:
            mock_smtp.return_value.__enter__.return_value.login.side_effect = Exception(
                "Unexpected error"
            )
            
            service = MailService()
            
            with pytest.raises(Exception):
                service.send_mail(mail_object)
    
    def test_send_mail_connection_timeout(self, mock_settings, mail_object):
        """Test handling of connection timeout."""
        with patch('services.mail_service.smtplib.SMTP_SSL') as mock_smtp:
            mock_smtp.return_value.__enter__.side_effect = TimeoutError("Connection timeout")
            
            service = MailService()
            
            with pytest.raises(TimeoutError):
                service.send_mail(mail_object)
    
    def test_send_mail_logs_connection_info(self, mock_settings, mock_smtp_connection, mail_object):
        """Test that send_mail logs SMTP connection information."""
        service = MailService()
        
        with patch('services.mail_service.logger') as mock_logger:
            service.send_mail(mail_object)
            
            # Verify logging calls were made
            mock_logger.info.assert_called()
    
    def test_send_mail_logs_success(self, mock_settings, mock_smtp_connection, mail_object):
        """Test that send_mail logs successful sending."""
        service = MailService()
        
        with patch('services.mail_service.logger') as mock_logger:
            service.send_mail(mail_object)
            
            # Find the success log call
            success_calls = [call for call in mock_logger.info.call_args_list 
                           if "successfully" in str(call).lower()]
            assert len(success_calls) > 0
    
    def test_send_mail_uses_smtp_ssl(self, mock_settings, mail_object):
        """Test that send_mail uses SMTP_SSL for secure connection."""
        with patch('services.mail_service.smtplib.SMTP_SSL') as mock_smtp:
            mock_connection = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_connection
            
            service = MailService()
            service.send_mail(mail_object)
            
            # Verify SMTP_SSL was called with correct parameters
            mock_smtp.assert_called_once_with("127.0.0.1", 465)
    
    def test_send_mail_calls_starttls(self, mock_settings, mock_smtp_connection, mail_object):
        """Test that send_mail calls starttls for TLS encryption."""
        service = MailService()
        
        service.send_mail(mail_object)
        
        # Verify starttls was called
        mock_smtp_connection.starttls.assert_called()
    
    def test_send_mail_with_various_requirement_lengths(self, mock_settings, mock_smtp_connection):
        """Test email sending with various requirement text lengths."""
        for length in [10, 100, 250, 500]:
            mail_data = {
                "firstname": "Test",
                "lastname": "User",
                "email": "test@example.com",
                "country_code": "1",
                "phone": "1234567890",
                "city": "Test City",
                "country": "Test Country",
                "contact_reason": "Test reason",
                "requirement": "A" * length
            }
            mail_object = Mail(**mail_data)
            service = MailService()
            
            service.send_mail(mail_object)
            
            # Verify message was sent
            assert mock_smtp_connection.send_message.called


class TestMailServiceErrorHandling:
    """Test cases for error handling in MailService."""
    
    def test_send_mail_logs_authentication_error(self, mock_settings, valid_mail_data):
        """Test that authentication errors are logged."""
        mail_object = Mail(**valid_mail_data)
        
        with patch('services.mail_service.smtplib.SMTP_SSL') as mock_smtp:
            mock_smtp.return_value.__enter__.return_value.login.side_effect = smtplib.SMTPAuthenticationError(
                535, "Invalid credentials"
            )
            
            with patch('services.mail_service.logger') as mock_logger:
                service = MailService()
                
                with pytest.raises(ConnectionError):
                    service.send_mail(mail_object)
                
                # Verify error was logged
                error_calls = [call for call in mock_logger.error.call_args_list 
                             if "authentication" in str(call).lower()]
                assert len(error_calls) > 0
    
    def test_send_mail_logs_unexpected_error(self, mock_settings, valid_mail_data):
        """Test that unexpected errors are logged."""
        mail_object = Mail(**valid_mail_data)
        
        with patch('services.mail_service.smtplib.SMTP_SSL') as mock_smtp:
            mock_smtp.return_value.__enter__.return_value.login.side_effect = RuntimeError(
                "Unexpected error"
            )
            
            with patch('services.mail_service.logger') as mock_logger:
                service = MailService()
                
                with pytest.raises(RuntimeError):
                    service.send_mail(mail_object)
                
                # Verify error was logged
                mock_logger.error.assert_called()
