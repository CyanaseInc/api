# Generated by Django 3.2.16 on 2023-11-09 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0060_auto_20231101_1011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='bussiness_name',
            new_name='company_category',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='coi',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='logo',
            field=models.ImageField(default='default_logo.jpg', upload_to='api_profile'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='moa',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
