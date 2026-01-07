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


@pytest.fixture(autouse=True)
def reset_slowapi_storage():
    """Reset slowapi rate limiter storage before each test."""
    from middlewares.rate_limiting import limiter
    
    # Clear the rate limiter storage before test
    try:
        # slowapi Limiter stores the storage object internally
        # We need to access and clear the actual storage
        if hasattr(limiter, '_storage'):
            # Direct storage attribute
            if hasattr(limiter._storage, 'storage'):
                limiter._storage.storage.clear()
            else:
                limiter._storage.clear()
        elif hasattr(limiter, '_limiter'):
            # Alternative location in some versions
            if hasattr(limiter._limiter, 'storage'):
                limiter._limiter.storage.storage.clear()
    except Exception as e:
        # If we can't clear the storage normally, try to access it via the strategy
        try:
            import limits
            # Get the storage backend that was created
            if hasattr(limiter, 'backend'):
                limiter.backend.clear()
        except:
            pass
    
    yield
    
    # Also reset after the test
    try:
        if hasattr(limiter, '_storage'):
            if hasattr(limiter._storage, 'storage'):
                limiter._storage.storage.clear()
            else:
                limiter._storage.clear()
        elif hasattr(limiter, '_limiter'):
            if hasattr(limiter._limiter, 'storage'):
                limiter._limiter.storage.storage.clear()
    except Exception as e:
        try:
            import limits
            if hasattr(limiter, 'backend'):
                limiter.backend.clear()
        except:
            pass


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
def mock_settings():
    """Fixture providing mocked settings."""
    mock_config = MagicMock()
    mock_config.cpanel_server_hostname = "smtp.test.com"
    mock_config.cpanel_server_port = 465
    mock_config.email_user = "support@test.com"
    mock_config.email_password = "test_password"
    mock_config.api_port = 8000
    
    with patch('config.settings.settings', mock_config):
        yield mock_config


@pytest.fixture
def mock_logger():
    """Fixture providing a mocked logger."""
    with patch('utils.logger.get_logger') as mock:
        logger_instance = MagicMock()
        mock.return_value = logger_instance
        yield logger_instance


@pytest.fixture
def mock_mail_controller_instance(monkeypatch):
    """Fixture that replaces the global mail_controller instance in routes.mail module."""
    from routes import mail as mail_module
    
    mock_controller = MagicMock()
    # By default, set up a successful response
    mock_controller.send_contact_mail.return_value = {
        "success": True,
        "message": "Tu mensaje ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
        "email": "juan@example.com",
        "sender_name": "Juan Pérez"
    }
    
    # Replace the module-level mail_controller
    monkeypatch.setattr(mail_module, 'mail_controller', mock_controller)
    
    return mock_controller
