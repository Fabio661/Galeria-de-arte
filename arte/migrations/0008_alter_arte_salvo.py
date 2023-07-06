# Generated by Django 4.2.2 on 2023-07-05 02:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("arte", "0007_comentario"),
    ]

    operations = [
        migrations.AlterField(
            model_name="arte",
            name="salvo",
            field=models.ManyToManyField(
                default=False, related_name="salvar_arte", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]