# Generated by Django 5.0.7 on 2024-09-03 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0013_rentalhistory_fine_payed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalhistory',
            name='fine_payed',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
