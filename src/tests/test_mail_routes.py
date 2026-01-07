import pytest
from unittest.mock import patch, MagicMock
from fastapi import status
from fastapi.testclient import TestClient

class TestHealthCheckEndpoint:
    """Test cases for GET /mail/health endpoint."""
    
    def test_health_check_success(self, test_client, mock_settings):
        """Test successful health check response."""
        with patch('routes.mail.MailController') as mock_controller_class:
            mock_controller = MagicMock()
            mock_controller_class.return_value = mock_controller
             
            response = test_client.get("/mail/health")
            
            # Verify response
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data['status'] == "healthy"
            assert data['service'] == "mail_service"
            assert "operational" in data['message'].lower()
    
    def test_health_check_response_structure(self, test_client, mock_settings):
        """Test health check response has correct structure."""
        with patch('routes.mail.MailController') as mock_controller_class:
            mock_controller = MagicMock()
            mock_controller_class.return_value = mock_controller
            
            response = test_client.get("/mail/health")
            
            data = response.json()
            assert 'status' in data
            assert 'service' in data
            assert 'message' in data
            assert isinstance(data['status'], str)
            assert isinstance(data['message'], str)
    
    def test_health_check_creates_mail_controller(self, test_client, mock_settings):
        """Test that health check creates a MailController."""
        with patch('routes.mail.MailController') as mock_controller_class:
            mock_controller = MagicMock()
            mock_controller_class.return_value = mock_controller
            
            test_client.get("/mail/health")
            
            # Verify MailController was instantiated
            mock_controller_class.assert_called()
    
    def test_health_check_service_unavailable_on_error(self, test_client, mock_settings):
        """Test health check returns 503 when controller fails."""
        with patch('routes.mail.MailController') as mock_controller_class:
            mock_controller_class.side_effect = Exception("Service initialization failed")
            
            response = test_client.get("/mail/health")
            
            # Verify service unavailable response
            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    
    def test_health_check_rate_limiting(self, mock_settings, monkeypatch):
        """Test rate limiting on health check endpoint (5 per minute)."""
        from main import app
        
        # Create fresh test client
        fresh_client = TestClient(app)
        
        # First 5 requests should succeed
        for i in range(5):
            response = fresh_client.get("/mail/health")
            assert response.status_code == status.HTTP_200_OK
        
        # 6th request should be rate limited
        response = fresh_client.get("/mail/health")
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


class TestSendContactMailEndpoint:
    """Test cases for POST /mail/send endpoint."""
    
    def test_send_contact_mail_success(self, test_client, valid_mail_data, mock_settings, mock_mail_controller_instance):
        """Test successful contact mail sending."""
        mock_mail_controller_instance.send_contact_mail.return_value = {
            "success": True,
            "message": "Tu mensaje ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
            "email": valid_mail_data['email'],
            "sender_name": f"{valid_mail_data['firstname']} {valid_mail_data['lastname']}"
        }
        
        with patch('services.mail_service.smtplib.SMTP_SSL'):
            response = test_client.post("/mail/send", json=valid_mail_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data['success'] is True
            assert "exitosamente" in data['message']
    
    def test_send_contact_mail_response_structure(self, test_client, valid_mail_data, mock_settings, mock_mail_controller_instance):
        """Test send contact mail response structure."""
        mock_mail_controller_instance.send_contact_mail.return_value = {
            "success": True,
            "message": "Tu mensaje ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
            "email": valid_mail_data['email'],
            "sender_name": f"{valid_mail_data['firstname']} {valid_mail_data['lastname']}"
        }
        
        with patch('services.mail_service.smtplib.SMTP_SSL'):
            response = test_client.post("/mail/send", json=valid_mail_data)
            
            data = response.json()
            assert 'success' in data
            assert 'message' in data
            assert 'email' in data
            assert 'sender_name' in data
    
    def test_send_contact_mail_with_invalid_email(self, test_client, mock_settings):
        """Test sending with invalid email format."""
        invalid_data = {
            "firstname": "Juan",
            "lastname": "Pérez",
            "email": "not_an_email",
            "country_code": "593",
            "phone": "987654321",
            "city": "Quito",
            "country": "Ecuador",
            "contact_reason": "Consulta general",
            "requirement": "Me gustaría conocer más sobre sus servicios."
        }
        
        response = test_client.post("/mail/send", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_send_contact_mail_with_short_firstname(self, test_client, mock_settings):
        """Test sending with firstname too short."""
        invalid_data = {
            "firstname": "J",
            "lastname": "Pérez",
            "email": "juan@example.com",
            "country_code": "593",
            "phone": "987654321",
            "city": "Quito",
            "country": "Ecuador",
            "contact_reason": "Consulta general",
            "requirement": "Me gustaría conocer más sobre sus servicios."
        }
        
        response = test_client.post("/mail/send", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_send_contact_mail_with_short_requirement(self, test_client, mock_settings):
        """Test sending with requirement too short."""
        invalid_data = {
            "firstname": "Juan",
            "lastname": "Pérez",
            "email": "juan@example.com",
            "country_code": "593",
            "phone": "987654321",
            "city": "Quito",
            "country": "Ecuador",
            "contact_reason": "Consulta general",
            "requirement": "Hola"
        }
        
        response = test_client.post("/mail/send", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_send_contact_mail_missing_field(self, test_client, mock_settings):
        """Test sending with missing required field."""
        incomplete_data = {
            "firstname": "Juan",
            "lastname": "Pérez",
            "email": "juan@example.com",
            "country_code": "593",
            "phone": "987654321",
            "city": "Quito",
            # missing country and other fields
            "contact_reason": "Consulta general",
            "requirement": "Me gustaría conocer más sobre sus servicios."
        }
        
        response = test_client.post("/mail/send", json=incomplete_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_send_contact_mail_with_extra_field(self, test_client, valid_mail_data, mock_settings):
        """Test sending with extra field (should fail due to ConfigDict(extra='forbid'))."""
        data_with_extra = {
            **valid_mail_data,
            "extra_field": "not allowed"
        }
        
        response = test_client.post("/mail/send", json=data_with_extra)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_send_contact_mail_calls_controller(self, test_client, valid_mail_data, mock_settings, mock_mail_controller_instance):
        """Test that endpoint calls the controller."""
        mock_mail_controller_instance.send_contact_mail.return_value = {
            "success": True,
            "message": "Tu mensaje ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
            "email": valid_mail_data['email'],
            "sender_name": f"{valid_mail_data['firstname']} {valid_mail_data['lastname']}"
        }
        
        with patch('services.mail_service.smtplib.SMTP_SSL'):
            test_client.post("/mail/send", json=valid_mail_data)
            
            # Verify controller method was called
            mock_mail_controller_instance.send_contact_mail.assert_called_once()
    
    def test_send_contact_mail_value_error_response(self, test_client, valid_mail_data, mock_settings, mock_mail_controller_instance):
        """Test handling of ValueError from controller."""
        mock_mail_controller_instance.send_contact_mail.side_effect = ValueError("Invalid data")
        
        with patch('services.mail_service.smtplib.SMTP_SSL'):
            response = test_client.post("/mail/send", json=valid_mail_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "Invalid data" in data['detail']
    
    def test_send_contact_mail_connection_error_response(self, test_client, valid_mail_data, mock_settings, mock_mail_controller_instance):
        """Test handling of ConnectionError from controller."""
        mock_mail_controller_instance.send_contact_mail.side_effect = ConnectionError("SMTP server unreachable")
        
        with patch('services.mail_service.smtplib.SMTP_SSL'):
            response = test_client.post("/mail/send", json=valid_mail_data)
        
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        data = response.json()
        assert "Could not connect to the mail server" in data['detail']
    
    def test_send_contact_mail_generic_error_response(self, test_client, valid_mail_data, mock_settings):
        """Test handling of generic Exception from controller."""
        with patch('routes.mail.MailController') as mock_controller_class:
            mock_controller = MagicMock()
            mock_controller.send_contact_mail.side_effect = Exception("Unexpected error")
            mock_controller_class.return_value = mock_controller
            
            response = test_client.post("/mail/send", json=valid_mail_data)
            
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def test_send_contact_mail_rate_limiting(self, valid_mail_data, mock_settings, mock_mail_controller_instance, monkeypatch):
        """Test rate limiting on send endpoint (10 per minute)."""
        from main import app
        from middlewares.rate_limiting import limiter
        
        # Create fresh test client for this test
        fresh_client = TestClient(app)
        
        mock_mail_controller_instance.send_contact_mail.return_value = {
            "success": True,
            "message": "Tu mensaje ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
            "email": valid_mail_data['email'],
            "sender_name": f"{valid_mail_data['firstname']} {valid_mail_data['lastname']}"
        }
        
        with patch('services.mail_service.smtplib.SMTP_SSL'):
            # First 10 requests should succeed
            for i in range(10):
                response = fresh_client.post("/mail/send", json=valid_mail_data)
                assert response.status_code == status.HTTP_200_OK
            
            # 11th request should be rate limited
            response = fresh_client.post("/mail/send", json=valid_mail_data)
            assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


class TestMailRoutesMetadata:
    """Test cases for route metadata and documentation."""
    
    def test_health_check_has_correct_status_code(self, mock_settings, monkeypatch):
        """Test that health check endpoint has correct status code metadata."""
        from main import app
        
        # Use a separate isolated test client instance
        fresh_client = TestClient(app)
        
        response = fresh_client.get("/mail/health")
        
        # Verify the actual response status
        assert response.status_code == status.HTTP_200_OK
    
    def test_send_endpoint_accepts_post(self, test_client, valid_mail_data, mock_settings):
        """Test that send endpoint only accepts POST requests."""
        # POST should work
        with patch('routes.mail.MailController') as mock_controller_class:
            mock_controller = MagicMock()
            mock_controller.send_contact_mail.return_value = {
                "success": True,
                "message": "Tu mensaje ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
                "email": valid_mail_data['email'],
                "sender_name": f"{valid_mail_data['firstname']} {valid_mail_data['lastname']}"
            }
            mock_controller_class.return_value = mock_controller
            
            response = test_client.post("/mail/send", json=valid_mail_data)
            assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED
        
        # GET should not be allowed
        response = test_client.get("/mail/send")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_health_endpoint_accepts_get(self, test_client, mock_settings):
        """Test that health endpoint only accepts GET requests."""
        with patch('routes.mail.MailController') as mock_controller_class:
            mock_controller = MagicMock()
            mock_controller_class.return_value = mock_controller
            
            # GET should work
            response = test_client.get("/mail/health")
            assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED
            
            # POST should not be allowed
            response = test_client.post("/mail/health", json={})
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
