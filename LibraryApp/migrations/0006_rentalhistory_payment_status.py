# Generated by Django 5.0.7 on 2024-09-01 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0005_rentalhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalhistory',
            name='payment_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
