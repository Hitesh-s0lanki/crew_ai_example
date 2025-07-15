from src.crew.financial_researcher_crew.financial_researcher import FinancialResearcherCrew

# importing llm 
from src.llms.opeanai_llm import OpenAILLM
from src.llms.gemini_llm import GeminiLLM

if __name__ == "__main__":
    
    # Using the openai instance 
    openai = OpenAILLM()
    openai_llm = openai.get_llm_model()

    # Using the Gemini instance 
    gemini = GeminiLLM()
    gemini_llm = gemini.get_llm_model()

    # Define the crew functioning
    crew = FinancialResearcherCrew(openai_llm=openai_llm, gemini_llm=gemini_llm).crew_formation()
    inputs = {
        'company': 'Google'
    }

    result = crew.kickoff(inputs=inputs)

    # print(result.raw)

