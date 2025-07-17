import os
from dotenv import load_dotenv

from crewai import LLM
class GeminiLLM:
    def __init__(self):
        load_dotenv()        
        self.model_name = "gemini/gemini-2.0-flash"

    def get_llm_model(self) -> LLM:

        os.environ["GEMINI_API_KEY"] = google_api_key = os.getenv('GEMINI_API_KEY')

        if not google_api_key:
            raise ValueError("API key is required to call OpenAI.")

        try:
            llm = LLM(
                model=self.model_name,
                temperature=0.7,
            )
            return llm
        except Exception as e:
            error_msg = f"OpenAI initialization error: {e}"
            raise ValueError(error_msg)
    