# dj-check-constraint-validation

From the [constraints reference](https://docs.djangoproject.com/en/3.2/ref/models/constraints/#module-django.db.models.constraints)
in the django documentation,

> Validation of Constraints
> 
> In general constraints are not checked during full_clean(), and do not raise ValidationErrors. Rather you’ll get a database integrity error on save(). UniqueConstraints without a condition (i.e. non-partial unique constraints) are different in this regard, in that they leverage the existing validate_unique() logic, and thus enable two-stage validation. In addition to IntegrityError on save(), ValidationError is also raised during model validation when the UniqueConstraint is violated.

`dj-check-constraint-validation.CheckConstraintMixin` will programmatically generate form validation from the Q objects
specified in the [CheckConstraint.check](https://docs.djangoproject.com/en/3.2/ref/models/constraints/#check). This leads 
us to define the check constraint on the model once without having to define similar logic again on the form. 

## Installation

```
pip install dj-check-constraint-validation
```

## Quickstart

```python
from django.db import models
from django import forms
from django.db.models import CheckConstraint, F, Q

from dj_check_constraint_validation import CheckConstraintsMixin

class Dog(models.Model):
    name = models.CharField(max_length=32)
    nick_name = models.CharField(max_length=32)

    class Meta:
        constraints = [
            CheckConstraint(check=~Q(name=F("nick_name")), name="name-nick-name-check"),
        ]

class DogForm(CheckConstraintsMixin, forms.ModelForm):
    class Meta:
        model = Dog
        fields = ["name", "nick_name"]
```
