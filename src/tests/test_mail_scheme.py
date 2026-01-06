import pytest
from pydantic import ValidationError
from schemes.mail_scheme import Mail


class TestMailSchemeValidation:
    """Test cases for Mail schema validation."""
    
    def test_valid_mail_data(self, valid_mail_data):
        """Test that valid mail data passes validation."""
        mail = Mail(**valid_mail_data)
        assert mail.firstname == "Juan"
        assert mail.lastname == "Pérez"
        assert mail.email == "juan@example.com"
        assert mail.country_code == "593"
        assert mail.phone == "987654321"
        assert mail.city == "Quito"
        assert mail.country == "Ecuador"
        assert mail.contact_reason == "Soporte Técnico Corporativo Bitdefender"
        assert mail.requirement == "Me gustaría conocer más sobre sus servicios."
    
    def test_firstname_min_length(self):
        """Test firstname minimum length validation."""
        with pytest.raises(ValidationError) as exc_info:
            Mail(
                firstname="J",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
        assert "at least 2 characters" in str(exc_info.value)
    
    def test_firstname_max_length(self):
        """Test firstname maximum length validation."""
        long_name = "A" * 36
        with pytest.raises(ValidationError) as exc_info:
            Mail(
                firstname=long_name,
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
        assert "at most 35 characters" in str(exc_info.value)
    
    def test_firstname_invalid_characters(self):
        """Test firstname pattern validation with invalid characters."""
        with pytest.raises(ValidationError) as exc_info:
            Mail(
                firstname="Juan123",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
        assert "String should match pattern" in str(exc_info.value)
    
    def test_firstname_with_special_characters_allowed(self):
        """Test firstname with allowed special characters (apostrophe, hyphen)."""
        mail = Mail(
            firstname="Jean-Pierre",
            lastname="O'Brien",
            email="jean@example.com",
            country_code="33",
            phone="123456789",
            city="Paris",
            country="France",
            contact_reason="Soporte Técnico Corporativo Bitdefender",
            requirement="I would like to know more about your services and pricing."
        )
        assert mail.firstname == "Jean-Pierre"
        assert mail.lastname == "O'Brien"
    
    def test_lastname_validation(self):
        """Test lastname follows same rules as firstname."""
        with pytest.raises(ValidationError):
            Mail(
                firstname="Juan",
                lastname="P",
                email="juan@example.com",
                country_code="593",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
    
    def test_invalid_email_format(self):
        """Test email validation with invalid format."""
        with pytest.raises(ValidationError) as exc_info:
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="not_an_email",
                country_code="593",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
        assert "value is not a valid email address" in str(exc_info.value).lower()
    
    def test_email_with_valid_formats(self):
        """Test email validation with various valid formats."""
        valid_emails = [
            "user@example.com",
            "user+tag@example.co.uk",
            "first.last@example.org",
            "user123@sub.example.com"
        ]
        
        for email in valid_emails:
            mail = Mail(
                firstname="Juan",
                lastname="Pérez",
                email=email,
                country_code="593",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
            assert mail.email == email
    
    def test_country_code_pattern(self):
        """Test country code pattern validation."""
        # Valid country codes
        mail = Mail(
            firstname="Juan",
            lastname="Pérez",
            email="juan@example.com",
            country_code="1",
            phone="987654321",
            city="Quito",
            country="Ecuador",
            contact_reason="Soporte Técnico Corporativo Bitdefender",
            requirement="Me gustaría conocer más sobre sus servicios."
        )
        assert mail.country_code == "1"
        
        # Invalid country code (non-numeric)
        with pytest.raises(ValidationError):
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="juan@example.com",
                country_code="ABC",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
    
    def test_phone_min_length(self):
        """Test phone minimum length validation."""
        with pytest.raises(ValidationError):
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="1234567",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
    
    def test_phone_max_length(self):
        """Test phone maximum length validation."""
        with pytest.raises(ValidationError):
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="123456789012345123",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
    
    def test_phone_cannot_start_with_zero(self):
        """Test that phone number cannot start with zero."""
        with pytest.raises(ValidationError):
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="0987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
    
    def test_city_validation(self):
        """Test city field validation."""
        with pytest.raises(ValidationError):
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="987654321",
                city="Q",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
    
    def test_country_validation(self):
        """Test country field validation."""
        with pytest.raises(ValidationError):
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="987654321",
                city="Quito",
                country="E",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
    
    def test_contact_reason_min_length(self):
        """Test contact_reason minimum length validation."""
        with pytest.raises(ValidationError):
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="ab",
                requirement="Me gustaría conocer más sobre sus servicios."
            )
    
    def test_contact_reason_max_length(self):
        """Test contact_reason maximum length validation."""
        long_reason = "A" * 101
        with pytest.raises(ValidationError):
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason=long_reason,
                requirement="Me gustaría conocer más sobre sus servicios."
            )
    
    def test_requirement_min_length(self):
        """Test requirement minimum length validation."""
        with pytest.raises(ValidationError):
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Hola"
            )
    
    def test_requirement_max_length(self):
        """Test requirement maximum length validation."""
        long_requirement = "A" * 501
        with pytest.raises(ValidationError):
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement=long_requirement
            )
    
    def test_extra_fields_not_allowed(self):
        """Test that extra fields are not allowed due to ConfigDict(extra='forbid')."""
        with pytest.raises(ValidationError) as exc_info:
            Mail(
                firstname="Juan",
                lastname="Pérez",
                email="juan@example.com",
                country_code="593",
                phone="987654321",
                city="Quito",
                country="Ecuador",
                contact_reason="Soporte Técnico Corporativo Bitdefender",
                requirement="Me gustaría conocer más sobre sus servicios.",
                extra_field="not allowed"
            )
        assert "extra_field" in str(exc_info.value).lower()
    
    def test_mail_schema_as_dict(self, valid_mail_data):
        """Test Mail schema can be converted to dictionary."""
        mail = Mail(**valid_mail_data)
        mail_dict = mail.model_dump()
        
        assert isinstance(mail_dict, dict)
        assert len(mail_dict) == 9
        assert all(key in mail_dict for key in valid_mail_data.keys())
    
    def test_mail_schema_json_serializable(self, valid_mail_data):
        """Test Mail schema is JSON serializable."""
        mail = Mail(**valid_mail_data)
        json_str = mail.model_dump_json()
        
        assert isinstance(json_str, str)
        assert "juan@example.com" in json_str
        assert "Pérez" in json_str
