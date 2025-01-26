import json

from processor.processor import Processor
from utils.get_groq_responses import get_groq_response

CONTEXT = """
You are part of a grievance mapping system. Your role is to map grievances to the most appropriate government officer based on their area of expertise and responsibilities. Each officer has specific roles and jurisdictions. Use the extracted grievance, context, and officer profiles provided below to make the best match. The output must be a JSON object.

**Government Officer Profiles**:
1. **Officer Name**: Rajesh Kumar
   **Department**: Water Supply & Sanitation
   **Responsibilities**: Water supply issues, sanitation projects, and water conservation efforts.
   **Jurisdiction**: Urban and rural areas.

2. **Officer Name**: Priya Sharma
   **Department**: Electricity Board
   **Responsibilities**: Power outages, electricity connections, billing disputes, and infrastructure maintenance.
   **Jurisdiction**: State-wide, including industrial and residential areas.

3. **Officer Name**: Anil Mehta
   **Department**: Traffic Management
   **Responsibilities**: Traffic congestion, road safety, signal maintenance, and parking issues.
   **Jurisdiction**: Urban areas and highways.

4. **Officer Name**: Deepak Verma
   **Department**: Law & Order
   **Responsibilities**: Maintaining public order, addressing civil disputes, and managing security concerns.
   **Jurisdiction**: All regions.

5. **Officer Name**: Kavita Singh
   **Department**: Healthcare
   **Responsibilities**: Public health programs, hospital management, and grievances related to medical facilities.
   **Jurisdiction**: Rural and urban areas.

6. **Officer Name**: Nandini Gupta
   **Department**: Education
   **Responsibilities**: School and college management, scholarships, and teacher-related grievances.
   **Jurisdiction**: State-wide, including rural and urban areas.

**Mapping Instructions**:
1. Use the context and grievance content to identify the grievance category.
2. Match the grievance with the officer whose responsibilities best align with the issue.
3. Consider jurisdiction when assigning the grievance.
4. Return a JSON object containing the matched officer's details, grievance summary, and justification for the mapping.

**Example Output**:
{
  "matched_officer": {
    "name": "Priya Sharma",
    "department": "Electricity Board",
    "jurisdiction": "State-wide"
  },
  "grievance_summary": "Complaint about frequent power outages in residential areas.",
  "justification": "The grievance pertains to electricity issues in residential areas, which fall under the responsibilities of the Electricity Board and Priya Sharma's jurisdiction."
}
"""  # noqa


class Mapper(Processor):
    """Maps the grievance to the relevant government officer."""

    async def process(self, data):
        """Maps the grievance to the relevant government officer."""
        print("Request recieved to map the grievance")
        extracted_grievance = data.get("extarcted_grievance", "")
        if not extracted_grievance:
            raise ValueError("The extracted grievance is missing.")

        messages = [
            {"role": "system", "content": CONTEXT},
            {"role": "user", "content": f"Grievance: {extracted_grievance}"},
        ]

        response_text = get_groq_response(messages, model="llama3-8b-8192")
        response_json = json.loads(response_text)
        print(f"Officer mapping: {response_json}")
        data["officer_mapping"] = response_json

        return data
