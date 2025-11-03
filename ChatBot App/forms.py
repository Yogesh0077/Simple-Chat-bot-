from django import forms
from .models import Chat

class UserInputForm(forms.Form):
    user_input = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Type a message...'}))

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['user_input', 'uploaded_file']