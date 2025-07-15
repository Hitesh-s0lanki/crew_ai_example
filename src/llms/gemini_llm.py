import os
from openai import OpenAI 
from dotenv import load_dotenv

class GeminiLLM:
    def __init__(self):
        load_dotenv()        
        self.model_name = "gemini-2.0-flash"

    def get_llm_model(self) -> OpenAI:

        google_api_key = os.getenv('GOOGLE_API_KEY')

        if not google_api_key:
            raise ValueError("API key is required to call OpenAI.")

        try:
            llm = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
            return llm
        except Exception as e:
            error_msg = f"OpenAI initialization error: {e}"
            raise ValueError(error_msg)
    