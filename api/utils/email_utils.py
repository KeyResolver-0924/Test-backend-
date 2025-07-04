import aiohttp
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from api.config import Settings
from api.utils.template_utils import render_template

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Default placeholder logo using system styling colors
DEFAULT_LOGO_URL = "https://placehold.co/300x100/64748b/ffffff?text=Mortgage+Deed+System"

async def send_email(
    recipient_email: str,
    subject: str,
    template_name: str,
    template_context: Dict[str, Any],
    settings: Settings
) -> bool:
    """
    Send an HTML email using templates through Mailgun API.
    
    Args:
        recipient_email: Email address of the recipient
        subject: Email subject
        template_name: Name of the template file to use
        template_context: Context data for the template
        settings: Application settings
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        logger.debug(f"Preparing to send email to {recipient_email}")
        logger.debug(f"Using template: {template_name}")
        logger.debug(f"Template context: {template_context}")
        logger.debug(f"Mailgun settings - Domain: {settings.MAILGUN_DOMAIN}, From: {settings.EMAILS_FROM_EMAIL}")
        
        # Add common template variables
        context = {
            **template_context,
            'logo_url': getattr(settings, 'COMPANY_LOGO_URL', None),  # Now None is acceptable as fallback
            'current_year': datetime.now().year
        }
        
        # Render the HTML template
        html_content = render_template(template_name, context)
        logger.debug("Successfully rendered email template")
        
        # Prepare the email data
        data = {
            "from": f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>",
            "to": recipient_email,
            "subject": subject,
            "html": html_content
        }
        logger.debug(f"Prepared email data: {data}")
        
        auth = aiohttp.BasicAuth("api", settings.MAILGUN_API_KEY)
        mailgun_url = f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages"
        logger.debug(f"Using Mailgun URL: {mailgun_url}")
        
        async with aiohttp.ClientSession() as session:
            logger.debug("Making request to Mailgun API")
            async with session.post(
                mailgun_url,
                data=data,
                auth=auth
            ) as response:
                response_text = await response.text()
                logger.debug(f"Mailgun API response status: {response.status}")
                logger.debug(f"Mailgun API response: {response_text}")
                
                if response.status == 200:
                    logger.info(f"Email sent successfully to {recipient_email}")
                    return True
                else:
                    logger.error(f"Failed to send email. Status: {response.status}, Error: {response_text}")
                    return False
                    
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}", exc_info=True)
        return False 