# Generated by Django 4.1.3 on 2023-07-28 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_alter_riskprofile_investment_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
