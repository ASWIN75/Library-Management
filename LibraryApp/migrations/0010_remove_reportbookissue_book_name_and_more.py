# Generated by Django 5.0.7 on 2024-09-02 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0009_reportbookissue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportbookissue',
            name='book_name',
        ),
        migrations.AddField(
            model_name='rentalhistory',
            name='issue_reported',
            field=models.BooleanField(default=False),
        ),
    ]
