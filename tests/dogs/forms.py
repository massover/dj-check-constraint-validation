from django import forms

from dj_check_constraint_validation import CheckConstraintsMixin
from tests.dogs.models import Dog


class DogForm(CheckConstraintsMixin, forms.ModelForm):
    class Meta:
        model = Dog
        fields = ["name", "nick_name"]
