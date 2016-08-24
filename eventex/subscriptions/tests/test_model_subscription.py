from django.test import TestCase
from datetime import datetime
from ..models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Leonardo Flores',
            cpf='12345678901',
            email='contato@leonardocouy.com',
            phone='37-123456789'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """
        Subscription must have an auto created_at attr.
        """
        self.assertIsInstance(self.obj.created_at, datetime)