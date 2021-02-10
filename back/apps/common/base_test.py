from django.test import TestCase

__all__ = ["BaseTest"]


class BaseTest(TestCase):
    maxDiff = 5000
