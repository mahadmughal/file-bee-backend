from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from file_bee import settings


class HelpRequestEmailer:
    def __init__(self, help_request, email_from=settings.EMAIL_HOST_USER):
        self.help_request = help_request
        self.email_from = email_from

    def send_confirmation_email(self):
        """
        Sends a confirmation email to the user who submitted the help request.
        """
        subject = 'Confirmation of Your Help Request'
        context = {
            'email': self.help_request.email,
            'subject': self.help_request.subject,
            'description': self.help_request.description,
            'request_id': self.help_request.id,
            'created_at': self.help_request.created_at,
            'attachment_link': self.help_request.attachment.url,
        }

        message = render_to_string(
            'emails/help_request_confirmation.html', context)

        email = EmailMessage(
            subject,
            message,
            self.email_from,
            [self.help_request.email]
        )
        email.send()
