from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """
        GET /inscricao/ must return status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Must use subscriptions/subscription_form.html
        """
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """
        HTML must contain imput tags
        """
        tags = (
            ('<form', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1)
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_check_csrf(self):
        """
        Form must have CSRF
        """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """
        Context must have subscription form
        """
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Leonardo Flores', cpf='12345678901', email='contato@leonardocouy.com', phone='37-99714083')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/1/"""
        self.assertRedirects(self.resp, '/inscricao/1/')

    def test_send_subscribe_email(self):
        """Send email after successful subscribe"""
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())
