# Generated by Django 3.0 on 2023-03-14 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_ram", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="role",
            name="active",
            field=models.BooleanField(blank=True, default=True, verbose_name="Active"),
        ),
    ]
