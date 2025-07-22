import boto3
import json

s3 = boto3.client("s3", region_name="us-east-1")
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

BUCKET_NAME = "cognitive-shadow-shruti"
TABLE_NAME = "CognitiveShadowMeetings"
GRAPH_TABLE_NAME = "CognitiveShadowDecisionGraph"

def save_to_s3(meeting_id, audio_path, transcript):
    s3.upload_file(audio_path, BUCKET_NAME, f"{meeting_id}/audio.mp3")
    s3.put_object(
        Bucket=BUCKET_NAME, 
        Key=f"{meeting_id}/transcript.json",
        Body=json.dumps({"meeting_id": meeting_id, "transcript": transcript})
    )

def save_metadata(meeting_id, transcript, summary):
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item={
        "meeting_id": meeting_id,
        "transcript": transcript,
        "summary": summary
    })

def fetch_past_summaries(limit=5):
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.scan(Limit=limit)
        summaries = [item["summary"] for item in response.get("Items", [])]
        return summaries
    except Exception as e:
        print(f"[DynamoDB ERROR] {e}")
        return []

def save_decision_graph(meeting_id, decisions: list):
    try:
        table = dynamodb.Table(GRAPH_TABLE_NAME)
        for d in decisions:
            table.put_item(Item={
                "meeting_id": meeting_id,
                "decision": d.get("decision", "unknown"),
                "responsible": d.get("responsible", "unknown"),
                "related_to": d.get("related_to", "unknown")
            })
    except Exception as e:
        print(f"[Graph ERROR] {e}")
