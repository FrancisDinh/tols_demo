import textwrap
import openai

def wrapped(text: str, width: int = 80):
    print("\n".join(textwrap.wrap(text, width=width)))

def check_openai_api_key(api_key):
    openai.api_key = api_key
    try:
        openai.Model.list()
    except openai.error.AuthenticationError as e:
        return False
    else:
        return True
    
def answer_idk():
    answers = [
    "I'm sorry, but I don't have that information.",
    "Unfortunately, I don't have the answer you're looking for.",
    "I'm not familiar with that topic, so I can't provide any insight.",
    "I'm afraid I don't know the answer to your question."
    ]
    return random.choice(answers)