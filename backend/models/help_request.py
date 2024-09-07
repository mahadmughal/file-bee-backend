from django.db import models


class HelpRequest(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    description = models.TextField()
    attachment = models.FileField(
        upload_to='media/help_request_attachments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Help Request: {self.subject} - {self.email}"
