import os
import sys
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from email_utils import send_email_notification

sys.path.insert(0, 'C:/Users/Oluwadara/Desktop/election_project/electioneer')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_system.settings')
application = get_wsgi_application()

def test_send_email():
    subject = "Test Email"
    body = "<h1>This is a test email</h1><p>If you received this, the setup works!</p>"
    recipient_email = settings.ADMIN_EMAIL
    
    send_email_notification(subject, body, recipient_email)
    print("Test email sent!")

if __name__ == "__main__":
    test_send_email()
