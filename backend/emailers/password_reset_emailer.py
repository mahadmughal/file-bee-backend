from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from file_bee import settings


class PasswordResetEmailer:

    def __init__(self, reset_token, user, email_from=settings.EMAIL_HOST_USER):
        self.reset_token = reset_token
        self.user = user
        self.email_from = email_from

    def send_email(self):
        """
        Sends a password reset email to the user.
        """
        subject = 'Password Reset for Your Account'
        context = {'username': self.user.username,
                   'reset_url': self.get_reset_url()}
        message = render_to_string(
            'emails/password_reset_email.html', context)  # Use template
        email = EmailMessage(
            subject, message, self.email_from, [self.user.email])
        email.send()

    def get_reset_url(self):
        """
        Generates the reset password URL using the reset token.
        """
        return f"http://localhost:3000/reset_password/{self.reset_token}"  # Assuming http protocol
