# Generated by Django 5.0.7 on 2024-09-05 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0014_alter_rentalhistory_fine_payed'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalhistory',
            name='reported_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
