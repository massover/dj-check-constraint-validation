from django.db import models
from django.db.models import CheckConstraint
from django.db.models import F
from django.db.models import Q


class Dog(models.Model):
    name = models.CharField(max_length=32)
    nick_name = models.CharField(max_length=32)

    class Meta:
        constraints = [
            CheckConstraint(check=~Q(name=F("nick_name")), name="name-nick-name-check"),
        ]
