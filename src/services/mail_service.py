"""
Mail Service Module

This module handles email sending operations using SMTP protocol.
It manages connections to the email server and email composition.

Author: ISHelper Team
Version: 1.0.0
"""

import smtplib
from email.message import EmailMessage
from schemes.mail_scheme import Mail
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class MailService:
	"""Service for sending emails via SMTP.
	
	This class manages SMTP connections and handles the actual email sending process.
	It uses cPanel SMTP credentials for authentication.
	"""

	def __init__(self):
		"""Initialize the MailService with SMTP server credentials.
		
		Loads configuration from settings including:
		- SMTP server hostname
		- SMTP server port
		- Email user credentials
		- Email password
		"""
		self.server_hostname = settings.cpanel_server_hostname
		self.server_port = settings.cpanel_server_port
		self.user_email = settings.email_user
		self.user_password = settings.email_password
		logger.info("MailService successfully initialized")
  
	def send_mail(self, mail: Mail) -> None:
		"""
		Send an email with contact information.
		
		This method constructs an email message from the Mail object and sends it
		through an SMTP server using SSL/TLS encryption.
		
		Args:
			mail (Mail): The Mail object containing sender and message information.
		
		Returns:
			None
		
		Raises:
			ConnectionError: If SMTP authentication fails or connection issues occur.
			Exception: For unexpected errors during email sending.
		
		Email Details:
			- Uses SMTP_SSL for secure connection
			- Authenticates with configured email credentials
			- Sends email to the configured admin email address
		"""
     
		msg = EmailMessage()
		
		body = f"""
Datos de contacto:
- Nombre: {mail.firstname} {mail.lastname}
- Email: {mail.email}
- País: {mail.country}
- Ciudad: {mail.city}
- Código de país: {mail.country_code}
- Teléfono: {mail.country_code} {mail.phone}

Motivo de contacto: {mail.contact_reason}

Requerimiento:
{mail.requirement}
		"""

		msg.set_content(body)

		msg['Subject'] = f"Nuevo contacto de {mail.firstname} {mail.lastname}"
		msg['From'] = self.user_email
		msg['To'] = self.user_email

		try:
			logger.info(f"Connecting to SMTP server: {self.server_hostname}:{self.server_port}")
			
			with smtplib.SMTP_SSL(self.server_hostname, int(self.server_port)) as server:
				server.ehlo()
				server.starttls()
				server.ehlo()
				server.login(self.user_email, self.user_password)
				server.send_message(msg)
				
				logger.info(f"Email has been sent successfully from {mail.email}")
				
		except smtplib.SMTPAuthenticationError as e:
			logger.error(f"SMTP authentication error: {str(e)}")
			raise ConnectionError("Invalid email credentials") from e
			
		except smtplib.SMTPException as e:
			logger.error(f"SMTP Error: {str(e)}")
			raise ConnectionError("Error during connecting to the server") from e
			
		except Exception as e:
			logger.error(f"Unexpected error when sending email: {str(e)}")
			raise

