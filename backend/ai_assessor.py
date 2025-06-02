import os
from dotenv import load_dotenv
import openai
from openai import OpenAIError, OpenAI  # Added OpenAI class
from fastapi import HTTPException
from prompt import response_format_json, prompt_string
load_dotenv()

def generate_ai_assessment(vuln):
    """
    Generates an AI assessment for the given vulnerability object.
    """
    client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))  # Create OpenAI client instance
    try:
        # Combine system messages for better efficiency
        system_content = (
            f"I want you to always reply in the following JSON format: {response_format_json()}\n\n"
            f"{prompt_string()}"
        )
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},  # Enforce JSON response
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": str(vuln)}  # Properly structured user input
            ]
        )
        # Extract content from response
        content = response.choices[0].message.content.strip()
        # print(content)  # Print the actual content instead of full response
        return content

    except OpenAIError as e:
        print("OpenAI Error:", e)
        return HTTPException(status_code=500, detail=f"OpenAI Error: {str(e)}")
    except Exception as e:
        print("Unexpected Error:", e)
        return HTTPException(status_code=500, detail=f"Unexpected error during AI assessment: {str(e)}")