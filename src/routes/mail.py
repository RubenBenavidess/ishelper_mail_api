"""
Mail Routes Module

This module defines all API endpoints related to email functionality.
It includes routes for sending contact emails with automatic request validation.

Author: ISHelper Team
Version: 1.0.0
"""

from fastapi import APIRouter, HTTPException, status, Request, Response
from controllers.mail_controller import MailController
from schemes.mail_scheme import Mail
from utils.logger import get_logger
from middlewares.rate_limiting import limiter

logger = get_logger(__name__)

router = APIRouter(
    prefix="/mail",
    tags=["Mail"],
    responses={
        400: {"description": "Invalid data"},
        503: {"description": "Service unavailable"},
        500: {"description": "Internal server error"}
    }
)

mail_controller = MailController()


@router.post(
    "/send",
    status_code=status.HTTP_200_OK,
    summary="Send contact email",
    description="Sends an email with the provided contact information. The data is automatically validated according to the Mail schema.",
    response_model=dict,
    tags=["Email"],
    responses={
        200: {"description": "Email sent successfully"},
        400: {"description": "Invalid email data provided"},
        503: {"description": "Email service temporarily unavailable"},
        500: {"description": "Internal server error occurred"}
    }
)
@limiter.limit("10/minute", error_message="Too many requests")
async def send_contact_mail(request: Request, response: Response, mail: Mail) -> dict:
    """
    Send a contact email.
    
    This endpoint receives contact information and sends an email to the support team.
    The request body must contain valid contact information including name, email, phone, etc.
    
    Args:
        mail (Mail): The mail request body containing sender and message information.
    
    Returns:
        dict: A response dictionary containing success status, message, email, and sender name.
    
    Raises:
        HTTPException: 400 if invalid data is provided.
        HTTPException: 503 if unable to connect to mail server.
        HTTPException: 500 for other unexpected errors.
    """
    try:
        logger.info(f"New POST request /mail/send from {mail.email}")
        
        result = mail_controller.send_contact_mail(mail)
        
        return result
        
    except ValueError as e:
        logger.error(f"Invalid data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )
        
    except ConnectionError as e:
        logger.error(f"Connection error to the mail server: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not connect to the mail server. Please try again later."
        )
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error processing your request. Please try again later."
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Check service status",
    description="Checks that the mail service is running and correctly configured",
    response_model=dict
)
@limiter.limit("5/minute", error_message="Too many requests")
async def health_check(request: Request, response: Response) -> dict:
    try:
        logger.info("Health check requested")
        
        MailController()
        
        logger.info("Successful health check")
        
        return {
            "status": "healthy",
            "service": "mail_service",
            "message": "The mail delivery service is operational"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "service": "mail_service",
                "message": f"The mail service is unavailable: {str(e)}"
            }
        )
    
