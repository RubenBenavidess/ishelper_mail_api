import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from utils.logger import get_logger
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

logger = get_logger(__name__)

class Settings(BaseSettings):
    
    try: 
        cpanel_server_hostname: str = os.getenv("CPANEL_SERVER_HOSTNAME", "")
        cpanel_server_port: int = int(os.getenv("CPANEL_SERVER_PORT", "465"))
        email_user: str = os.getenv("EMAIL_USER", "")
        email_password: str = os.getenv("EMAIL_PASSWORD", "")
        
        api_port: int = int(os.getenv("API_PORT", "8000"))
        print(api_port)
    except Exception as e:
        logger.error(f"Unexpected error when initializing settings class: {str(e)}")
        raise


# Instancia global de configuración
settings = Settings()
