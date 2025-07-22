import ollama

MODEL_NAME = "phi3"

def generate_meeting_summary(transcript: str) -> str:
    prompt = f"""
    You are an AI meeting assistant.
    Be precise, concise, and strictly factual.
    ONLY summarize based on this transcript:

    {transcript}

    Return:
    1. A 3-4 sentence factual summary
    2. A list of action items (if any)
    """

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a precise meeting assistant."},
            {"role": "user", "content": prompt}
        ],
        options={"temperature": 0.7}  
    )

    return response["message"]["content"]

def detect_contradictions(current_summary: str, past_summaries: list) -> str:
    if not past_summaries:
        return "No past meetings available for comparison."
    
    past_text = "\n".join([f"-{s}" for s in past_summaries])

    prompt = f""" 
    You are an AI decision auditor.

    Past meeting summaries:
    {past_text}

    Current meeting summary:
    {current_summary}

    Identify any direct contradictions or reversals of decisions. If none, say 'No contradictions found.'
    """

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role":"system", "content": "Your are an unbiased meeting decision auditor."},
            {"role":"user", "content": prompt}
        ],
        options={"temperature":0}
    )

    return response["message"]["content"]

def detect_gaps(current_transcript: str, expected_topics: list) -> str:
    if not expected_topics:
        return "No agenda topics provided."
    
    topics = ", ".join(expected_topics)

    prompt = f"""
    Transcript: 
    {current_transcript}

    Expected topics: 
    {topics}

    Identify which expected topics were NOT discussed or mentioned. If all were covered, say 'All expected topics discussed.'
    """

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an agenda gap detector."},
            {"role":"user", "content":prompt}
        ],
        options={"temperature":0}
    )

    return response["message"]["content"]

def generate_clarification_questions(transcript: str, summary: str) -> str:
    prompt = f"""
    You are an AI meeting assistant tasked with identifying ambiguous or unclear points
    in the discussion and raising clarifying questions.

    Transcript: {transcript}

    Summary: {summary}

    Rules:
    1. Only ask about genuinely unclear or vague details (e.g., dates, responsibilities, numbers, features).
    2. Do not repeat already clear points.
    3. Return in this format:
       Clarification Questions:
       - <question 1>
       - <question 2>
    If everything is clear, respond with: "No clarifications needed."
    """

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a clarification assistant."},
            {"role": "user", "content": prompt}
        ],
        options={"temperature": 0.4}  # slightly higher to ask insightful questions
    )
    return response["message"]["content"]

def extract_decision_graph(summary: str) -> list:
    """
    Extracts key decisions as graph-like triples.
    Returns a list of {decision, responsible, related_to}.
    """
    prompt = f"""
    You are an AI extracting structured decisions for a knowledge graph.

    Summary: {summary}

    Return decisions as JSON list, in this format:
    [
      {{
        "decision": "<main decision or action>",
        "responsible": "<person or team, if mentioned, else 'unknown'>",
        "related_to": "<related topic or context>"
      }}
    ]
    """
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a decision graph extractor."},
            {"role": "user", "content": prompt}
        ],
        options={"temperature": 0}
    )
    import json
    try:
        return json.loads(response["message"]["content"])
    except:
        return []
