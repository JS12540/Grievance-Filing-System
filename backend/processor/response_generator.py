import json

from processor.processor import Processor
from utils.get_groq_responses import get_groq_response

BASE_CONTEXT = """
You are a language model that generates a response based on the input data.
Your task is to construct a professional and empathetic response to user grievances in the selected language.
The response must address the grievance and provide relevant details about the assigned officer or department.
Output the result in JSON format.

Output should be in JSON format, like this:
{"response": "Your generated response here"}
"""  # noqa


class ResponseGenerator(Processor):
    """Generates a response based on the input data."""

    async def process(self, data):
        """Generates a response based on the input data."""
        selected_language = data.get("selected_language")
        extracted_grievance = data.get("extracted_grievance")
        officer_mapping = data.get("officer_mapping")

        context = (
            f"Language: {selected_language}\n"
            f"Grievance: {extracted_grievance}\n"
            f"Officer/Department Details: {officer_mapping}\n\n"
        )

        messages = [
            {"role": "system", "content": BASE_CONTEXT},
            {"role": "user", "content": context},
        ]

        response_text = get_groq_response(messages, model="llama3-8b-8192")
        response_json = json.loads(response_text)
        print(f"Response generated: {response_json}")
        data["bot_response"] = response_json["response"]

        return data
