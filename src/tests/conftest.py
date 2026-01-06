import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from pydantic import EmailStr


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("CPANEL_SERVER_HOSTNAME", "smtp.test.com")
    monkeypatch.setenv("CPANEL_SERVER_PORT", "465")
    monkeypatch.setenv("EMAIL_USER", "support@test.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "test_password")
    monkeypatch.setenv("API_PORT", "8000")


@pytest.fixture
def test_client():
    """Create FastAPI test client."""
    from main import app
    return TestClient(app)


@pytest.fixture
def valid_mail_data():
    """Fixture providing valid mail data for testing."""
    return {
        "firstname": "Juan",
        "lastname": "Pérez",
        "email": "juan@example.com",
        "country_code": "593",
        "phone": "987654321",
        "city": "Quito",
        "country": "Ecuador",
        "contact_reason": "Soporte Técnico Corporativo Bitdefender",
        "requirement": "Me gustaría conocer más sobre sus servicios."
    }


@pytest.fixture
def invalid_mail_data_variants():
    """Fixture providing various invalid mail data for validation testing."""
    return {
        "short_firstname": {
            "firstname": "J",
            "lastname": "Pérez",
            "email": "juan@example.com",
            "country_code": "593",
            "phone": "987654321",
            "city": "Quito",
            "country": "Ecuador",
            "contact_reason": "Soporte Técnico Corporativo Bitdefender",
            "requirement": "Me gustaría conocer más sobre sus servicios."
        },
        "invalid_email": {
            "firstname": "Juan",
            "lastname": "Pérez",
            "email": "not_an_email",
            "country_code": "593",
            "phone": "987654321",
            "city": "Quito",
            "country": "Ecuador",
            "contact_reason": "Soporte Técnico Corporativo Bitdefender",
            "requirement": "Me gustaría conocer más sobre sus servicios."
        },
        "invalid_phone": {
            "firstname": "Juan",
            "lastname": "Pérez",
            "email": "juan@example.com",
            "country_code": "593",
            "phone": "123",
            "city": "Quito",
            "country": "Ecuador",
            "contact_reason": "Soporte Técnico Corporativo Bitdefender",
            "requirement": "Me gustaría conocer más sobre sus servicios."
        },
        "short_requirement": {
            "firstname": "Juan",
            "lastname": "Pérez",
            "email": "juan@example.com",
            "country_code": "593",
            "phone": "987654321",
            "city": "Quito",
            "country": "Ecuador",
            "contact_reason": "Soporte Técnico Corporativo Bitdefender",
            "requirement": "Hola"
        },
        "invalid_characters_in_firstname": {
            "firstname": "Juan123",
            "lastname": "Pérez",
            "email": "juan@example.com",
            "country_code": "593",
            "phone": "987654321",
            "city": "Quito",
            "country": "Ecuador",
            "contact_reason": "Soporte Técnico Corporativo Bitdefender",
            "requirement": "Me gustaría conocer más sobre sus servicios."
        }
    }


@pytest.fixture
def mock_mail_service():
    """Fixture providing a mocked MailService."""
    with patch('controllers.mail_controller.MailService') as mock:
        service_instance = MagicMock()
        mock.return_value = service_instance
        yield service_instance


@pytest.fixture
def mock_smtp_connection():
    """Fixture providing a mocked SMTP connection."""
    with patch('services.mail_service.smtplib.SMTP_SSL') as mock:
        connection = MagicMock()
        mock.return_value.__enter__.return_value = connection
        yield connection


@pytest.fixture
def mock_settings(monkeypatch):
    """Fixture providing mocked settings."""
    from config.settings import Settings
    
    mock_config = Settings()
    mock_config.cpanel_server_hostname = "smtp.test.com"
    mock_config.cpanel_server_port = 465
    mock_config.email_user = "support@test.com"
    mock_config.email_password = "test_password"
    mock_config.api_port = 8000
    
    monkeypatch.setattr("config.settings.settings", mock_config)
    return mock_config


@pytest.fixture
def mock_logger():
    """Fixture providing a mocked logger."""
    with patch('utils.logger.get_logger') as mock:
        logger_instance = MagicMock()
        mock.return_value = logger_instance
        yield logger_instance
