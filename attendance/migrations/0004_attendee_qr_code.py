# Generated by Django 5.1.2 on 2024-10-21 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_alter_session_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_codes/'),
        ),
    ]
