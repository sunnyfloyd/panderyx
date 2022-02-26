# Generated by Django 4.0.1 on 2022-02-26 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tools", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tool",
            name="inputs",
            field=models.ManyToManyField(
                blank=True, related_name="outputs", to="tools.Tool"
            ),
        ),
    ]
