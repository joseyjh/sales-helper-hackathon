from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

template = """
2.Discovery
- Current Situation
- Challenges
- Impact
- Existing Solutions

3.Presentation
- Value Proposition
- Customization
- Features and Benefits
- Demonstration (if applicable)

4.Handling Objections
- Adoption Concerns
- Ease of Use
- Support
- Pricing

5.Closing
Summary
Proposal
Assumptive Close
Confirmation
"""


def is_relevant(query):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.4,
        # response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": f"You are a sales person\n\n The information provided to you are a part of the conversation from you interacting with the customers, who are looking to potentially engage with your service or product. Currently, they may or may not be interested in the service or product you are providing and it is your role to ask the right questions to figure it out. Based on the reply that they have responded with, tell me if I should answer further with questions with a 'yes' ONLY if the context of the response falls under {template} or if it just contextual information with 'no'. If 'yes', explain to me the framework in which you made this decision. And if 'no', explain why"},
            {"role": "user", "content": query}
        ]
    )

    text = response.choices[0].message.content

    return "yes" in text.lower()
