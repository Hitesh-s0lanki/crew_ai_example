import uvicorn
import asyncio
from asyncio import to_thread
from src.crew.financial_researcher_crew.financial_researcher import FinancialResearcherCrew
from src.crew.debate_crew.debate_crew import DebaterCrew
from src.crew.book_researcher_crew.book_researcher_crew import BookResearcherCrew
from src.crew.engineering_team_crew.engineering_team_crew import EngineeringTeamCrew

# importing llm 
from src.llms.opeanai_llm import OpenAILLM
from src.llms.gemini_llm import GeminiLLM

# event streaming 
import json
from src.event_listener.custom_event_streamer import event_queue

# importing fastapi 
from fastapi import FastAPI, Request, HTTPException, Path, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware with settings that match frontend requirements
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
    expose_headers=["Content-Type"], 
)

async def event_generator():
    """ Pull one event at a time from the queue and emit as SSE. """
    while True:
        payload = await event_queue.get()
        # send the event
        yield f"data: {json.dumps(payload)}\n\n"
        # if this is the Crew Completed event, stop the generator
        if payload.get("title") == "Crew Output":
            break

@app.get("/stream/{crew_name}")
async def stream_any_crew(
    request: Request,
    crew_name: str = Path(..., description="Slug name of the crew to run"),
    input: str = Query(..., description="Single input value for the crew"),
):
    # 1) Validate crew exists
    if not crew_name:
        raise HTTPException(status_code=404, detail=f"Crew '{crew_name}' not found")

    # sanity‐check
    if not input:
        raise HTTPException(400, "Query - param `input` is required")

    # Using the openai instance 
    openai = OpenAILLM()
    openai_llm = openai.get_llm_model()

    # Using the Gemini instance 
    gemini = GeminiLLM()
    gemini_llm = gemini.get_llm_model()
    
    # Cases for the crew name
    if crew_name == "debater":
        # Define the crew functioning
        debater_crew = DebaterCrew(openai_llm=openai_llm, gemini_llm=gemini_llm)
        crew = debater_crew.crew_formation()
        inputs = {
            'motion': input
        }
        
        def _run_and_emit_final():
            # run kickoff (emits all intermediate events via bus)
            crew.kickoff(inputs=inputs)

            # Get the output from the crew
            output = debater_crew.get_tasks_output()

            # now push the final payload yourself
            event_queue.put_nowait({
                "title": "Crew Output",
                "type": "crew",
                "propose": output["propose"],
                "oppose": output["oppose"],
                "decide": output["decide"]
            })
        
    elif crew_name == "financial-researcher":
        # Define the crew functioning
        crew = FinancialResearcherCrew(openai_llm=openai_llm, gemini_llm=gemini_llm).crew_formation()
        inputs = {
            'company': input
        }
        
        def _run_and_emit_final():
            # run kickoff (emits all intermediate events via bus)
            result = crew.kickoff(inputs=inputs)

            # now push the final payload yourself
            event_queue.put_nowait({
                "title": "Crew Output",
                "type": "crew",
                "response": result.raw  # or result.some_field if you need a sub‑field
            })
        
            
    elif crew_name == "book-researcher":
        # Define the crew functioning
        book_researcher_crew = BookResearcherCrew(openai_llm=openai_llm, gemini_llm=gemini_llm)
        crew = book_researcher_crew.crew_formation()
        inputs = {
            'genre': input
        }
        
        def _run_and_emit_final():
            # run kickoff (emits all intermediate events via bus)
            crew.kickoff(inputs=inputs)
            
            # Get the output from the crew
            output = book_researcher_crew.get_tasks_output()

            # now push the final payload yourself
            event_queue.put_nowait({
                "title": "Crew Output",
                "type": "crew",
                "trending_topics": output["trending_topics"],
                "top_novelists": output["top_novelists"],
                "genre_research": output["genre_research"]
            })
            
    elif crew_name == "engineering-team":
        # Define the crew functioning
        engineering_team_crew = EngineeringTeamCrew(openai_llm=openai_llm, gemini_llm=gemini_llm)
        # Create the crew
        crew = engineering_team_crew.crew_formation()
        # Define the inputs for the crew
       
        inputs = {
            'requirements': input,
            'module_name': f"my_module.py",
            'class_name': "my_module"
        }
        
        def _run_and_emit_final():
            # run kickoff (emits all intermediate events via bus)
            crew.kickoff(inputs=inputs)
            
            # Get the output from the crew
            output = engineering_team_crew.get_tasks_output()

            # now push the final payload yourself
            event_queue.put_nowait({
                "title": "Crew Output",
                "type": "crew",
                "design": output["design"],
                "code": output["code"],
                "frontend": output["frontend"],
                "test": output["test"]
            })

    else:
        raise HTTPException(status_code=404, detail=f"Crew '{crew_name}' not found")
    
    # run in background thread so the SSE stream can open immediately
    asyncio.create_task(to_thread(_run_and_emit_final))
        
    return StreamingResponse(event_generator(), media_type="text/event-stream")



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)