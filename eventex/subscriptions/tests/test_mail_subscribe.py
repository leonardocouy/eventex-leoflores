from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Leonardo Flores', cpf='12345678901', email='contato@leonardocouy.com', phone='37-99714083')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]
        
    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'contato@leonardocouy.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Leonardo Flores',
            '12345678901',
            'contato@leonardocouy.com',
            '37-99714083',
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

