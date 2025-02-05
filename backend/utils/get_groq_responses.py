from constants import GROQ_API_KEY
from groq import Groq

client = Groq(api_key=f"{GROQ_API_KEY}")


def get_groq_response(messages, model):
    """Get response from Groq API."""
    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.3,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq API error: {e}")
        return None
