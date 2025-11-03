from django.db import models
from django.contrib.auth.models import User

class ChatHistory(models.Model):
    MODEL_CHOICES = [
        ("gemini", "Gemini Pro"),
        ("dialogpt", "DialoGPT"),
        ("rule_based", "Rule-Based"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_input = models.TextField()
    bot_response = models.TextField()
    model_used = models.CharField(max_length=20, choices=MODEL_CHOICES, default="gemini")
    polarity = models.FloatField(null=True, blank=True)
    subjectivity = models.FloatField(null=True, blank=True)
    uploaded_file = models.FileField(upload_to='chat_uploads/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.model_used}] {self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_input = models.TextField()
    bot_response = models.TextField()
    polarity = models.FloatField(null=True, blank=True)
    subjectivity = models.FloatField(null=True, blank=True)
    uploaded_file = models.FileField(upload_to='uploads/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
