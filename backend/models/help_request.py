from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class HelpRequest(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    description = models.TextField()
    attachment = models.FileField(
        upload_to='media/help_request_attachments/', storage=S3Boto3Storage(), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Help Request: {self.subject} - {self.email}"
