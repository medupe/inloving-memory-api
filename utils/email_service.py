from typing import Annotated
from fastapi.params import Depends
from mailersend import emails
import os
mailer = emails.NewEmail("mlsn.2478110123b42ae6c0abf1b8426e2feca11d204f5f24f9a81523f9689627939a")
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