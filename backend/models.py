from django.db import models
from django.core.files import File
from backend.mimetype_converter import MimetypeConverter
import datetime
import pdb

# Create your models here.

class DocumentConversion(models.Model):
    original_file = models.FileField(upload_to='media/uploaded_files/', default='default.pdf')
    original_filename = models.CharField(max_length=255)
    original_mimetype = models.CharField(max_length=100)
    original_size = models.IntegerField()
    converted_file = models.FileField(upload_to='media/converted_files/')
    converted_filename = models.CharField(max_length=255, null=True)
    converted_mimetype = models.CharField(max_length=100, blank=True, null=True)
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
        mimetype_converter = MimetypeConverter(self.original_mimetype, self.converted_mimetype, self.original_file)
        converted_file_path = mimetype_converter.convert()

        self.converted_file = File(open(converted_file_path, 'rb'))
        self.converted_filename = self.converted_file.name.split('/')[-1]
        self.completed_at = datetime.datetime.now()
        self.status = 'completed'
        self.save()

    


class SupportedConversion(models.Model):
    original_mimetype = models.CharField(max_length=100)
    target_mimetype = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    
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
                conversion_dict[original_mimetype] = []

            conversion_dict[original_mimetype].append(target_mimetype)
            
        return conversion_dict

    def __str__(self):
        return f"original_mimetype={self.original_mimetype}, target_mimetype={self.target_mimetype}, available={self.available}"