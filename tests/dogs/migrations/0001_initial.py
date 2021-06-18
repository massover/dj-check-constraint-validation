# Generated by Django 3.2.4 on 2021-06-18 01:13

import django.db.models.expressions
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Dog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32)),
                ("nick_name", models.CharField(max_length=32)),
            ],
        ),
        migrations.AddConstraint(
            model_name="dog",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("name", django.db.models.expressions.F("nick_name")), _negated=True
                ),
                name="name-nick-name-check",
            ),
        ),
    ]
