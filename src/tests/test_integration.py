# """
# Integration Tests for Mail API

# This module contains integration tests that test multiple components together.
# It tests the full flow from HTTP request to email sending.

# Author: ISHelper Team
# Version: 1.0.0
# """

# import pytest
# from unittest.mock import patch, MagicMock
# from fastapi import status


# class TestFullEmailSendingFlow:
#     """Test cases for the complete email sending flow."""
    
#     def test_full_flow_send_mail_to_smtp(self, test_client, valid_mail_data, mock_settings, mock_smtp_connection):
#         """Test the complete flow from API request to SMTP sending."""
#         with patch('routes.mail.MailController') as mock_controller_class:
#             mock_controller = MagicMock()
#             mock_controller.send_contact_mail.return_value = {
#                 "success": True,
#                 "message": "Tu mensaje ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
#                 "email": valid_mail_data['email'],
#                 "sender_name": f"{valid_mail_data['firstname']} {valid_mail_data['lastname']}"
#             }
#             mock_controller_class.return_value = mock_controller
            
#             # Make HTTP request
#             response = test_client.post("/mail/send", json=valid_mail_data)
            
#             # Verify HTTP response
#             assert response.status_code == status.HTTP_200_OK
#             data = response.json()
#             assert data['success'] is True
#             assert data['email'] == valid_mail_data['email']
    
#     def test_health_check_before_sending_mail(self, test_client, valid_mail_data, mock_settings):
#         """Test health check passes before sending mail."""
#         with patch('routes.mail.MailController') as mock_controller_class:
#             mock_controller = MagicMock()
#             mock_controller_class.return_value = mock_controller
            
#             # First, check health
#             health_response = test_client.get("/mail/health")
#             assert health_response.status_code == status.HTTP_200_OK
            
#             # Then, send mail
#             mock_controller.send_contact_mail.return_value = {
#                 "success": True,
#                 "message": "Tu mensaje ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
#                 "email": valid_mail_data['email'],
#                 "sender_name": f"{valid_mail_data['firstname']} {valid_mail_data['lastname']}"
#             }
            
#             mail_response = test_client.post("/mail/send", json=valid_mail_data)
#             assert mail_response.status_code == status.HTTP_200_OK


# class TestErrorHandlingFlow:
#     """Test cases for error handling across the entire application flow."""
    
#     def test_validation_error_response_format(self, test_client, mock_settings):
#         """Test that validation errors have proper response format."""
#         invalid_data = {
#             "firstname": "J",
#             "lastname": "Pérez",
#             "email": "juan@example.com",
#             "country_code": "593",
#             "phone": "987654321",
#             "city": "Quito",
#             "country": "Ecuador",
#             "contact_reason": "Consulta general",
#             "requirement": "Me gustaría conocer más sobre sus servicios."
#         }
        
#         response = test_client.post("/mail/send", json=invalid_data)
        
#         assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#         # Verify error response has detail field
#         assert 'detail' in response.json()
    
#     def test_service_error_500_response(self, test_client, valid_mail_data, mock_settings):
#         """Test that service errors return 500 status code."""
#         with patch('routes.mail.MailController') as mock_controller_class:
#             mock_controller = MagicMock()
#             mock_controller.send_contact_mail.side_effect = RuntimeError("Unexpected error")
#             mock_controller_class.return_value = mock_controller
            
#             response = test_client.post("/mail/send", json=valid_mail_data)
            
#             assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


# class TestMultipleRequests:
#     """Test cases for handling multiple requests."""
    
#     def test_multiple_sequential_requests(self, test_client, mock_settings):
#         """Test handling multiple sequential requests."""
#         with patch('routes.mail.MailController') as mock_controller_class:
#             mock_controller = MagicMock()
#             mock_controller.send_contact_mail.return_value = {
#                 "success": True,
#                 "message": "Tu mensaje ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
#                 "email": "test@example.com",
#                 "sender_name": "Test User"
#             }
#             mock_controller_class.return_value = mock_controller
            
#             mail_data = {
#                 "firstname": "Test",
#                 "lastname": "User",
#                 "email": "test@example.com",
#                 "country_code": "1",
#                 "phone": "1234567890",
#                 "city": "Test City",
#                 "country": "Test Country",
#                 "contact_reason": "Test reason",
#                 "requirement": "This is a test requirement for testing purposes."
#             }
            
#             # Send multiple requests
#             for i in range(3):
#                 response = test_client.post("/mail/send", json=mail_data)
#                 assert response.status_code == status.HTTP_200_OK
#                 data = response.json()
#                 assert data['success'] is True
    
#     def test_multiple_health_checks(self, test_client, mock_settings):
#         """Test multiple health check requests."""
#         with patch('routes.mail.MailController') as mock_controller_class:
#             mock_controller = MagicMock()
#             mock_controller_class.return_value = mock_controller
            
#             # Make multiple health checks
#             for i in range(3):
#                 response = test_client.get("/mail/health")
#                 assert response.status_code == status.HTTP_200_OK
#                 data = response.json()
#                 assert data['status'] == "healthy"
