import openai
from openai import OpenAIError
from fastapi import HTTPException
from services import ai_service
import schemas
from prompt import response_format_json, prompt_string  # Ensure these are importable

def generate_ai_assessment(vuln, data={}) -> str:
    """
    Generates an AI assessment for the given vulnerability object.
    """
    vuln_data_json = data or schemas.VulnerabilityBase.from_orm(vuln).json()
    try:
        ai_service.configure_openai()
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"I want you to always reply in the following JSON format: {response_format_json()}"},
                {"role": "system", "content": prompt_string()},
                {"role": "system", "content": vuln_data_json}
            ]
        )
        print(response)
        return response.choices[0].message['content'].strip()
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during AI assessment: {str(e)}")
