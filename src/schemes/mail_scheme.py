"""
Mail Schema Module

This module defines the Pydantic schemas for email validation.
It provides request body validation for mail endpoints.

Author: ISHelper Team
Version: 1.0.0
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class Mail(BaseModel):
    """Schema for mail contact requests.
    
    This model defines the structure and validation rules for contact email submissions.
    All fields are validated according to the specified patterns and constraints.
    
    Attributes:
        firstname (str): Sender's first name. Must be 2-35 characters with valid characters.
        lastname (str): Sender's last name. Must be 2-35 characters with valid characters.
        email (EmailStr): Sender's email address. Must be a valid email format.
        country_code (str): International country calling code (e.g., '593' for Ecuador).
        phone (str): Sender's phone number. Must be 8-15 digits.
        city (str): Sender's city. Must be 2-60 characters with valid characters.
        country (str): Sender's country. Must be 2-100 characters with valid characters.
        contact_reason (str): Reason for contact. Must be 3-100 characters.
        requirement (str): Detailed requirement or message. Free-form text field.
    """
    
    firstname: str = Field(
        min_length=2,
        max_length=35,
        description="Sender's first name",
        pattern=r"^[a-zA-ZÀ-ÿ\u00f1\u00d1\s'-]+$",
        example="Juan"
    )

    lastname: str = Field(
        min_length=2,
        max_length=35,
        description="Sender's last name",
        pattern=r"^[a-zA-ZÀ-ÿ\u00f1\u00d1\s'-]+$",
        example="Pérez"
    )

    email: EmailStr = Field(
        description="Sender's email address in valid format",
        example="juan@example.com"
    )

    country_code: str = Field(
        description="International country calling code (e.g., 593 for Ecuador)",
        pattern=r"^\d{1,4}",
        example="593"
    )

    phone: str = Field(
        description="Phone number (8-15 digits)",
        pattern=r"^[1-9][0-9]{7,14}$",
        example="987654321"
    )

    city: str = Field(
        min_length=2,
        max_length=60,
        description="Sender's city",
        pattern=r"^[a-zA-ZÀ-ÿ\u00f1\u00d1\s'-]+$",
        example="Quito"
    )

    country: str = Field(
        min_length=2,
        max_length=100,
        description="Sender's country",
        pattern=r"^[a-zA-ZÀ-ÿ\u00f1\u00d1\s'.-]+$",
        example="Ecuador"
    )

    contact_reason: str = Field(
        description="Reason for contacting (3-100 characters)",
        pattern=r'^[a-zA-ZÀ-ÿ\u00f1\u00d1\s?¿!¡.,]{3,100}$',
        example="General inquiry"
    )

    requirement: str = Field(
        description="Detailed requirement or message",
        example="I would like to know more about your services."
    )


    requirement: str = Field(
        min_length=10,
        max_length=500,
        description="Detalle del requerimiento"
    )
    
    model_config = ConfigDict(extra="forbid")

