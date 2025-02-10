from typing import Annotated
from fastapi.params import Depends
from mailersend import emails
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access variables

EMAIL_SERVICE_API_KEY = os.getenv("EMAIL_SERVICE_API_KEY")


mailer = emails.NewEmail(EMAIL_SERVICE_API_KEY)
class EmailService:
    async def sendEmail(self,name,email,subject,html_content):
       
        mail_body = {}
        mail_from = {
            "name": "Memory",
            "email": "medupe.molepo@trial-o65qngknzyogwr12.mlsender.net",
        }
        recipients = [
            {
                "name": name,
                "email": email,
            }
        ]
        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject(subject, mail_body)
        mailer.set_html_content(html_content, mail_body)
        mailer.set_plaintext_content("This is the text content", mail_body)
        # using print() will also return status code and data
        mailer.send(mail_body)


def get_email_service():
    return EmailService()

email_dependency = Annotated[EmailService,Depends(get_email_service)]