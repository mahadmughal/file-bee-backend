# Generated by Django 3.2.12 on 2024-01-12 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentConversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_file', models.FileField(default='default.pdf', upload_to='media/uploaded_files/')),
                ('original_filename', models.CharField(max_length=255)),
                ('original_mimetype', models.CharField(max_length=100)),
                ('original_size', models.IntegerField()),
                ('converted_file', models.FileField(upload_to='media/converted_files/')),
                ('converted_filename', models.CharField(max_length=255, null=True)),
                ('converted_mimetype', models.CharField(blank=True, max_length=100, null=True)),
                ('converted_size', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('error_message', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('expired', 'expired'), ('failed', 'failed')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SupportedConversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_mimetype', models.CharField(max_length=100)),
                ('target_mimetype', models.CharField(max_length=100)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
    ]
