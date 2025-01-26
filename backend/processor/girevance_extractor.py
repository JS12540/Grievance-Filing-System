import json

from processor.processor import Processor
from utils.get_groq_responses import get_groq_response

CONTEXT = """
You are an advanced AI language model tasked with extracting grievance details from the provided context for a government grievance system. Analyze the given text and extract the following information in JSON format:

1. **Grievance Text**: The main complaint or grievance mentioned.
2. **Location**: The specific location related to the grievance (e.g., city, district, state).
3. **Grievance Type**: The category or type of the grievance (e.g., sanitation, electricity, water supply, road issues, etc.).

If any of these details are not explicitly mentioned in the context, leave their values as `null`. Ensure the output is in the following JSON format:

Response json
{
  "grievance_text": "<Extracted grievance text>",
  "location": "<Extracted location>",
  "grievance_type": "<Extracted grievance type>"
}

Examples:

Example 1
Context: "There has been no water supply in my area for the past 3 days. This is happening in Sector 12, Noida."

{
  "grievance_text": "There has been no water supply in my area for the past 3 days.",
  "location": "Sector 12, Noida",
  "grievance_type": "water supply"
}

Example 2
Context: "The streetlights in MG Road, Bangalore, have not been working for weeks, creating safety issues at night."

{
  "grievance_text": "The streetlights in MG Road, Bangalore, have not been working for weeks, creating safety issues at night.",
  "location": "MG Road, Bangalore",
  "grievance_type": "electricity"
}
"""  # noqa


class ExtractGirevance(Processor):
    """Extracts girevance from the input data."""

    async def process(self, data):
        """Process the text and extract the grievance details."""
        print("Request recieved to extract grievance")
        user_message = data["text"]

        messages = [
            {"role": "system", "content": CONTEXT},
            {"role": "user", "content": f"User message: {user_message}"},
        ]

        response_text = get_groq_response(messages, "llama3-8b-8192")
        response_json = json.loads(response_text)
        print(f"Grievance extracted: {response_json}")
        data["extarcted_grievance"] = response_json

        return data
