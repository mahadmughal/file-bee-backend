from django.db import models
from backend.converters.mimetype_converter import MimetypeConverter
import datetime
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class DocumentConversion(models.Model):
    original_file = models.FileField(
        upload_to='media/uploaded_files/', storage=S3Boto3Storage(), default='default')
    original_filename = models.CharField(max_length=255)
    original_mimetype = models.CharField(max_length=100)
    original_size = models.IntegerField()
    converted_file = models.FileField(
        upload_to='media/converted_files/', storage=S3Boto3Storage(), default='default')
    converted_filename = models.CharField(max_length=255, null=True)
    converted_mimetype = models.CharField(
        max_length=100, blank=True, null=True)
    converted_size = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('expired', 'expired'),
        ('failed', 'failed'),
    ))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='document_conversions',
        on_delete=models.CASCADE,
        verbose_name='User',
        null=True
    )

    def to_dict(self):
        return {
            'original_file': str(self.original_file),
            'original_filename': self.original_filename,
            'original_mimetype': self.original_mimetype,
            'original_size': self.original_size,
            'converted_file': str(self.converted_file),
            'converted_mimetype': self.converted_mimetype,
            'converted_size': self.converted_size,
            'created_at': self.created_at,
            'completed_at': self.completed_at,
            'error_message': self.error_message,
            'status': self.status,
        }

    def conversion(self):
        mimetype_converter = MimetypeConverter(
            self.original_mimetype, self.converted_mimetype, self.original_file)
        converted_file = mimetype_converter.convert()

        supported_conversion = SupportedConversion.objects.filter(
            original_mimetype=self.original_mimetype,
            target_mimetype=self.converted_mimetype,
            available=True
        ).first()

        self.converted_filename = f"{self.original_filename.rsplit(
            '.')[0]}.{supported_conversion.target_extension}"

        self.converted_file.save(
            self.converted_filename, converted_file, save=False)
        self.completed_at = datetime.datetime.now()
        self.status = 'completed'
        self.save()


class SupportedConversion(models.Model):
    original_mimetype = models.CharField(max_length=100)
    target_mimetype = models.CharField(max_length=100)
    original_extension = models.CharField(max_length=50, null=True)
    target_extension = models.CharField(max_length=50, null=True)
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            ('original_mimetype', 'target_mimetype'),
            ('original_extension', 'target_extension'),
        )

    @classmethod
    def get_available_conversions(cls):
        return cls.objects.filter(available=True)

    @classmethod
    def is_conversion_available(cls, original_mimetype, target_mimetype):
        return cls.objects.filter(
            original_mimetype=original_mimetype,
            target_mimetype=target_mimetype,
            available=True
        )

    @classmethod
    def get_available_conversions_for_source(cls, original_mimetype):
        return cls.objects.filter(
            original_mimetype__contains=original_mimetype,
            available=True
        ).values_list("target_mimetype", flat=True)

    @classmethod
    def get_available_conversions_for_all_sources(cls):
        available_conversions = cls.get_available_conversions()
        conversion_dict = {}

        for conversion in available_conversions:
            original_mimetype = conversion.original_mimetype
            target_mimetype = conversion.target_mimetype

            if original_mimetype not in conversion_dict:
                conversion_dict[original_mimetype] = {
                    'targetable_mimetypes': [], 'extension': conversion.original_extension}
            if target_mimetype not in conversion_dict:
                conversion_dict[target_mimetype] = {
                    'targetable_mimetypes': [], 'extension':  conversion.target_extension}

            conversion_dict[original_mimetype]['targetable_mimetypes'].append(
                target_mimetype)

        return conversion_dict

    @classmethod
    def get_original_mimetype(cls, file_mimetype, file_extension):
      # 1. Check for exact match
        exact_matches = cls.objects.filter(
            original_mimetype__iexact=file_mimetype, available=True)
        if exact_matches.exists():
            return exact_matches.first().original_mimetype

        # 2. Check for substring match
        for mimetype in cls.objects.filter(available=True).values_list('original_mimetype', flat=True):
            if file_extension.lower() in mimetype.lower():
                return mimetype

        # 3. No match found
        return None

    def __str__(self):
        return f"original_mimetype={self.original_mimetype}, target_mimetype={self.target_mimetype}, original_extension={self.original_extension}, target_extension={self.target_extension}, available={self.available}"
