from django.test import TestCase
from .chatbot_logic import get_bot_response

class ChatbotLogicTests(TestCase):
    def test_hello(self):
        self.assertIn("Hi", get_bot_response("hello"))

    def test_unknown(self):
        self.assertIn("trouble", get_bot_response("xyz"))
