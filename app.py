import uvicorn
import asyncio
from asyncio import to_thread
from src.crew.financial_researcher_crew.financial_researcher import FinancialResearcherCrew

# importing llm 
from src.llms.opeanai_llm import OpenAILLM
from src.llms.gemini_llm import GeminiLLM

# event streaming 
import json
from src.event_listener.custom_event_streamer import event_queue

# importing fastapi 
from fastapi import FastAPI, Request, Query, HTTPException
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
    """
    Pull one event at a time from the queue and emit as SSE.
    """
    while True:
        payload = await event_queue.get()
        # send the event
        yield f"data: {json.dumps(payload)}\n\n"
        # if this is the Crew Completed event, stop the generator
        if payload.get("title") == "Crew Output":
            break

@app.get("/stream/financial-researcher")
async def streamFinancialReseacher(
        request: Request,
        company: str = Query(..., description="Company name to research")
    ):

    # sanity‐check
    if not company:
        raise HTTPException(400, "Query - param `company` is required")

    # Using the openai instance 
    openai = OpenAILLM()
    openai_llm = openai.get_llm_model()

    # Using the Gemini instance 
    gemini = GeminiLLM()
    gemini_llm = gemini.get_llm_model()

    # Define the crew functioning
    crew = FinancialResearcherCrew(openai_llm=openai_llm, gemini_llm=gemini_llm).crew_formation()
    inputs = {
        'company': company
    }

    def _run_and_emit_final():
        # run kickoff (emits all intermediate events via bus)
        result = crew.kickoff(inputs=inputs)

        # write the raw output into output.md
        with open("output.md", "w", encoding="utf-8") as f:
            f.write(result.raw)

        print("✅ Output written to output.md")

        # now push the final payload yourself
        event_queue.put_nowait({
            "title": "Crew Output",
            "type": "crew",
            "response": result.raw  # or result.some_field if you need a sub‑field
        })

    # run in background thread so the SSE stream can open immediately
    asyncio.create_task(to_thread(_run_and_emit_final))

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)


