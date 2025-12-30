"""
Mail Controller Module

This module handles the business logic for mail operations.
It acts as an intermediary between routes and services.

Author: ISHelper Team
Version: 1.0.0
"""

from services.mail_service import MailService
from schemes.mail_scheme import Mail
from utils.logger import get_logger

logger = get_logger(__name__)


class MailController:
    """Controller for handling mail operations.
    
    This class orchestrates mail-related operations and coordinates
    between the route handlers and the mail service layer.
    """
    
    def __init__(self):
        """Initialize the MailController with a MailService instance."""
        self.mail_service = MailService()
    
    def send_contact_mail(self, mail: Mail) -> dict:
        """
        Process and send a contact email.
        
        This method handles the business logic for sending contact emails,
        including validation and service coordination.
        
        Args:
            mail (Mail): The mail request object containing sender and message information.
        
        Returns:
            dict: A response dictionary with success status and message.
                Contains keys: 'success', 'message', 'email', 'sender_name'
        
        Raises:
            Exception: May raise exceptions from MailService if email sending fails.
        """
        logger.info(f"Processing contact requirement for {mail.email}")
        
        self.mail_service.send_mail(mail)
        
        logger.info(f"Contact requirement successfully processed from {mail.email}")
        
        return {
            "success": True,
            "message": "Tu mensaje ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
            "email": mail.email,
            "sender_name": f"{mail.firstname} {mail.lastname}"
        }

