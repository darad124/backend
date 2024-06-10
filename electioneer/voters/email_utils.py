import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_email_notification(subject, body, recipient_email):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{'email': recipient_email}],
        subject=subject,
        html_content=body,
        sender={'email': 'no-reply@example.com', 'name': 'Election System'}
    )
    
    try:
        api_response = api_instance.send_transac_email(email)
        logger.info(f"Email sent successfully: {api_response}")
    except ApiException as e:
        logger.error(f"Error sending email: {e}")
