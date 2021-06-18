#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dj-check-constraint-validation
------------

Tests for `dj-check-constraint-validation` models module.
"""
import pytest
from django.db import IntegrityError
from django.db.models import F
from django.db.models import Q

from dj_check_constraint_validation.core import eval_q
from tests.dogs.forms import DogForm
from tests.dogs.models import Dog


class TestForm:
    @pytest.mark.django_db
    def test_it_fails_validation_when_check_constraint_would_fail(self):
        data = {"name": "Bruce", "nick_name": "Bruce"}
        form = DogForm(data)
        assert form.is_valid() is False

        with pytest.raises(IntegrityError):
            Dog.objects.create(**data)

    @pytest.mark.django_db
    def test_happy_path(self):
        data = {"name": "Bruce", "nick_name": "Nugget"}
        form = DogForm(data)
        assert form.is_valid() is True

        Dog.objects.create(**data)
        assert Dog.objects.count() == 1


class TestEvalQ:
    def test_and_when_children_are_truthy(self):
        q = Q(hello="sup", haha="man")
        result = eval_q(q, {"hello": "sup", "haha": "man"})
        assert result is True

    def test_f_expr_with_operator_when_true(self):
        q = Q(
            balance=F("price") - F("discount"),
        )
        result = eval_q(q, {"balance": 50, "price": 75, "discount": 25})
        assert result is True

    def test_f_expr_with_operator_when_false(self):
        q = Q(
            balance=F("price") - F("discount"),
        )
        result = eval_q(q, {"balance": 99999, "price": 75, "discount": 25})
        assert result is False

    def test_f_expr_lhs_recursive(self):
        q = Q(
            balance=F("price") - F("discount") - F("recursive"),
        )
        result = eval_q(
            q, {"balance": 50, "price": 75, "discount": 10, "recursive": 15}
        )
        assert result is True

    def test_and_when_children_are_falsy(self):
        q = Q(hello="sup", haha="man")
        result = eval_q(q, {"hello": "sup", "haha": "not true!"})
        assert result is False

    def test_negated(self):
        q = Q(hello="sup")
        result = eval_q(~q, {"hello": "sup"})
        assert result is False

    def test_or_with_two_qs(self):
        q = Q(hello="sup") | Q(hello="goodbye")
        result = eval_q(q, {"hello": "sup"})
        assert result is True

        result = eval_q(q, {"hello": "goodbye"})
        assert result is True

    def test_and_with_two_qs(self):
        q = Q(hello="sup") & Q(sky="blue")
        result = eval_q(q, {"hello": "sup", "sky": "green"})
        assert result is False

        result = eval_q(q, {"hello": "sup", "sky": "blue"})
        assert result is True

    def test_with_f(self):
        q = Q(hello=F("sup"))
        result = eval_q(q, {"hello": "hi", "sup": "hi"})
        assert result is True

        q = Q(hello=F("sup"))
        result = eval_q(q, {"hello": "hi", "sup": "not hi"})
        assert result is False
