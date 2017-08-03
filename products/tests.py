import random

from django.test import TestCase
from django.db.models import Q

from .models import Product


class TestProducts(TestCase):
    """Test Product model."""

    def setUp(self):
        products = [
            Product(
                is_adult=i % 2 == 0,
                is_active=random.randint(1, 10) % 2 == 0
            )
            for i in range(0, 20)
        ]

        Product.objects.bulk_create(products)

        self.adult = Product.objects.filter(is_adult=True)
        self.active = Product.objects.filter(is_active=True)

    def test_product_intersection(self):
        """Test products intersection."""
        adult_and_active = Product.objects.filter(
            is_active=True, is_adult=True
        )

        products_intersection = self.active.intersection(self.adult)
        assert list(products_intersection) == list(adult_and_active)
        assert list(self.active & self.adult) == list(products_intersection)

    def test_products_union(self):
        """Tet products union."""
        adult_or_active = Product.objects.filter(
            Q(is_active=True) | Q(is_adult=True)
        )

        products_union = self.active.union(self.adult)
        assert list(products_union) == list(adult_or_active)
        assert list(self.active | self.adult) == list(products_union)

    def test_active_difference(self):
        """Test products active but not adult."""
        active_but_not_adult = Product.objects.filter(
            is_active=True
        ).exclude(
            is_adult=True
        )

        active_difference = self.active.difference(self.adult)
        assert list(active_difference) == list(active_but_not_adult)

    def test_adult_difference(self):
        """Test adult products but not active."""
        adult_but_not_active = Product.objects.filter(
            is_adult=True
        ).exclude(
            is_active=True
        )

        adult_difference = self.adult.difference(self.active)
        assert list(adult_difference) == list(adult_but_not_active)
