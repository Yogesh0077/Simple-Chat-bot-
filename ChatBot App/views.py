from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatHistory
from .utils import clean_text  # , analyze_sentiment
from transformers import AutoModelForCausalLM, AutoTokenizer
from django.conf import settings
import google.generativeai as genai
import re

# === Configure Gemini API ===
genai.configure(api_key=settings.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

# === Load DialoGPT Model ===
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
dialogpt_model = AutoModelForCausalLM.from_pretrained(model_name)

# === Rule-Based Response ===
def rule_based_response(user_input):
    user_input = clean_text(user_input)
    user_input_lower = user_input.lower()

    if re.fullmatch(r"(hello|hi|hey)", user_input_lower):
        return "Hi there! How can I help you?"
    elif "bye" in user_input_lower:
        return "Goodbye! Have a great day!"
    elif "science" in user_input_lower:
        return "Science is the study of the natural world through observation and experiment."
    elif "love" in user_input_lower:
        return "Love is a complex set of emotions, behaviors, and beliefs."
    return None

# === DialoGPT Response ===
def get_dialogpt_response(user_input):
    try:
        inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
        outputs = dialogpt_model.generate(
            inputs,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.9,
        )
        return tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    except Exception as e:
        print("DialoGPT error:", e)
        return "⚠️ DialoGPT is currently unavailable."

# === Gemini API Response ===
def get_gemini_response(prompt):
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini error:", e)
        return "⚠️ Gemini API is currently unavailable or quota exceeded."

# === Main Chat View ===
@login_required
def chatbot_view(request):
    user = request.user

    if request.method == "POST":
        user_input = request.POST.get("user_input")
        mode = request.POST.get("model", "gemini")  # Default to Gemini
        uploaded_file = request.FILES.get("uploaded_file")

        # Step 1: Rule-based logic
        bot_response = rule_based_response(user_input)
        model_used = "rule_based"

        # Step 2: If no rule matches, use selected model
        if not bot_response:
            if mode == "dialogpt":
                bot_response = get_dialogpt_response(user_input)
                model_used = "dialogpt"
            elif mode == "gemini":
                bot_response = get_gemini_response(user_input)
                model_used = "gemini"
            else:
                bot_response = "⚠️ Unknown model selected."
                model_used = "unknown"

        # Optional: Sentiment analysis
        # polarity, subjectivity = analyze_sentiment(bot_response)

        # Step 3: Save conversation
        ChatHistory.objects.create(
            user=user,
            user_input=user_input,
            bot_response=bot_response,
            model_used=model_used,
            uploaded_file=uploaded_file if uploaded_file else None,
            # polarity=polarity,
            # subjectivity=subjectivity,
        )

        # Step 4: Return AJAX
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"bot_response": bot_response})

    # Step 5: Chat history
    history = ChatHistory.objects.filter(user=user).order_by("timestamp")
    return render(request, "chat.html", {"history": history})

# === Clear Chat History ===
@login_required
def clear_chat(request):
    if request.method == "POST":
        ChatHistory.objects.filter(user=request.user).delete()
    return redirect("chatbot_view")

# === Chat Statistics View ===
@login_required
def chat_stats(request):
    chats = ChatHistory.objects.filter(user=request.user)

    sentiments = [chat.polarity for chat in chats if chat.polarity is not None]
    subjectivities = [chat.subjectivity for chat in chats if chat.subjectivity is not None]

    average_polarity = sum(sentiments) / len(sentiments) if sentiments else 0

    positive = len([p for p in sentiments if p > 0.1])
    neutral = len([p for p in sentiments if -0.1 <= p <= 0.1])
    negative = len([p for p in sentiments if p < -0.1])

    return render(request, "chatbot_app/stats.html", {
        "sentiments": sentiments,
        "subjectivities": subjectivities,
        "average_polarity": round(average_polarity, 2),
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
    })
