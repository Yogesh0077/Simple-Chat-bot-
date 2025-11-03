from django.urls import path, include
from chatbot_app.views import chatbot_view, clear_chat, chat_stats

urlpatterns = [
    path("", chatbot_view, name="chatbot_view"),                # Main chat interface
    path("clear/", clear_chat, name="clear_chat"),              # Clear chat history
    path("stats/", chat_stats, name="chat_stats"),              # Chat statistics
    path("accounts/", include("django.contrib.auth.urls")),     # Login/logout/password routes
]

