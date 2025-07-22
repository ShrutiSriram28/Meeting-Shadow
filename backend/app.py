from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from whisper_transcriber import transcribe_audio
from llm_reasoner import generate_meeting_summary, detect_contradictions, detect_gaps, generate_clarification_questions, extract_decision_graph
from storage import save_to_s3, save_metadata, fetch_past_summaries, save_decision_graph
import uuid
import os
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Cognitive Shadow Backend is running!"}

@app.post("/upload_audio/")
async def upload_audio(audio: UploadFile = File(...)):
    meeting_id = str(uuid.uuid4())
    temp_path = f"temp_{audio.filename}"

    try:
        with open(temp_path, "wb") as f:
            f.write(await audio.read())

        transcript = transcribe_audio(temp_path)
        summary = generate_meeting_summary(transcript)
        past_summaries = fetch_past_summaries()
        contradictions = detect_contradictions(summary, past_summaries)
        gaps = detect_gaps(transcript, ["budget", "timeline", "team allocation"])
        clarifications = generate_clarification_questions(transcript, summary)
        decisions = extract_decision_graph(summary)
        save_decision_graph(meeting_id, decisions)
        save_to_s3(meeting_id, temp_path, transcript)
        save_metadata(meeting_id, transcript, summary)
        return {
            "meeting_id": meeting_id,
            "transcript": transcript,
            "summary": summary,
            "decision_auditor": contradictions,
            "cognitive_gaps": gaps,
            "clarification_questions": clarifications,
            "decision_graph": decisions
        }

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)