# python_backend/services/llm_service.py
import openai
import os
import json
from typing import Dict, Any

class LLMService:
    """
    A centralized service for interacting with the OpenAI API.
    Handles client initialization, prompt execution, and response parsing.
    """
    def __init__(self, model: str = "gpt-4.1-mini"):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def execute_prompt(self, prompt_template: str, context: Dict[str, Any], is_json: bool = False) -> str | Dict[str, Any]:
        """
        Formats a prompt, executes it against the LLM, and returns the response.
        """
        final_prompt = prompt_template.format(**context)
        
        response_format = {"type": "json_object"} if is_json else {"type": "text"}
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": final_prompt}],
                response_format=response_format
            )
            content = response.choices[0].message.content
            
            if is_json:
                return json.loads(content)
            return content
        except Exception as e:
            # In a real app, you'd have more robust logging here
            error_message = f"LLM API Error: {e}"
            print(error_message)
            if is_json:
                return {"error": error_message}
            return error_message
