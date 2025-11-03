from .views import rule_based_response, ai_model_response

def get_bot_response(user_input, mode="gemini"):
    rule = rule_based_response(user_input)
    if rule:
        return rule
    return ai_model_response(user_input, mode=mode)
